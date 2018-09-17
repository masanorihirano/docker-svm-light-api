# coding: utf-8
from flask import Flask, abort, jsonify, request, send_file, g
import os
import uuid
import subprocess
from datetime import datetime

api = Flask(__name__)
api.config['JSON_AS_ASCII'] = False
# limit upload file size : 100MB
api.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

UPLOAD_DIR = "/tmp"

files = os.listdir("/tmp")
for file in files:
    try:
        os.remove(file)
    except:
        print("Delete Eroor")

old_file_dict = {}

@api.route('/svm-light/v1/learn', methods=['POST'])
def learn():
    try:
        if not (request.files and 'example_file' in request.files):
            abort(400)
        filename = os.path.join(UPLOAD_DIR,str(uuid.uuid4()))
        request.files['example_file'].save(filename)
        result_file = filename + ".model"
        if "option" in request.values:
            cmd = ["bin/svm_learn"]
            cmd += request.values["option"].encode("utf-8").split(" ")
            cmd += [filename,result_file]
            print cmd
            subprocess.check_call(cmd)
        else:
            subprocess.check_call(["bin/svm_learn",filename,result_file])
        os.remove(filename)
        old_file_dict[result_file] = datetime.now()
        return send_file(result_file, as_attachment = True, attachment_filename = "svm_model", mimetype = "text/plain")
    except Exception as e:
        print(e)
        abort(500)

@api.route('/svm-light/v1/classify', methods=['POST'])
def classify():
    try:
        if not (request.files and 'example_file' in request.files):
            abort(400)
        if not (request.files and 'model_file' in request.files):
            abort(400)
        example_filename = os.path.join(UPLOAD_DIR,str(uuid.uuid4()))
        request.files['example_file'].save(example_filename)
        model_filename = os.path.join(UPLOAD_DIR,str(uuid.uuid4()))
        request.files['model_file'].save(model_filename)
        result_file = os.path.join(UPLOAD_DIR,str(uuid.uuid4()))
        if "option" in request.values:
            cmd = ["bin/svm_classify"]
            cmd += request.values["option"].encode("utf-8").split(" ")
            cmd += [example_filename,model_filename,result_file]
            print cmd
            subprocess.check_call(cmd)
        else:
            subprocess.check_call(["bin/svm_classify",example_filename,model_filename,result_file])
        os.remove(example_filename)
        os.remove(model_filename)
        old_file_dict[result_file] = datetime.now()
        return send_file(result_file, as_attachment = True, attachment_filename = "svm_prediction", mimetype = "text/plain")
    except Exception as e:
        print(e)
        abort(500)

@api.after_request
def common(response):
    del_candidate = []
    for (old_file, time) in old_file_dict.iteritems():
        if int(datetime.now().strftime('%s')) - int(time.strftime('%s')) >= 0*10*60:
            try:
                os.remove(old_file)
            except:
                print("Delete Eroor")
            del_candidate.append(old_file)
    for i in del_candidate:
        del old_file_dict[i]
    return response


@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@api.errorhandler(405)
def not_allowed(error):
    return jsonify({'error': 'Method Not Allowed. You have to use POST method.'}), 405

@api.errorhandler(400)
def bad_post(error):
    return jsonify({'error': 'Inputs are not correct.'}), 400

@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error.'}), 500

api.run(host='0.0.0.0', port=3001,debug=True)