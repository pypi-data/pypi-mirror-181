[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][bsd3-image]][bsd3-url]


# thcouch

## Overview
TangledHub library for couchdb with a focus on asynchronous functions


## Licensing
thcouch is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details


## Installation
```bash
pip instal thcouch
```


## Testing
```bash
docker-compose build --no-cache thcouch-test ; docker-compose run --rm thcouch-test
```


## Building
```bash
docker-compose build thcouch-build ; docker-compose run --rm thcouch-build
```


## Publish
```bash
docker-compose build thcouch-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thcouch-publish
```


<!-- Links -->

<!-- Badges -->
[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause
[build-image]: https://img.shields.io/badge/build-success-brightgreen
[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green

[pypi-project-url]: https://pypi.org/project/thcouch/
[stable-ver-image]: https://img.shields.io/pypi/v/thcouch?label=stable
[python-ver-image]: https://img.shields.io/pypi/pyversions/thcouch.svg?logo=python&logoColor=FBE072
[status-image]: https://img.shields.io/pypi/status/thcouch.svg



