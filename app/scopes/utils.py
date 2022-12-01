from app.scopes.enums import ScopeEnum


def create_scopes_for_application(app_name: str):
    scope_list = [(f"{app_name}:{e.value}", f"{e.value.capitalize()} {app_name}") for e in ScopeEnum]
    scope_dict = {}

    for scope in scope_list:
        if scope[0] not in scope_dict:
            scope_dict[scope[0]] = scope[1]

    return list(scope_dict.items())
