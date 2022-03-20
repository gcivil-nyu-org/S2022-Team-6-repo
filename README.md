# CoviGuard - Development

[![Build Status](https://app.travis-ci.com/gcivil-nyu-org/S2022-Team-6-repo.svg?branch=develop)](https://app.travis-ci.com/gcivil-nyu-org/S2022-Team-6-repo)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/S2022-Team-6-repo/badge.svg?branch=develop)](https://coveralls.io/github/gcivil-nyu-org/S2022-Team-6-repo?branch=develop)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Development Environment
- conda create --name coviguard python=3.9.5
- conda activate coviguard
- conda install --file requirements/dev.txt
- create a .env file in coviguard directory
- SECRET_KEY = 'password' and DATABASES_PASSWORD='password'
