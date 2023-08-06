# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postgres_composite_types']

package_data = \
{'': ['*'],
 'postgres_composite_types': ['templates/postgres_composite_types/forms/widgets/*']}

install_requires = \
['Django>=3.2.16', 'psycopg2>=2.8.4']

setup_kwargs = {
    'name': 'django-postgres-composite-types',
    'version': '1.0.0b0',
    'description': 'Postgres composite types support for Django',
    'long_description': '# Django Postgres composite types\n\nAn implementation of Postgres\' [composite types](http://www.postgresql.org/docs/current/static/rowtypes.html)\nfor [Django](https://docs.djangoproject.com/en/1.9/).\n\n## Usage\n\nInstall with:\n\n    pip install django-postgres-composite-types\n\nThen add \'postgres_composite_types\' to your `INSTALLED_APPS`:\n\n    INSTALLED_APPS = [\n        # ... Other apps\n        \'postgres_composite_types\',\n    ]\n\nDefine a type and add it to a model:\n\n```python\nfrom django.db import models\nfrom postgres_composite_types import CompositeType\n\nclass Address(CompositeType):\n    """An address."""\n\n    address_1 = models.CharField(max_length=255)\n    address_2 = models.CharField(max_length=255)\n\n    suburb = models.CharField(max_length=50)\n    state = models.CharField(max_length=50)\n\n    postcode = models.CharField(max_length=10)\n    country = models.CharField(max_length=50)\n\n    class Meta:\n        db_type = \'x_address\'  # Required\n\n\nclass Person(models.Model):\n    """A person."""\n\n    address = Address.Field()\n```\n\nAn operation needs to be prepended to your migration:\n\n```python\nimport address\nfrom django.db import migrations\n\n\nclass Migration(migrations.Migration):\n\n    operations = [\n        # Registers the type\n        address.Address.Operation(),\n        migrations.AddField(\n            model_name=\'person\',\n            name=\'address\',\n            field=address.Address.Field(blank=True, null=True),\n        ),\n    ]\n```\n\n## Examples\n\nArray fields:\n\n```python\nclass Card(CompositeType):\n    """A playing card."""\n\n    suit = models.CharField(max_length=1)\n    rank = models.CharField(max_length=2)\n\n    class Meta:\n        db_type = \'card\'\n\n\nclass Hand(models.Model):\n    """A hand of cards."""\n    cards = ArrayField(base_field=Card.Field())\n```\n\nNested types:\n\n```python\nclass Point(CompositeType):\n    """A point on the cartesian plane."""\n\n    x = models.IntegerField()\n    y = models.IntegerField()\n\n    class Meta:\n        db_type = \'x_point\'  # Postgres already has a point type\n\n\nclass Box(CompositeType):\n    """An axis-aligned box on the cartesian plane."""\n    class Meta:\n        db_type = \'x_box\'  # Postgres already has a box type\n\n    top_left = Point.Field()\n    bottom_right = Point.Field()\n```\n\n## Gotchas and Caveats\n\nThe migration operation currently loads the _current_ state of the type, not\nthe state when the migration was written. A generic `CreateType` operation\nwhich takes the fields of the type would be possible, but it would still\nrequire manual handling still as Django\'s `makemigrations` is not currently\nextensible.\n\nChanges to types are possible using `RawSQL`, for example:\n\n```python\noperations = [\n    migrations.RunSQL([\n        "ALTER TYPE x_address DROP ATTRIBUTE country",\n        "ALTER TYPE x_address ADD ATTRIBUTE country integer",\n    ], [\n        "ALTER TYPE x_address DROP ATTRIBUTE country",\n        "ALTER TYPE x_address ADD ATTRIBUTE country varchar(50)",\n    ]),\n]\n```\n\nHowever, be aware that if your earlier operations were run using current DB\ncode, you will already have the right types\n([bug #8](https://github.com/danni/django-postgres-composite-types/issues/8)).\n\nIt is recommended to that you namespace your custom types to avoid conflict\nwith future PostgreSQL types.\n\nLookups and indexes are not implemented yet\n([bug #9](https://github.com/danni/django-postgres-composite-types/issues/9),\n[bug #10](https://github.com/danni/django-postgres-composite-types/issues/10)).\n\n## Running Tests\n\nClone the repository, go to it\'s base directory and run the following commands.\n\n    pip install tox\n    tox\n\nOr if you want a specific environment\n\n    tox -e py311-dj41\n\n## Authors\n\n-   Danielle Madeley <danielle@madeley.id.au>\n-   Tim Heap <hello@timheap.me>\n\n## License\n\nThis project is licensed under the BSD license.\nSee the LICENSE file for the full text of the license.\n',
    'author': 'Danielle Madeley',
    'author_email': 'danielle@madeley.id.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
