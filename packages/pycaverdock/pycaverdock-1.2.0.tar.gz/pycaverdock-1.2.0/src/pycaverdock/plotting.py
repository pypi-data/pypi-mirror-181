# MIT License

# Copyright (c) 2022 Loschmidt Laboratories & IT4Innovations

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import ticker
from matplotlib.lines import Line2D

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple

from . import Direction, EnergyProfile, TrajectoryType


@dataclass
class EnergyProfilePlot:
    """
    Plots the energy profile.

    :param name: Name of the simulation.
    :param energy_profile: Object with saved energy profile.
    :param trajectory_type: Type of calculated simulation for plotting LOWERBOUND - lowerbound, UPPERBOUND - upperbound profile.
    """

    name: str
    energy_profile: EnergyProfile
    trajectory_type: TrajectoryType

    @property
    def frame(self):
        f = self.energy_profile.frame.copy()
        f["name"] = self.name
        f["direction"] = self.energy_profile.direction.name
        f["trajectory_type"] = self.trajectory_type.name
        return f


class ActiveSiteLocation(Enum):
    LEFT = auto()
    RIGHT = auto()


def plot_results(profiles: List[EnergyProfilePlot], output, share_axes: bool = True, force_active_site_location: Optional[ActiveSiteLocation] = None, lowerbound_color: str = "orange", upperbound_color: str = "blue", radius_color: str = "green", legend_bbox_to_anchor: Optional[Tuple[float]] = None, max_plots_per_row: int = 4, show_zero_energy_line: bool = True, zero_energy_line_color: str = "lightgrey"):
    """
    Defines settings for plotting results into png figures.

    :param profiles: Object with energy profile for plotting.
    :param output: Name of the output png file.
    :param share_axes: Share the scale of plot axes for multiple results.
    :param force_active_site_location: Sets the side of plot where the active site will be oriented in.
    :param lowerbound_color: Color setting for lowerbound energy curve.
    :param upperbound_color: Color settings for upperbound energy curve.
    :param radius_color: Color settings for tunnel radius curve.
    :param legend_bbox_to_anchor: Coordinates for the anchoring of legend bbox.
    :param max_plots_per_row: Number of plots on a singel row when plotting multiple results.
    :param show_zero_energy_line: Show zero line for energy axis.
    :param zero_energy_line_color: Color of energy zero line.
    """
    colors = [lowerbound_color, upperbound_color]
    df = pd.concat(map(lambda x: x.frame, profiles))

    def plot(data, **kwargs):
        data = data.copy()

        is_type_upperbound = (data["trajectory_type"] == TrajectoryType.UPPERBOUND.name).all()
        is_direction_in = bool((data["direction"] == Direction.IN.name).all())
        if is_type_upperbound:
            data["ubE"] = data["maxE"]

        keys = ["lbE"]
        if is_type_upperbound:
            keys.append("ubE")

        titles = ["active site", "surface"]
        if is_direction_in:
            titles.reverse()

        value_data = data[["distance", *keys]].copy()
        data_radius = data[["distance", "radius"]].copy()

        if force_active_site_location:
            should_reverse = (force_active_site_location == ActiveSiteLocation.RIGHT and not is_direction_in) or (force_active_site_location == ActiveSiteLocation.LEFT and is_direction_in)

            if should_reverse:
                for key in keys:
                    value_data[key] = value_data[key].iloc[::-1].values
                data_radius["radius"] = data_radius["radius"].iloc[::-1].values
                titles.reverse()

        value_data = pd.melt(value_data, id_vars=["distance"], value_vars=keys)

        if show_zero_energy_line:
            plt.axhline(y=0, color=zero_energy_line_color, linestyle="dashed")
        ax = sns.lineplot(data=value_data, x="distance", y="value", hue="variable",
                          hue_order=["lbE", "ubE"], palette=colors)

        plt.text(0.04, 0.5, titles[0], ha="center", va="center", rotation=90,
                 transform=ax.transAxes)
        plt.text(0.96, 0.5, titles[1], ha="center", va="center", rotation=90,
                 transform=ax.transAxes)

        ax2 = ax.twinx()
        ax2.set_ylabel("Tunnel radius [Å]")
        ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:.1f}"))
        if share_axes:
            ax2.set_ylim(df['radius'].min() - .1, df['radius'].max() + .1)

        sns.lineplot(data=data_radius, x="distance", y="radius", linestyle="dotted", color=radius_color,
                     ax=ax2)

    experiment_count = len(df["name"].unique())

    col_wrap = min(experiment_count, max_plots_per_row)
    g = sns.FacetGrid(df, col="name", col_wrap=col_wrap, sharex=share_axes,
                      sharey=share_axes)
    g.map_dataframe(plot, dual_axis=True)
    g.set_titles(template='{col_name}')

    # Set chart dimensions manually to overcome hard-coded tight_layout used by FacetGrid
    g.fig.set_figwidth(col_wrap * 5)

    row_count = int(math.ceil(experiment_count / col_wrap))
    g.fig.set_figheight(row_count * 4)

    legend = {
        "radius": Line2D([], [], marker="o", color="white", markerfacecolor=radius_color, markersize=4),
        "lbE": Line2D([], [], marker="_", color=colors[0]),
        "ubE": Line2D([], [], marker="_", color=colors[1])
    }

    legend_bbox_to_anchor_right = 1.02
    if legend_bbox_to_anchor:
        pass
    elif col_wrap == 1:
        legend_bbox_to_anchor = (.636, legend_bbox_to_anchor_right)
    elif col_wrap == 2:
        legend_bbox_to_anchor = (.7745, legend_bbox_to_anchor_right)
    elif col_wrap == 3:
        legend_bbox_to_anchor = (.8355, legend_bbox_to_anchor_right)
    elif col_wrap == 4:
        legend_bbox_to_anchor = (.8695, legend_bbox_to_anchor_right)
    else:
        legend_bbox_to_anchor = (.9, 1.02)

    g.add_legend(loc="upper right", borderaxespad=0, legend_data=legend, ncol=3, bbox_to_anchor=legend_bbox_to_anchor, frameon=True)

    for ax in g.axes.flat:
        ax.set_xlabel("Distance [Å]")
        ax.set_ylabel("Binding energy [kcal/mol]")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{x:.1f}"))
        ax.tick_params(labelbottom=True)

    plt.savefig(output, bbox_extra_artists=(g._legend,), bbox_inches='tight')
