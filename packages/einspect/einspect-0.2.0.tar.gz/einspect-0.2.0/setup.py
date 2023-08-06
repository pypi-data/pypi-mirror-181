# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['einspect', 'einspect.structs', 'einspect.views']

package_data = \
{'': ['*']}

install_requires = \
['pycapi>=0.82.1,<0.83.0', 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'einspect',
    'version': '0.2.0',
    'description': 'Extended Inspect - view and modify memory structs of runtime objects.',
    'long_description': '# einspect\n\nExtended Inspect for CPython\n\nProvides simple and robust ways to view and modify the base memory structures of Python objects at runtime.\n\n> *einspect* is in very early stages of development, API may change at any time without notice.\n\nNote: The below examples show interactions with a `TupleView`, but applies much the same way generically for\nmany of the specialized `View` subtypes that are dynamically returned by the `view` function. If no specific\nview is implemented, the base `View` will be used which represents limited interactions on the assumption of\n`PyObject` struct parts.\n\n\n```python\nfrom einspect import view\n\nobj = (1, 2, 3)\nv = view(obj)\n\nprint(v)\n```\n> `TupleView[tuple](<PyTupleObject at 0x10078dd00>)`\n\n## 1. Viewing python object struct attributes\n\nState information of the underlying `PyTupleObject` struct can be accessed through the view\'s attributes.\n```python\nprint(v.ref_count)  # ob_refcnt\nprint(v.type)       # ob_type\nprint(v.size)       # ob_size\nprint(v.items)      # ob_item\n```\n> ```\n> 4\n> <class \'tuple\'>\n> 3\n> <einspect.structs.c_long_Array_3 object at 0x105038ed0>\n> ```\n\n## 2. Writing to view attributes\n\nWriting to these attributes will affect the underlying object of the view.\n\nNote that most memory-unsafe attribute modifications require entering an unsafe context manager with `View.unsafe()`\n```python\nwith v.unsafe():\n    v.size -= 1\n\nprint(obj)\n```\n> `(1, 2)`\n\n## 3. Writing to view attributes\n\nSince `items` is an array of integer pointers to python objects, they can be replaced by `id()` addresses to modify\nindex items in the tuple.\n```python\nfrom einspect import view\n\ntup = (100, 200)\n\nwith view(tup).unsafe() as v:\n    s = "dog"\n    v.item[0] = id(s)\n\nprint(tup)\n```\n> ```\n> (\'dog\', 200)\n> \n> >> Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)\n> ```\n\nSo here we did set the item at index 0 with our new item, the string `"dog"`, but this also caused a segmentation fault.\nNote that the act of setting an item in containers like tuples and lists "steals" a reference to the object, even\nif we only supplied the address pointer.\n\nTo make this safe, we will have to manually increment a ref-count before the new item is assigned. To do this we can\neither create a `view` of our new item, and increment its `ref_count += 1`, or use the apis from `einspect.api`, which\nare pre-typed implementations of `ctypes.pythonapi` methods.\n```python\nfrom einspect import view\nfrom einspect.api import Py\n\ntup = (100, 200)\n\nwith view(tup).unsafe() as v:\n    a = "bird"\n    Py.IncRef(a)\n    v.item[0] = id(a)\n    \n    b = "kitten"\n    Py.IncRef(b)\n    v.item[1] = id(b)\n\nprint(tup)\n```\n> `(\'bird\', \'kitten\')`\n \n🎉 No more seg-faults, and we just successfully set both items in an otherwise immutable tuple.\n\nTo make the above routine easier, you can access an abstraction by simply indexing the view.\n\n```python\nfrom einspect import view\n\ntup = ("a", "b", "c")\n\nv = view(tup)\nv[0] = 123\nv[1] = "hm"\nv[2] = "🤔"\n\nprint(tup)\n```\n> `(123, \'hm\', \'🤔\')`\n',
    'author': 'ionite34',
    'author_email': 'dev@ionite.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
