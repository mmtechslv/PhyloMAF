export SPHINX_APIDOC_OPTIONS="members,undoc-members,show-inheritance,inherited-members"
rm -rf api
sphinx-apidoc -M --tocfile index -e -E -H API -o api/ ../pmaf "../pmaf/tests/*"

# export PYTHONPATH=/home/mmtechslv/akasha/PhyloMAF
# sphinx-autogen -o generated *.rst
