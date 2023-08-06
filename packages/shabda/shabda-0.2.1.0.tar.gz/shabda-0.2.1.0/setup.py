# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shabda']

package_data = \
{'': ['*'], 'shabda': ['templates/*']}

install_requires = \
['flask[async]',
 'freesound-api',
 'google-cloud-texttospeech',
 'gunicorn',
 'pydub',
 'requests',
 'termcolor',
 'typer[all]']

entry_points = \
{'console_scripts': ['shabda = shabda_cli:cli']}

setup_kwargs = {
    'name': 'shabda',
    'version': '0.2.1.0',
    'description': 'A semantic audio samples curator for livecoding software',
    'long_description': 'Shabda\n======\n\n![Shabda logo](https://raw.githubusercontent.com/ilesinge/shabda/master/assets/logo.png)\n\n\nShabda is a tool to fetch random samples from https://freesound.org/ based on given words or to generate Text-to-Speech samples for use in impro sessions on instruments such as Tidal Cycles and Estuary.\n\n[Shabda](https://en.wikipedia.org/wiki/Shabda) is the Sanskrit word for "speech sound". In Sanskrit grammar, the term refers to an utterance in the sense of linguistic performance. \n\nInstall\n-------\n\n- Install Python 3: https://www.python.org/\n- Install pip: https://pypi.org/project/pip/\n- Install ffmpeg: https://ffmpeg.org/ (e.g. Debian/Ubuntu: `apt install ffmpeg`)\n- Install Shabda for standard usage: `pip install shabda`\nor\n- Install shabda for hacking:\n    - Install poetry: https://python-poetry.org/docs/#installation\n    - In Shabda repository, install dependencies: `poetry install`\n\nUse (command line)\n------------------\n\nIn order to download a sample pack, execute in the terminal `shabda <definition> --licenses <license_name>`.\n\nAny word can be a pack definition. If you want more than one sample, separate words by a comma: `blue,red`\n\nYou can define how many variations of a sample to assemble by adding a colon and a number.\ne.g. `blue,red:3,yellow:2` will produce one \'blue\' sample, three \'red\' samples and two \'yellow\' sample.\n\nThe optional `--licenses` parameter allows to fetch only samples that have the specified license. Multiple licenses can be allowed by repeating the `--licenses` argument. Possible licenses are `cc0` (Creative Commons Zero), `by` (Creative Commons Attribution), and `by-nc` (Creative Commons Attribution Non-Commercial).\n\nFull example:\n```\nshabda spaghetti:2,monster:4 --licenses cc0 --licenses by\n```\n\nThe first time you execute this command, it will ask you for a Freesound token, that you will be redirected to. You will need a Freesound account.\n\nBy default, samples will be downloaded in a `samples` directory under the current working directory. You can override this by adding a `config.ini` file to the `$HOME/.shabda/` directory, containing:\n\n```ini\n[shabda]\n\nsamples_path=/path/to/your/desired/samples/directory/\n```\n\nUse (web application)\n---------------------\n\nLaunch the web application:\n\nIn debug mode:\n```\nFLASK_APP=shabda FLASK_DEBUG=1 flask run\n```\nIn production:\n```\ngunicorn --workers=4 "shabda:create_app()" -b localhost:8000\n```\n\nTest\n----\n\n```\npoetry run pytest\n```\n\nNotes\n-----\n\nWith Estuary, Shabda makes use of this feature: https://github.com/dktr0/estuary/wiki#adding-sound-files-to-estuarywebdirt-on-the-fly\n\nAll command line examples must be preceded by `poetry run` if in hacking/development mode.\n\nRoadmap\n-----\n\nSee: https://github.com/users/ilesinge/projects/4\n',
    'author': 'Alexandre G.-Raymond',
    'author_email': 'alex@ndre.gr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://shabda.ndre.gr/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
