import numpy as np
import onnxruntime as ort
from io import BytesIO
from urllib import request
from PIL import Image

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

def get_model_output(model_name, url):
    session = ort.InferenceSession(model_name)

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    input_shape = session.get_inputs()[0].shape
    target_height = input_shape[2]
    target_width = input_shape[3]
    target_size = (target_width, target_height)

    img = download_image(url)
    img_prepared = prepare_image(img, target_size)
    
    x = np.array(img_prepared, dtype='float32')
    X = np.array([x])
    X = preprocess_input(X)
    X = X.transpose(0, 3, 1, 2)
    
    outputs = session.run([output_name], {input_name: X})
    return outputs[0][0]

if __name__ == "__main__":
    url = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
    
    print("Checking hair_classifier_empty.onnx...")
    try:
        result_empty = get_model_output("hair_classifier_empty.onnx", url)
        print(f"Result for empty: {result_empty}")
    except Exception as e:
        print(f"Error with empty model: {e}")

    print("\nChecking hair_classifier_v1.onnx...")
    try:
        result_v1 = get_model_output("hair_classifier_v1.onnx", url)
        print(f"Result for v1: {result_v1}")
    except Exception as e:
        print(f"Error with v1 model: {e}")
