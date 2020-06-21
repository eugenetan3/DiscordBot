import flask
import time
from flask import Flask, request, jsonify
import json
import os


app = flask.Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def default():
    print("Howdy")
    return

if __name__ == '__main__':
    app.run(debug=True)