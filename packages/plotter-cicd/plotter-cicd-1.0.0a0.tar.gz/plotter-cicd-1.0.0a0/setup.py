# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plotter']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0', 'numpy>=1.23.5,<2.0.0']

entry_points = \
{'console_scripts': ['plotter = plotter:main']}

setup_kwargs = {
    'name': 'plotter-cicd',
    'version': '1.0.0a0',
    'description': 'Python template project',
    'long_description': "# poetry-cicd-example\nBare bones repository demonstrating a python [poetry](https://python-poetry.org/) project using GitHub actions\n\nAssumptions:\n\n* Project is hosted on github.com \n* Project uses an organization-scoped GitHub App for CICD operations\n* Project built using [poetry](https://python-poetry.org/)\n* Docker images will be published to ghcr.io\n* Credentials stored in GitHub Secrets\n  * CICD_APP_ID\n  * CICD_APP_PRIVATE_KEY\n  * SONAR_TOKEN\n  * GITHUB_TOKEN\n* Branch names: `main`, `develop`, `issues/*`\n* Project is using [semantic versioning](https://semver.org/)\n\n## Important Notes\n\n* After merging to `master`, a new change request should be opened to merge `master`\nback in to `develop` so that the version in `develop` is at least one minor version \nahead of `master`. This can't be automated because development likely will have continued while\nthe release was being evaluated and will cause merge conflicts since both branches will have\nmodified the version number. \n* Changes made in release branches should also be pushed back to `develop` if they are critical. Otherwise, the\nmerge from `master` to `develop` after release will incorporate the changes.\n* It is recommended that only one change request targeting `master` should be open at any given time. \n\n## Stages Overview\n\nThe main unit of work for Jenkins pipelines are Stages. Stages can contain sub-stages and can be conditionally run. At a high-level, this template defines the following\nstages listed below. In general, the stages are executed in order from top to bottom. However, some stages can be skipped for any particular run of the pipeline. \n\n* **Checkout**  \n  This stage checks out the code as triggered by the server event.  \n\n## Git Branching Strategy\n\nThe template is built with the assumption that the project follows the [git-workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) branching\nstrategy. A lot of the functionality is conditional on matching against branch naming conventions. Therefore, it is important that the project conform to this workflow.\n\n## Software Versioning\n\nThis template assumes the use of [semantic versioning](https://semver.org/) for the project being built. The strategy can be summarized as:\n\n* The `develop` branch always contains a [prerelease](https://semver.org/#spec-item-9) version of the project\n* The `develop` branch will always be at least 1 minor version ahead of `master`\n* Feature branches (prefixed with `issues/`) are branched from `develop`. When a feature branch is built, [build metadata](https://semver.org/#spec-item-10) is appended to the prerelease version \n* Every merge to develop increments the prerelease version number by one\n* Release branches are branched from `develop` and are named as `release/<semver>` where `<semver>` is a valid 'major.minor.patch' semantic version string.\n* The `<semver>` part of the branch name is used as the version for the release. See [Releasing](#Releasing) for details\n* As soon as a release branch is created, the minor version in the `develop` branch is bumped automatically by the `release-created.yml` workflow\n* Release candidates are created once a change request is created from a `release/*` branch that targets `master`\n* When a release candidate is created, the prerelease identifier is set to `rc` and the prerelease version is reset to 1\n* Any change (commit) to a release candidate change request results in a bump to the prerelease version\n* Merges to master remove the prerelease version and identifier but leave the remaining 'major.minor.patch' version\n* Tags using the version as the tag name are created for every new prerelease, release candidate, and release\n\n## Releasing\n\nWhen it is time to cut a release from the develop branch, a decision must be made. Is the release a major, minor, or patch release?\nThere are rules that should be followed when determining if the release is [minor](https://semver.org/#spec-item-7) or [major](https://semver.org/#spec-item-8).\n\nIf it is minor, create a branch prefixed with `release/` and followed by the development version without prerelease version or identifier. \nFor example, if `0.2.0-alpha.4` is the current develop version, then create a branch called `release/0.2.0`\n\nIf it is major, create a branch prefixed with `release/` and followed by the development major version incremented by 1 and using 0 for minor and patch number. \nFor example, if `0.2.0-alpha.4` is the current develop version, then create a branch called `release/1.0.0`\n\n## Reviews\n\nThere are two points of review in this workflow:\n\n1. When a change request is initiated from a feature branch to develop. This is a chance for developers to review the code that was developed as part of the feature request\nand suggest changes. The assumption is that code that makes it to develop is eligible for release and it will be deployed to a system integration testing (SIT) environment.\n2. When a change request is initiated from a release branch to `master`. This is a chance for other stakeholders to review the proposed changed that will be released \nto operations (OPS). As soon as a change request is initiated, the software will be deployed to a user acceptance testing (UAT) environment so that functionality can be tested.\nIt is recommended that only one change request targeting `master` should be open at any given time. \n",
    'author': 'Frank Greguska',
    'author_email': '89428916+frankinspace@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/podaac/poetry-cicd-example',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
