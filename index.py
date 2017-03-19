"""
Copyright (c) 2017 Marco Aceti <dev@marcoaceti.it>

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTIONWITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

from config import GITHUB_USERNAME, GITHUB_PASSWORD

import xml.etree.ElementTree as Et

import subprocess
import os
import shutil

from flask import Flask, redirect, jsonify
app = Flask(__name__)


@app.route('/<author>/<repo>')
def index(author, repo):
    os.chdir('/tmp')

    clone = 'https://{user}:{password}@github.com/{author}/{repo}'.format(
        user=GITHUB_USERNAME, password=GITHUB_PASSWORD, author=author, repo=repo
    )

    subprocess.call(['git', 'clone', clone, repo])
    subprocess.call(['cloc', repo, '--xml', '--out=temp.xml'])

    try:
        shutil.rmtree('/tmp/' + repo)
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "No repository found"})

    tree = Et.parse('temp.xml')
    os.remove('temp.xml')

    count = tree.find('header/n_lines').text
    return redirect('https://img.shields.io/badge/lines%20of%20code-{count}-brightgreen.svg'.format(count=count))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=4998)
