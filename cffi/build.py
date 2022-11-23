from cffi import FFI
from os import environ
from pathlib import Path

curdir = Path(__file__).parent.resolve()
pdflibdir = Path(environ["PDFLIB_DIR"]) / "bind" / "c"

ffibuilder = FFI()
ffibuilder.set_source(
    "cpdflib._pdflib",
    (curdir / "source.c").read_text(),
    libraries=[ "pdf", "stdc++" ],
    include_dirs=[ str(pdflibdir / "include") ],
    library_dirs=[ str(pdflibdir / "lib") ],
)
ffibuilder.cdef(
    (curdir / "cdef").read_text()
)
