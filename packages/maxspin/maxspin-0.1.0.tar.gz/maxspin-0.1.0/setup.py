# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxspin']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.8.0,<0.9.0',
 'flax>=0.4.2,<0.5.0',
 'jax>=0.3.13,<0.4.0',
 'numpy>=1.22.3,<2.0.0',
 'optax>=0.1.2,<0.2.0',
 'scipy>=1.8.1,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'maxspin',
    'version': '0.1.0',
    'description': 'Estimate spatial information in spatial -omics datasets.',
    'long_description': '\n![Maxspin](https://raw.github.com/dcjones/maxspin/main/logo.png)\n\n\nMaxspin (maximization of spatial information) is an information theoretic\napproach to quantifying the degree of spatial organization in spatial\ntranscriptomics (or other spatial omics) data.\n\n## Installation\n\nThe python package can be installed with:\n```sh\npip install maxspin\n```\n\n## Basic Usage\n\nThis package operates on `AnnData` objects from the [anndata](https://github.com/scverse/anndata) package.\n\nWe assume the existence of a spatial neighborhood graph. A simple and effective\nway of doing this is Delaunay triangulation, for example using [squidpy](https://github.com/scverse/squidpy).\n\n```python\nimport squidpy as sq\n\nsq.gr.spatial_neighbors(adata, delaunay=True, coord_type="generic")\n```\n\nSpatial information can then be measured using the `spatial_information` function.\n\n```python\nfrom maxspin import spatial_information\n\nspatial_information(adata, prior=None)\n```\n\nThis adds a `spatial_information` column to the `var` metadata.\n\nSimilarly, pairwise spatial information can be computed with\n`pairwise_spatial_information`. This function will test every pair of genes,\nwhich is pretty impractical for large numbers of genes, so it\'s a good idea to\nsubset the `AnnData` object before calling this.\n\n\n```python\nfrom maxspin import pairwise_spatial_information\n\npairwise_spatial_information(adata, prior=None)\n```\n\nFor a more detailed example, check out the [tutorial](https://github.com/dcjones/maxspin/blob/main/tutorial.ipynb).\n\n## Interpreting the spatial information score\n\nThe method compute a score for every cell/spot that\'s in `[0,1]`, like a\ncorrelation but typically much smaller, and sums them to arrive at a spatial\ninformation score that is then in `[0, ncells]`. It\'s possible to normalize for\nthe number of cells by just dividing, but by default a pattern involving more\ncells is considered more spatially coherent, hence the sum.\n\n## Normalization\n\nThere are different ways spatial information can be computed. By default, no\nnormalization is done and spatial information is computed on absolute counts.\nUncertainty is incorporated using a Gamma-Poisson model.\n\nIf `prior=None` is used, the method makes no attempt to account for estimation\nuncertainty and computes spatial information directly on whatever is in\n`adata.X`.\n\nThe recommended way to run `spatial_information` is with some kind of normalized\nestimate of expression with some uncertainty estimation. There are two\nrecommended ways of doing this: SCVI and Vanity.\n\n\n## SCVI\n\n[SCVI](https://scvi-tools.org/) is a convenient and versatile probabilistic\nmodel of sequencing experiments, from which we can sample from the posterior to\nget normalized point estimates with uncertainty.\n\nUsing Maxspin with SCVI looks something like this:\n\n\n```python\nimport scvi\nimport numpy as np\nfrom maxspin import spatial_information\n\nscvi.model.SCVI.setup_anndata(adata)\nmodel = scvi.model.SCVI(adata, n_latent=20)\n\n# Sample log-expression values from the posterior.\nposterior_samples = np.log(model.get_normalized_expression(return_numpy=True, return_mean=False, n_samples=20, library_size="latent"))\nadata_scvi = adata.copy()\nadata_scvi.X = np.mean(posterior_samples, axis=0)\nadata_scvi.layers["std"] = np.std(posterior_samples, axis=0)\n\nspatial_information(adata_scvi, prior="gaussian")\n```\n\nThe [tutorial](https://github.com/dcjones/maxspin/blob/main/tutorial.ipynb) has\na more in depth example of using SCVI.\n\n## Vanity\n\n\nI developed the normalization method [vanity](https://github.com/dcjones/vanity)\nin part as convenient way to normalize spatial transcriptomics data in a way\nthat provides uncertainty estimates. The preferred way of running vanity + maxspin is then:\n\n```python\nfrom maxspin import spatial_information\nfrom vanity import normalize_vanity\n\nnormalize_vanity(adata)\nspatial_information(adata, prior="gaussian")\n\n```\n\nCompared to SCVI, this model more aggressively shrinks low expression genes,\nwhich might cause it to miss something very subtle, but is less likely to detect\nspurious patterns.\n',
    'author': 'Daniel C. Jones',
    'author_email': 'djones3@fredhutch.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dcjones/maxspin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
