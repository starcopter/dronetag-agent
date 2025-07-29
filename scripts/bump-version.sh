#!/bin/bash

# Parse arguments
git_add=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--git-add)
            git_add=true
            shift
            ;;
        *)
            version=${1#v}
            shift
            ;;
    esac
done

if [ -z "$version" ]; then
    echo "Usage: $0 <version> [--git-add]"
    exit 1
fi

# Update version in auterion-app.yml
sed -i "s/^app-version:.*/app-version: $version/" auterion-app.yml
$git_add && git add auterion-app.yml

for project in . services/agent; do
    # Update version in pyproject.toml
    sed -i "s/^version = .*/version = \"$version\"/" "$project/pyproject.toml"
    # Update uv.lock
    uv sync --no-active --project "$project"
    # git-add pyproject.toml and uv.lock if --git-add is set
    $git_add && git add "$project/pyproject.toml" "$project/uv.lock"
done

exit 0
