*** Settings ***
Documentation       Show-case multiple ways of extracting information from different
...    kinds of PDF files (text based and scans), mainly presenting invoice data.

Library    Collections
Library    ExtendedPDF
Library    RPA.DocumentAI
Library    RPA.Excel.Files
Library    RPA.Tables
Library    String

Suite Teardown    Close All PDFs


*** Keywords ***
Camelot Table As Excel
    [Documentation]    Export table from text PDF invoice as Excel file, then read its
    ...    content into a table by choosing the header correctly and stripping unwanted
    ...    columns.

    ${camelot_tables} =    Get Tables From PDF    devdata${/}text-invoice-table.pdf
    ...    flavor=stream  # notice the algorithm of detecting tables
    @{files} =     Export Tables To Files    ${camelot_tables}
    ...    ${OUTPUT_DIR}${/}invoice.xlsx    output_format=excel

    Open Workbook    ${files}[${0}]    read_only=${True}
    ${table} =    Read Worksheet As Table    header=${True}    start=${3}
    Pop Table Column    ${table}    1
    Log  Table columns: ${table.columns}
    @{last_items} =      Get Table Row    ${table}    -1    as_list=${True}
    Log List    ${last_items}

    [Teardown]    Close Workbook


Camelot Table As CSV
    [Documentation]    Export table from text PDF invoice as CSV file, then read its
    ...    content into a table which doesn't contain a header.

    ${camelot_tables} =    Get Tables From PDF    devdata${/}text-invoice.pdf
    ...    flavor=lattice  # notice the algorithm of detecting tables
    @{files} =     Export Tables To Files    ${camelot_tables}
    ...    ${OUTPUT_DIR}${/}invoice.csv    output_format=csv

    ${table} =    Read table from CSV    ${files}[${0}]    header=${False}
    ${rows}    ${columns} =    Get Table Dimensions    ${table}
    FOR    ${idx}    IN RANGE    0    ${rows}
        @{items} =    Get Table Row    ${table}    ${idx}    as_list=${True}
        Log    ${items}[${0}]: ${items}[${1}]
    END


*** Tasks ***
Extract Text Data With RPA
    [Documentation]    Extract textual data with the local help of `RPA.PDF` library.

    # Keywords below work with the standard `RPA.PDF` library as well.
    Open PDF    devdata${/}text-invoice.pdf

    # Get the entire raw text from the PDF.
    ${text} =    Get Text From PDF
    Log To Console    ${text}

    # Retrieve only text pars matching locator. (and its neighbours)
    # Test regular expressions with: https://regexr.com/
    @{matches} =    Find Text    Service    direction=down
    Log    First item under "Service": ${matches[0].neighbours}[${0}]

    @{matches} =    Find Text    subtext:Web Design    regexp=.*%  # filters for percentage neighbours
    Log    The "Adjust" column value to the right of the 'Web Design' "Service": ${matches[0].neighbours}[${0}]

    @{matches} =    Find Text    subtext:total    ignore_case=${True}    direction=down
    ...    closest_neighbours=${4}
    Log    Next 4 prices below "Sub Total": ${matches[1].neighbours}

    @{matches} =    Find Text    regex:.*@
    Log    Show all the lines containing an e-mail address:
    FOR    ${match}    IN    @{matches}
        ${mail_line} =    Get Lines Matching Pattern    ${match.anchor}    *@*
        Log    ${mail_line}
    END


Extract Tabular Data With Camelot
    [Documentation]    Extract tables with the Camelot library.
    ...    (see external dependency: https://pypi.org/project/camelot-py/)

    # Keywords below require the extended PDF library. (`ExtendedPDF`)
    Camelot Table As Excel
    Camelot Table As CSV


Extract Structured Data With AI
    [Documentation]    Extract fields detected in both text or image-based PDFs using
    ...    3rd-party external services wrapped by the `RPA.DocumentAI` library.

    ${image_pdf} =    Set Variable    devdata${/}image-invoice.pdf

    # No text can be retrieved at all from this kind of image-based invoice.
    Open PDF    ${image_pdf}
    ${text} =    Get Text From PDF
    Log To Console    Text: ${text}
    @{matches} =    Find Text    subtext:item    ignore_case=${True}
    Log To Console    Matches: ${matches}

    # Keywords below work with the `RPA.DocumentAI` library.
    Init Engine    base64ai    vault=document_ai:base64ai
    Predict    ${image_pdf}
    @{data} =    Get Result
    Log List    ${data}
