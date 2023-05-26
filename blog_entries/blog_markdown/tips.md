
- [Description](#description)
- [Git commands](#git-commands)
    - [Important](#important)
    - [Less important](#less-important)
    - [Take-it-back commands](#take-it-back-commands)
    - [Pre-commit](#pre-commit)
- [Python](#python)
    - [Forcing python to reimport a library](#forcing-python-to-reimport-a-library)
- [Pyspark](#pyspark)
    - [Time sliding windows](#time-sliding-windows)
    - [Flattening nested dataframes](#flattening-nested-dataframes)
- [Plots](#plots)
    - [Gantt](#gantt)
    - [Time Series quick decomposition](#time-series-quick-decomposition)
    - [Pareto](#pareto)
- [Maps](#maps)
- [Other resources](#other-resources)



# Description
This is a blog entry that I will use to share some things I have found to be useful but that do not really require a lengthy specified blog entry.

I think of it as a **notes to self** section of my website.

---

# Git commands
  Many of these commands can be found [in this website](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)

## Important

  * **git branch**  list all the branches in my local repo  
  * **git branch new_branch**  Creates a branch named **new_branch**  
  * **git branch -d localBranchName**  Delete branch locally  
  * **git checkout -b some_branch**  Create and check out a new branch named **some_branch**. If we drop the **-b** we can only   checkout an existing branch
  * **git pull**  fetch the specified remote's copy of current branch and merge it into the local copy  
  * **git add file1 file2**  adds file1 and file 2 to the algorithm that keeps track of changes in the next commit.  
  * **git commit -m 'short message' -m 'more descriptive message'**  creates a commit with the changes we have made and some   comments about what we did
  * **git push**  push the branch to be merged  

## Less important

  * **git --version** 
  * **git status**
  * **git log** shows the entire commit history 
  * **git diff** shows differences between the branch and the working directory.
  * **git clone URL_of_repo**

## Take-it-back commands

  If we messed something up, we can try and revert the changes:

  * **git revert commit_key** undoes all the changes made in commit and applies it to the current branch
  * **git reset file1** remove file1 from the staging area but leaves working directory unchanged
  * **git reset --hard HEAD** resets to last valid commit
  * **git log** see history
  
To get single files or folders from a branch (in case we accidentally deleted a file or something like that) we can use:
```bash
git fetch --all
git checkout origin/master -- <your_file_path>
git add <your_file_path>
git commit -m "<your_file_name> updated"
```

## Pre-commit
Arguably, one of the tools that helps the most when coding within a team is to make use of automatic tests and/or quick
style fixes to our code. A quick example: spotting and fixing `trailing white spaces` manually
(who has time for that???). The tool to use in this case is [pre-commit](https://pre-commit.com/), which is run when you launch a `git commit` command and prevents you from making a commit or fixes your files if one of your predefined hooks fails.

After installing pre-commit via `pip install pre-commit` you can run 
```bash
pre-commit sample-config
```
to create a basic first configuration file: `.pre-commit-config.yaml`. This yaml file will consist of a couple of sources (*repo*) with corresponding versions (*rev*) and a series of hooks to be used (*hook* and a list of identifiers *id*).
The file looks like:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
    -   id: black
```
Which you can modify to your convenience. For instance, you may want to run some hooks with specific arguments or explicitly skip a given file for some particular hook:

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: trailing-whitespace
    -   id: check-added-large-files
        args: ['--maxkb=1024']
        exclude: "notebooks/some_jupyter_notebook.ipynb, some_data.csv"
-   repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
    -   id: black
        args:['--line-length=100']
```

Now that you have a yaml you want to work with, you can install the pre-commit hooks:
```bash
pre-commit install
```

Now, even though these hooks are supposed to run right before the commit in an automated way, it is nice to be able to run them directly as a sanity check when you are fixing some of the issues you have:
```bash
pre-commit run --all-files
pre-commit run <ONE_FILE_NAME> # to run hooks on just one specific file
```

It is very importatn that if one of your files fails to pass one of the hooks you'll need to tell git you want to add the modified version that will now pass the check, otherwise you will never be able to actually commit and push (unless you want to skip the pre-commit hooks verification via `git commit -m <MESSAGE> --no-verify` which is not recommended).
```bash
git add <MODIFIED_FILE_NAME>
git add commit -m <MESSAGE>
``` 

---


# Python
## Forcing python to reimport a library
When using jupyter notebooks, IPython optimizes the amount of imports by disregarding those that have been already imported and saved on memory.
This is of course counterproductive when you are trying to have a utils file to create clean jupyter notebooks for presentation purposes that have a lot of code behind. 
Saving the python file you're working on and rerunning the jupyter cell containing the import won't be enough.

However, you can enforce the reload of functions `f, g, h` from library `X` with:
```python
from importlib import reload
import X
from X import (f, g, h)

reload(X)
```

---

# Pyspark

## Time sliding windows

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def lagged_window(
    window_partition_columns:str,
    time_column:str,
    window_size:float=7,
    lagging_days:float=0
):
    """This function creates a sliding window of constant width from a date column based on a single time column

    Args:
        window_partition_columns (list of str): Names of the columns to be used as partition.
            These columns "reset" the windowing function.
        time_column (str): Column with the date or timestamp to be used to order the rows for the windowing function
        window_size (int or float): number of days or portion of a day to be used as interval for the window size.
            This will be rounded to integer seconds. Defaults to 7.
        lagging_days (int or float): number of days to shift the windowing function. Defaults to 0

    Returns:
        pyspark.sql.window.Window
    """
    days_to_s = lambda x: int(24 * 60 * 60 * x)

    win = (
        Window.partitionBy(window_partition_columns)
        .orderBy(F.col(time_column).cast("timestamp").cast("long"))
        .rangeBetween(-(days_to_s(window_size + lagging_days)), -days_to_s(lagging_days))
    )
    return win

# Example
part_cols = ['shop', 'city', 'customer', 'device']
lag_window = Window.partitionBy(part_cols).orderBy('time_column')

df_with_moving_average = (
    df
    .withColumn('col_1D_MA', F.avg('col').over(lagged_window(part_cols, 'time_column', window_size=1)))
    .withColumn('col_30m_MA', F.avg('col').over(lagged_window(part_cols, 'time_column', window_size=(.5/24))))
)
```

## Flattening nested dataframes
```python
def flatten_df(nested_df):
    """Flatten a spark dataframe

    Args:
        nested_df (pyspark.sql.dataframe.DataFrame): dataframe with possible struct-type columns
    
    Returns:
        pyspark.sql.dataframe.DataFrame with a column per 'key' of the nested_df struct-type columns
    
    """
    flat_cols = [c[0] for c in nested_df.dtypes if c[1][:6] != 'struct']
    nested_cols = [c[0] for c in nested_df.dtypes if c[1][:6] == 'struct']

    flat_df = nested_df.select(flat_cols +
                               [F.col(nc+'.'+c).alias(nc+'_'+c)
                                for nc in nested_cols
                                for c in nested_df.select(nc+'.*').columns])
    return flat_df
```


---

# Plots

## Gantt

```python
def gantt_chart(
    df: pd.DataFrame,
    tasks_column: str,
    initial_time_column: str,
    end_time_column: str,
    color_dict: dict = None,
) -> plt.Figure:
    """Gantt plot that shows where each individual task starts and ends.
    Each task can have multiple time intervals

    Args:
        df (pd.DataFrame): pandas dataframe with 
        tasks_column (str): name of the column containing categorical data
        initial_time_column (str): start time of task interval
        end_time_column (str): end time of task interval
        color_dict (dict, optional): colors assigned to each task interval. Defaults to None.

    Returns:
        plt.Figure: Gantt plot
    """
    if color_dict:
        cd = color_dict
    else:
        cd = {}
        for i in df[tasks_column].unique():
            cd[i] = "#" + "".join([np.random.choice([i for i in set("0123456789ABCDEF")]) for j in range(6)])

    fig, ax = plt.subplots(1, figsize=(25, 6))
    # Plot
    ax.barh(
        df[tasks_column],
        df[end_time_column] - df[initial_time_column],
        left=df[initial_time_column],
        color=df[tasks_column].apply(lambda x: cd[x]),
        height=0.9,
    )

    # Axes formatting
    ax.yaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1, interval=3))
    fig.autofmt_xdate(which="both")
    plt.show()

    return fig
```

## Time Series quick decomposition
Hopefullly a time saver when we just want to see quickly some characteristics of a time series.
```python
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

```

## Pareto 
```python
def plot_pareto(
    df: pd.DataFrame, categorical_column: str, value_column: str, threshold_on_value: float = None
) -> go.Figure:
    """Plot Pareto's curve and compare to the usual 80/20 principle

    Args:
        df (pd.DataFrame): dataframe with at least a categorical and a value column
        categorical_column (str): name of the categorical column to consider.
        value_column (str): name of the values column
        threshold_on_value (float, optional): cutoff at which categorical entities will be grouped under a unique group.
            If None, all elements are shown independently. Defaults to None.

    Returns:
        go.Figure: Pareto plot
    """

    df["n_elements"] = 1
    df["elem_group"] = df.apply(
        lambda x: x[categorical_column] if x[value_column] > threshold_on_value else "below_threshold", axis=1
    )

    df_grouped = df.groupby("elem_group").agg({value_column: "sum", "n_elements": "sum"}).reset_index()
    df_grouped = df_grouped.sort_values(by=value_column, ascending=False)

    is_below_thr = df_grouped["elem_group"] == "below_threshold"
    df_grouped = pd.concat([df_grouped[~is_below_thr], df_grouped[is_below_thr]])

    df_grouped["cumulative_pct_val"] = 100 * df_grouped[value_column].cumsum() / df_grouped[value_column].sum()
    df_grouped["cat_order_per_value"] = df_grouped["n_elements"].cumsum()
    df_grouped["cum_pct_categories"] = 100 * df_grouped["cat_order_per_value"] / df_grouped["n_elements"].sum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df_grouped["cum_pct_categories"],
            y=df_grouped["cumulative_pct_val"],
            name=f"cumulative % of {value_column}",
            mode="lines+markers",
            marker_color="rgba(255,0,0,.5)",
            customdata=df_grouped[["elem_group", "n_elements", value_column]],
            hovertemplate="<br>".join(
                [
                    "<b>%{y:0.2f}</b>",
                    "Element: <b>%{customdata[0]}</b>",
                    "Value: <b>%{customdata[2]:,}</b>",
                    "Cumulative % categories: <b>%{x}</b>",
                    
                    "n_elements: <b>%{customdata[1]}</b>",
                ]
            ),
        ),
        secondary_y=True,
    )

    fig.add_trace(
        go.Bar(
            x=df_grouped["cum_pct_categories"],
            y=df_grouped[value_column],
            name=value_column,
            marker=dict(color="rgba(0,0,255,.5)"),
        )
    )

    fig.add_hline(y=80, line=dict(color="rgba(0,0,0,.3)", dash="dash"), secondary_y=True)
    fig.add_vline(x=20, line=dict(color="rgba(0,0,0,.3)", dash="dash"))

    fig.update_layout(
        hovermode="x unified", title=f"Pareto chart of {value_column} per {categorical_column}", height=600, width=1600
    )
    return fig
```

---

# Maps

---

# Other resources
There's a plethora of tips, guidelines and tutorials about MLOps, Data Science, Visualizations and Analysis out there.
Some of my personal favourites are:
* [MadeWithML by Goku Mohandas](https://madewithml.com/)
* [Kuhyen Tran's tips](https://khuyentran1401.github.io/reproducible-data-science/README.html)
* [Geographic Data Science by Sergio Rey, Dani Arribas and Levi Wolf](https://geographicdata.science/book/intro.html)
* [Python Data Science Handbook by Jake VanderPlas](https://jakevdp.github.io/PythonDataScienceHandbook/)