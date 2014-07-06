import datetime, os, socket

from flask import abort, Flask, json, jsonify, redirect, request, render_template, Response, send_from_directory, url_for
from flask.ext.admin import Admin
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView
from PIL import Image

app = Flask(__name__)

if socket.gethostname() == 'local-dev.maxfierke.com':
    app.config.from_object('config.DevConfig')
else:
    app.config.from_object('config.ProdConfig')

db = MongoEngine(app)
api = MongoRest(app)

class Project(db.Document):
    project_id = db.StringField(max_length=255, unique=True)
    name = db.StringField(max_length=60, required=True)
    status = db.ReferenceField('ProjectStatus')
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField()
    short_description = db.StringField(max_length=140, required=True)
    description = db.StringField(max_length=5000, required=True)
    image = db.ReferenceField('ProjectImage')
    github = db.StringField(max_length=200)
    links = db.ListField(db.ReferenceField('ProjectLink'))
    categories = db.ListField(db.ReferenceField('ProjectTag'))
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

class ProjectImage(db.Document):
    project = db.ReferenceField('Project', required=True)
    image = db.ImageField(thumbnail_size=(400, 400, True), required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.project.name

class ProjectLink(db.Document):
    title = db.StringField(max_length=140, required=True)
    url = db.URLField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

class ProjectStatus(db.Document):
    name = db.StringField(max_length=40, required=True)
    label = db.StringField(max_length=10, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

class ProjectTag(db.Document):
    name = db.StringField(max_length=25, required=True)
    slug = db.StringField(max_length=25, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

class ProjectLinkResource(Resource):
    document = ProjectLink

class ProjectStatusResource(Resource):
    document = ProjectStatus

class ProjectTagResource(Resource):
    document = ProjectTag

class ProjectResource(Resource):
    document = Project
    related_resources = {
        'categories': ProjectTagResource,
        'links': ProjectLinkResource,
        'status': ProjectStatusResource
    }
    filters = {
        'project_id': [ops.Exact],
    }

    def get_object(self, pk, qfilter=None):
        qs = self.get_queryset()

        if qfilter:
            qs = qfilter(qs)
        return qs.get(project_id=pk)

    def get_objects(self, **kwargs):
        qs = super(ProjectResource, self).get_objects(**kwargs)
        return qs.order_by('+end_date', '-start_date', '+status__name')

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
    projects = Project.objects.order_by('+end_date', '-start_date', '+status__name').all()
    project_tags = ProjectTag.objects.order_by('name').all()
    return render_template('projects.html', title='Projects', projects=projects, project_tags=project_tags)


## API Functions
@api.register(name='projects', url='/api/project/')
class ProjectView(ResourceView):
    resource = ProjectResource
    methods = [methods.Fetch, methods.List]

@app.route('/api/project/<project_id>/image', methods=['GET'])
def api_project_image(project_id):
    project = Project.objects.get_or_404(project_id=project_id)
    proj_image = project.image.image.read()
    return Response(proj_image, mimetype=project.image.image.content_type)

@app.route('/api/project/<project_id>/thumbnail', methods=['GET'])
def api_project_thumb(project_id):
    project = Project.objects.get_or_404(project_id=project_id)
    proj_thumb = project.image.image.thumbnail.read()
    return Response(proj_thumb, mimetype=project.image.image.content_type)

@app.route('/api', methods=['GET'])
def api():
    return render_template('api.html', title='API')

## Error Handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', status_code=404, message='Not Found'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors.html', status_code=500, message='Internal Server Error'), 500

# Main hook
if __name__ == '__main__':
    admin = Admin(app, name="MaxFierke.com")
    admin.add_view(ModelView(Project, name='Projects', endpoint='project', category='Projects'))
    admin.add_view(ModelView(ProjectImage, name='Project Images', endpoint='project_image', category='Projects'))
    admin.add_view(ModelView(ProjectLink, name='Project Links', endpoint='project_link', category='Projects'))
    admin.add_view(ModelView(ProjectStatus, name='Project Statuses', endpoint='project_status', category='Projects'))
    admin.add_view(ModelView(ProjectTag, name='Project Tags', endpoint='project_tag', category='Projects'))

    app.run(debug=True)
