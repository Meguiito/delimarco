from flask import Flask, jsonify, request, make_response, send_file, request
import io
import flask
from io import BytesIO
import base64
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
client = MongoClient("mongodb+srv://"+os.environ["MONGO_USER"]+":"+os.environ["MONGO_PASSWORD"]+"@cluster0.sziulk8.mongodb.net/?retryWrites=true&w=majority")
db = client.Facturas
factras = db.facts
db2=client.ImagenesFacturas
imagees=db2.Images
# Settings
cors=CORS(app)



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/<data>")
def api(data):
    return jsonify({"message": "Successfully received client request for "+data+"."})


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
