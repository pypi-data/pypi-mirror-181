# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kernel_catalogo_videos',
 'kernel_catalogo_videos.castmembers',
 'kernel_catalogo_videos.castmembers.application',
 'kernel_catalogo_videos.castmembers.application.use_cases',
 'kernel_catalogo_videos.castmembers.application.use_cases.create',
 'kernel_catalogo_videos.castmembers.application.use_cases.delete',
 'kernel_catalogo_videos.castmembers.application.use_cases.get',
 'kernel_catalogo_videos.castmembers.application.use_cases.search',
 'kernel_catalogo_videos.castmembers.application.use_cases.update',
 'kernel_catalogo_videos.castmembers.domain',
 'kernel_catalogo_videos.castmembers.infrastructure',
 'kernel_catalogo_videos.categories',
 'kernel_catalogo_videos.categories.application',
 'kernel_catalogo_videos.categories.application.use_cases',
 'kernel_catalogo_videos.categories.application.use_cases.create',
 'kernel_catalogo_videos.categories.application.use_cases.delete',
 'kernel_catalogo_videos.categories.application.use_cases.get',
 'kernel_catalogo_videos.categories.application.use_cases.search',
 'kernel_catalogo_videos.categories.application.use_cases.update',
 'kernel_catalogo_videos.categories.domain',
 'kernel_catalogo_videos.categories.infrastructure',
 'kernel_catalogo_videos.core',
 'kernel_catalogo_videos.core.application',
 'kernel_catalogo_videos.core.domain',
 'kernel_catalogo_videos.core.infrastructure',
 'kernel_catalogo_videos.genres',
 'kernel_catalogo_videos.genres.application',
 'kernel_catalogo_videos.genres.application.use_cases',
 'kernel_catalogo_videos.genres.application.use_cases.create',
 'kernel_catalogo_videos.genres.application.use_cases.delete',
 'kernel_catalogo_videos.genres.application.use_cases.get',
 'kernel_catalogo_videos.genres.application.use_cases.search',
 'kernel_catalogo_videos.genres.application.use_cases.update',
 'kernel_catalogo_videos.genres.domain',
 'kernel_catalogo_videos.genres.infrastructure',
 'kernel_catalogo_videos.videos',
 'kernel_catalogo_videos.videos.application',
 'kernel_catalogo_videos.videos.application.use_cases',
 'kernel_catalogo_videos.videos.application.use_cases.create',
 'kernel_catalogo_videos.videos.application.use_cases.delete',
 'kernel_catalogo_videos.videos.application.use_cases.get',
 'kernel_catalogo_videos.videos.application.use_cases.search',
 'kernel_catalogo_videos.videos.application.use_cases.update',
 'kernel_catalogo_videos.videos.domain',
 'kernel_catalogo_videos.videos.infrastructure']

package_data = \
{'': ['*']}

install_requires = \
['pika>=1.3.1,<2.0.0',
 'python-slugify>=7.0.0,<8.0.0',
 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'kernel-catalogo-videos',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'Lucas',
    'author_email': 'lucassrod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
