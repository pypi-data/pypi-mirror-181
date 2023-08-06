"""
-----------------------------------------------------------------------------------------
plots module
-----------------------------------------------------------------------------------------
Provides functions to visualize Signal class.

### Functions:

- iplot()     : Signal interactive plot for Notebooks.
- isubplot()  : Signal interactive subplot for Notebooks.

### Author: 

Alejandro Alcaine Otín, Ph.D.
    lalcaine@usj.es"""

# DEPENDENCIES

import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.palettes import Colorblind
from bokeh.models import HoverTool
from bokeh.layouts import gridplot

from pybiosig.signal import Signal

# INTERACTIVE VISUALIZATIONS


def iplot(
    signal: Signal,
    x_lim: tuple = None,
    y_lim: tuple = None,
    fig_title: str = "",
    x_label: str = "Time (s)",
    y_label: str = "Amplitude (mV)",
    legend: list[str] = None,
    plot_width: int = 700,
    plot_height: int = 450,
    line_width: float = 1.5,
    to_notebook: bool = True,
) -> figure:
    """Signal interactive plot for Notebooks.

    Args:
        signal (Signal): Signal to visualize.

        x_lim (tuple, optional): Horizontal axis span limitation.
        Defaults to None: Time span of the signal/s.

        y_lim (tuple, optional): Vertical axis span limitation.
        Defaults to None: Amplitude range of the signal/s.

        fig_title (str, optional): Title of the figure.
        Defaults to "".

        x_label (str, optional): Label for the horizontal axis.
        Defaults to "Time (s)".

        y_label (str, optional): Label for the vertical axis.
        Defaults to "Amplitude (mV)".

        legend (list[str], optional): Legend to be displayed (for multiple signals).
        Defaults to None: No legend is going to be displayed.

        plot_width (int, optional): Width of the plot.
        Defaults to 700.

        plot_height (int, optional): Height of the plot.
        Defaults to 450.

        line_width (float, optional): Width of the signal line.
        Defaults to 1.5.

        to_notebook (bool, optional): Output plot into notebook.
        Defaults to True.

    Returns:
        figure: Bokeh figure object.
    """
    if to_notebook:
        output_notebook(hide_banner=True)

    t = signal.time_vector
    s = signal.get_signal_gain()

    x_lim = (min(t), max(t)) if x_lim is None else x_lim
    y_lim = (s.min() * 1.05, s.max() * 1.05) if y_lim is None else y_lim

    plot = figure(
        title=fig_title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        x_range=x_lim,
        y_range=y_lim,
        width=plot_width,
        height=plot_height,
        toolbar_location="below",
    )

    try:
        if legend is None:
            for i in range(signal.num_signals):
                plot.line(t, s[:, i], line_width=line_width, color=Colorblind[8][i % 8])
        else:
            for leg in legend:
                try:
                    i = signal.channels.index(leg)
                    plot.line(
                        t,
                        s[:, i],
                        line_width=line_width,
                        color=Colorblind[8][i % 8],
                        legend_label=leg,
                    )
                except ValueError:
                    print(f"WARNING: {leg} is not an available signal.")

            plot.legend.click_policy = "hide"

            plot.add_layout(plot.legend[0], "right")

        plot.add_tools(
            HoverTool(
                line_policy="nearest",
                point_policy="snap_to_data",
                tooltips=[(y_label, "$y{0.00}"), (x_label, "$x{0.00}")],
            )
        )

        show(plot, notebook_handle=to_notebook)

        return plot
    except Exception as error:
        print("Error:" + str(error))
        return -1


def isubplot(
    signal: Signal,
    x_lim: tuple = None,
    y_lim: tuple = None,
    sync_axis: bool = True,
    fig_title: list[str] = None,
    x_label: str = "Time (s)",
    y_label: str = "Amplitude (mV)",
    plot_width: int = 700,
    plot_height: int = 300,
    line_width: float = 1.5,
    to_notebook: bool = True,
) -> figure:
    """Signal interactive subplots for Notebooks.

    Args:
        signal (Signal): Signal to visualize.

        x_lim (tuple, optional): Horizontal axis span limitation.
        Defaults to None: Time span of the signal/s.

        y_lim (tuple, optional): Vertical axis span limitation.
        Defaults to None: Automatically handled by bokeh.

        sync_axis (bool, optional): Controls wether to sync or not axis among subplots.
        Defaults to True.

        fig_title (list[str], optional): Each subplot title.
        Defaults to None: Subplots are named "Signal 1", "Signal 2", ...

        x_label (str, optional): Label for the horizontal axis.
        Defaults to "Time (s)".

        y_label (str, optional): Label for the vertical axis.
        Defaults to "Amplitude (mV)".

        plot_width (int, optional): Width of the plot.
        Defaults to 700.

        plot_height (int, optional): Height of the plot.
        Defaults to 300.

        line_width (float, optional):  Width of the signal line.
        Defaults to 1.5.

        to_notebook (bool, optional): Output plot into notebook.
        Defaults to True.

    Returns:
        figure: Bokeh figure object.
    """
    if to_notebook:
        output_notebook(hide_banner=True)

    t = signal.time_vector
    s = signal.get_signal_gain()

    x_lim = (min(t), max(t)) if x_lim is None else x_lim

    try:
        if fig_title is None:
            fig_title = [f"signal {i + 1:d}" for i in range(signal.num_signals)]

        if y_lim is None:
            plots = [
                figure(
                    title=title,
                    x_axis_label=x_label,
                    y_axis_label=y_label,
                    x_range=x_lim,
                    width=plot_width,
                    height=plot_height,
                )
                for title in fig_title
            ]
        else:
            plots = [
                figure(
                    title=title,
                    x_axis_label=x_label,
                    y_axis_label=y_label,
                    x_range=x_lim,
                    y_range=y_lim,
                    width=plot_width,
                    height=plot_height,
                )
                for title in fig_title
            ]

        for i, plot in enumerate(plots):
            try:
                j = signal.channels.index(fig_title[i])
                plot.line(
                    t, s[:, j], line_width=line_width
                )
            except ValueError:
                plot.line(t, s[:, i], line_width=line_width)

            if i > 0 and sync_axis:  # This synchronizes all subplots for panning
                plot.x_range = plots[0].x_range
                plot.y_range = plots[0].y_range

            plot.add_tools(
                HoverTool(
                    line_policy="nearest",
                    point_policy="snap_to_data",
                    tooltips=[(y_label, "$y{0.00}"), (x_label, "$x{0.00}")],
                )
            )

        show(
            gridplot(children=plots, ncols=1, merge_tools=True),
            notebook_handle=to_notebook,
        )

        return plot
    except Exception as error:
        print("Error:" + str(error))
        return -1
    
