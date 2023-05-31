"""
Convert a folder of PDF to a folder of LabelME samples
"""
#!/bin/env python3
import json
from io import BytesIO
from base64 import b64encode
from os import path, makedirs, listdir
from argparse import ArgumentParser

import fitz
from PIL import Image, ImageDraw
from tqdm import tqdm
from src import extract, labelme


def main():
    """Main entry point"""
    parser = ArgumentParser()
    parser.add_argument("inputdir")
    parser.add_argument("outputdir")

    args = parser.parse_args()
    assert path.isdir(args.inputdir)
    for basename in tqdm(listdir(args.inputdir), "Extracting"):
        if not basename.endswith(".pdf"):
            continue
        input_file = path.join(args.inputdir, basename)
        outputs = extract.extract_pdf(input_file)
        labelmes = [labelme.create_labelme_sample(page) for page in outputs]

        for i, sample in enumerate(labelmes):
            name = extract.gen_suffix(basename, f"-{i:03d}")
            name = extract.replace_ext(name, ".json")
            data = json.dumps(sample, ensure_ascii=False, indent=4)
            output_path = path.join(args.outputdir, name)
            with open(output_path, "w", encoding='utf-8') as fp:
                fp.write(data)


if __name__ == "__main__":
    main()
