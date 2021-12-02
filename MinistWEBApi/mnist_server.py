from flask import Flask
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
from flask import request
import base64
import math
from PIL import Image
from io import BytesIO
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
# variables Flask
app = Flask(__name__)
api = Api(app)


# se carga el modelo de Logistic Regression del Notebook #3
pkl_filename = "ModelMnistLR.pkl"
with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)


class Predict(Resource):

    @staticmethod
    @app.route('/post_mnist', methods = ['POST'])
    def post_mnist():
        print("Begin post Method")
        # parametros
        jsonData = request.get_json()
  
        base64_data = jsonData['base64']

        base64_data=base64_data.replace("b'", "")
        base64_data=base64_data.replace("'", "")

        print("OK Get Base 64")


        imgdata = base64.b64decode(base64_data)
        img = Image.open(BytesIO(imgdata)).convert('L')

        print("OK transform to image")

        img = img.resize((28, 28), Image.ANTIALIAS)


        imgGray = np.array(img).reshape(1, 784).astype(np.uint8) #/ 255

        print("ready to predict")
        
        out = {'Prediccion': int(model.predict(imgGray)[0])}

        print("GOT the prediction")

        return out, 200

api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True, port='1080')