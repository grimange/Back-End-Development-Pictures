from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """ return all pictures in data list """
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """ get picture in data list by picture id """
    if data:
        for d in data:
            if id == d['id']:
                return jsonify(d), 200
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """ add picture to data list """
    if data:
        picture = request.json
        for d in data:
            if picture['id'] == d['id']:
                return {"Message": f"picture with id {picture['id']} already present"}, 302
        data.append(picture)
        # jsonFile = open(json_url, 'w')
        # jsonFile.write(json.dumps(data))
        return jsonify(picture), 201
    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """ update picture on the data list """
    if data:
        picture = request.json
        for d in data:
            if id == d['id']:
                data.remove(d)
                data.append(picture)
                return jsonify(picture), 200
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500    
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """ delete picture in data list """
    if data:
        for d in data:
            if id == d['id']:
                data.remove(d)
                return jsonify({}), 204
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500    