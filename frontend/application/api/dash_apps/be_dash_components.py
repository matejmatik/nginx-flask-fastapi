
from dash.dcc import Graph, Loading, Store, Interval
from dash_bootstrap_components import Switch
from plotly.graph_objs import Figure

DEFAULT_PLOTLY_GRAPH_CONFIG = {
    "template":"plotly_dark"
}

def BeHiddenDashThemeSwitch(_id: str) -> Switch:
    
    return Switch(
        id=_id,
        class_name="is-hidden",
        persistence=True,
    )

def BeInterval(
    _id: str,
    interval_in_seconds: int = 1,
    n_intervals: int = 0,
) -> Interval:

    return Interval(
        id=_id,
        interval=interval_in_seconds * 1000,
        n_intervals=n_intervals,
    )


def BeLoading(
    children: list = [],
    loading_in_fullscreen: bool = False,
) -> Loading:

    return Loading(
        children=children,
        type="default",
        fullscreen=loading_in_fullscreen,
        color="#F15922",
    )


def BeFigure() -> Figure:
    return Figure(
        layout={
            "template":"plotly_dark"
        },
    )


def BeGraph(
    _id: str,
    style: dict = {},
    with_loading: bool = False,
    loading_in_fullscreen: bool = False,
    **kwargs,
) -> Graph:
    
    graph_elt: Graph = Graph(
                    id=_id,
                    style=style,
                    config=DEFAULT_PLOTLY_GRAPH_CONFIG,
                    figure=BeFigure(),
                    **kwargs
                )
    
    if with_loading:
        return BeLoading(
            children=[graph_elt],
            loading_in_fullscreen=loading_in_fullscreen,
        )

    return graph_elt

def BeStore(
    _id: str,
    data: dict = {},
    storage_type: str = "session",
    with_loading: bool = False,
    loading_in_fullscreen: bool = False,
) -> Store:

    store_elt: Store = Store(
        id=_id,
        data=data,
        storage_type=storage_type,
    )
    
    if with_loading:
        return BeLoading(
            children=[store_elt],
            loading_in_fullscreen=loading_in_fullscreen,
        )

    return store_elt