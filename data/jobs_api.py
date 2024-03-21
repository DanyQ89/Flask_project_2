import flask
from flask import jsonify, request, make_response

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'404': 'not found error'})
    return jsonify(
        {
            f'job {str(job_id)}': job.to_dict()

        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def post_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'collaborators', 'hazard', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    job_need = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        hazard=request.json['hazard'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job_need)
    db_sess.commit()
    return jsonify({'id': job_need.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'collaborators', 'hazard', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    job_need = db_sess.query(Jobs).get(job_id)
    if not job_need:
        return make_response(jsonify({'error': 'Not found'}, 400))

    job_need.job = request.json['job']
    job_need.team_leader = request.json['team_leader']
    job_need.work_size = request.json['work_size']
    job_need.collaborators = request.json['collaborators']
    job_need.hazard = request.json['hazard']
    job_need.is_finished = request.json['is_finished']

    db_sess.commit()
    return jsonify({'success': "OK"})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
