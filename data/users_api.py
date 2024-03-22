import flask
from flask import jsonify, request, make_response

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)

params = ['name', 'surname', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password', 'city_from']


@blueprint.route('/api/users', methods=['GET'])
def get_all_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict() for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'bad request'}), 400)
    return jsonify(
        {
            f'user {user_id}': user.to_dict()
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return make_response(jsonify({'error': 'empty request'}), 400)
    elif not all(item in request.json for item in params):
        return make_response(jsonify({'error': 'bad request'}), 400)

    db_sess = db_session.create_session()

    user = User(
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from'],
        hashed_password=request.json['hashed_password']
    )

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in params):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 400)
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.city_from = request.json['city_from']
    user.hashed_password = request.json['hashed_password']

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DElETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 400)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

