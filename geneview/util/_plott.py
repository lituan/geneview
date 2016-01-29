"""
Small ploting-related utility functions.
Ref from: the seaborn repo's utils.py on github
"""
import warnings

import numpy as np
import matplotlib.pyplot as plt

def axlabel(xlabel, ylabel, **kwargs):
    """Grab current axis and label it."""
    ax = plt.gca()
    ax.set_xlabel(xlabel, **kwargs)
    ax.set_ylabel(ylabel, **kwargs)


def despine(fig=None, ax=None, top=True, right=True, left=False,
            bottom=False, offset=None, trim=False):
    """
    Remove the top and right spines from plot(s).

    Parametes
    ---------
    fig : matplotlib figure, optional
        Figure to despine all axes of, default uses current figure.

    ax : matplotlib axes, optional
        Specific axes object to despine.

    top, right, left, bottom : boolean, optional
        If True, remove that spine.

    offset : int or None  (default), optional
        Absolute distance, in points, spines should be moved away
        from the axes (negative values move spines inward).

    trim : bool, optional
        If true, limit spines to the smallest and largest major tick
        on each non-despined axis.

    Returns
    -------
    None
    """
    # Get references to the axes we want
    if fig is None and ax is None:
        axes = plt.gcf().axes
    elif fig is not None:
        axes = fig.axes
    elif ax is not None:
        axes = [ax]

    for ax_i in axes:
        for side in ["top", "right", "left", "bottom"]:
            # Toggle the spine objects
            is_visible = not locals()[side]
            ax_i.spines[side].set_visible(is_visible)
            if offset is not None and is_visible:
                _set_spine_position(ax_i.spines[side], ('outward', offset))

        # Set the ticks appropriately
        if bottom:
            ax_i.xaxis.tick_top()
        if top:
            ax_i.xaxis.tick_bottom()
        if left:
            ax_i.yaxis.tick_right()
        if right:
            ax_i.yaxis.tick_left()

        if trim:
            # clip off the parts of the spines that extend past major ticks
            xticks = ax_i.get_xticks()
            if xticks.size:
                firsttick = np.compress(xticks >= min(ax_i.get_xlim()), 
                                        xticks)[0]
                lasttick = np.compress(xticks <= max(ax_i.get_xlim()),
                                       xticks)[-1]
                ax_i.spines['bottom'].set_bounds(firsttick, lasttick)
                ax_i.spines['top'].set_bounds(firsttick, lasttick)
                newticks = xticks.compress(xticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_xticks(newticks)

            yticks = ax_i.get_yticks()
            if yticks.size:
                firsttick = np.compress(yticks >= min(ax_i.get_ylim()),
                                        yticks)[0]
                lasttick = np.compress(yticks <= max(ax_i.get_ylim()),
                                       yticks)[-1]
                ax_i.spines['left'].set_bounds(firsttick, lasttick)
                ax_i.spines['right'].set_bounds(firsttick, lasttick)
                newticks = yticks.compress(yticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_yticks(newticks)


def offset_spines(offset=10, fig=None, ax=None):
    """Simple function to offset spines away from axes.
    Use this immediately after creating figure and axes objects.
    Offsetting spines after plotting or manipulating the axes
    objects may result in loss of labels, ticks, and formatting.
    Parameters
    ----------
    offset : int, optional
        Absolute distance, in points, spines should be moved away
        from the axes (negative values move spines inward).
    fig : matplotlib figure, optional
        Figure to despine all axes of, default uses current figure.
    ax : matplotlib axes, optional
        Specific axes object to despine
    Returns
    -------
    None
    """
    warn_msg = "`offset_spines` is deprecated and will be removed in v0.5"
    warnings.warn(warn_msg, UserWarning)

    # Get references to the axes we want
    if fig is None and ax is None:
        axes = plt.gcf().axes
    elif fig is not None:
        axes = fig.axes
    elif ax is not None:
        axes = [ax]

    for ax_i in axes:
        for spine in ax_i.spines.values():
            _set_spine_position(spine, ('outward', offset))


def _set_spine_position(spine, position):
    """
    Set the spine's position without resetting an associated axis.
    As of matplotlib v. 1.0.0, if a spine has an associated axis, then
    spine.set_position() calls axis.cla(), which resets locators, formatters,
    etc.  We temporarily replace that call with axis.reset_ticks(), which is
    sufficient for our purposes.
    """
    axis = spine.axis
    if axis is not None:
        cla = axis.cla
        axis.cla = axis.reset_ticks
    spine.set_position(position)
    if axis is not None:
        axis.cla = cla