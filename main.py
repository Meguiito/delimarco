from flask import Flask, jsonify, request, make_response, send_file
import io
import flask
from io import BytesIO
import base64
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os
import bson
from bson.objectid import ObjectId
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


@app.route('/facts', methods=['PUT'])
def createUser():
  print(request.json)
  id = db.facts.insert_one({
    'nfac': request.json['nfac'],
    'empresa': request.json['empresa'],
    'monto': request.json['monto'],
    'ciudad': request.json['ciudad'],
    'contacto': request.json['contacto'],
    'ingreso': request.json['ingreso'],
    'totalfac': request.json['totalfac'],
  })
  return jsonify("error")


@app.route('/facts', methods=['GET'])
def getUsers():
    factras = []
    for doc in db.facts.find():
        factras.append({
            '_id': str(ObjectId(doc['_id'])),
            'nfac': doc['nfac'],
            'empresa': doc['empresa'],
            'monto': doc['monto'],
            'ciudad': doc['ciudad'],
            'contacto': doc['contacto'],
            'ingreso': doc['ingreso'],
            'totalfac': doc['totalfac'],

        })
    return jsonify(factras)

@app.route('/facts/<id>', methods=['GET'])
def getUser(id):
  user = db.facts.find_one({'_id': ObjectId(id)})
  print(user)
  return jsonify({
      '_id': str(ObjectId(user['_id'])),
      'nfac': user['nfac'],
      'empresa': user['empresa'],
      'monto': user['monto'],
      'ciudad': user['ciudad'],
      'contacto': user['contacto'],
      'ingreso': user['ingreso'],
      'totalfac': user['totalfac'],

  })


@app.route('/facts/<id>', methods=['DELETE'])
def deleteUser(id):
  db.facts.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'User Deleted'})

@app.route('/facts/<id>', methods=['PUT'])
def updateUser(id):
  print(request.json)
  db.facts.update_one({'_id': ObjectId(id)}, {"$set": {
    'nfac': request.json['nfac'],
    'empresa': request.json['empresa'],
    'monto': request.json['monto'],
    'ciudad': request.json['ciudad'],
    'contacto': request.json['contacto'],
    'ingreso': request.json['ingreso'],
    'totalfac': request.json['totalfac'],
  }})
  return jsonify({'message': 'Factura actualizada actualizado'})


@app.route('/Images', methods=['POST'])
def upload_image():
    image = request.files['image']
    nfact = request.form['nfact']
    image_data = image.read()
    image_encoded = base64.b64encode(image_data).decode('utf-8')
    id = db2.Images.insert_one({'image': image_encoded, 'nfact': nfact})
    return 'Image uploaded successfully!'

@app.route('/Images/<id>', methods=['GET'])
def download_image(id):
    image = db2.Images.find_one({'_id': ObjectId(id)})
    image_data = base64.b64decode(image['image'])
    return send_file(io.BytesIO(image_data), mimetype='image/jpeg', as_attachment=True ,download_name="pepe.jpg")

@app.route("/Images", methods=["GET"])
def get_images():
    images = list(db2.Images.find({}))
    print(images)
    return jsonify({"images": [{"id": str(image["_id"]), "image": image["image"], "nfact": image["nfact"]} for image in images]})

 
@app.route('/Images/<id>', methods=['DELETE'])
def deleteimg(id):
  db2.Images.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'Image Deleted'})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
