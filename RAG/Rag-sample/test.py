import os
import json
import logging
import datetime
import pymupdf
from PIL import Image

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Initialize
# --------------------------------------------------

PDF_FILE = "Maths-Book/chapter1.pdf"

OUTPUT_DIR = "Maths-Book/output"

TEXT_DIR = os.path.join(OUTPUT_DIR, "text")

IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

METADATA_FILE = os.path.join(
    OUTPUT_DIR,
    "save_image_metadata.json"
)


def initialize():

    os.makedirs(TEXT_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    logger.info("Opening PDF")

    return pymupdf.open(PDF_FILE)


# --------------------------------------------------
# Extract Text
# --------------------------------------------------

def extract_text(doc):

    logger.info("Extracting text...")

    pages = []

    for page_no, page in enumerate(doc, start=1):

        text = page.get_text()

        filename = f"page_{page_no}.txt"

        filepath = os.path.join(TEXT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        pages.append({

            "page": page_no,

            "text_file": filepath,

            "word_count": len(text.split()),

            "image_count": len(page.get_images(full=True))

        })

    return pages


# --------------------------------------------------
# Validate Image
# --------------------------------------------------

def is_valid_image(path):

    try:

        with Image.open(path) as img:

            img.verify()

        return True

    except Exception:

        return False


# --------------------------------------------------
# Repair PNG
# --------------------------------------------------

def repair_png(page, xref, image_path):

    logger.warning("Repairing %s", image_path)

    rects = page.get_image_rects(xref)

    if not rects:
        return None

    rect = rects[0]

    pix = page.get_pixmap(
        matrix=pymupdf.Matrix(3, 3),
        clip=rect,
        alpha=False
    )

    repaired = image_path.replace(
        ".png",
        "_repaired.png"
    )

    pix.save(repaired)

    return repaired


# --------------------------------------------------
# Extract Images
# --------------------------------------------------

def extract_images(doc):

    logger.info("Extracting images...")

    metadata = []

    for page_no in range(len(doc)):

        page = doc.load_page(page_no)

        images = page.get_images(full=True)

        logger.info(
            "Page %s -> %s images",
            page_no + 1,
            len(images)
        )

        for image_no, image in enumerate(images, start=1):

            xref = image[0]

            image_data = doc.extract_image(xref)

            ext = image_data["ext"]

            filename = f"page_{page_no+1}_image_{image_no}.{ext}"

            image_path = os.path.join(
                IMAGE_DIR,
                filename
            )

            with open(image_path, "wb") as f:

                f.write(image_data["image"])

            repaired = False

            repaired_path = None

            if ext.lower() == "png":

                if not is_valid_image(image_path):

                    repaired = True

                    repaired_path = repair_png(
                        page,
                        xref,
                        image_path
                    )

            metadata.append({

                "page": page_no + 1,

                "image_name": filename,

                "image_path": image_path,

                "xref": xref,

                "width": image[2],

                "height": image[3],

                "color_space": image[5],

                "extension": ext,

                "repaired": repaired,

                "repaired_path": repaired_path,

                "processed_time": datetime.datetime.now().isoformat()

            })

    return metadata


# --------------------------------------------------
# Save Metadata
# --------------------------------------------------

def save_metadata(metadata):

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )

    logger.info("Metadata saved")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    doc = initialize()

    logger.info("Starting extraction pipeline")

    pages = extract_text(doc)

    metadata = extract_images(doc)

    save_metadata(metadata)

    logger.info("Pages Processed : %s", len(pages))

    logger.info("Images Processed: %s", len(metadata))

    doc.close()

    logger.info("Pipeline Finished")


if __name__ == "__main__":
    main()