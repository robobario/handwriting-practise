import tempfile

from bottle import post, run, request, response, hook, route
import os
import json

from pdf_generator import gen_pdf

directory = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(directory, "data", "config.json")) as f:
    config = json.load(f)


def get_config(name):
    return config['samples'][name]


def read_bytes(path):
    with open(path, "rb") as guts:
        return guts.read()


@post('/sheet')
def sheet():
    body = request.json["body"]
    config_name = request.json["config_name"]
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        pdf_target = os.path.join(tmpdirname, "temp.pdf")
        gen_pdf(body, get_config(config_name), tmpdirname, "temp", pdf_target)
        pdfBody = read_bytes(pdf_target)
    response.content_type = "application/pdf"
    response.headers.append("Content-Disposition", "inline; filename=\"mypdf.pdf\"")
    return pdfBody


_allow_origin = 'https://robobario.github.io'
_allow_methods = 'POST'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers


@route('/', method='OPTIONS')
@route('/<path:path>', method='OPTIONS')
def options_handler(path=None):
    return


run(host='0.0.0.0', port=int(os.environ["PORT"]), debug=True)
