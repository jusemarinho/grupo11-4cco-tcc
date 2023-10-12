from flask import Flask
from recognator import Recognator
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def recognition():
  recognator = Recognator()
  prediction = recognator.predict(file_key='test/cat2-test.jpeg')
  return prediction

app.run()