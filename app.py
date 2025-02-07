from flask import Flask, request, jsonify
from models.meal import Meal
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
db.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)