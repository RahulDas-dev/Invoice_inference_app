import logging
from pathlib import Path

from pydantic import BaseModel
from quart import Blueprint, current_app, jsonify, make_response
from quart_schema import DataSource, validate_request, validate_response
from quart_schema.pydantic import File
from quart_uploads import UploadNotAllowed

from library.extensions import pdf_loader
from service.invoice import iter_workflow
from src.service.invoice.output_format import InvoiceData

from .background_task import cleanup_temp_files

invoice_bp = Blueprint("process", __name__, url_prefix="/process_invoice")

logger = logging.getLogger(__name__)


class Reqst(BaseModel):
    document: File


@invoice_bp.route("/", methods=["POST"])
@validate_request(Reqst, source=DataSource.FORM_MULTIPART)
@validate_response(InvoiceData, 201)
async def process_single_invoice(data: Reqst) -> tuple:
    # document = (await request.files).get("file", None)
    logger.info(f"document.filename {data.document.filename}")
    if data.document is None or data.document.filename is None:
        logger.error("Uploaded files is not valid...")
        return InvoiceData(error_message="Invalid File Object"), 403
    try:
        uploaded_file = await pdf_loader.save(data.document)
    except UploadNotAllowed:
        logger.error("Uploaded files is not valid...")
        return InvoiceData(error_message="File not allowed"), 403
    uploaded_path = Path(pdf_loader.path(uploaded_file))
    logger.info(f"Uploaded files {uploaded_file} ...")
    try:
        result = await iter_workflow(uploaded_path)  # Use await here
    except Exception as e:
        logger.error(f"Error While Processing {e!s}...")
        current_app.add_background_task(cleanup_temp_files, [uploaded_path])
        return await make_response(jsonify(message=str(e))), 403
    invoices = result.to_invoice_data()
    logger.info(f"Processed invoices: {invoices}")
    current_app.add_background_task(cleanup_temp_files, [uploaded_path, result.image_dir])
    return invoices, 201
