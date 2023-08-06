import importlib
from typing import Union

from assertpy import assert_that

from deepdriver.sdk.chart.chart import Chart
from deepdriver.sdk.data_types.table import Table
from deepdriver.sdk.data_types.image import Image


def visualize(obj: Union[Chart, Table, Image]) -> None:
    assert_that(obj).is_not_none()

    if isinstance(obj, Chart):
        plotly_path = "plotly.express"
        plotly_module = importlib.import_module(plotly_path)
        plotly_chart_func = getattr(plotly_module, obj.chart_type)

        fig = plotly_chart_func(
            x=obj.data.dataframe[obj.data_fields["x"]],
            y=obj.data.dataframe[obj.data_fields["y"]],
            labels=obj.data_fields,
            title=obj.label_fields["title"],
        )
        fig.show()
    elif isinstance(obj, Table):
        # from IPython.core.display import display, HTML
        # display(HTML(obj.data.dataframe._repr_html_()))

        plotly_path = "plotly.graph_objects"
        plotly_module = importlib.import_module(plotly_path)

        fig = plotly_module.Figure(
            data=[plotly_module.Table(
                    header=dict(values=obj.data.columns),
                    cells=dict(values=obj.data.dataframe.T))
                  ],
        )
        fig.show()
    elif isinstance(obj, Image):
        # from IPython.core.display import display, HTML
        # display(HTML(obj.data.dataframe._repr_html_()))

        plotly_path = "plotly.express"
        plotly_module = importlib.import_module(plotly_path)
        import numpy as np
        fig = plotly_module.imshow(
            np.array(obj.data)
        )
        fig.show()
