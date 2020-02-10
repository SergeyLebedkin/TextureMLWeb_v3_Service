from flask import Blueprint, request, jsonify
from utils import *

# create web server
web_server = Blueprint("web_server", __name__)

@web_server.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

# sermentation 2d server
@web_server.route("/texml_v3", methods=["POST"])
def seg2d():
    # get request data
    request_data = request.get_json()
    # extract image data
    images_name, images = extract_image_data(request_data["payload"])
    print("images received:     ", images_name)
    # create image segmentations
    print("start calculations...", images_name)
    images_crop, images_repr = calculate_crops(images)
    print("images calculated:   ", images_name)
    # create response_data
    response_data = pack_image_data(images_crop, images_repr)
    print("images sended:       ", images_name)
    print("=====================")
    # send results
    return jsonify(response_data)