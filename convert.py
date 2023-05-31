#!/bin/env python3
from io import BytesIO
from base64 import b64encode
from os import path, makedirs, listdir
from argparse import ArgumentParser

import fitz
from PIL import Image, ImageDraw
from tqdm import tqdm
from src import extract


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
        print(outputs)


if __name__ == "__main__":
    main()
