import numpy as np
import os
import onnxruntime as ort
from io import BytesIO
from urllib import request
from PIL import Image

model_name = "hair_classifier_empty.onnx"
session = ort.InferenceSession(model_name)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


input_shape = session.get_inputs()[0].shape
target_height = input_shape[2]
target_width = input_shape[3]
target_size = (target_width, target_height)

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.Resampling.NEAREST)
    return img

def preprocess_input(x):
   
    x /= 255.0
    return x

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def predict(url):
    img = download_image(url)
    img_prepared = prepare_image(img, target_size)
    x = np.array(img_prepared, dtype='float32')
    
    X = np.array([x])
    X = preprocess_input(X)
    
    X = X.transpose(0, 3, 1, 2)
    
    outputs = session.run([output_name], {input_name: X})
    output_value = outputs[0][0]
    
    # print(f"Raw output: {output_value}")
    return float(sigmoid(output_value))

def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return {
        'prediction': result
    }

if __name__ == "__main__":
  
    url = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
    print(predict(url))
