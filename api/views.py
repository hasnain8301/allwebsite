from flask import jsonify, request, make_response
from flask.blueprints import Blueprint
from api.models import Project
from api import db
from api.decorator import token_required

# Create A Blueprint 
views = Blueprint('views', __name__, url_prefix='/project/')

# route to add a new project in database
@views.route('/add', methods=['POST'])
@token_required
def add_project(current_user):
    # get json data from request
    data = request.get_json()

    # if data exist in request create a project instance and save 
    if data:
        # Create project Instance from "POST" Data 
        add_new_project = Project(project_name=data['project_name'], project_url=data['project_url'], project_type=data['project_type'])

        # Create a database session and commit data in tables
        db.session.add(add_new_project)
        db.session.commit()
        result = {'message':'Project created successfully'}
        return jsonify(result), 201
    
    else:
        result = {'message':'somthing went wrong please try again'}
        return jsonify(result), 404




@views.route('/all')
@token_required
def get_all_projects(current_user):
    # get all projects from database
    all_projects = Project.query.all()

    # create empity list to append projects
    projects_list = []

    # iterate through all project query set
    for proj in all_projects:
        project = dict()

        project['id'] = proj.id
        project['project_name'] = proj.project_name
        project['project_url'] = proj.project_url
        project['project_type'] = proj.project_type
        project['created_at'] = proj.created_at
        project['last_deployed'] = proj.last_deployed
        project['project_status'] = proj.project_status

        # Append data in projects_list
        projects_list.append(project)

    # return projects_list as response
    return jsonify({'Projects' : projects_list}), 200



# route to update a project 
@views.route('/update', methods=['PUT'])
@token_required
def update_projects(current_user):

    # get json data from request
    data = request.get_json()

    # if data exist in request create a project instance to be update
    if data:
        project_to_update = Project.query.get(data['id'])

        # check if the project exist or not
        if not project_to_update:
            result = {'message':'invalid project id'}
            return jsonify(result), 404
        
        # update data one by one in to the fields
        if data.get('last_deployed'):
            project_to_update.last_deployed = data['last_deployed']

        if data.get('project_name'):
            project_to_update.project_name = data['project_name']

        if data.get('project_status'):
            project_to_update.project_status = data['project_status']
        
        if data.get('project_type'):
            project_to_update.project_type = data['project_type']

        if data.get('project_url'):
            project_to_update.project_url = data['project_url']

        # Save the changes in database
        db.session.add(project_to_update)
        db.session.commit()

        # return suceess message
        return jsonify({'message' : 'project updates successfully'}), 200
    
    result = {'message':'somthing went wrong please try again'}
    return jsonify(result), 404



# route to delete a project 
@views.route('/delete/<id>', methods=['DELETE'])
@token_required
def delete_projects(current_user, id):

    # fetch project object to be deleted
    project_to_delete = Project.query.get(id)

    # check if project exist which is to be deleted
    if not project_to_delete:
        result = {'message':'invalid project id'}
        return jsonify(result), 404
    
    # delete the project object from database
    db.session.delete(project_to_delete)
    db.session.commit()

    return jsonify({'message' : 'project deleted successfully'}), 200