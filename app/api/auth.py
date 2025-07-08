from flask import request, jsonify
from flask.views import MethodView
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token

class RegisterView(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists"}), 409

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created successfully"}), 201

class LoginView(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token), 200

        return jsonify({"msg": "Bad username or password"}), 401