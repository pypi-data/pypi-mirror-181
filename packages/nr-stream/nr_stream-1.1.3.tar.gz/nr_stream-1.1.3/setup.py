# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stream']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nr-stream',
    'version': '1.1.3',
    'description': '',
    'long_description': '# nr-stream\n\nThis package provides utilities for writing functional-style code in Python. The package originally contained only\nthe `Stream` class, hence the name, but since we\'ve adopted the terminology for letting us *streamline* large chunks\nof our code.\n\n## API\n\n### Optional objects\n\nRepresents an optional value, i.e. one that either has a valid value or is `None`. The class is useful to\nchain modifications and have them execute based on whether a value is available or not.\n\n__Example__\n\n```py\nimport os\nfrom nr.stream import Optional\n\nopt = Optional(os.getenv("SOMEVAR"))\nvalue = opt.or_else_get(lambda: do_something_else())\nvalue = opt.or_else_raise(lambda: Exception("SOMEVAR not set"))\nopt = opt.map(lambda value: value + " another value")\nlen(opt.stream().count())  # 0 or 1\n```\n\n### Refreshable objects\n\nA Refreshable is a container for a value that can be updated and inform listeners. A chained operations on a\nrefreshable will be replayed if the parent refreshable is updated. This is eager evaluation, not lazy evaluation\nand allows performant calls to `.get()` without going through a lazy chain of operations each time.\n\nUnlike `Optional` or `Stream`, the `Refreshable` knows no "empty" state.\n\nThis class is often useful to pass configuration data around in your application. It allows making modifications\nto the configuration and have it automatically propagate throughout the application.\n\n__Example__\n\n```py\nfrom nr.stream import Refreshable\n\nroot = Refreshable[int | None](None)\nchild = root.map(lambda v: 42 if v is None else v)\n\nprint(root.get())  # None\nprint(child.get()) # 42\nroot.update(10)\nprint(root.get())  # 10\nprint(child.get()) # 10\n```\n\n### Stream objects\n\nThe Stream class wraps an iterable and allows you to build a chain of modifiers on top of it. This often\ngreatly simplifies consecutive operations on an iterable object and its items.\n\n__Example__\n\n```py\nfrom nr.stream import Stream\n\nvalues = [3, 6, 4, 7, 1, 2, 5]\nassert list(Stream(values).chunks(values, 3, fill=0).map(sum)) == [13, 10, 5]\n```\n\n> __Important__: Stream objects always immediately convert the object passed to an iterator. This means\n> that you cannot branch stream objects, as both forks will share the same initial iterator.\n\n### Supplier objects\n\nThe Supplier class allows you to lazily evaluate the retrieval of a value, as well as chain modifications\non top of it and even trace the lineage of these modifications. It provides convenience methods such as\n`.map()`, `.once()`, `.get_or_raise()`. Unlike an `Optional`, a supplier will treat `None` as a valid value\nand instead separately track the state of "no value".\n\nTrying to read a value from an empty supplier raises a `Supplier.Empty` exception. Note that suppliers _always_\nevaluate lazily, unlike `Optional`.\n\n__Example__\n\n```py\nfrom nr.stream import Supplier\n\nsup = Supplier.of(42)\nsup = sup.map(lambda value: print(value))\nassert sup.get() == None  # prints: 42\nassert sup.get() == None  # prints: 42\n\nSupplier.void().get()  # raises Supplier.Empty\n```\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
