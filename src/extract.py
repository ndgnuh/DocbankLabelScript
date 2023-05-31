from os import path
from typing import List

import fitz
from tqdm import tqdm
from .convert import bytes2pillow
from .structures import Extracted


def extract_pdf(pdfpath: str) -> List[Extracted]:
    """
    Extract texts positions and rasterized page from pdf file and store  them in labelme format

    Args:
        pdfpath:
            Path to PDF file

    Returns:
        outputs:
            List of labelme jsons.
    """
    doc = fitz.open(pdfpath)
    outputs = []
    pbar = tqdm(doc, path.basename(pdfpath))
    for page in pbar:
        # Extracting images of the pages
        pixmap = page.get_pixmap()
        image = bytes2pillow(pixmap.tobytes())

        # Extract texts
        texts = []
        noises = []
        boxes = []
        for x1, y1, x2, y2, word, a, b, c in page.get_text("words"):
            texts.append(word)
            boxes.append([x1, y1, x2, y2])

        # Store outputs
        ex = Extracted(image=image, texts=texts, boxes=boxes)
        outputs.append(ex)
    return outputs


def gen_suffix(name: str, suffix: str) -> str:
    """Helper function to create pretty suffix name

    Args:
        name:
            The basename to prettify
        suffix:
            The suffix

    Examples:
        >>> name_suffix("sample.json", "-01")
        sample-01.json
    """
    namepart, extpart = path.splitext(name)
    return f"{namepart}{suffix}{extpart}"


def replace_ext(filepath: str, ext: str) -> str:
    """Replace file extension of file path"""
    basename, _ = path.splitext(filepath)
    return f"{basename}{ext}"
