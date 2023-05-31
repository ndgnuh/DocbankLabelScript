from dataclasses import dataclass
from typing import List, Tuple, Optional, Annotated
from PIL import Image

Box = Tuple[int, int, int, int]
Box.__doc__ = "Bounding box format x1 y1 x2 y2"


@dataclass
class Extracted:
    """Information of an extracted PDF page

    Attributes:
        image:
            Pillow image converted from the PDF page
        texts:
            List of all the texts
        boxes:
            Location of the corresponding texts
    """

    image: Image
    texts: List[str]
    boxes: List[Box]
