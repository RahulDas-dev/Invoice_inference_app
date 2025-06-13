import threading

from flask import current_app
from flask_restx import Namespace, Resource, abort, fields, reqparse
from flask_restx._http import HTTPStatus
from werkzeug.datastructures import FileStorage

from library.extensions import pdf_loader
from service import InvoiceService, Pdf2ImgService

from .signals import house_keeping

ns = Namespace("process", description="Process Uploaded Document Extracts Invoice Information")

upload_parser = reqparse.RequestParser()

upload_parser.add_argument("document", type=FileStorage, location="files", required=True)

item_model = ns.model(
    "item",
    {
        "slno": fields.Integer,
        "price": fields.String,
        "quantity": fields.String,
        "description": fields.String,
        "currency": fields.String,
    },
)

company_model = ns.model(
    "company",
    {
        "name": fields.String,
        "gst_no": fields.String,
        "pan_no": fields.String,
        "address": fields.String,
        "phone_number": fields.String,
        "email": fields.String,
    },
)

tax_component = ns.model(
    "tax_components",
    {
        "CGST": fields.Float,
        "SGST": fields.Float,
        "IGST": fields.Float,
    },
)
invoice_model = ns.model(
    "invoice_details",
    {
        "invoice_number": fields.String,
        "invoice_date": fields.String,
        "seller_details": fields.Nested(company_model),
        "buyer_details": fields.Nested(company_model),
        "items": fields.List(fields.Nested(item_model)),
        "total_tax": fields.Nested(tax_component),
        "total_charge": fields.Float,
        "total_discount": fields.Float,
        "total_amount": fields.Float,
        "amount_paid": fields.Float,
        "amount_due": fields.Float,
        "page_no": fields.Integer,
    },
)
model = ns.model("Invoice", {"details": fields.List(fields.Nested(invoice_model))})


@ns.route("/", endpoint="process")
class Upload(Resource):
    @ns.marshal_with(model, code=HTTPStatus.CREATED)
    @ns.doc(
        responses={
            201: "Success",
            400: "Invalid File Format",
            500: "Error While Saving Document",
        }
    )
    @ns.expect(upload_parser)
    def post(self) -> tuple:
        args = upload_parser.parse_args()
        document = args["document"]
        if document is None or not isinstance(document, FileStorage) or document.filename is None:
            return abort(HTTPStatus.BAD_REQUEST, "Invalid File Object")
        uploaded_file = pdf_loader.save(document)
        ns.logger.info(f"Uploaded files {uploaded_file.name!s} ...")
        image_directory = Pdf2ImgService.convert(uploaded_file)
        ns.logger.info(f"Converted to Images {image_directory.name!s} ...")
        data, dadta_str = InvoiceService.run(image_directory)
        ns.logger.info("Agents Complited Extraction ...")
        if current_app.config.get("CLEANUP_TEMP_FILES", False):
            threading.Thread(
                target=house_keeping.send,
                name="house_keeping_thread",
                args=[self],
                kwargs={"file_paths": [uploaded_file, image_directory]},
            ).start()
        return data.model_dump(), 201
