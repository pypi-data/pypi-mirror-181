import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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


@standard_chart_formatting_2y
def chart_contribution_effect_with_negative_values_and_2y(
    _df: pd.DataFrame,
    bars_positive_list: list,
    bars_negative_list: list,
    lines_list: list,
    round_y2_num_digits=2,
    **kwargs,
):
    """ """
    df = _df.copy()
    x = df.index.astype(str)

    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    bar_sum_pos = 0
    for col in bars_positive_list:
        fig.add_trace(
            go.Bar(x=x, y=df[col].values, name=col, showlegend=True, yaxis="y1")
        )
        bar_sum_pos += df[col].fillna(0).values

    bar_sum_neg = 0
    for col in bars_negative_list:
        fig.add_trace(
            go.Bar(x=x, y=-df[col].values, name=col, showlegend=True, yaxis="y1")
        )
        bar_sum_neg += df[col].fillna(0).values

    # Largest magnitude in line plots for use in setting bounds
    max_abs_value_secondary = 0
    for col in lines_list:
        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[col].values,
                name=col,
                showlegend=True,
                yaxis="y2",
                hovertemplate="%{y:." + str(round_y2_num_digits) + "f}",
            )
        )
        max_abs_value_secondary = max(
            max_abs_value_secondary, max(abs(df[col].dropna()))
        )

    return fig


@standard_chart_formatting_2y
def chart_bar_and_lines(
    _df: pd.DataFrame,
    bar_column: str,
    line_columns_list: list,
    are_negative_numbers_possible: bool = False,
    max_abs_value_main_y: float = None,
    max_abs_value_secondary_y: float = None,
    **kwargs,
):
    """ """
    df_output = _df.copy()

    # make index as str so that it is JSON serializable
    df_output.index = df_output.index.astype(str)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=df_output.index, y=df_output[bar_column].values, name=bar_column),
        secondary_y=False,
    )

    for line_column in line_columns_list:
        fig.add_trace(
            go.Scatter(
                x=df_output.index, y=df_output[line_column].values, name=line_column
            ),
            secondary_y=True,
        )

    # if numbers could be negative then make some changes
    if are_negative_numbers_possible:
        # find max_abs_value_main_y
        max_abs_value_main_y_actual = df_output[bar_column].abs().max()
        if max_abs_value_main_y is None:
            max_abs_value_main_y = max_abs_value_main_y_actual

        # find max_abs_value_secondary_y
        max_abs_value_secondary_y_actual = (
            df_output[line_columns_list].abs().max(axis=1).max(axis=0)
        )
        if max_abs_value_secondary_y is None:
            max_abs_value_secondary_y = max_abs_value_secondary_y_actual

    return fig


@standard_chart_formatting_1y
def chart_cohort(
    _df: pd.DataFrame,
    cohort_col_name: str,
    x_axis_col_name: str,
    color_col_name: str,
    line_to_be_dashed: str = None,
    **kwargs,
):
    df = _df.copy()
    df = df.dropna(axis=0, how="all")
    df = df.reset_index()
    df = pd.melt(df, id_vars=cohort_col_name).reset_index()

    # create dashed line if required
    if line_to_be_dashed is not None:
        temp_col_name = "dashed_or_not"
        non_dash_line = 0
        dash_line = 3
        df[temp_col_name] = non_dash_line
        df.loc[df[cohort_col_name] == line_to_be_dashed, temp_col_name] = dash_line
    else:
        temp_col_name = ""

    df[x_axis_col_name] = df[x_axis_col_name].astype(str)
    fig = (
        px.line(
            df,
            x=x_axis_col_name,
            y="value",
            color=color_col_name,
            line_dash=temp_col_name,
        )
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(cohort_col_name + "=", ""))
        )
        .for_each_trace(lambda t: t.update(name=t.name.replace("00:00:00", "")))
        .for_each_trace(lambda t: t.update(name=t.name.replace(temp_col_name, "")))
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(", =" + str(non_dash_line), ""))
        )
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(", =" + str(dash_line), ""))
        )
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(color_col_name + "=", ""))
        )
        .for_each_trace(lambda t: t.update(name=t.name.replace(", 0", "")))
        .for_each_trace(lambda t: t.update(name=t.name.replace(", 3", "")))
    )

    return fig


@standard_chart_formatting_2y
def chart_cohort_2y(
    _df: pd.DataFrame,
    _df_ct_ue: pd.DataFrame,
    cohort_col_name: str,
    x_axis_col_name: str,
    x2_axis_col_name: str,
    y2_axis_col_name: str,
    color_col_name: str,
    line_to_be_dashed: str = None,
    **kwargs,
):
    df = _df.copy()
    # df = df.dropna(axis=0, how="all")
    df = df.reset_index()
    df = pd.melt(df, id_vars=cohort_col_name).reset_index()
    df_ct_ue = _df_ct_ue.copy()

    # Sort values
    df = df.sort_values(by=[cohort_col_name], ascending=True)
    df_ct_ue = df_ct_ue.sort_values(by=[x2_axis_col_name], ascending=True)

    # create dashed line if required
    if line_to_be_dashed is not None:
        temp_col_name = "dashed_or_not"
        non_dash_line = 0
        dash_line = 3
        df[temp_col_name] = non_dash_line
        df.loc[df[cohort_col_name] == line_to_be_dashed, temp_col_name] = dash_line

    # primary axis
    df[x_axis_col_name] = df[x_axis_col_name].astype(str)
    fig = (
        px.line(
            df,
            x=x_axis_col_name,
            y="value",
            color=color_col_name,
            line_dash=temp_col_name,
        )
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(cohort_col_name + "=", ""))
        )
        .for_each_trace(lambda t: t.update(name=t.name.replace("00:00:00", "")))
        .for_each_trace(lambda t: t.update(name=t.name.replace(temp_col_name, "")))
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(", =" + str(non_dash_line), ""))
        )
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(", =" + str(dash_line), ""))
        )
        .for_each_trace(
            lambda t: t.update(name=t.name.replace(color_col_name + "=", ""))
        )
    )

    # secondary axis
    df_ct_ue[x2_axis_col_name] = df_ct_ue[x2_axis_col_name].astype(str)
    fig2 = px.bar(df_ct_ue, x=x2_axis_col_name, y=y2_axis_col_name)
    fig2.update_traces(opacity=0.2)
    fig2.update_traces(yaxis="y2")

    # Combine the two together
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    subfig.add_traces(fig.data + fig2.data)

    return subfig


@standard_chart_formatting_1y
def stacked_bar_chart(
    _df: pd.DataFrame,
    **kwargs,
):
    """ """
    df = _df.copy()
    df.index = df.index.astype(str)

    x = df.index
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Bar(x=x, y=df[col].values, name=col))

    fig.update_layout(barmode="relative")
    return fig


@standard_chart_formatting_1y
def multiple_line_charts(
    _df: pd.DataFrame,
    x_col_name: str,
    y_col_name: str,
    color_col_name: str = None,
    hover_col_list: list = None,
    **kwargs,
):
    """ """
    df = _df.copy()

    if color_col_name is not None:
        if hover_col_list is not None:
            fig = px.line(
                df,
                x=x_col_name,
                y=y_col_name,
                color=color_col_name,
                hover_data=hover_col_list,
            ).for_each_trace(
                lambda t: t.update(name=t.name.replace(color_col_name + "=", ""))
            )
        else:
            fig = px.line(
                df, x=x_col_name, y=y_col_name, color=color_col_name
            ).for_each_trace(
                lambda t: t.update(name=t.name.replace(color_col_name + "=", ""))
            )
    else:
        if hover_col_list is not None:
            fig = px.line(df, x=x_col_name, y=color_col_name, hover_data=hover_col_list)
        else:
            fig = px.line(df, x=x_col_name, y=color_col_name)

    return fig
