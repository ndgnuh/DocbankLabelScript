from dataclasses import dataclass
from typing import List, Tuple, Optional
from PIL import Image


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
    boxes: List[Tuple[int, int, int, int]]
