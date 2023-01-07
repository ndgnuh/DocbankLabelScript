from argparse import ArgumentParser
from PIL import Image, features
from os import path, walk, makedirs
from icecream import ic
from tqdm import tqdm
import json
import PIL


def find_images(root):
    lookup = {k: True for k in Image.registered_extensions()}
    found = []
    for root, _, files in walk(root):
        image_files = [
            path.join(root, file) for file in files
            if lookup.get(path.splitext(file)[1], False)
        ]

        found.extend(image_files)
    return found


def main(inputdir, outputdir):
    image_files = find_images(inputdir)
    annotation_files = [
        path.splitext(file)[0] + ".json"
        for file in image_files
    ]

    counter = 0
    makedirs(outputdir, exist_ok=True)
    makedirs(path.join(outputdir, "images"), exist_ok=True)

    # Empty the annotation file
    annotation_file = path.join(outputdir, "annotation.txt")
    with open(annotation_file, "w") as f:
        f.write("")

    # num_texts = 0
    # for a_file in tqdm(annotation_files):
    #     with open(a_file, encoding="utf-8") as io:
    #         annotation = json.load(io)
    #         boxes = annotation['boxes']
    #         num_texts += len(boxes)

    pbar = zip(image_files, annotation_files)
    pbar = tqdm(pbar, total=len(image_files))
    for (i_file, a_file) in pbar:
        image = Image.open(i_file)
        width, height = image.size
        with open(a_file, encoding="utf-8") as io:
            annotation = json.load(io)
            boxes = annotation['boxes']
            texts = annotation['texts']
            for (x1, y1, x2, y2), text in zip(boxes, texts):
                h = y2 - y1
                w = x2 - x1
                if w < h or h < 16:
                    continue

                x1 = x1 / 1000 * width
                x2 = x2 / 1000 * width
                y1 = y1 / 1000 * height
                y2 = y2 / 1000 * height

                try:
                    counter += 1
                    output_name = f"{counter:09d}.jpg"
                    output_file = path.join(outputdir, "images", output_name)
                    cropped = image.crop((x1, y1, x2, y2))
                    cropped.save(output_file)
                    with open(annotation_file, "a", encoding="utf-8") as io:
                        io.write(f"images/{output_name}\t{text}\n")
                except Exception:
                    counter = counter - 1


if __name__ == "__main__":
    main("output-pdf-vn", "pdf-ocr-dataset")
