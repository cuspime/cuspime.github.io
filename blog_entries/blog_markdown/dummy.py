import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
from plotly.subplots import make_subplots


def plot_time_series_decomposition(
    df: pd.DataFrame,
    value_column: str,
    time_column: str,
    model: str = "multiplicative",
    show_autocorrelation_plot: bool = True,
    lags_for_acf: int = 365 * 2,
):
    """
    Show the time series decomposition of a time series pandas dataframe

    Args:
        df (pd.DataFrame): pandas dataframe to try and extract seasonalities.
        value_column (str): name of the column with the values to analyse
        time_column (str): name of the column used to extract seasonalities and trends.
        model (str):       one of 'additive' or 'multiplicative'. Default is 'multiplicative'
        show_autocorrelation_plot (bool): True if an autocorrelation plot wants to be displayed. Default is True
        lags_for_acf (int): number of lags to consider in the autocorrelation plot. Default is 365 * 2

    Returns:
        None
    """
    data_orig = df[[time_column, value_column]].copy()
    data_orig.set_index(pd.DatetimeIndex(df[time_column], freq="D"), inplace=True)
    analysis = data_orig[value_column]

    decompose_result_mult = seasonal_decompose(analysis, model=model)
    trend = decompose_result_mult.trend
    seasonal = decompose_result_mult.seasonal
    residual = decompose_result_mult.resid

    fig = make_subplots(
        rows=3,
        cols=1,
        vertical_spacing=0.05,
        horizontal_spacing=0.15,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=(["Original set and Trend", "Seasonal", "Residual"]),
        shared_xaxes=True,
        specs=[[{}], [{}], [{"secondary_y": True}]],
    )

    # Original
    fig.add_trace(
        go.Scattergl(
            x=df[time_column],
            y=df[value_column],
            name="Original",
            line_color="rgba(30,125,245,.5)",
            mode="markers",
        ),
        col=1,
        row=1,
    )

    # Trend
    fig.add_trace(
        go.Scattergl(
            x=analysis.index,
            y=trend,
            name="Trend",
            line_color="black",
            mode="lines",
        ),
        col=1,
        row=1,
    )

    # Seasonal
    fig.add_trace(
        go.Scattergl(
            x=analysis.index,
            y=seasonal,
            name="Seasonal",
            line_color="black",
            mode="lines",
        ),
        col=1,
        row=2,
    )

    # Residual
    fig.add_trace(
        go.Scattergl(
            x=analysis.index,
            y=residual,
            name="Residual",
            line_color="black",
            mode="lines",
        ),
        col=1,
        row=3,
        secondary_y=False,
    )

    fig.update_layout(height=800, width=1400)
    if show_autocorrelation_plot:
        my_dpi = 96
        fig_plt, ax = plt.subplots(figsize=(1400 / my_dpi, 200 / my_dpi), dpi=my_dpi)
        plot_acf(analysis, lags=lags_for_acf, ax=ax)
        fig_plt.show()
    fig.show()

    return None
