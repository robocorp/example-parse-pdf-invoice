# Extract data from PDF files displaying invoice like information

Show-case multiple ways of extracting information from different kinds of PDF files
(text based or scans), mainly presenting invoice data.

Read more on the
[challenges](https://pypdf.readthedocs.io/en/latest/user/extract-text.html) of getting
information out of PDF files.

## Tasks

### `Extract Text Data With RPA`

Extract textual data with the local help of `RPA.PDF` library.

Watch demo: https://www.loom.com/share/4bc28045f45941d18d935a60e35e227a

> Usually this is sufficient for most of the cases.


### `Extract Tabular Data With Camelot`

Extract tables with the Camelot library. (see external
[dependency](https://pypi.org/project/camelot-py/))

Watch demo: https://www.loom.com/share/87d434dad8d748ada566a8c199cbea90

> This is useful for getting out nicely formatted tabular data, but comes at the cost
> of heavier dependencies brought in the built environment.

### `Extract Structured Data With AI`

Extract fields detected in both text or image-based PDFs using 3rd-party external
services wrapped by the `RPA.DocumentAI` library.

Watch demo: https://www.loom.com/share/e9753b884b6f4aa1ac0271580a0cf682

> When all the options above fail (or provide inaccurate data), it is time to employ a
> Machine Learning model specially trained to detect and structure fields of interest
> from the provided input file, be it text-based or even image.
