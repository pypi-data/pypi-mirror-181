# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cacheing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cacheing',
    'version': '0.1.0',
    'description': 'a performant python cacheing library',
    'long_description': '## cacheing - Pure Python Cacheing Library\n\n\n![Coverage](https://img.shields.io/codecov/c/github/breid48/rcache?token=E2GVMUS6KU)\n\n---\n\n### Motivation\n\n---\n\nThe initial motivation behind this package was twofold: fix the long insertion/eviction times in `cachetools.LFUCache` and provide an alternative to the `cachetools.TTLCache` offering variable per-key TTL\'s.\n\n\n### Installation\n\n---\n\n```\npip install -U cacheing\n```\n\nAnd then in your python interpreter:\n\n```python\nimport cacheing\n```\n\n### Updating\n\n---\n\n\n\n### Usage\n\n---\n\n```python\n>>> from cacheing import LFUCache\n\n>>> cache = LFUCache(capacity=2)\n\n>>> cache[1] = 2\n>>> cache[2] = 3\n>>> cache[3] = 4\n\n>>> cache\nLFUCache{2: 3, 3: 4}\n```\n\n### Benchmark\n\n---\n\ncacheing has an included benchmarking library found in `./benchmark`.\n\n```shell\n$ python3 ./benchmark.py --help\n\nusage: benchmark [-h] [--cache [CACHE [CACHE ...]]] [--method [{get,set,delete} [{get,set,delete} ...]]]\n\narguments:\n  -h, --help            show this help message and exit\n  --cache [CACHE [CACHE ...]], -c [CACHE [CACHE ...]]\n                        cache(s) to benchmark. example: cacheing.LRUCache.\n  --method [{get,set,delete} [{get,set,delete} ...]], -m [{get,set,delete} [{get,set,delete} ...]]\n                        method(s) to benchmark.\n```\n\n#### Run the Benchmarks:\n```shell\n$ cd benchmark\n\n$ python3 ./benchmark.py --cache cachetools.LRUCache cacheing.LRUCache --method set get delete\n```\n\n\n### Performance\n\n--- \nAll benchmark times were measured using the provided `benchmark` library. See the\n[benchmark section](#Benchmark) for details. The default benchmarking configuration executes 100,000 get operations, \n20,000 set operations and `n = cache_size` delete operations. The median, p90, and p99 times for each\noperation, measured in microseconds, or `1e-6`, are displayed in the figures below.\n\n---\n\n####    Get (LFU Cache)  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;            Delete (LFU Cache)\n\n<img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lfu_get.png" width="300"> <img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lfu_delete.png" width="300">\n\n####    Set (LFU Cache) &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;            Set - Cross Section (LFU Cache)\n\n<img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lfu_set.png" width="300"> <img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lfu_set_crosssection.png" width="300">\n\n---\n\n####    Set (LRU Cache)  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;            Get (LRU Cache)\n\n<img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lru_set.png" width="300"> <img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lru_get.png" width="300">\n\n#### Delete (LRU Cache)\n\n<img src="https://raw.githubusercontent.com/breid48/cacheing/main/assets/lru_delete.png" width="300">\n',
    'author': 'Blake Reid',
    'author_email': 'breid48@uwo.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/breid48/cacheing',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
