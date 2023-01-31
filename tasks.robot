*** Settings ***
Documentation       Show-case multiple ways of extracting information from different
...    kinds of PDF files (text based and scans) presenting invoice data.


*** Tasks ***
Extract Text Data With RPA
    [Documentation]    Extract textual data with the local help of `RPA.PDF` library.


Extract Tabular Data With Camelot
    [Documentation]    Extract tables with the Camelot library.
    ...    (see external dependency: https://pypi.org/project/camelot-py/)


Extract Structured Data With AI
    [Documentation]    Extract fields detected in both text or image-based PDFs using
    ...    3rd-party external services wrapped by the `RPA.DocumentAI` library.
