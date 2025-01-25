from imageParsing import imageParse
from pdf2image import convert_from_path

pdf = "sample.pdf"
pages = convert_from_path(pdf, 500)
for i, page in enumerate(pages):
    page.save(f"page_{i}.jpg", "JPEG")