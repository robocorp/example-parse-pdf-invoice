from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal

from typing import List

def find_row(pdf_path: str, search_text: str) -> List[str]:
    """
    Find all elements from the same row by matching the coordinates.
    """
    for page_layout in extract_pages(pdf_path):
        horizontal_text_box_elements = [element for element in page_layout if isinstance(element, LTTextBoxHorizontal)]
        search_elements = [element for element in horizontal_text_box_elements if search_text in element.get_text()]
        for search_element in search_elements:
            x0, y0, _, y1 = search_element.bbox
            row_elements = []
            # match all elements
            for element in horizontal_text_box_elements:
                # add the element we are using to search
                if element == search_element:
                    row_elements.append(element.get_text().strip())
                    continue
                ex0, ey0, _, ey1 = element.bbox
                # Check if the element is at the same y-coordinate and after the the search element in the x-coordinate
                if (ey0 == y0 and ey1 == y1 and ex0 > x0):
                    row_elements.append(element.get_text().strip())
            return row_elements

def find_column(pdf_path: str, search_text: str):
    columns_elements = []
    for page_layout in extract_pages(pdf_path):
        horizontal_text_box_elements = [element for element in page_layout if isinstance(element, LTTextBoxHorizontal)]
        search_elements = [element for element in horizontal_text_box_elements if search_text in element.get_text()]
        for search_element in search_elements:
            x0, ey0, x1, _ = search_element.bbox
            # match all elements
            for element in horizontal_text_box_elements:
                # add the element we are using to search
                if element == search_element:
                    columns_elements.append(element.get_text().strip())
                    continue
                ex0, y0, ex1, _ = element.bbox
                # Check if the element is at the same x-coordinate (give or take)
                if (ex0 >= x0 and ex1 <= (x1 + 1) and ey0 > y0):
                    columns_elements.append(element.get_text().strip())
            return columns_elements


