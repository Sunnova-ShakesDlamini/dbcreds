# Web API

## FastAPI Application

::: dbcreds.web.main.app
    options:
      show_source: false

## Routes

::: dbcreds.web.main
    options:
      show_source: false
      members:
        - index
        - create_environment
        - list_environments
        - edit_environment_form
        - update_environment
        - test_environment
        - get_environment_expiry

## Authentication

::: dbcreds.web.auth
    options:
      show_source: false
      members:
        - get_current_user
        - authenticate_user

## Error Handling

::: dbcreds.web.errors.WebErrorHandler
    options:
      show_source: false
