# Minor tips

# Description
This is a blog entry that I will use to share some things I have found to be useful but that do not really require a lengthy specified blog entry.

I think of it as a **notes to self** section of my website.

# Git
  Many of these commands can be found [in this website](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)
* Important
  * **git branch**  list all the branches in my local repo  
  * **git branch new_branch**  Creates a branch named **new_branch**  
  * **git branch -d localBranchName**  Delete branch locally  
  * **git checkout -b some_branch**  Create and check out a new branch named **some_branch**. If we drop the **-b** we can only   checkout an existing branch
  * **git pull**  fetch the specified remote's copy of current branch and merge it into the local copy  
  * **git add file1 file2**  adds file1 and file 2 to the algorithm that keeps track of changes in the next commit.  
  * **git commit -m 'short message' -m 'more descriptive message'**  creates a commit with the changes we have made and some   comments about what we did
  * **git push**  push the branch to be merged  

* Less important
  * **git --version** 
  * **git status**
  * **git log** shows the entire commit history 
  * **git diff** shows differences between the branch and the working directory.
  * **git clone URL_of_repo**

* Take it back
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

# Pyspark


# Plots

## Gantt

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def gantt_chart(
    df: pd.DataFrame,
    tasks_column: str,
    initial_time_column: str,
    end_time_column: str,
    color_dict: dict = None,
) -> plt.Figure:
    if color_dict:
        cd = color_dict
    else:
        cd = {}
        for i in df["tasks_column"].unique():
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