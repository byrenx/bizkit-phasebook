from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    matched_user_ids = {} # store matched user ids here for faster lookup
    matched_users = []

    match = False

    for user in USERS:
        if user.get('id') == args.get('id'):
            matched_user_ids[user.get('id')] = user.get('id')
            matched_users.append(user)
            continue
        if args.get('name') and is_name_match(user.get('name'), args.get('name')):
            match = True
        if args.get('age') and is_age_match(user.get('age'), args.get('age')):
            match = True
        if args.get('occupation') and is_occupation_match(user.get('occupation'), args.get('occupation')):
            match = True
        if match and not matched_user_ids.get(user.get('id')):
            # add user to match lists
            matched_user_ids[user.get('id')] = user.get('id')
            matched_users.append(user)
        match = False

    return matched_users

def is_age_match(user_age, target_age):
    return user_age >= int(target_age) - 1 and user_age <= int(target_age) + 1

def is_name_match(user_name, target_name):
    return target_name.lower() in user_name.lower()

def is_occupation_match(user_occupation, target_occupation):
    return target_occupation.lower() in user_occupation.lower()
