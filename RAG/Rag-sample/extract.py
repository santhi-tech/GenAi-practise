import os
import pymupdf
import datetime 
from PIL import Image # pillow is the package for images
import logging, json


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("This is to extract data from pdf")


# Initalize the pdf file here
def initialize(pdf_name="chapter1.pdf",
               image_folder="images",
               text_folder="text",
               json_file="save_image_metadata.json"):

    pdf_path = os.path.join("Maths-Book", pdf_name)
    image_folder= os.path.join("Maths-Book", image_folder)
    text_folder = os.path.join("Maths-Book", text_folder)
    json_file = os.path.join("Maths-Book",json_file)
    
    logger.info(f"Opening pdf_file: {pdf_path}")
    doc = pymupdf.open(pdf_path)

    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)

    return doc, image_folder, text_folder, json_file

# Extract_chapter
def extract_chapter(doc):

    pages = []

    for page_number, page in enumerate(doc, start=1):

        pages.append({
            "page": page_number,
            "text": page.get_text(),
            "current_date": datetime.datetime.now().isoformat(),
            "image_count": len(page.get_images(full=True))
        })
    logger.info(f"extract_chapter: {pages}")
    return pages


def extract_text(doc,text_folder):

    logger.info("Extracting text...")

    pages = []

    for page_no, page in enumerate(doc, start=1):

        text = page.get_text()

        filename = f"page_{page_no}.txt"

        filepath = os.path.join(text_folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        pages.append({

            "page": page_no,

            "text_file": filepath,

            "word_count": len(text.split()),

            "image_count": len(page.get_images(full=True))

        })

    return pages
 
def extract_images(doc,image_folder):

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

            image_path = os.path.join(image_folder,filename)

            with open(image_path, "wb") as f:

                f.write(image_data["image"])

            metadata.append({

                "page": page_no + 1,

                "image_name": filename,

                "image_path": image_path,

                "xref": xref,

                "width": image[2],

                "height": image[3],

                "color_space": image[5],

                "extension": ext,

                "processed_time": datetime.datetime.now().isoformat()

            })

    return metadata


def save_original_image(image_path,image_data):
    """
        Saving original image in images folder.
    """
    with open(image_path, "wb") as f:
        f.write(image_data["image"])

def validate_image(image_path):
    """
        validating image with extenstion.
    """
    if not image_path.lower().endswith(".png"):
        return True
    return is_valid_image(image_path)

def get_image_rect(page, xref):
    """
        Returns the rectangle occupied by the image on the page.
    """

    rects = page.get_image_rects(xref)

    if rects:
        return rects[0]

    return None

def repair_image(page, xref, image_path):
    logging.warning("Repairing PNG %s", image_path)

    rect = get_image_rect(page, xref)

    if rect is None:
        raise ValueError(f"No rectangle found for image {xref}")

    repaired_path = image_path.replace(
        ".png",
        "_repaired.png"
    )

    pix = page.get_pixmap(
        clip=rect,
        dpi=300
    )

    pix.save(repaired_path)

    return repaired_path


def is_valid_image(image_path):
    """
    Returns True if the image can be opened successfully.
    Returns False if the image is corrupted or unreadable.
    """

    try:
        with Image.open(image_path) as img:
            logger.info(f"validating {image_path} without fully decoding it")
            img.verify()   # Verify the image without fully decoding it
        return True

    except Exception:
        return False
    

def save_metadata(metadata_list, json_file):
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=4)


def get_image_metadata(page_no, image):

    return {

        "page": page_no,

        "xref": image[0],

        "width": image[2],

        "height": image[3],

        "color_space": image[5],

        "repaired": False

    }

def close(doc):
    logger.info("clossing the document pdf file")
    doc.close()


def main():

    doc, image_folder, text_folder, json_file = initialize()
    extract_text(doc,text_folder)
    metadata_list = extract_images(doc,image_folder)
    save_metadata(metadata_list, json_file)
    close(doc)


if __name__ == "__main__":
    main()