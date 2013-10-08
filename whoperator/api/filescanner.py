from whoperator import app, filescanner
from flask import jsonify


@app.route('/filescanner/start')
def start_filescanner():
    filescanner.resume_scan()
    return jsonify({'filescanner_status': 'started'})


@app.route('/filescanner/stop')
def stop_filescanner():
    filescanner.stop_scan()
    return jsonify({'filescanner_status': 'stopped'})


@app.route('/filescanner/job')
def get_filescanner_jobs():
    state = {
        'active_job': filescanner.current_job.as_dict() if filescanner.current_job else None,
        'pending_jobs': [job.as_dict() for job in filescanner.job_queue],
        'completed_jobs': [job.as_dict() for job in filescanner.completed_jobs],
        'current_file': filescanner.current_file.as_dict() if filescanner.current_file else None
    }
    return jsonify(state)


@app.route('/filescanner/current_file')
def filescanner_current_file():
    return jsonify({'current_file': filescanner.current_file.as_dict() if filescanner.current_file else None})


@app.route('/filescanner/job/<string:job_id>', methods=['DELETE'])
def delete_filescanner_job(job_id):
    if filescanner.delete_job(job_id):
        return jsonify({'deleted': job_id})
    else:
        response = jsonify({'error': 'Unknown job id.'})
        response.status_code = 500
        return response
