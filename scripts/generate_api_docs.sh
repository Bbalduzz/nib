#!/bin/bash
# Script to regenerate API documentation from Python source code
#
# This script uses sphinx-apidoc to generate .rst files from the Python source.
# Run this whenever you add new modules or significantly change the API.
#
# Usage:
#   ./scripts/generate_api_docs.sh
#
# For pre-commit hook usage, add to .pre-commit-config.yaml:
#   - repo: local
#     hooks:
#       - id: generate-api-docs
#         name: Generate API docs
#         entry: ./scripts/generate_api_docs.sh
#         language: script
#         files: ^python/nib/.*\.py$
#         pass_filenames: false

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Paths
PYTHON_SRC="$PROJECT_ROOT/python/nib"
DOCS_DIR="$PROJECT_ROOT/docs"
API_DIR="$DOCS_DIR/api"

echo "Regenerating API documentation..."
echo "  Source: $PYTHON_SRC"
echo "  Output: $API_DIR"

# Create API directory if it doesn't exist
mkdir -p "$API_DIR"

# Run sphinx-apidoc
# Options:
#   -f        : Force overwriting of existing files
#   -e        : Put each module on its own page
#   -M        : Put module documentation before submodule documentation
#   -o        : Output directory
#   --implicit-namespaces : Interpret module paths as implicit namespace packages
sphinx-apidoc \
    -f \
    -e \
    -M \
    -o "$API_DIR" \
    "$PYTHON_SRC" \
    --implicit-namespaces

echo ""
echo "API documentation generated successfully!"
echo ""
echo "To build the full documentation, run:"
echo "  cd $DOCS_DIR && make html"
echo ""
echo "The generated HTML will be in $DOCS_DIR/_build/html/"
