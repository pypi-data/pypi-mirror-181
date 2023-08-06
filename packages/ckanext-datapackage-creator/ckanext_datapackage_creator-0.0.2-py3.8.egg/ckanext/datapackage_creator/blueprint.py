import json

from flask import Blueprint, make_response, request

from .inference import inference_data


dp_creator = Blueprint(u'datapackage_creator', __name__)


@dp_creator.route('/inference')
def inference():
    response = make_response()
    if request.method == 'POST':
        response.content_type = 'application/json'
        file = request.files['file']
        file.save(f'/tmp/{file.filename}')
        result = inference_data(f'/tmp/{file.filename}')
        response.data = json.dumps(result)
    else:
        response.status = 405
    return response
