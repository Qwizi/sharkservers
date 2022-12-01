from app.scopes.utils import create_scopes_for_application


def create_scopes(applications):
    scopes_dict = {}
    for app in applications:
        application_scopes = create_scopes_for_application(app)
        for v in application_scopes:
            if v[0] not in scopes_dict:
                scopes_dict[v[0]] = v[1]
    return scopes_dict
