#!/bin/bash

# Extract version from pyproject.toml
VERSION=$(grep '^version = ' services/agent/pyproject.toml | sed 's/version = "\(.*\)"/\1/')

# Update version in auterion-app.yml
sed -i "s/^app-version: .*/app-version: $VERSION  # auto-generated, do not edit/" auterion-app.yml
