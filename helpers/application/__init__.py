from flask import Flask, jsonify
from flask_restful import Api

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:emmanuel1@localhost:5432/censoescolar"

api = Api(app)

