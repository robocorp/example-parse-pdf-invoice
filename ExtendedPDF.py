from pathlib import Path
from typing import Optional

import camelot
from RPA.PDF import PDF
from RPA.PDF.keywords import keyword


class ExtendedPDF(PDF):

    """Quickstart: https://camelot-py.readthedocs.io/en/master/user/quickstart.html?highlight=read_pdf"""

    @keyword
    def get_tables_from_pdf(self, source_path: Optional[str] = None, *args, **kwargs):
        """Documentation: https://camelot-py.readthedocs.io/en/master/api.html?highlight=read_pdf#camelot.read_pdf"""

        self.switch_to_pdf(source_path)

        tables = camelot.read_pdf(self.active_pdf_document.path, *args, **kwargs)
        return tables

    @keyword
    def export_tables_to_files(
        self, tables, output_path: str, output_format: str = "csv", **kwargs
    ):
        """Documentation: https://camelot-py.readthedocs.io/en/master/api.html?highlight=export#camelot.core.TableList.export"""

        # Supported formats: csv|excel|html|json|markdown|sqlite
        tables.export(output_path, f=output_format, **kwargs)

        # Returns all the exported files, which is one per table. (pages X tables)
        path = Path(output_path)
        pattern = f"{path.stem}*{path.suffix}"
        return path.parent.glob(pattern)
