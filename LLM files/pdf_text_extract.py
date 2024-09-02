import re
from pdfminer.high_level import extract_pages,extract_text
from pdfminer.layout import LTTextBoxHorizontal
required_text = []

pdf_path = ["/Users/saitejasriyerramsetti/Documents/MLH/LLM Quiz Generator/LLM files/ Simple Pendulum.pdf"]


def extract_title_and_theory_section(pdf_paths):
    results = []

    for pdf_path in pdf_paths:
        title = None
        required_text = []

        # Extract the entire text from the PDF
        text_all = extract_text(pdf_path)

        # Extract the title
        for page_layout in extract_pages(pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()
                    match = re.search(r'Lab \d+: (.*)', text)
                    if match:
                        title = match.group(1)  # Extract the title after "Lab #: "
                        required_text.append(title)
                        break  
            if title:  # If title is found, stop searching
                break

        # Extract the section between "Theory" and "Procedure"
        match = re.search(r'Theory(.*?)(?=Procedure)', text_all, re.DOTALL)
        if match:
            theory_text = match.group(1).strip()
            required_text.append(theory_text)
        else:
            required_text.append("No text found between 'Theory' and 'Procedure'")

        # Store the results for this PDF
        results.append({
            "pdf": pdf_path,
            "title": title if title else "Title not found",
            "theory_section": required_text[-1] if len(required_text) > 1 else "No theory section found"
        })

    return results
title = extract_title_and_theory_section(pdf_path)
print(title)
