import pandas as pd
import plotly.express as px

# Formating
def set_layout_and_display_2y(
    figure_object,
    x_col_name: str,
    y1_col_name: str,
    y2_col_name: str,
    title_str: str,
    y1_is_percentage: bool,
    y2_is_percentage: bool,
    x_is_int: bool,
    x_is_date: bool,
    size_width: int,
    size_height: int,
    are_negative_numbers_possible: bool = False,
    max_abs_value_main_y: float = None,
    max_abs_value_secondary_y: float = None,
    y_bound_multiple: float = 1.1,
    barmode_type: str = "relative",
):

    # Set y as percentage if required
    if y1_is_percentage:
        figure_object.layout.yaxis.tickformat = ",.0%"
    if y2_is_percentage:
        figure_object.layout.yaxis2.tickformat = ",.0%"

    # Set proper format for x axis
    if x_is_int:
        figure_object.layout.xaxis.tickformat = ",d"
    elif x_is_date:
        figure_object.update_layout(xaxis=dict(tickformat="%m-%Y"))

    # Set legend position and size
    figure_object.update_layout(
        width=size_width,
        height=size_height,
        xaxis_title=x_col_name,
        title=title_str,
        barmode=barmode_type,
    )

    # Set y axis names
    figure_object.update_yaxes(title_text=y1_col_name, secondary_y=False)
    figure_object.update_yaxes(title_text=y2_col_name, secondary_y=True)

    # Align 0 - This will work as long as there are no negative values
    figure_object.update_yaxes(rangemode="tozero")
    figure_object.update_xaxes(rangemode="tozero")

    # Update y axis range if required
    if are_negative_numbers_possible:

        if max_abs_value_secondary_y is None:
            raise ValueError("Pls provide abs max value for secondary y axis")
        if max_abs_value_main_y is None:
            raise ValueError("Pls provide abs max value for primary y axis")

        figure_object.update_yaxes(
            scaleanchor="y1",
            scaleratio=1,
            constraintoward="bottom",
            secondary_y=False,
            range=[
                max_abs_value_main_y * -y_bound_multiple,
                max_abs_value_main_y * y_bound_multiple,
            ],
        )

        figure_object.update_yaxes(
            scaleanchor="y2",
            scaleratio=1,
            constraintoward="bottom",
            secondary_y=True,
            range=[
                max_abs_value_secondary_y * -y_bound_multiple,
                max_abs_value_secondary_y * y_bound_multiple,
            ],
        )

    # https://community.plotly.com/t/plotly-express-with-xaxis-having-integers-strings/34777/2
    figure_object.update_layout(xaxis_type="category")

    return figure_object


def set_layout_and_display_1y(
    figure_object,
    x_col_name,
    y_col_name,
    title_str,
    y_is_percentage,
    showlegend,
    show_y_axis,
    show_x_axis,
    size_width,
    size_height,
    y_axis_range,
):
    """
    Sets the layout and displays the chart
    """

    # Set the layout
    figure_object.update_layout(
        title=title_str,
        xaxis_title=x_col_name,
        yaxis_title=y_col_name,
        showlegend=showlegend,
        yaxis={"visible": show_y_axis},
        xaxis={"visible": show_x_axis},
        width=size_width,
        height=size_height,
        yaxis_range=y_axis_range,
    )

    # Set the y axis to be percentage
    if y_is_percentage:
        figure_object.update_yaxes(tickformat=",.0%")

    return figure_object


## MAIN FUNCTIONS ##


def standard_chart_formatting_1y(func):
    """
    Decorator for adding formatting on top of charts
    """

    def inner(*args, **kwargs):
        fig = func(*args, **kwargs)

        # Lets bypass the decorator if certain conditions are met
        bypass_decorator = False
        for key in ["marginal", "facet_col", "facet_row"]:
            if key in kwargs:
                bypass_decorator = True

        if bypass_decorator:
            return fig

        # x_title_text
        x_title_text = kwargs["x_title_text"] if "x_title_text" in kwargs else None
        # y_title_text
        y_title_text = kwargs["y_title_text"] if "y_title_text" in kwargs else None
        # title
        title = kwargs["title"] if "title" in kwargs else None
        # y_is_percentage
        y_is_percentage = (
            kwargs["y_is_percentage"] if "y_is_percentage" in kwargs else False
        )
        # showlegend
        showlegend = kwargs["showlegend"] if "showlegend" in kwargs else True
        # show_y_axis
        show_y_axis = kwargs["show_y_axis"] if "show_y_axis" in kwargs else True
        # show_x_axis
        show_x_axis = kwargs["show_x_axis"] if "show_x_axis" in kwargs else True
        # size_width
        size_width = kwargs["size_width"] if "size_width" in kwargs else 1000
        # Size height
        size_height = kwargs["size_height"] if "size_height" in kwargs else 500

        fig = set_layout_and_display_1y(
            figure_object=fig,
            x_col_name=x_title_text,
            y_col_name=y_title_text,
            title_str=title,
            y_is_percentage=y_is_percentage,
            showlegend=showlegend,
            show_y_axis=show_y_axis,
            show_x_axis=show_x_axis,
            size_width=size_width,
            size_height=size_height,
            y_axis_range=None,
        )
        return fig

    return inner


def standard_chart_formatting_2y(func):
    """
    Decorator for adding formatting on top of charts
    """

    def inner(*args, **kwargs):
        fig = func(*args, **kwargs)

        # x_title_text
        x_title_text = kwargs["x_title_text"] if "x_title_text" in kwargs else None
        # y_title_text
        y1_title_text = kwargs["y1_title_text"] if "y1_title_text" in kwargs else None
        y2_title_text = kwargs["y2_title_text"] if "y2_title_text" in kwargs else None
        # title
        title = kwargs["title"] if "title" in kwargs else None
        # y_is_percentage
        y1_is_percentage = (
            kwargs["y1_is_percentage"] if "y1_is_percentage" in kwargs else False
        )
        y2_is_percentage = (
            kwargs["y2_is_percentage"] if "y2_is_percentage" in kwargs else False
        )
        # showlegend
        showlegend = kwargs["showlegend"] if "showlegend" in kwargs else True
        # show_y_axis
        show_y1_axis = kwargs["show_y1_axis"] if "show_y1_axis" in kwargs else True
        show_y2_axis = kwargs["show_y2_axis"] if "show_y2_axis" in kwargs else True
        # show_x_axis
        show_x_axis = kwargs["show_x_axis"] if "show_x_axis" in kwargs else True
        # size_width
        size_width = kwargs["size_width"] if "size_width" in kwargs else 1000
        # Size height
        size_height = kwargs["size_height"] if "size_height" in kwargs else 500
        # others
        x_is_int = kwargs["x_is_int"] if "x_is_int" in kwargs else False
        x_is_date = kwargs["x_is_date"] if "x_is_date" in kwargs else not x_is_int
        are_negative_numbers_possible = (
            kwargs["are_negative_numbers_possible"]
            if "are_negative_numbers_possible" in kwargs
            else False
        )
        max_abs_value_main_y = (
            kwargs["max_abs_value_main_y"] if "max_abs_value_main_y" in kwargs else None
        )
        max_abs_value_secondary_y = (
            kwargs["max_abs_value_secondary_y"]
            if "max_abs_value_secondary_y" in kwargs
            else None
        )
        y_bound_multiple = (
            kwargs["y_bound_multiple"] if "y_bound_multiple" in kwargs else 1.1
        )

        fig = set_layout_and_display_2y(
            figure_object=fig,
            x_col_name=x_title_text,
            y1_col_name=y1_title_text,
            y2_col_name=y2_title_text,
            title_str=title,
            y1_is_percentage=y1_is_percentage,
            y2_is_percentage=y2_is_percentage,
            x_is_int=x_is_int,
            x_is_date=x_is_date,
            size_width=size_width,
            size_height=size_height,
            are_negative_numbers_possible=are_negative_numbers_possible,
            max_abs_value_main_y=max_abs_value_main_y,
            max_abs_value_secondary_y=max_abs_value_secondary_y,
            y_bound_multiple=y_bound_multiple,
        )
        return fig

    return inner


# Function to create histogram plot using plotly
@standard_chart_formatting_1y
def histogram_plotly(
    df: pd.DataFrame,
    x_col_name: str,
    y_col_name: str,
    nbins: int,
    color: str = None,
    **kwargs,
) -> None:
    """
    color can be used to plot different categories separately - For example same plot for different sex
    """
    fig = px.histogram(df, x=x_col_name, y=y_col_name, color=color, nbins=nbins)

    return fig


@standard_chart_formatting_1y
def line_plotly(
    df: pd.DataFrame,
    x_col_name: str,
    hover_data: list,
    **kwargs,
) -> None:
    """
    Options for marginal include "histogram", "rug"
    """
    fig = px.line(df, x=x_col_name, y="cdf", hover_data=hover_data)
    return fig


@standard_chart_formatting_1y
def plotly_heatmap(
    _df: pd.DataFrame,
    annotation: bool = True,
    **kwargs,
) -> None:
    df = _df.copy()
    fig = px.imshow(
        df.round(2),
        color_continuous_scale="RdBu",
        origin="lower",
        text_auto=annotation,
    )
    """
    fig.update_layout(showlegend=False)
    fig.update_yaxes(visible=show_y_axis)
    fig.update_layout(
        autosize=False,
        width=size,
        height=size,
    )
    """
    return fig
