.PHONY: build build-runtime install clean

# Build the Swift runtime and copy to Python SDK
build-runtime:
	cd package && swift build -c release
	cp package/.build/release/nib-runtime sdk/python/nib/bin/nib-runtime
	codesign --force --sign - sdk/python/nib/bin/nib-runtime
	@echo "Runtime built, signed, and copied to sdk/python/nib/bin/nib-runtime"

# Build everything
build: build-runtime

# Install the Python package in development mode
install: build-runtime
	pip install -e .

# Clean build artifacts
clean:
	rm -rf package/.build
	rm -f sdk/python/nib/bin/nib-runtime
