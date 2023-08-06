README
######


**NAME**

``opr`` - object programming runtime


**SYNOPSIS**


``import opr``


**INSTALL**

``pip3 install opr --upgrade --force-reinstall``


**DESCRIPTION**


With ``opr`` your can have the commands of a irc bot available on your cli.
Instead of having to join a irc channel and give commands to your bot, you
can run these commands on your shell.

``opr`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object.


**CONFIGURATION**

``opr`` looks for it's modules in ~/.opr/mod. A collection of sample modules 
can be found in /usr/local/opr/mod. Copy what modules you want to ~/.opr/mod,
or write your own modules and put them in ~/.opr/mod. 


**PROGRAMMING**


The ``opr`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> import opr
>>> o = opr.Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from opr import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

>>> from opr import Object, save
>>> o = Object()
>>> save(o)
>>> 'opr.Object/c13c5369-8ada-44a9-80b3-4641986f09df/2021-08-31/15:31:05.717063'


**AUTHOR**


Bart Thate


**COPYRIGHT**

``opr`` is placed in the Public Domain. No Copyright, No License.
