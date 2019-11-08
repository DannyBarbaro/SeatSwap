import os, sys
from Model import Group
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'db_code'))
import Repository as db
from ViewModel import jsonify, GroupView

from flask_api import status
from flask import Blueprint, request

group = Blueprint('group', __name__)

@group.route('/createGroup', methods=['POST'])
def create_group():
    """
    Request: {"group" : <obj>}

    Response: empty
    """
    if 'group' not in request.json:
        return {'invalid_key': 'Invalid group creation request'}, status.HTTP_400_BAD_REQUEST
    if 'owner' not in request.json['group']:
        return {'no_owner': 'No owner in group request'}, status.HTTP_400_BAD_REQUEST
    if 'event' not in request.json['group']:
        return {'no_event': 'No event in group request'}, status.HTTP_400_BAD_REQUEST
    
    new_group = Group(request.json['group'])
    if db.get_group_by_owner(new_group.owner, new_group.event):
        return {'group_exists': 'This group has been created already'}, status.HTTP_400_BAD_REQUEST
    
    db.add_group(new_group)
    return "", status.HTTP_200_OK

@group.route('/groups')
def get_group():
    """
    Parameters: id = <id>

    Response: {"group" : <obj>}
    """
    if 'id' not in request.args:
        return {'no_user': 'user id missing from request'}, status.HTTP_400_BAD_REQUEST 

    group = db.get_group_by_id(request.args['id'])
    if group:
        return jsonify({'group': GroupView(group)})
    else:
        return jsonfiy({'group': None})

@group.route('/groups/join', methods=['POST'])
def join_group():
    """
    Request: {"groupId" : <id>, "userId" : <id>}

    Response: empty
    """
    if 'groupId' not in request.json:
        return {'no_group_id': 'Group id missing from request'}, status.HTTP_400_BAD_REQUEST
    if 'userId' not in request.json:
        return {'no_user': 'Joining user id missing from request'}, status.HTTP_400_BAD_REQUEST

    group = db.get_group_by_id(request.json['groupId'])
    if group:
        db.add_user_to_group(request.json['userId'], group)
        return "", status.HTTP_200_OK
    else:
        return {'group_not_found': 'Requested group could not be found'}, status.HTTP_400_BAD_REQUEST

@group.route('/groups/leave')
def leave_group():
    """
    Params: groupId = <id>, userId = <id>

    Response: empty
    """
    if 'groupId' not in request.args:
        return {'no_group_id': 'Group id missing from request'}, status.HTTP_400_BAD_REQUEST
    if 'userId' not in request.args:
        return {'no_user': 'Leaving user missing from request'}, status.HTTP_400_BAD_REQUEST

    group = db.get_group_by_id(request.args['groupId'])
    if group:
        if request.args['userId'] in group.members:
            db.remove_user_from_group(request.args['userId'], group)
            return "", status.HTTP_200_OK
        else:
            return {'user_not_in_group': 'User does not belong to specified group'}, status.HTTP_400_BAD_REQUEST
    else:
        return {'group_not_found': 'Requested group could not be found'}, status.HTTP_400_BAD_REQUEST

@group.route('/groups/list')
def get_all_groups():
    """
    Request: empty

    Response: {"groups" : [<obj>]}
    """
    return jsonify({'groups': [GroupView(g) for g in db.get_all_groups()]}), status.HTTP_200_OK

@group.route('/groups/mine')
def get_user_groups():
    """
    Params: "userId" = <id>

    Response: {"groups" : [<obj>]}
    """
    if 'userId' not in request.args:
        return {'no_user': 'User id missing from request'}, status.HTTP_400_BAD_REQUEST
    
    return jsonify({'groups': [GroupView(g) for g in db.get_groups_with_user(request.args['userId'])]}), status.HTTP_200_OK

