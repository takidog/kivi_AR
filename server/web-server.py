import json
import os
import util
import redis
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_file, send_from_directory, url_for)

from kivicube_account import kivicube_account
from kivicube_client import kivicube_viewer
from kivicube_script import create_AR_to_output

app = Flask(__name__)

try:
    REDIS_URL = os.environ['REDIS_URL']
except KeyError:
    REDIS_URL = 'redis://127.0.0.1:6379'
kivicube_user = kivicube_account(
    username='buluni.ha@gmail.com', password='dogewow')
kivi_viewer = kivicube_viewer()
red_string = redis.StrictRedis.from_url(
    url=REDIS_URL, db=4, charset="utf-8", decode_responses=True)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
ALLOWED_MIME_TYPES = {'image/jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


@app.route('/webxr-view/<path:filename>')
def custom_static(filename):
    return send_from_directory('webxr-view/', filename)


@app.route('/api/view/scene')
def scene():
    if red_string.exists(request.args.get('unique_id')):
        return jsonify(json.loads(red_string.get(request.args.get('unique_id')))), 200
    return 404


@app.route('/<path:model_id>')
def index(model_id):

    if red_string.exists(model_id):
        return render_template('template.html')
    return "QQ"


@app.route('/upload', methods=['POST'])
def upload():
    show_image = request.files['show_image']
    detection_image = request.files['detection_image']

    show_image_filename = util.randStr(32)+".jpg"
    detection_image_filename = util.randStr(32)+".jpg"
    show_image.save('tmp/'+show_image_filename)
    detection_image.save('tmp/' + detection_image_filename)

    res = create_AR_to_output(
        user=kivicube_user,
        viewer=kivi_viewer,
        show_image='tmp/{}'.format(show_image_filename),
        detection_image='tmp/{}'.format(detection_image_filename)
    )
    os.system('rm -f tmp/{}'.format(show_image_filename))
    os.system('rm -f tmp/{}'.format(detection_image_filename))
    if isinstance(res, str):
        return jsonify({'id': res}), 200
    return jsonify({}), 500


if __name__ == '__main__':
    app.debug = True
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run()
