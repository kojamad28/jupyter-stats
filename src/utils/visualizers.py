from typing import List, Optional

import matplotlib
import pandas as pd

matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa
import seaborn as sns  # noqa

sns.set_context('poster', 1.5)


class BaseVisualizer:
    """
    Attributes
    ----------
    _row_size : int, default 10
        horizontal size of a subplot
    _col_size : int, default 10
        vertical size of a subplot
    
    Methods
    -------
    _calc_nrows_ncols
    _get_ax
    """

    def __init__(self, row_size: int = 10, col_size: int = 10):
        self._row_size = row_size
        self._col_size = col_size

    def _calc_nrows_ncols(self, nplots: int, max_ncols: int):
        """
        Calculates numbers of rows and columns for subplots.

        Parameters
        ----------
        nplots : int
            Number of subplots in the figure
        max_ncols : int
            Maximum number of columns in the figure

        Returns
        -------
        nrows : int
            Calculated number of rows in the figure
        ncols : int
            Calculated number of columns in the figure
        """
        if isinstance(nplots, int) and isinstance(max_ncols, int):
            if nplots <= 0 or max_ncols <= 0:
                raise ValueError('nplots and max_ncols must be positive values.')
        else:
            raise TypeError('nplots and max_ncols must be positive integers.')

        if nplots < max_ncols:
            ncols = nplots
        else:
            ncols = max_ncols

        nrows = nplots // ncols + int(nplots % ncols != 0)

        return nrows, ncols
    
    def _get_subplots(self, nrows: int, ncols: int):
        return plt.subplots(nrows, ncols, figsize=(self._col_size*ncols, self._row_size*nrows), tight_layout=True)
    
    def _get_ax(self, axes: matplotlib.axes.Axes, idx: int, nrows: int, ncols: int):
        """
        Gets axis object for the subplot.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            Axes objects to draw the plot onto
        idx : int
            Index number in plotted dataset
        nrows : int
            Number of rows in the figure
        ncols : int
            Number of columns in the figure

        Returns
        -------
        matplotlib.axes.Axes
        """

        if nrows > 1 and ncols > 1:
            return axes[idx // ncols, idx % ncols]
        elif nrows * ncols == 1:
            return axes
        else:
            return axes[idx]
        

class DataFrameVisualizer(BaseVisualizer):
    """
    Attributes
    ----------
    _dataframe : pandas.DataFrame
        Dataset for visualization
    _row_size : int, default 10
        Horizontal size of a subplot
    _col_size : int, default 10
        Vertical size of a subplot
    """

    def __init__(self, dataframe: pd.DataFrame, row_size: int, col_size: int):
        super().__init__(row_size, col_size)
        self._dataframe = dataframe

    def _plot_dots(
            self, x_col: str, y_col: str, plot_size: float, ax: matplotlib.axes.Axes,
            hue_col: Optional[str] = None, **kwargs
        ):
        sns.stripplot(data=self._dataframe, x=x_col, y=y_col, hue=hue_col, size=plot_size, ax=ax, **kwargs)

    def plot_bar(
            self, x_col: str, y_cols: List[str],
            hue_col: Optional[str] = None, max_ncols: int = 5,
            xlabel: str = '', ylabel: str = '',
            plot_dots: bool = True, plot_size: float = 10,
            long_xticklabels: bool = False, **kwargs
        ):
        nrows, ncols = self._calc_nrows_ncols(len(y_cols), max_ncols)
        fig, axes = self._get_subplots(nrows, ncols)

        for i, y_col in enumerate(y_cols):
            ax_i = self._get_ax(axes, i, nrows, ncols)
            sns.barplot(data=self._dataframe, x=x_col, y=y_col, hue=hue_col, ax=ax_i, **kwargs)

            if plot_dots:
                self._plot_dots(x_col, y_col, hue_col, plot_size, ax=ax_i)
            
            ax_i.set(xlabel=xlabel, ylabel=ylabel, title=y_col)

            if long_xticklabels:
                ax_i.set_xticklabels(ax_i.get_xticklabels(), rotation=45, ha='right')

        return fig
