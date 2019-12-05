import click
import logging.config
import time
from elasticsearch import Elasticsearch

from flask import Flask, send_file, request

app = Flask(__name__)


@app.route('/test')
def index():
    data = request.args or {}
    print(type(data.get('type')))
    return "hello world"


@app.route('/test/download')
def download():
    file_path = 'E:\README.md'
    # as_attachment 重命名
    # attachment_filename 重命名的文件名
    rv = send_file(file_path, as_attachment=True, attachment_filename='chat_messages.txt')
    return rv


if __name__ == "__main__":
    app.run(port=9999, debug=True)

