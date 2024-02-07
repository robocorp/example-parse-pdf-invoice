import os

from robocorp import log
from robocorp.tasks import task

from PyPDFLibrary import PyPDFLibrary
from PDFMinerLibrary import find_row, find_column

PDF_INVOICE_FILE_PATH = os.path.join("devdata", "text-invoice.pdf")
PDF_INVOICE_TABLE_FILE_PATH = os.path.join("devdata", "text-invoice-table.pdf")

EXCEL_FILE_STARTING_ROW_INDEX = 3


def print_all_text(pdf_lib: PyPDFLibrary) -> None:
    text_from_all_pages = pdf_lib.parse_text()
    log.info(text_from_all_pages)


def find_service_description(pdf_lib: PyPDFLibrary) -> None:
    pattern = r".*Service.*\n.{4}(.*)\n(.+?\.\.\.)"
    matches = pdf_lib.find_matches(pattern)
    assert len(matches) > 0, f"Text could not be found for: {pattern}"
    text = "\n".join(matches)
    log.info(f"First item under service: {text}")


def find_web_design_service_value(pdf_lib: PyPDFLibrary) -> None:
    pattern = r".*Service.*\n.*Web Design.*\n.*?\$(.{5}) (.{5}) (.{6})"
    matches = pdf_lib.find_matches(pattern)
    assert len(matches) >= 3, f"Unexpected match found: {matches}"
    log.info(
        f'The "Adjust" column value to the right of the "Web Design" "Service": {matches[1]}'
    )


def find_prices(pdf_lib: PyPDFLibrary) -> None:
    pattern = r"Sub Total (.*)\nTax (.*)\nTotal (.*)"
    matches = pdf_lib.find_matches(pattern)
    assert len(matches) > 0, f"No matches found for pattern: {pattern}"
    log.info(f'Next 3 prices below "Sub Total": {matches}')


def find_lines_with_email_addresses(pdf_lib: PyPDFLibrary) -> None:
    pattern = r"^.*\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b.*$"
    matches = pdf_lib.find_matches(pattern)
    assert len(matches) > 0, f"No matches found for pattern: {pattern}"
    log.info(f"Show all the lines containing an e-mail address: {matches}")


def print_values_from_row() -> None:
    row = find_row(PDF_INVOICE_TABLE_FILE_PATH, 'Test Item')
    log.info(f"Elements in searched row: {row}")
    assert row == ['Test Item', '1 hrs', '10.00', '20', '10.00', '2.00', '12.00']


def print_values_from_column() -> None:
    column = find_column(PDF_INVOICE_TABLE_FILE_PATH, 'Total gross')
    log.info(f"Column: {column}")
    assert column == ['Total gross', '12.00', '414.00', '360.00', '786.00', '786.00']


@task
def extract_text_data() -> None:
    pdf_lib = PyPDFLibrary()

    try:
        pdf_lib.open_pdf(PDF_INVOICE_FILE_PATH)
        print_all_text(pdf_lib)
        find_service_description(pdf_lib)
        find_web_design_service_value(pdf_lib)
        find_prices(pdf_lib)
        find_lines_with_email_addresses(pdf_lib)
    finally:
        pdf_lib.close()


@task
def extract_elements_from_table() -> None:
    print_values_from_row()
    print_values_from_column()


