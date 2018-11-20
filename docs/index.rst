.. Zmei Generator documentation master file, created by
   sphinx-quickstart on Sun Jan  7 00:25:10 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Zmei Utils
============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Zmei Utils - is a set of small utilities that is needed by Zmei gene

Install::

   pip install zmei-utils


Utilities available:

* **ZmeiReactJsonEncoder** - extension of json encoder'a that supports django model auto-serialization.
* **ZmeiDataViewMixin** - adds convenient and efficient get_data() method instead of get_context_data()
* **CrudView**, **CrudMultiplexerView** - allow to mix together multiple generic views like CreateView, DeleteView ..etc
* **ZmeiReactViewMixin** - server-side React render inside Django without external tooling



