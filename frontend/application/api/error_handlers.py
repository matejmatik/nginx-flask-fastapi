from flask import Flask, render_template


def __page_not_found(e) -> str:
    return render_template("core/errors/404.jinja2"), 404


def __page_forbidden(e) -> str:
    return render_template("core/errors/403.jinja2"), 403


def __page_internal_server_error(e) -> str:
    return render_template("core/errors/500.jinja2"), 500


def register_api_error_handlers(app: Flask) -> None:
    for error_code, func in [
        (404, __page_not_found),
        (403, __page_forbidden),
        (500, __page_internal_server_error),
    ]:
        app.register_error_handler(error_code, func)
