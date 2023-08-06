# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_pipedream']

package_data = \
{'': ['*']}

install_requires = \
['singer-sdk==0.15.0']

entry_points = \
{'console_scripts': ['tap-pipedream = tap_pipedream.tap:TapPipedream.cli']}

setup_kwargs = {
    'name': 'tap-pipedream',
    'version': '0.0.1b1',
    'description': '`tap-pipedream` is a Singer tap for Pipedream, built with the Meltano SDK for Singer Taps.',
    'long_description': '<div align="center">\n\n# tap-pipedream\n\n<div>\n  <a href="https://results.pre-commit.ci/latest/github/edgarrmondragon/tap-pipedream/main">\n    <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/edgarrmondragon/tap-pipedream/main.svg"/>\n  </a>\n  <a href="https://github.com/edgarrmondragon/tap-pipedream/blob/main/LICENSE">\n    <img alt="License" src="https://img.shields.io/github/license/edgarrmondragon/tap-pipedream"/>\n  </a>\n</div>\n\nSinger tap for Pipedream. Built with the [Meltano Singer SDK](https://sdk.meltano.com).\n\n</div>\n\n## Capabilities\n\n* `catalog`\n* `state`\n* `discover`\n* `about`\n* `stream-maps`\n* `schema-flattening`\n\n## Settings\n\n| Setting             | Required | Default | Description |\n|:--------------------|:--------:|:-------:|:------------|\n| token               | True     | None    | API Token for Pipedream |\n| start_date          | False    | None    | Earliest timestamp to get data from |\n| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |\n| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |\n| flattening_enabled  | False    | None    | \'True\' to enable schema flattening and automatically expand nested properties. |\n| flattening_max_depth| False    | None    | The max depth to flatten schemas. |\n\nA full list of supported settings and capabilities is available by running: `tap-pipedream --about`\n\n### Source Authentication and Authorization\n\nTo generate an API key, follow the instructions [in the docs](https://pipedream.com/docs/api/auth/#pipedream-api-key).\n\n## Usage\n\nYou can easily run `tap-pipedream` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-pipedream --version\ntap-pipedream --help\ntap-pipedream --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tests` subfolder and then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-pipedream` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-pipedream --help\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\nInstall Meltano (if you haven\'t already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-pipedream\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-pipedream --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-pipedream target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to\ndevelop your own taps and targets.\n',
    'author': 'Edgar Ramírez-Mondragón',
    'author_email': 'edgarrm358@gmail.com',
    'maintainer': 'Edgar Ramírez-Mondragón',
    'maintainer_email': 'edgarrm358@gmail.com',
    'url': 'https://github.com/edgarrmondragon/tap-pipedream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
