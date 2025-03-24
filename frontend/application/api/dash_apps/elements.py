# BISOL Energija Dash Elements Generator Object
# -----------------------------------------------------------------------------
# --- Layouts   ---------------------------------------------------------------


def BeContainer(
    children: list = [],
    fluid: bool = False,
    style: dict = {},
    className: str = "",
    shadow: bool = True,
) -> object:
    from dash_bootstrap_components import Container

    return Container(
        children=children,
        fluid=fluid,
        className=f"{'shadow-lg p-5 rounded' if shadow else ''} {className}",
        style=style,
    )


def BeRow(
    children: list = [],
    style: dict = {},
    className: str = "",
) -> object:
    from dash_bootstrap_components import Row

    return Row(
        children=children,
        className=className,
        style=style,
    )


def BeCol(
    children: list = [],
    width: int = 12,
    style: dict = {},
    className: str = "",
) -> object:
    from dash_bootstrap_components import Col

    return Col(
        children=children,
        width=width,
        className=className,
        style=style,
    )


def BeTitle(
    children: list = [],
    size: int = 1,
    style: dict = {},
    className: str = "",
) -> object:
    from dash.html import H1, H2, H3, H4, H5, H6

    return {
        1: H1,
        2: H2,
        3: H3,
        4: H4,
        5: H5,
        6: H6,
    }[size](
        children=children,
        style=style,
        className=f"display-{size} {className}",
    )


def BeText(
    _id: str,
    children: list = [],
    style: dict = {},
    className: str = "",
) -> object:
    from dash.html import P

    return P(
        id=_id,
        children=children,
        style=style,
        className=className,
    )


def BeCard(card_header: str, _id: str, color: str, tooltip: str = "") -> object:
    from dash_bootstrap_components import Card, CardBody, CardHeader, Tooltip

    return Card(
        [
            CardHeader(card_header, style={"font-size": "1.3em"}),
            CardBody(
                BeText(
                    _id=_id,
                    children=[],
                    className="card-text text-center",
                    style={"fontSize": "1.2em"},
                ),
            ),
            (Tooltip(tooltip, target=_id, placement="bottom") if tooltip else None),
        ],
        className="",
        color=color,
        # inverse=True,
        outline=True,
        class_name="h-100 m-0 border-1",
    )


def BeInfoCard(
    title: str,
    _id: str,
    color: str = "secondary",
    tooltip: str = None,
) -> object:
    from dash.html import P
    from dash_bootstrap_components import Card, CardBody, Tooltip

    return Card(
        [
            CardBody(
                [
                    P(
                        children=[title],
                        className="card-title text-muted text-center",
                    ),
                    BeText(
                        _id=_id,
                        children=[],
                        className="card-text text-center",
                        style={"fontSize": "1.2em"},
                    ),
                ]
            ),
            (Tooltip(tooltip, target=_id, placement="bottom") if tooltip else None),
        ],
        className="shadow-sm w-100",
        color=color,
        outline=True,
        style={"fontSize": "1.1em"},
    )


def BeSemaforumCard(
    card_header: str, card_body: str, color: str, inverse=True, outline=True
) -> object:
    from dash_bootstrap_components import Card, CardBody, CardHeader

    return Card(
        [
            CardHeader(card_header, style={"font-size": "1.3em"}),
            CardBody(card_body),
        ],
        className="",
        color=color,
        inverse=inverse,
        outline=outline,
        class_name="h-100 m-0 border-1",
    )


def BeTabs(
    _id: str,
    tabs: list[(str, str)],
    active_tab: str,
    style: dict = {},
    className: str = "",
):
    from dash_bootstrap_components import Tab, Tabs

    return Tabs(
        [
            Tab(
                label=label,
                tab_id=tab_id,
            )
            for label, tab_id in tabs
        ],
        id=_id,
        active_tab=active_tab,
        class_name=f"nav nav-pills nav-fill bg-secondary {className}",
        style=style,
    )


# -----------------------------------------------------------------------------
# --- Buttons   ---------------------------------------------------------------


def BeLocation(_id: str) -> object:
    from dash.dcc import Location

    return Location(
        id=_id,
        refresh=True,
    )


def BeInterval(
    _id: str,
    interval: int = None,
) -> object:
    from dash.dcc import Interval

    INTERVAL_LONG = 60 * 60 * 1000
    return Interval(
        id=_id,
        interval=INTERVAL_LONG if interval is None else interval,
        n_intervals=0,
    )


def BeLoading(
    children: list = [],
    fullscreen: bool = False,
) -> object:
    from dash.dcc import Loading

    return Loading(
        children=children,
        type="default",
        fullscreen=fullscreen,
        color="#F15922",
        className="bg-dark",
    )


# -----------------------------------------------------------------------------
# --- Graph and plots   -------------------------------------------------------


def BeFigure() -> object:
    from plotly.graph_objects import Figure

    return Figure(
        layout={
            "template": "plotly_dark",
            # "margin": {"l": 50, "r": 30, "t": 60, "b": 60},
        }
    )


def BeSubplot(
    rows,
    cols,
    shared_xaxes: bool = True,
    vertical_spacing: int = 0.1,
    specs: list = None,
    subplot_titles: tuple = None,
    column_widths: list = None,
    row_heights: list = None,
) -> object:
    from plotly.subplots import make_subplots

    return make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=shared_xaxes,
        vertical_spacing=vertical_spacing,
        specs=specs,
        subplot_titles=subplot_titles,
        column_widths=column_widths,
        row_heights=row_heights,
    )


def BeSubplotSecY() -> object:
    from plotly.subplots import make_subplots

    return make_subplots(specs=[[{"secondary_y": True}]])


def BeGraph(
    _id: str,
    style: dict = {},
) -> object:
    from dash.dcc import Graph

    return Graph(
        id=_id,
        style=style,
        config={"template": "plotly_dark"},
        figure=BeFigure(),
    )


# -----------------------------------------------------------------------------
# --- Inputs  -----------------------------------------------------------------
def BeButton(
    _id: str,
    icon: str,
    **kwargs,
):
    from dash.html import Button, Span

    return Button(
        [
            Span(
                className=f"mx-2 {icon} text-warning",
            ),
        ],
        id=_id,
        className="btn fs-5",
        n_clicks=0,
        **kwargs,
    )


def BeModal(
    _id: str,
    is_open: bool,
    modal_title: str,
    modal_body: list,
):
    from dash_bootstrap_components import (
        Button,
        Modal,
        ModalBody,
        ModalFooter,
        ModalHeader,
    )

    return Modal(
        [
            ModalHeader(modal_title, close_button=True),
            ModalBody(modal_body),
            ModalFooter(
                Button(
                    "Zapri",
                    id=f"{_id}-close",
                    className="btn btn-secondary",
                    n_clicks=0,
                )
            ),
        ],
        id=_id,
        is_open=is_open,
        size="lg",
    )


def BeSwitch(
    _id: str,
    label: str,
    disabled: bool = False,
    hidden: bool = False,
    checked: bool = False,
):
    from dash_mantine_components import Switch

    return Switch(
        id=_id,
        size="sm",
        radius="xl",
        label=label,
        checked=checked,
        color="orange",
        className="text-center",
        disabled=disabled,
        style={"display": "none"} if hidden else None,
    )


def BeSlider(
    _id: str,
    min_val: int,
    max_val: int,
    value: int,
    className: str = "",
    showLabelOnHover: bool = False,
    labelsAlwaysOn: bool = False,
    updatemode: str = "mouseup",
    step: int = 1,
) -> object:
    from dash_mantine_components import Slider

    return Slider(
        id=_id,
        min=min_val,
        max=max_val,
        value=value,
        showLabelOnHover=showLabelOnHover,
        labelAlwaysOn=labelsAlwaysOn,
        updatemode=updatemode,
        step=step,
        className=className,
    )


def BeDatePicker(
    _id: str,
    value: str,
    min_date: str,
    max_date: str,
    initial_month: str,
    clearable: bool = False,
):
    from dash_mantine_components import DatePicker

    return DatePicker(
        id=_id,
        inputFormat="DD. MM. YYYY",
        # description="Izberi datum ...",
        value=value,
        minDate=min_date,
        maxDate=max_date,
        initialMonth=initial_month,
        clearable=clearable,
    )


def BeDateRange(
    _id: str,
    value: list[str, str],
    min_date: str,
    max_date: str,
    intial_month: str,
    class_name: str = "",
    with_description: bool = True,
) -> object:
    from dash_mantine_components import DateRangePicker

    return DateRangePicker(
        id=_id,
        inputFormat="DD. MM. YYYY",
        description="Izberi datum ..." if with_description else None,
        value=value,
        minDate=min_date,
        maxDate=max_date,
        initialMonth=intial_month,
        className=class_name,
    )


def BeHidden(_id, value: str = "") -> object:
    from dash.dcc import Input

    return Input(id=_id, type="hidden", readOnly=True, value=value)


# -----------------------------------------------------------------------------
# --- Dropdowns   -------------------------------------------------------------


def YearDropdown(
    _id: str,
    style: dict = {},
    className: str = "",
) -> object:
    from dash_mantine_components import Select

    return Select(
        id=_id,
        data=[{"label": year, "value": year} for year in range(2023, 2027)],
        value=2025,
        style=style,
        className=className,
        description="Izberi leto ... ",
    )


def BeDropdownV2(
    _id: str,
    data: list,
    value: str,
    style: dict = {},
    className: str = "",
    description: str = "",
):
    from dash_mantine_components import Select

    return Select(
        id=_id,
        data=data,
        value=value,
        style=style,
        className=className,
        description=description,
    )


def BeDropdown(
    _id: str,
    options: list,
    value: str,
    placeholder: str = "",
    style: dict = {},
    className: str = "",
    multi: bool = False,
    clearable: bool = False,
    searchable: bool = False,
) -> object:
    from dash.dcc import Dropdown

    return Dropdown(
        id=_id,
        options=options,
        value=value,
        placeholder=placeholder,
        multi=multi,
        clearable=clearable,
        searchable=searchable,
        style=style,
        className=className,
    )
