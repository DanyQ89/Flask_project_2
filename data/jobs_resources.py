from . import db_session
from .jobs import Jobs
from flask_restful import abort, Resource, reqparse
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('hazard', required=True, type=int)
parser.add_argument('is_finished', required=True, type=bool)


def abort_if_job_not_found(job_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f'Job {job_id} not found')


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(job_id)
        return jsonify(
            {
                f'job {job.id}': job.to_dict()
            }
        )

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(job_id)
        sess.delete(job)
        sess.commit()
        return jsonify(
            {'success': 'OK'}
        )


class JobsListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        jobs = sess.query(Jobs).all()
        return jsonify(
            {'jobs': [i.to_dict() for i in jobs]}
        )

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            hazard=args['hazard'],
            is_finished=args['is_finished']
        )
        sess.add(job)
        sess.commit()
        return jsonify(
            {
                'success': 'OK',
                'id': job.id
            }
        )
