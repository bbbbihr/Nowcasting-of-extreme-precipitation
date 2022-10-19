
from matplotlib import cm
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from . import ensscores, probscores

def plot_intensityscale(iss, fig=None, vmin=-2, vmax=1, kmperpixel=None, unit=None):
    """Plot a intensity-scale verification table with a color bar and axis
    labels.

    Parameters
    ----------
    iss : dict
        An intensity-scale verification results dictionary returned by
        pysteps.verification.spatialscores.intensity_scale.
    fig : matplotlib.figure.Figure
        Optional figure object to use for plotting. If not supplied, a new
        figure is created.
    vmin : float
       Optional minimum value for the intensity-scale skill score in the plot.
       Defaults to -2.
    vmax : float
       Optional maximum value for the intensity-scale skill score in the plot.
       Defaults to 1.
    kmperpixel : float
       Optional conversion factor from pixels to kilometers. If supplied,
       the unit of the shown spatial scales is km instead of pixels.
    unit : string
       Optional unit of the intensity thresholds.

    """
    if fig is None:
        fig = plt.figure()

    ax = fig.gca()

    im = ax.imshow(iss["SS"], vmin=vmin, vmax=vmax, interpolation="nearest",
                   cmap=cm.jet)
    cb = fig.colorbar(im)
    cb.set_label(iss["label"])

    if unit is None:
        ax.set_xlabel("Intensity threshold")
    else:
        ax.set_xlabel("Intensity threshold [%s]" % unit)
    if kmperpixel is None:
        ax.set_ylabel("Spatial scale [pixels]")
    else:
        ax.set_ylabel("Spatial scale [km]")

    ax.set_xticks(np.arange(iss["SS"].shape[1]))
    ax.set_xticklabels(iss["thrs"])
    ax.set_yticks(np.arange(iss["SS"].shape[0]))
    if kmperpixel is None:
        scales = iss["scales"]
    else:
        scales = iss["scales"] * kmperpixel
    ax.set_yticklabels(scales)

def plot_rankhist(rankhist, ax=None):
    """Plot a rank histogram.

    Parameters
    ----------
    rankhist : dict
        A rank histogram object created by ensscores.rankhist_init.
    ax : axis handle
        Axis handle for the figure. If set to None, the handle is taken from
        the current figure (matplotlib.pylab.gca()).

    """
    if ax is None:
        ax = plt.gca()

    r = ensscores.rankhist_compute(rankhist)
    x = np.linspace(0, 1, rankhist["num_ens_members"] + 1)
    ax.bar(x, r, width=1.0/len(x), align="edge", color="gray", edgecolor="black")

    ax.set_xticks(x[::3] + (x[1] - x[0]))
    ax.set_xticklabels(np.arange(1, len(x))[::3])
    ax.set_xlim(0, 1+1.0/len(x))
    ax.set_ylim(0, np.max(r)*1.25)

    ax.set_xlabel("Rank of observation (among ensemble members)")
    ax.set_ylabel("Relative frequency")

    ax.grid(True, axis='y', ls=':')

def plot_reldiag(reldiag, ax=None):
    """Plot a reliability diagram.

    Parameters
    ----------
    reldiag : dict
        A ROC curve object created by probscores.reldiag_init.
    ax : axis handle
        Axis handle for the figure. If set to None, the handle is taken from
        the current figure (matplotlib.pylab.gca()).

    """
    if ax is None:
        ax = plt.gca()

    # Plot the reliability diagram.
    f = 1.0 * reldiag["Y_sum"] / reldiag["num_idx"]
    r = 1.0 * reldiag["X_sum"] / reldiag["num_idx"]

    mask = np.logical_and(np.isfinite(r), np.isfinite(f))

    ax.plot(r[mask], f[mask], "kD-")
    ax.plot([0, 1], [0, 1], "k--")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.grid(True, ls=':')

    ax.set_xlabel("Forecast probability")
    ax.set_ylabel("Observed relative frequency")

    # Plot sharpness diagram into an inset figure.
    iax = inset_axes(ax, width="35%", height="20%", loc=4, borderpad=3.5)
    bw = reldiag["bin_edges"][2] - reldiag["bin_edges"][1]
    iax.bar(reldiag["bin_edges"][:-1], reldiag["sample_size"], width=bw,
            align="edge", color="gray", edgecolor="black")
    iax.set_yscale("log", basey=10)
    iax.set_xticks(reldiag["bin_edges"])
    iax.set_xticklabels(["%.1f" % max(v, 1e-6) for v in reldiag["bin_edges"]])
    yt_min = int(max(np.floor(np.log10(min(reldiag["sample_size"][:-1]))), 1))
    yt_max = int(np.ceil(np.log10(max(reldiag["sample_size"][:-1]))))
    t = [pow(10.0, k) for k in range(yt_min, yt_max)]

    iax.set_yticks([int(t_) for t_ in t])
    iax.set_xlim(0.0, 1.0)
    iax.set_ylim(t[0], 5*t[-1])
    iax.set_ylabel("log10(samples)")
    iax.yaxis.tick_right()
    iax.yaxis.set_label_position("right")
    iax.tick_params(axis="both", which="major", labelsize=6)

def plot_ROC(ROC, ax=None, opt_prob_thr=False):
    """Plot a ROC curve.

    Parameters
    ----------
    ROC : dict
        A ROC curve object created by probscores.ROC_curve_init.
    ax : axis handle
        Axis handle for the figure. If set to None, the handle is taken from
        the current figure (matplotlib.pylab.gca()).
    opt_prob_thr : bool
        If set to True, plot the optimal probability threshold that maximizes 
        the difference between the hit rate (POD) and false alarm rate (POFD).

    """
    if ax is None:
        ax = plt.gca()

    POFD,POD,area = probscores.ROC_curve_compute(ROC, compute_area=True)
    p_thr = ROC["prob_thrs"]

    ax.plot([0, 1], [0, 1], "k--")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("False alarm rate (POFD)")
    ax.set_ylabel("Probability of detection (POD)")
    ax.grid(True, ls=':')

    if opt_prob_thr:
        l, = ax.plot(POFD, POD, "kD-")
        opt_prob_thr_idx = np.argmax(np.array(POD) - np.array(POFD))
        ax.scatter([POFD[opt_prob_thr_idx]], [POD[opt_prob_thr_idx]], c='r', s=150,
                   facecolors=None, edgecolors='r')

    for p_thr_,x,y in zip(p_thr, POFD, POD):
        if p_thr_ > 0.05 and p_thr_ < 0.95:
            ax.text(x+0.02, y-0.02, "%.2f" % p_thr_, fontsize=7)
