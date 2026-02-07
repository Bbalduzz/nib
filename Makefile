.PHONY: build build-runtime install clean pypi pypi-test bump-patch bump-minor bump-major

# Build the Swift runtime (universal binary: arm64 + x86_64) and copy to Python SDK
build-runtime:
	@python scripts/stamp_version.py
	cd package && swift build -c release --arch arm64 --arch x86_64
	cp package/.build/apple/Products/Release/nib-runtime sdk/python/nib/bin/nib-runtime
	codesign --force --sign - sdk/python/nib/bin/nib-runtime
	@echo "Runtime built, signed, and copied to sdk/python/nib/bin/nib-runtime"

# Build everything
build: build-runtime

# Install the Python package in development mode
install: build-runtime
	pip install -e .

# Build wheel and publish to PyPI
pypi: build-runtime
	pip install -q build wheel twine
	rm -rf dist
	python -m build --wheel
	python -m wheel tags --platform-tag macosx_11_0_universal2 --remove dist/*.whl
	twine upload dist/*

# Build wheel and publish to TestPyPI (for dry runs)
pypi-test: build-runtime
	pip install -q build wheel twine
	rm -rf dist
	python -m build --wheel
	python -m wheel tags --platform-tag macosx_11_0_universal2 --remove dist/*.whl
	twine upload --repository testpypi dist/*

# Version bumping (single source: sdk/python/nib/__init__.py)
VERSION_FILE = sdk/python/nib/__init__.py

bump-patch:
	@python scripts/bump.py patch

bump-minor:
	@python scripts/bump.py minor

bump-major:
	@python scripts/bump.py major

# Clean build artifacts
clean:
	rm -rf package/.build
	rm -rf dist
	rm -f sdk/python/nib/bin/nib-runtime
