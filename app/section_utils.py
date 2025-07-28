from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

MAX_PAGES = 50

def extract_full_text(pdf_path):
    pages_text = []
    for i, page_layout in enumerate(extract_pages(pdf_path)):
        if i >= MAX_PAGES:
            break
        page_text = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text += element.get_text()
        pages_text.append(page_text)
    return pages_text

def slice_section_text(pages_text, outline, idx):
    start_page = outline[idx]["page"] - 1
    start_title = outline[idx]["text"]
    if idx + 1 < len(outline):
        end_page = outline[idx + 1]["page"] - 1
    else:
        end_page = len(pages_text) - 1

    if start_page == end_page:
        page_text = pages_text[start_page]
        pos = page_text.find(start_title)
        return page_text[pos:] if pos >= 0 else page_text
    else:
        return "\n".join(pages_text[start_page:end_page + 1])