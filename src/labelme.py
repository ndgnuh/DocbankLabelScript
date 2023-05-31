def labelme_rect(label: str, box: list):
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
        "group_id": null,
        "description": "",
        "shape_type": "rectangle",
        "flags": {},
    }


def create_labelme_sample(image, classes, boxes):
    """Create a labelme formatted json dict from the inputs

    Args:
        image:
            A Pillow image, this will be stored in the sample as B64
        classes:
            List of text classes
        boxes:
            List of bounding box in (xyxy) format

    Returns:
        sample:
            The sample in labelme format.
    """
    pass
