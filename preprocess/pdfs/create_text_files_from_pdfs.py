import argparse
import os
import re
import glob
import json
import PyPDF2
from PyPDF2 import PdfFileReader

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}:

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information

def read_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texts = []

    for i in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[i]
        texts.append(page.extract_text())

    return texts

def process_pdfs(pdf_directory):
    # Get all PDF files in the directory
    all_pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

    for path in all_pdf_files:
        print("Generating text from pdf:", path)
        texts = read_pdf(path)
        prefix = ".".join(path.split(".")[:-1])
        prefix = re.sub(" ", "_", prefix)
        folder = os.path.join("texts", prefix)

        if not os.path.isdir(folder):
            os.makedirs(folder)
        
        with open(os.path.join(folder, "all_texts.txt"), "w") as tf:
            with open(os.path.join(folder, "slides.json"), "w") as f:
                json.dump(texts, f, indent=4)

            for ti, text in enumerate(texts):
                text_path = os.path.join(folder, f"{ti}.txt")
                with open(text_path, "w") as wf:
                    print(ti, "\n", text)
                    wf.write(text)
                    tf.write(f"### {str(ti)} ###\n")
                    tf.write(text + "\n")
                print("##")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process PDFs in a directory to extract text content")
    parser.add_argument("pdf_directory", type=str, help="Directory containing PDF files")
    args = parser.parse_args()

    # Process PDFs in the specified directory
    process_pdfs(args.pdf_directory)

