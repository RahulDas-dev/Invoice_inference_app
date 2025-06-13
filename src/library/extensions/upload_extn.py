from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, Union

from flask import Flask, abort, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

TEXT = ("txt",)
DOCUMENTS: Tuple[str, ...] = ("rtf", "odf", "ods", "gnumeric", "abw", "doc", "docx", "xls", "xlsx", "pdf")
IMAGES: Tuple[str, ...] = ("jpg", "jpe", "jpeg", "png", "gif", "svg", "bmp", "webp")
DEFAULTS: Tuple[str, ...] = TEXT + DOCUMENTS + IMAGES


def extension(filename: str) -> str:
    ext = Path(filename).suffix
    if ext == "":
        ext = Path(filename).stem
    return ext.lstrip(".")


def lowercase_ext(filename: str) -> str:
    path = Path(filename)
    if path.suffix:
        return path.stem + path.suffix.lower()
    return filename


def addslash(url: str) -> str:
    if url.endswith("/"):
        return url
    return url + "/"


class UploadNotAllowedError(Exception):
    """
    This exception is raised if the upload was not allowed. You should catch
    it in your view code and display an appropriate message to the user.
    """


@dataclass(frozen=True, slots=True, eq=True)
class UploadConfiguration:
    destination: str = field(default="")
    base_url: str = field(default="")
    allow: Tuple[str, ...] = field(default_factory=tuple)
    deny: Tuple[str, ...] = field(default_factory=tuple)


class UploadSet:
    def __init__(self, name: str = "files", extensions: Tuple[str, ...] = DEFAULTS):
        if not name.isalnum():
            raise ValueError("Name must be alphanumeric (no underscores)")
        self.name = name
        self.extensions = extensions
        self._config = UploadConfiguration()

    @property
    def config(self) -> UploadConfiguration:
        return self._config

    @config.setter
    def config(self, cfg: UploadConfiguration) -> None:
        self._config = cfg

    def url(self, filename: str) -> str:
        base = self.config.base_url
        if base is None or base == "":
            return url_for("_uploads.uploaded_file", setname=self.name, filename=filename, _external=True)
        return base + filename

    def path(self, filename: str, folder: Optional[str] = None) -> Path:
        if folder is not None:
            target_folder = Path(self.config.destination) / Path(folder)
        else:
            target_folder = Path(self.config.destination)
        return Path(target_folder) / Path(filename)

    def file_allowed(self, basename: str) -> bool:
        return self.extension_allowed(extension(basename))

    def extension_allowed(self, ext: str) -> bool:
        return (ext in self.config.allow) or (ext in self.extensions and ext not in self.config.deny)

    def get_basename(self, filename: str) -> str:
        return lowercase_ext(secure_filename(filename))

    def save(self, storage: FileStorage, folder: Optional[str] = None, name: Optional[str] = None) -> Path:
        if not isinstance(storage, FileStorage):
            raise TypeError("Storage must be a werkzeug.FileStorage")
        if storage.filename is None:
            raise TypeError("Storage must be a werkzeug.FileStorage")
        if folder is None and name is not None and "/" in name:
            path = Path(name)
            folder, name = str(path.parent), path.name

        basename = self.get_basename(storage.filename)

        if not self.file_allowed(basename):
            abort(403, description=f"File is not allowed: {basename}")

        if name:
            basename = name + extension(basename) if name.endswith(".") else name

        target_folder = Path(self.config.destination) / Path(folder) if folder else Path(self.config.destination)

        if not target_folder.exists():
            target_folder.mkdir(parents=True)

        target = target_folder / basename
        if target.exists():
            basename = self.resolve_conflict(str(target_folder), basename)
            target = target_folder / basename

        storage.save(target)
        return target

    def resolve_conflict(self, target_folder: str, basename: str) -> str:
        name, ext = Path(basename).stem, Path(basename).suffix
        count = 0
        while True:
            count += 1
            newname = f"{name}_{count}{ext}"
            newpath = Path(target_folder) / Path(newname)
            if not newpath.exists():
                return newname


def config_for_set(uset: UploadSet, app: Flask, defaults: Optional[dict] = None) -> UploadConfiguration:
    config = app.config
    prefix = f"UPLOADES_{uset.name.upper()}_"
    using_defaults = False
    if defaults is None:
        defaults = {"dest": None, "url": None}

    allow_extns = tuple(config.get(prefix + "ALLOW", ()))
    deny_extns = tuple(config.get(prefix + "DENY", ()))
    destination = config.get(prefix + "DEST")
    base_url = config.get(prefix + "URL")

    if destination is None:
        if defaults["dest"] is not None:
            using_defaults = True
            destination = Path(str(defaults["dest"])) / Path(secure_filename(uset.name))
            if not destination.exists():
                destination.mkdir(parents=True)
        else:
            raise RuntimeError(f"No Destination is set for {uset.name} Kindly Set {prefix}DEST or UPLOADS_DEFAULT_DEST")

    if base_url is None and using_defaults and defaults["url"]:
        base_url = addslash(defaults.get("url", "")) + uset.name + "/"

    config = UploadConfiguration(str(destination), str(base_url), allow_extns, deny_extns)
    uset.config = config
    return config


def configure_uploads(app: Flask, upload_sets: Union[UploadSet, Tuple[UploadSet]]) -> None:
    if isinstance(upload_sets, UploadSet):
        upload_sets = (upload_sets,)

    defaults = {
        "dest": app.config.get("UPLOADS_DEFAULT_DEST", None),
        "url": app.config.get("UPLOADS_DEFAULT_URL", None),
    }

    for uset in upload_sets:
        config_for_set(uset, app, defaults)


pdf_loader = UploadSet(name="pdf", extensions=("pdf", "PDF"))
