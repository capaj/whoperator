from whoperator import app, filescanner
from flask import jsonify


@app.route('/filescanner')
def get_filescanner_state():
    state = {
        'active_job': filescanner.current_job.as_dict() if filescanner.current_job else None,
        'pending_jobs': [job.as_dict() for job in filescanner.job_queue],
        'completed_jobs': [job.as_dict() for job in filescanner.completed_jobs],
        'current_file': filescanner.current_file.as_dict() if filescanner.current_file else None
    }
    return jsonify(state)
