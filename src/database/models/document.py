import uuid
from typing import Any, Dict

from sqlalchemy import JSON, UUID, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import db


class Document(db.Model):
    __tablename__ = "document"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    metainfo: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=text("'{}'"))
    content: Mapped[str] = mapped_column(String(), default=text("''"))

    __table_args__ = (UniqueConstraint(document_id, name="unique_document"),)

    def __repr__(self):
        return f"<Document [id={self.id} filename={self.filename}]>"

    @property
    def page_count(self) -> int:
        return self.metainfo.get("page_count", 0)

    def add_text(self, text: str) -> None:
        self.text = text
