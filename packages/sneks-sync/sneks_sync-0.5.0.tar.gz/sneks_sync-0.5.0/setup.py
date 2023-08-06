# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sneks']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.1.0,<3.0.0',
 'coiled>=0.2.7,<0.3.0',
 'rich>=12.4.4,<13.0.0',
 'setuptools>=65.3.0',
 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'sneks-sync',
    'version': '0.5.0',
    'description': 'Launch a Dask cluster from a virtual environment',
    'long_description': '# sneks\n\nGet your snakes in a row.\n\n`sneks` lets you launch a [Dask cluster in the cloud](https://coiled.io/), matched to your local software environment\\*, in a single line of code. No more dependency mismatches or Docker image building.\n\n```python\nfrom sneks import get_client\n\nclient = get_client()\n```\n\n\\*your local [Poetry](https://python-poetry.org/) or [PDM](https://pdm.fming.dev/latest/) environment. You must use poetry or PDM. Locking package managers are what sensible people use, and you are sensible.\n\n*Neat! Sneks also supports ARM clusters! Just pass ARM instances in `scheduler_instace_types=`, `worker_instace_types=` and cross your fingers that all your dependencies have cross-arch wheels!*\n\n## Installation\n\n```shell\npoetry add -G dev sneks-sync\n```\n\n## A full example:\n\n```shell\nmkdir example && cd example\npoetry init -n\npoetry add -G dev sneks-sync\npoetry add distributed==2022.5.2 dask==2022.5.2 bokeh pandas pyarrow  # and whatever else you want\n```\n```python\nfrom sneks import get_client\nimport dask.dataframe as dd\n\nclient = get_client(name="on-a-plane")\nddf = dd.read_parquet(\n    "s3://nyc-tlc/trip data/yellow_tripdata_2012-*.parquet",\n)\nprint(ddf.groupby(\'passenger_count\').trip_distance.mean().compute())\n```\n\nOh wait, we forgot to install a dependency!\n```shell\npoetry add foobar\n```\n\nWhen we reconnect to the cluster (using the same name), the dependencies on the cluster update automatically.\n```python\nfrom sneks import get_client\nimport dask.dataframe as dd\nimport foobar  # ah, how could we forget this critical tool\n\nclient = get_client(name="on-a-plane")\nddf = dd.read_csv(\n    "s3://nyc-tlc/csv_backup/yellow_tripdata_2012-*.csv",\n)\nmeans = ddf.groupby(\'passenger_count\').trip_distance.mean()\nmeans.apply(foobar.optimize).compute()\n\n```\n\n## Caveats\n\nThis is still a proof-of-concept-level package. It\'s been used personally quite a bit, and proven reliable, but use at your own risk.',
    'author': 'Gabe Joseph',
    'author_email': 'gjoseph92@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.4,<4.0.0',
}


setup(**setup_kwargs)
