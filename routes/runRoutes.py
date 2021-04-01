"""Routes
"""
from http import HTTPStatus
from run import app
from flask import request
import data
import json
import urllib.parse
import pyodbc


@app.route("/<audioFileType>", methods=['POST'])
def create_file(audioFileType): 
    #get json data
    passrequest_data = request.get_json()

    if audioFileType.lower() == 'song':
        return json.dumps(data.insertSong(passrequest_data))
    elif audioFileType.lower() == 'podcast':
        return json.dumps(data.insertPodcast(passrequest_data))
    elif audioFileType.lower() == 'audiobook':
        return json.dumps(data.insertAudioBook(passrequest_data))     
    else:
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))



@app.route("/<audioFileType>/<audioFileID>", methods=['DELETE'])
def delete_file(audioFileType, audioFileID):
    return json.dumps(data.del_file(audioFileType, audioFileID))


@app.route("/<audioFileType>/<audioFileID>", methods=['PUT'])
def update_file(audioFileType, audioFileID):
    #get json data
    passrequest_data = request.get_json()

    if audioFileType.lower() == 'song':
        return json.dumps(data.updateSong(passrequest_data, audioFileID))
    elif audioFileType.lower() == 'podcast':
        return json.dumps(data.updatePodcast(passrequest_data, audioFileID))
    elif audioFileType.lower() == 'audiobook':
        return json.dumps(data.updateAudioBook(passrequest_data, audioFileID))
    else:
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))


@app.route("/<audioFileType>/<audioFileID>", methods=['GET'])
def get_file(audioFileType, audioFileID):
    audiodata = json.dumps(data.get_databyid(audioFileType, audioFileID), default=str)
    if audiodata == '0':
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        return audiodata


@app.route("/<audioFileType>", methods=['GET'])
def get_audiofiletype(audioFileType):
    audiodata = json.dumps(data.get_databytype(audioFileType), default=str)
    if audiodata == '0':
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        return audiodata