from quart_schema import hide
from quart_uploads import UploadSet
from quart_uploads.route import uploaded_file

hide(uploaded_file)

pdf_loader = UploadSet(name="pdf", extensions=("pdf", " PDF"))
