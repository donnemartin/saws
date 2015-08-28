#!/usr/bin/env bash

flake8 --ignore=F811 --max-line-length=99 --exclude=build .
