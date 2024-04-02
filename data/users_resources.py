from . import db_session
from .users import User
from flask_restful import abort, Resource, reqparse
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('city_from', required=True)


def abort_if_user_not_found(user_id):
    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        return jsonify(
            {
                f'user {user_id}': user.to_dict()
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.delete(user)
        sess.commit()
        return jsonify(
            {'success': 'OK'}
        )


class UsersListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        users = sess.query(User).all()
        return jsonify(
            {'users': [i.to_dict() for i in users]}
        )

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            city_from=args['city_from']
        )
        sess.add(user)
        sess.commit()
        return jsonify(
            {
                'success': 'OK',
                'id': user.id
            }
        )
