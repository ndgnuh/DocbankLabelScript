from typing import Dict, List, Tuple
from .structures import Extracted, Box
from . import convert


def gen_labelme_rect(label: str, box: Box) -> Dict:
    """Create a rect annotation in labelme format

    Args:
        label:
            The label annotations
        box:
            List of coordinate in x1 y1 x2 y2 order
    """
    x1, y1, x2, y2 = box
    return {
        "label": label,
        "points": [[x1, y1], [x2, y2]],
        "group_id": None,
        "description": "",
        "shape_type": "rectangle",
        "flags": {},
    }


def create_labelme_sample(page: Extracted) -> Dict:
    """Create a labelme formatted json dict from the inputs

    Args:
        page:
            The information of extracted page

    Returns:
        sample:
            A dict of sample data in labelme format.
    """
    sample = {}
    sample["version"] = "5.2.1"
    sample["flags"] = {}
    sample["shapes"] = []
    sample["imageHeight"] = page.image.height
    sample["imageWidth"] = page.image.width
    sample["imagePath"] = ""
    sample["imageData"] = convert.pillow2base64(page.image)
    for box in page.boxes:
        shape = gen_labelme_rect('text', box)
        sample['shapes'].append(shape)
    return sample
