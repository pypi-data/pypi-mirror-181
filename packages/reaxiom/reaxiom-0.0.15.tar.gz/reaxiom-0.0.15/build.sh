rm /Users/test/axiom/master/code/huggingface/dist/*
rm -rf /Users/test/axiom/master/code/site-package/axiom/__pycache__

python -m build --outdir /Users/test/axiom/master/code/huggingface/dist
twine upload /Users/test/axiom/master/code/huggingface/dist/*
