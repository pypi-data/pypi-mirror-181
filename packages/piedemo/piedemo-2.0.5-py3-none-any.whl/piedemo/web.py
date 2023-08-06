import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from pathlib import Path
import shutil
from .checkpoint import url_download_file
from flask import Flask, send_from_directory, render_template, render_template_string, request, redirect, url_for, jsonify
import zipfile
import pickle
import copy
import threading
import time
import argostranslate
from argostranslate.translate import translate as argos_translate
from .ngrok_utils import run_with_ngrok
from .cache import Cache, make_storage


def parse_url(redirect_url):
    if '?' in redirect_url and '=' in redirect_url:
        path_url, values = redirect_url.split('?')
        values = dict(map(lambda x: tuple(x.split('=')), values.split('&')))
    else:
        path_url = redirect_url
        values = {}
    return path_url, values


class Web(object):
    PIEBREAK = '__piedemo__'

    def __init__(self,
                 pages,
                 name="PieDataWebDemo",
                 aggregation_rule='by_underscore'):
        self.name = name
        self.pages = pages
        self.aggregation_rule = aggregation_rule

        self.static_path = os.path.join(os.path.dirname(__file__), 'build')
        self.download_static_files()

    def download_static_files(self):
        if not os.path.exists(self.static_path):
            cached_path = os.path.join(os.path.dirname(__file__))
            zip_path = os.path.join(cached_path, 'static.zip')
            url_download_file(url="https://github.com/PieDataLabs/piedemo_frontend/releases/download/V2.0.5/static.zip",
                              cached_path=zip_path)
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(cached_path)
            os.remove(zip_path)

    def run(self,
            host='0.0.0.0',
            port=8008,
            debug=True,
            **options):
        print(self.static_path)
        app = Flask(self.name, static_folder=self.static_path)
        sem_translation = threading.Semaphore()

        if host == 'ngrok':
            run_with_ngrok(app)

        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            if path != "" and os.path.exists(app.static_folder + '/' + path):
                return send_from_directory(app.static_folder, path)
            else:
                return send_from_directory(app.static_folder, 'index.html')

        @app.route('/api/content/', methods=['GET'], defaults={"path": ""})
        @app.route('/api/content/<path:path>', methods=['GET'])
        def send_content(path):
            return jsonify(self.pages[path].get_content(**request.args))

        @app.route('/api/process/', methods=['POST'], defaults={"path": ''})
        @app.route('/api/process/<path:path>', methods=['POST'])
        def process(path):
            data = request.files.to_dict()
            data.update(request.form.to_dict())
            data.update(request.args.to_dict())
            data = self.aggregate(data)
            redirect_url = self.pages[path].process(**data)
            print("Redirected to:", redirect_url)
            path_url, values = parse_url(redirect_url)
            return redirect(url_for("serve", path=path_url, **values))

        @app.route("/api/translate/", methods=["POST"])
        def translate():
            data = request.json
            text = data['text']
            from_code = data['from_code']
            to_code = data['to_code']
            print("Translating:", from_code, to_code, text)
            sem_translation.acquire()
            result = argos_translate(text, from_code, to_code)
            sem_translation.release()
            return jsonify({"text": result})

        if host == 'ngrok':
            app.run(port=port, **options)
        else:
            app.run(host=host, port=port, debug=debug, **options)

    def aggregate(self, data):
        if self.aggregation_rule is None:
            return data

        if self.aggregation_rule == 'by_underscore':
            new_data = {}
            for key in data.keys():
                if self.PIEBREAK not in key:
                    new_data[key] = make_storage(data[key])

            for key in data.keys():
                if self.PIEBREAK not in key:
                    continue
                ks = key.split(self.PIEBREAK)
                setattr(new_data[ks[0]], self.PIEBREAK.join(ks[1:]), data[key])
            return new_data

        raise NotImplementedError()

    def __del__(self):
        shutil.rmtree(self.static_path)
