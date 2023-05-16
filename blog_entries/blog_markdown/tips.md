# Minor tips

# Description
This is a blog entry that I will use to share some things I have found to be useful but that do not really require a lengthy specified blog entry.

I think of it as a **notes to self** section of my website.


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
