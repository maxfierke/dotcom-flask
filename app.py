import os
import socket

from flask import abort, Flask, json, jsonify, redirect, request, render_template, send_from_directory, url_for
app = Flask(__name__)

if socket.gethostname() == 'local-dev.maxfierke.com':
	app.config.from_object('config.DevConfig')
else:
	app.config.from_object('config.ProdConfig')

with open('projects.json', 'r') as projects_fh:
	projects = json.load(projects_fh)['projects']

with open('socialmedia.json', 'r') as socialmedia_fh:
	socialmedia = json.load(socialmedia_fh)['accounts']

# Utility Functions
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

# Routed Functions

## HTML Site Functions
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def page_about():
    return render_template('about.html', title='About')

@app.route('/about/')
def redirect_about():
	return redirect(url_for('page_about'), code=301)

@app.route('/projects/')
def page_projects():
	return render_template('projects.html', title='Projects', projects=projects)


## API Functions
@app.route('/api/project/<project_id>', methods=['GET'])
def api_project(project_id):
	for proj in projects:
		if proj['project_id'] == project_id:
			return jsonify(proj)
	abort(404)

@app.route('/api/project', methods=['GET'])
def api_projects():
	return jsonify(projects=projects)

@app.route('/api/socialmedia/<service_name>', methods=['GET'])
def api_socialmedia_service(service_name):
	if service_name in socialmedia:
		return jsonify(socialmedia[service_name])
	abort(404)

@app.route('/api/socialmedia', methods=['GET'])
def api_socialmedia():
	return jsonify(accounts=socialmedia)

@app.route('/api', methods=['GET'])
def api():
	return render_template('api.html', title='API')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', status_code=404, message='Not Found'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors.html', status_code=500, message='Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
