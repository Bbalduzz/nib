# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXAPIDOC  ?= sphinx-apidoc
SOURCEDIR     = .
BUILDDIR      = _build
PYTHONDIR     = ../python

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean apidoc html html-strict livehtml linkcheck doctest

# Generate API documentation from source code (cleans stale files first)
apidoc:
	@rm -rf api/
	$(SPHINXAPIDOC) -f -e -M -o api/ $(PYTHONDIR)/nib --implicit-namespaces
	@echo "API documentation generated in api/"

# Clean build directory
clean:
	rm -rf $(BUILDDIR)
	@echo "Build directory cleaned."

# Build HTML documentation
html: apidoc
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build HTML with strict warnings (for CI)
html-strict: apidoc
	@$(SPHINXBUILD) -b html -W --keep-going "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished (strict mode). The HTML pages are in $(BUILDDIR)/html."

# Validate external and internal links
linkcheck: apidoc
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS) $(O)
	@echo
	@echo "Link check complete. Results in $(BUILDDIR)/linkcheck."

# Run doctests in documentation
doctest: apidoc
	@$(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)/doctest" $(SPHINXOPTS) $(O)
	@echo
	@echo "Doctest complete. Results in $(BUILDDIR)/doctest."

# Live reload server for development
livehtml: apidoc
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
