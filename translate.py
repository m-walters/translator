import argparse
import io
import os

from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def translate_pdf(src_lang: str, target_lang: str, input_path, output_path):
    # Initialize translator
    translator = GoogleTranslator(source=src_lang, target=target_lang)

    # Read the PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Extract the text from the page
        original_text = page.extract_text()

        # Translate the text
        translated_text = translator.translate(original_text)

        # Create a new blank page with translated text using ReportLab
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        text_object = can.beginText(72, 800)  # Starting position for text

        # Add translated text line by line
        for line in translated_text.split("\n"):
            text_object.textLine(line)

        can.drawText(text_object)
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        translated_pdf = PdfReader(packet)

        # Add the translated page to the writer
        writer.add_page(translated_pdf.pages[0])

    # Save the translated PDF
    writer.write(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Translate PDF files from one language to another."
    )
    parser.add_argument('src_lang', type=str, help='source language code')
    parser.add_argument('target_lang', type=str, help='target language code')
    parser.add_argument(
        'filenames', metavar='filenames', type=str, nargs='+',
        help='one or more filenames to translate'
    )
    args = parser.parse_args()

    src_lang = args.src_lang
    target_lang = args.target_lang
    in_dir = "docs/in/"
    out_dir = "docs/out/"

    fnames = args.filenames
    # If the only argument is a directory (or no argument given), we process all files
    if len(fnames) == 1 and os.path.isdir(fnames[0]):
        in_dir = fnames[0]
        fnames = os.listdir(in_dir)
    elif len(fnames) == 0:
        fnames = os.listdir(in_dir)

    for fname in fnames:
        # Strip the in_dir from the filename if exists
        fname = fname.split(in_dir)[-1]

        # Append _en to the output file name
        outname = fname.split(".")[0] + f"_{target_lang}.pdf"

        input_path = os.path.join(in_dir, fname)
        output_path = os.path.join(out_dir, outname)

        # Check paths
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File not found: {input_path}")

        translate_pdf(src_lang, target_lang, input_path, output_path)


if __name__ == "__main__":
    main()
