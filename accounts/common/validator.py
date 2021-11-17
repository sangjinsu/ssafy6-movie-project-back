import re


def password_validator(password):
    password_search_rules = [
        {'message': 'One lowercase letter required.', 'regex': '[a-z]+'},
        {'message': "One uppercase letter required.",  'regex': '[A-Z]+'},
        {'message': "One number required.", 'regex': '[0-9]+'}
    ]

    password_match_rules = [
        {'message': "8 characters minimum.", 'regex': '^.{8,}'},
    ]

    errors = []
    for rule in password_search_rules:
        p = re.compile(rule['regex'])
        if not p.search(password):
            errors.append(rule['message'])

    for rule in password_match_rules:
        p = re.compile(rule['regex'])
        if not p.match(password):
            errors.append(rule['message'])
    return errors


def username_validator(username):
    password_match_rules = [
        {'message': "8 characters minimum.", 'regex': '^.{8,}'},
        {'message': "20 characters maximum.", 'regex': '^.{,20}'},
    ]

    errors = []
    for rule in password_match_rules:
        p = re.compile(rule['regex'])
        if not p.match(username):
            errors.append(rule['message'])
    return errors
