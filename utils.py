from PIL import Image, ImageOps
from io import BytesIO
import base64
import json
import numpy
import glob
import os

# image_to_base64
def image_to_base64(image: Image) -> str:
    buff = BytesIO()
    image.save(buff, format="png")
    return base64.b64encode(buff.getvalue()).decode('utf-8')

# base64_to_image
def base64_to_image(data: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(data)))
 
# extract_image_data
def extract_image_data(data: dict) -> ([], []):
    images_name = []
    images = []
    # extract images
    for image_name in data["images"]:
        # decode image
        image = base64_to_image(data["images"][image_name]).convert("L")
        # append images
        images_name.append(image_name)
        images.append(image)
    # return results
    return images_name, images

# pack_image_data
def pack_image_data(images_crop: [], images_repr: []) -> dict:
    data = { "success": True, "images": { "crop": {}, "repr": {} } }
    # pack crops
    for image in images_crop:
        file_name, file_ext = os.path.splitext(os.path.basename(image.filename))
        data["images"]["crop"][file_name+file_ext] = image_to_base64(image)
    # pack representative crops
    for image in images_repr:
        file_name, file_ext = os.path.splitext(os.path.basename(image.filename))
        data["images"]["repr"][file_name+file_ext] = image_to_base64(image)
    return data

# calculate_crops
def calculate_crops(images: []) -> ([], []):
    images_crop = [Image.open(file) for file in glob.glob("./images/crops_images/*.png")]
    images_repr = [Image.open(file) for file in glob.glob("./images/representative_crops_images/*.png")]
    return images_crop, images_repr