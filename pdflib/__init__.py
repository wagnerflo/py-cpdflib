from ._pdflib.lib import *
from contextlib import contextmanager
from uuid import uuid4

def _char(s):
    return str(s).encode("utf8")

class Handle:
    def __init__(self):
        self._pdf = PDF_new()
        PDF_set_option(self._pdf, b"errorpolicy=return")
        PDF_set_option(self._pdf, b"stringformat=utf8")

    def __del__(self):
        PDF_delete(self._pdf)

    def set_license(self, key):
        PDF_set_option(self._pdf, _char(f"license={key}"))

    @contextmanager
    def begin_pdf(self, filename, optlist=""):
        PDF_begin_document(self._pdf, _char(filename), 0, _char(optlist))
        try:
            yield PDFDocument(self._pdf)
        finally:
            if _PDF_end_document(self._pdf, b""):
                raise Exception()

    @contextmanager
    def pvf(self, data):
        uuid = uuid4()
        PDF_create_pvf(self._pdf, uuid, 0, data, len(data), b"copy=true")
        try:
            yield uuid
        finally:
            PDF_delete_pvf(self._pdf, uuid, 0)

    @contextmanager
    def open_pdf(self, filename,  optlist=""):
        hndl = PDF_open_pdi_document(self._pdf, _char(filename), 0, _char(optlist))
        try:
            yield PDIDocument(self._pdf, hndl)
        finally:
            PDF_close_pdi_document(self._pdf, hndl)

    @contextmanager
    def load_font(self, fontname, encoding, optlist="keepfont"):
        hndl = PDF_load_font(
            self._pdf, _char(fontname), 0, _char(encoding), _char(optlist)
        )
        try:
            yield Font(self._pdf, hndl)
        finally:
            PDF_close_font(self._pdf, hndl)

class PDFPage:
    def __init__(self, pdf):
        self._pdf = pdf

    def fit_image(self, image, x, y, optlist=""):
        PDF_fit_image(self._pdf, image._hndl, x, y, _char(optlist))

    def fit_pdi(self, pdi_page, x, y, optlist=""):
        PDF_fit_pdi_page(self._pdf, pdi_page._hndl, x, y, _char(optlist))

    def fit_textline(self, text, x, y, optlist=""):
        PDF_fit_textline(self._pdf, _char(text), 0, x, y, _char(optlist))

    def set_font(self, font, size):
        PDF_setfont(self._pdf, font._hndl, size)

    def set_text_option(self, optlist):
        PDF_set_text_option(self._pdf, _char(optlist))

class PDFDocument:
    def __init__(self, pdf):
        self._pdf = pdf

    @contextmanager
    def new_page(self, width, height, optlist=""):
        PDF_begin_page_ext(self._pdf, width, height, _char(optlist))
        try:
            yield PDFPage(self._pdf)
        finally:
            PDF_end_page_ext(self._pdf, b"")

    @contextmanager
    def load_image(self, filename, imagetype="auto", optlist=""):
        hndl = PDF_load_image(
            self._pdf, _char(imagetype), _char(filename), 0, _char(optlist)
        )
        try:
            yield Image(self._pdf, hndl)
        finally:
            PDF_close_image(self._pdf, hndl)

    def set_info(self, key, value):
        PDF_set_info(self._pdf, _char(key), _char(value))

    def create_bookmark(self, title, optlist=""):
        return PDF_create_bookmark(self._pdf, _char(title), 0, _char(optlist))

class Font:
    def __init__(self, pdf, hndl):
        self._pdf = pdf
        self._hndl = hndl

class Image:
    def __init__(self, pdf, hndl):
        self._pdf = pdf
        self._hndl = hndl

class PDIDocument:
    def __init__(self, pdf, hndl):
        self._pdf = pdf
        self._hndl = hndl

    @contextmanager
    def open_page(self, pagenumber, optlist=""):
        hndl = PDF_open_pdi_page(
            self._pdf, self._hndl, pagenumber, _char(optlist)
        )
        try:
            yield PDIPage(self._pdf, hndl)
        finally:
            PDF_close_pdi_page(self._pdf, hndl)

class PDIPage:
    def __init__(self, pdf, hndl):
        self._pdf = pdf
        self._hndl = hndl

    def get_info(self, keyword, optlist=""):
        return PDF_info_pdi_page(
            self._pdf, self._hndl, _char(keyword), _char(optlist)
        )

    @property
    def width(self):
        return self.get_info("pagewidth")

    @property
    def height(self):
        return self.get_info("pageheight")

_pdf = Handle()
set_license = _pdf.set_license
begin_pdf = _pdf.begin_pdf
open_pdf = _pdf.open_pdf
load_font = _pdf.load_font
