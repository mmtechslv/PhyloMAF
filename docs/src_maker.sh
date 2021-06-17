export SPHINX_APIDOC_OPTIONS="members,undoc-members,show-inheritance,inherited-members,autosummary"
sphinx-apidoc -M --tocfile index -E -H API -o api/ ../pmaf
