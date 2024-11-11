import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_pred_vs_actual(
    df,
    col_actual: str,
    col_pred: str,
    col_hue: str | None = None,
    hue_title_fancy: str | None = None,
    hue_order: list | np.ndarray | None = None,
    hue_palette: dict | None = None,
    target_title_fancy: str = r"",
    target_units_title_fancy: str = r"",
    scores: dict | None = None,
    use_hue: bool = True,
    print_scores: bool = True,
) -> None:
    """
    Plot a scatter plot comparing actual vs predicted values, with optional color
    grouping based on a hue variable. Also display an ideal diagonal line on the plot
    and, if requested, the regression scores.

    Parameters
    ----------
    df : pd.DataFrame
        A Pandas DataFrame containing the actual and predicted values.
    col_actual : str
        The name of the column in the DataFrame representing the actual values.
    col_pred : str
        The name of the column in the DataFrame representing the predicted values.
    col_hue : str, optional
        The name of the column in the DataFrame to be used for color grouping (hue) if
        `use_hue` is set to `True`, by default `None`.
    hue_title_fancy : str, optional
        The title for the legend of the hue variable, by default `None`.
    hue_order : list or np.ndarray, optional
        The order of hue categories to be displayed in the legend, by default `None`.
    hue_palette : dict, optional
        A dictionary specifying colors for each hue category, by default `None`.
    target_title_fancy : str, optional
        The title to display for the target variable in the axis labels, by default
        `''`.
    target_units_title_fancy : str, optional
        The title to display for the target units in the axis labels, by default `''`.
    scores : dict, optional
        A dictionary containing regression scores (R-squared, RMSE, etc.), by default
        `None`.
    use_hue : bool, optional
        Whether to apply color grouping based on the hue variable, by default `True`.
    print_scores : bool, optional
        Whether to print the regression scores on the plot, by default `True`.

    Returns
    -------
    None
        This function does not return anything. It directly displays the plot.

    Raises
    ------
    ValueError
        If the given columns for actual or predicted values are not found in the
        DataFrame. Also if `use_hue` is set to `True` and the given column for the hue
        is not found.
    """

    # Plot with given RC context
    # [NOTE: seaborn uses matplotlib's RC (Runtime Configuration) and, therefore, there
    # is no need to configure Seaborn's RC in particular.]
    with plt.rc_context(
        {"axes.axisbelow": True, "text.usetex": True, "font.family": "serif"}
    ):
        # Initialise figure and axes
        plt.figure(figsize=(9, 7))
        ax = plt.axes()

        plt.title(rf"Actual and predicted {target_title_fancy}", pad=20)

        # Define scatter plot for actual and predicted target values
        sns.scatterplot(
            ax=ax,
            data=df,
            x=col_actual,
            y=col_pred,
            hue=col_hue if use_hue is True else None,
            hue_order=hue_order if use_hue is True else None,
            palette=hue_palette if use_hue is True else None,
            alpha=1.0,
            s=15,
        )

        # Plot text with the regression scores
        if print_scores is True and scores is not None:
            ax.text(
                x=0.03,
                y=0.97,
                s="".join(
                    [
                        f"{score_title_fancy} $=$ ${score_value:.3f}$" + "\n"
                        for (score_title_fancy, score_value) in scores.items()
                    ]
                ),
                fontsize=10,
                color="black",
                ha="left",
                va="top",
                transform=ax.transAxes,
            )

        # Define axes' ranges
        x_min = df[[col_actual, col_pred]].min().min()
        x_max = df[[col_actual, col_pred]].max().max()
        Delta_x = x_max - x_min
        x_min = x_min - 0.05 * Delta_x
        x_max = x_max + 0.05 * Delta_x
        y_min = x_min
        y_max = x_max
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Define the ideal diagonal line
        plt.axline(
            xy1=(0, 0),
            slope=1,
            color="black",
            linewidth=0.75,
            linestyle="solid",
            alpha=0.75,
            zorder=1,
        )

        # Define axes labels
        ax.set_xlabel(
            rf"Actual {target_title_fancy} $ \, [$ {target_units_title_fancy} $]$",
            fontdict={"fontsize": 10},
            labelpad=10,
        )
        ax.set_ylabel(
            rf"Predicted {target_title_fancy} $ \, [$ {target_units_title_fancy} $]$",
            fontdict={"fontsize": 10},
            labelpad=10,
        )

        # Enable axes' minor ticks
        ax.minorticks_on()

        # Set aspect ratio
        ax.set_aspect("equal")

        # Define grid
        ax.grid(
            visible=True,
            which="major",
            color="lightgray",
            linestyle="solid",
            linewidth=0.5,
        )
        ax.grid(
            visible=True,
            which="minor",
            color="lightgray",
            linestyle="dotted",
            linewidth=0.5,
        )

        # Legend
        if use_hue is True:
            plt.legend(
                title=hue_title_fancy,
                loc="center left",
                fontsize=10,
                labelspacing=1.25,
                framealpha=0,
                bbox_to_anchor=(1, 0.5),
            )

        # Show plot
        plt.show()
