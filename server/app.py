from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = [message.to_dict() for message in Message.query.all()]

    if request.method == 'GET':
        return make_response(messages, 200)
    elif request.method == 'POST':
        new_message = Message(
            username=request.get_json().get("username"),
            body=request.get_json().get("body"),
            created_at=request.get_json().get("created_at"),
            updated_at=request.get_json().get("updated_at")
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        return make_response(message_dict, 201)


@app.route('/messages/<int:id>', methods=['DELETE', 'PATCH'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        res = {
            "delete_successful": True,
            "message": "Message deleted."
        }
        return make_response(res, 200)
    elif request.method == 'PATCH':
        data = request.get_json()

        for attribute in request.get_json():
            setattr(message, attribute, request.get_json().get(attribute))

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        return make_response(message_dict, 200)

if __name__ == '__main__':
    app.run(port=5555)
