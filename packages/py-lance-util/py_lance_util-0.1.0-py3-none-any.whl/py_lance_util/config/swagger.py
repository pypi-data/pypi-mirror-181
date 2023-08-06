from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html


def init():
    applications.get_swagger_ui_html = swagger_monkey_patch


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="/doc/swagger/swagger-ui-bundle.js",
        swagger_css_url="/doc/swagger/swagger-ui.css")

