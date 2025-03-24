from dash import Dash
from flask import render_template
from markupsafe import Markup


class CustomDash(Dash):
    """
    CustomDash is a class that extends the Dash class from the dash library. It is used to add custom methods to the Dash class.

    Args:
        Dash (Dash): Dash class from the dash library
    """

    def interpolate_index(
        self,
        metas="",
        title="",
        css="",
        config="",
        scripts="",
        app_entry="",
        favicon="",
        renderer="",
    ):
        return render_template(
            "core/dash.jinja2",
            title=title,
            metas=Markup(metas),
            css=Markup(css),
            dash_config=Markup(config),
            scripts=Markup(scripts),
            app_entry=Markup(app_entry),
            renderer=Markup(renderer),
        )


def format_dash_id(name: str) -> str:
    """
    format_dash_id is used to format the name of the Dash component. Needs to have - instead of _ and no /.

    Args:
        name (str): Name of the Dash component

    Returns:
        str: Formatted name of the Dash component
    """

    return name.lower().replace("/", "").replace("_", "-")


def format_dash_endpoint(url: str) -> str:
    """
    endpoint_dash_formater is used to format the url of the Dash component.

    Args:
        url (str): Url of the Dash component

    Returns:
        str: Formatted url of the Dash component
    """
    if url[0] != "/" or url[-1] != "/":
        raise ValueError("Url must start and end with /")

    return url.replace("/", "").replace("-", "_")
