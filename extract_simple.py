from icecream import ic
from os import path, makedirs, listdir
from PIL import Image, ImageDraw
from io import BytesIO
from tqdm import tqdm
import uuid
import fitz
import json


def normalize_bounding_box(x1, y1, x2, y2, width, height):
    norm_const = 1000
    return (
        x1 / width * norm_const,
        y1 / height * norm_const,
        x2 / width * norm_const,
        y2 / height * norm_const,
    )


def pixmap_to_pilimage(pixmap):
    data = pixmap.tobytes()
    io = BytesIO(data)
    return Image.open(io)


def extract(pdf_file):
    doc = fitz.open(pdf_file)
    pages: List = []
    # Why the double s? because it's a list of a list of items
    textss: List[List] = []
    boxess: List[List] = []
    pbar = tqdm(doc, path.basename(pdf_file))
    for page in pbar:
        # Extracting images of the pages
        pixmap = page.get_pixmap()
        pixmap = pixmap_to_pilimage(pixmap)
        pages.append(pixmap)

        # Extracting the texts
        width, height = pixmap.size
        texts = []
        boxes = []
        for (x1, y1, x2, y2, word, _, _, _) in page.get_text("words"):
            box = normalize_bounding_box(x1, y1, x2, y2, width, height)
            boxes.append(box)
            texts.append(word)

        textss.append(texts)
        boxess.append(boxes)
    return pages, textss, boxess


def main(input_dir="test_sample", output_dir="outputs/something"):

    makedirs(output_dir, exist_ok=True)

    for file in listdir(input_dir):
        file = path.join(input_dir, file)
        name = str(uuid.uuid5(uuid.NAMESPACE_DNS, file))[:17]

        pages, textss, boxess = extract(file)
        counts = range(len(pages))

        for item in zip(counts, pages, textss, boxess):
            page_idx, page, texts, boxes = item
            annotations = dict(texts=texts, boxes=boxes)

            out_name = f"{name}-{page_idx:09d}"
            out_image = path.join(output_dir, f"{out_name}.jpg")
            out_annotations = path.join(output_dir, f"{out_name}.json")

            page.save(out_image)
            with open(out_annotations, "w", encoding="utf8") as f:
                json.dump(annotations, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    main(args.input, args.output)

# output_dir = "test_output"
# input_file = "/home/hung/Data/pdfs/vi/preparing-slides.pdf"
# input_file = "/home/hung/Data/pdfs/vi/6 khoa tim tai lieu_web.pdf"
# input_file = "/home/hung/Data/pdfs/vi/3_HƯỚNG DẪN TRÍCH DẪN TÀI LIỆU THAM KHẢO.pdf"
# input_file = "./test_sample/Shrapnel-White-Paper.pdf"
# input_file = "./test_sample/Huong dan dang ky doanh nghiep qua mang dien tu v4.pdf"
# doc = fitz.open(input_file)
# textboxes = []
# for i, page in enumerate(doc):
#     ic(page.derotation_matrix)
#     pixmap = page.get_pixmap()
#     name = path.join(output_dir, f"image-{i:04d}.jpg")
#     pixmap.save(name)
#     image = Image.open(name)
#     draw = ImageDraw.Draw(image)
#     text = page.get_text("words")
#     for (x1, y1, x2, y2, word, _, _, _) in text:
#         draw.rectangle((x1, y1, x2, y2), outline=(255, 0, 0))
#     image.save(name)
#     # x1, y1, x2, y2, word, _, _, _, _ = text
#     # ic(text)
#     # textboxes.append(text)
#     # text = json.loads(text)
#     # texts.append(text)

# with open("output.json", "w") as f:
#     json.dump(textboxes, f, ensure_ascii=False, indent=2)
