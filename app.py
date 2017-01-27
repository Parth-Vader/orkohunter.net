# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, render_template, redirect, request
from flask_session import Session

from handlers import depends as depends_handler

app = Flask(__name__, static_url_path='/static')
sess = Session()


@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


@app.route("/")
def main():
    return render_template('home/index.html')


@app.route("/abwid")
def abwid():
    return render_template('home/abwid.html')


@app.route("/contact")
def contact():
    return render_template('home/contact.html')


@app.route("/projects")
def projects():
    return render_template('home/projects.html')


@app.route("/keep")
def keep():
    return render_template('keep/index.html')


@app.route("/ping-me")
def ping_me():
    return render_template('ping-me/index.html')


@app.route("/ping-me/faqs")
def ping_me_faqs():
    return render_template('ping-me/faqs.html')


@app.route("/depends")
def depends():
    data = depends_handler.index()
    return render_template('depends/index.html', data=data)


@app.route("/depends/<package>")
def depends_package(package):
    analysis_exists, data = depends_handler.package_view(package)
    return render_template('depends/package.html', data=data, analysis_exists=analysis_exists)


@app.route("/depends/<package>/refresh")
def depends_package_refresh(package):
    depends_handler.package_refresh(package)
    return redirect("/depends/" + package)

app.secret_key = os.environ["APP_SECRET_KEY"]
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
app.debug = False

if __name__ == '__main__':
    app.run(debug=True)
