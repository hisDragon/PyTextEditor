# PyTextEditor v1.0
This is a Text Editor written using **tkinter** module of Python 3.

## Essential Resources

#### Python 3.x
You can download the latest version of Python 3 from [**here**](https://www.python.org/downloads/).
This comes with a built-in **tkinter** module and *no* further installation is required.

#### PyEnchant module
You can use the following command to install PyEnchant.
~~~
pip install pyenchant
~~~

An Example of How to use PyEnchant in Python 3.x Scripts
```python
import enchant
dictionary = enchant.Dict('en_US')  # Language to be use to check Spellings
dictionary.check('Hello')           # True
dictionary.check('Helo')            # False
dictionary.suggest('Helo')          # Suggests list of strings from higher probability to lower
```
Documentation of [**PyEnchant**](https://pyenchant.github.io/pyenchant/).

## Editor I Used To Develop PyTextEditor
**PyCharm** - Python IDE for Professional Developers.
You can Download it from [**here**](https://www.jetbrains.com/pycharm/download/).
Here is a good Guide to Install PyCharm on Windows 10 on [Youtube](https://www.youtube.com/watch?v=SZUNUB6nz3g)

#### TO-DO List
- [x] Non-Dynamic Spell Check to the PyTextEditor.
- [x] Dynamic Spell Check to the PyTextEditor.
- [ ] Advanced Status Bar - with Cursor Position.

## Use Of PyTextEditor v1.0
This is **not** a Text Editor for Professional Use and is still under Development.
There might still be some existing bugs and PyTextEditor has not yet been Tested.
**_PyTextEditor is not for Public Use_**
