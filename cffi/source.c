#include <pdflib.h>

int _PDF_end_document(PDF* p, const char* optlist) {
  PDF_TRY(p) {
    PDF_end_document(p, optlist);
    return 0;
  }
  PDF_CATCH(p) {
    return -1;
  }
  return 0;
}
