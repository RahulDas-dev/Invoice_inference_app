import uuid
from typing import Any, Dict

from sqlalchemy import JSON, UUID, Integer, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import db


class InvoiceInfo(db.Model):
    __tablename__ = "invoice_info"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    invoice_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer(), nullable=False)
    deatils: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=text("'{}'"))

    __table_args__ = (UniqueConstraint(invoice_id, name="unique_invoice_document"),)

    def __repr__(self):
        return f"<InvoiceInfo [id={self.id} document_id={self.document_id}]>"
