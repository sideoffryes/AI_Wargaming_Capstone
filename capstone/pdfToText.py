import sys

import pypdf


def pdf_to_text(pdf_path: str, output_txt: str):
    """Opens the specified PDF file and returns its contents as a text file.

    :param pdf_path: The path to the PDF file
    :type pdf_path: str
    :param output_txt: The path to save the text file containing the contents of the PDF file
    :type output_txt: str
    """
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = pypdf.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + '\n\n'  # Add double new lines between pages

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    pdf_path = sys.argv[1]

    output_txt = sys.argv[1].split(".")[0] + ".txt"

    pdf_to_text(pdf_path, output_txt)

    print("PDF converted to text successfully!")