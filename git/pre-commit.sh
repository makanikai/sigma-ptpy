#!/usr/bin/env bash

flake8 sigma_ptpy examples tests --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 sigma_ptpy examples tests --count --exit-zero --ignore=C901 --max-line-length=127 --statistics
