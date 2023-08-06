# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hm01', 'hm01.clusterers']

package_data = \
{'': ['*']}

install_requires = \
['HeapDict>=1.0.1,<2.0.0',
 'colorama>=0.4.5,<0.5.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'graphviz>=0.20.1,<0.21.0',
 'jsonpickle>=2.2.0,<3.0.0',
 'leidenalg>=0.9.0,<0.10.0',
 'networkit>=10.0,<11.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pytest>=7.1.3,<8.0.0',
 'structlog>=22.1.0,<23.0.0',
 'tomli>=2.0.1,<3.0.0',
 'treeswift>=1.1.28,<2.0.0',
 'typer>=0.6.1,<0.7.0',
 'typing-extensions>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['cm = hm01.cm:entry_point',
                     'cm2universal = hm01.to_universal:entry_point']}

setup_kwargs = {
    'name': 'connectivity-modifier',
    'version': '0.1.0b0',
    'description': 'connectivity modifier',
    'long_description': '# cm\n\nConnectivity Modifier (CM) is a generic meta-method for community detection while ensuring a certain connectivity\n(minimum number of edges to remove to disconnect a community) on the output communities (clusters). To be more precise, suppose that you want to ensure that Leiden clusters must not be "easily-cut". For example, ensuring that none of the output clusters have connectivity below\n$\\log_{10}(n)$, $n$ the size of any cluster, you can run CM paired with Leiden, and it will ensure that all output clusters have that minimum size cut. CM supports customizable requirements on the connectivity of the clusters. CM currently supports Leiden (CPM optimization), IKC, and Leiden (modularity optimization) out-of-the-box. After installing the necessary dependencies, users can simply run CM to obtain Leiden clusters with strong guarantees on connectivity.\n\n## Installation\n\nOur software is provided via PyPI and supports at least Python 3.9.\n\n```\npip3 install --pre connectivity-modifier # install prerelease version\n```\n\nNote that you must install [Viecut](https://github.com/VieCut/VieCut) as a dependency explicitly, i.e., `viecut` the binary must be compiled and the path to `viecut` must be specified in the config file (explained below).\n\nSay that you installed `viecut` in `/foo/bar/viecut`, then you want to create a config file in `~/.config/cm/config.toml` and have something like this:\n\n```toml\n[tools]\nikc_path = "{project_root}/third_party/ikc.py" # {project_root} is a specific path resolving to the source code root\nleiden_path = "" # currently obsolete\nviecut_path = "/foo/bar/viecut" # viecut\'s path\n```\n\nOr if the main executable detects that `cm.toml` is in the current working directory, the `cm.toml` config file will have the highest priority instead.\n\nAfter all this, try `cm --help`, and you should see something like this:\n\n```bash\nUsage: cm [OPTIONS]\n\n  Connectivity-Modifier (CM). Take a network and cluster it ensuring cut\n  validity\n\nOptions:\n  -i, --input TEXT                [required]\n[...]\n```\n\n## Usage\n\nOur main executable is provided as `cm`, and we list the options below:\n\n### `-i, --input GRAPH_TSV`\n\nThe input graph to be clustered, where `graph.tsv` is a tab-delimited edgelist, only including integer edge ids. Note that we follow the `igraph` convention, where we assume that the input node ids are continuous, and if not, dummy nodes are added.\n\n### `-c, --clusterer [leiden|ikc|leiden_mod]`\n\nThe clusterer to be paired with. If using with an existing clustering (`-e`), then the same clusterer must be used (see below). Otherwise, one must decide which clusterer should be used. The clusterers are:\n\n - `leiden`: Leiden (`leidenalg`) with CPM optimization, must specify `-g, --resolution` later\n - `ikc`: Iterative k-core, must specify `-k` later\n - `leiden_mod`: Leiden with modularity optimization, no other parameters allowed to be specified\n\n### `-e, --existing-clustering CLUSTERING_FILE`\n\nSpecifies the starting clustering (in effect saving time for `cm` to reproduce the initial clustering) to be `modified` to have sufficient connectivity thresholds (c.f. `-t`). The file format is "native" to the clustering method. For example, for IKC, it is the default IKC csv output format. For Leiden, it is the Leiden output format (i.e., tab-delimited node_id cluster_id file).\n\n### `-g, --resolution FLOAT`, `-k, --k INTEGER`\n\nThe respective parameters for either Leiden(CPM) (`-c leiden`) or IKC (`-c ikc`). Only at most one should be specified, and for modularity optimization neither should be specified.\n\n### `-o, --output OUTPUT_PREFIX`\n\nThe output prefix. Two files will be produced, first the `OUTPUT_PREFIX` will have a file denoting the last cluster a node has been in, and `{OUTPUT_PREFIX}.tree.json` is a serialized tree denoting the history of the execution of the algorithm. See also [converting the output to more parsable formats](#format-conversion).\n\n### `-t, --threshold TEXT`\n\nThreshold expression. `cm` guarantees that the output clustering all have clusters that are above a specific threshold. We list some examples for `-t` below:\n\n```bash\n# each line denotes a valid example for "-t"\n2 # connectivity must >= 2\n0.1mcd # connectivity must >= 0.1 MCD, MCD the minimum intra-cluster degree\n0.1mcd+42 # linear combinations are allowed to some extent\n1log10 # >= log10 of size of cluster\n99log10+0.0002mcd+1 # combinations like this are allowed\n```\n\n### `-d, --working-dir TEXT`\n\nEntirely optional; specifies where `cm` should store its temporary files.\n\n## Example commands\n\n```bash\n# Leiden, CPM optimization (resolution = 0.1)\n# BUT, the output clusters must satisfy global connectivity >= 1 * log10(n), n the size of cluster\ncm -i graph.tsv -c leiden -g 0.1 -t 1log10 -o leiden_clus.txt\n```\n\n```bash\n# IKC, k = 10\n# BUT, the output clusters must satisfy global connectivity >= 0.1 * mcd, MCD the minimum intra-cluster degree among all nodes\n# we additionally use an existing IKC clustering (ikc_output.csv) as the starting point to be modified\ncm -i graph.tsv -c ikc -k 10 -t 0.1mcd -e ikc_output.csv -o ikc_clus.txt\n```\n\n<!-- ```shell\n# clone the repo, and cd into the repo\npoetry install # install the hm01 script in PATH\nhm01 -i /srv/local/shared/external/dbid/george/exosome_dimensions_wedell_retraction-depleted_jc250-corrected_no_header.tsv -c ikc -k 10 -t 0.1mcd -d working_dir -o clusters.txt\n``` -->\n\n## Format Conversion\n\nThe default output of `cm` contains the entire history of the execution of the algorithm. This format allows preservation of much information, but often times for data analysis, only knowing the clustering *before* modifying the connectivity (i.e., as if just running the base method) and *after* modifying the connectivity is enough. These two sets of clusters can be obtained from `cm` using the specialized tool `cm2universal`:\n\n```bash\n# INPUT_GRAPH is the same INPUT_GRAPH\n# CM_OUTPUT_PREFIX is the same output prefix of `cm`, i.e., `{CM_OUTPUT_PREFIX}.tree.json` and `CM_OUTPUT_PREFIX` are existing files\n# CLUSTERS_OUTPUT_PREFIX is where you want the converted clusters\ncm2universal -g INPUT_GRAPH -i CM_OUTPUT_PREFIX -o CLUSTERS_OUTPUT_PREFIX\n```\n\nTwo files will be generated: `{CLUSTERS_OUTPUT_PREFIX}.original.json` and `{CLUSTERS_OUTPUT_PREFIX}.extant.json`, containing the original and after clusters respectively. The `json` files use the so-called "universal" new-line delimited JSON format, looking like this:\n\n```json\n{"label": "0", "nodes": [0, 3, 7, 9], "connectivity": 1}\n{"label": "46", "nodes": [5765736, 4717164, 14154348, 3144303, 6290035, 3668596, 1571445, 2620022, 4717176], "connectivity": 2}\n```\n\nThese files can be directly parsed (each line is a cluster, `label` the cluster name, `nodes` the node ids of that cluster, `connectivity` the edge connectivity) or can be paired with the data science tool [belinda](https://github.com/illinois-or-research-analytics/belinda).\n\n## Development\n\nWe use [Poetry](https://python-poetry.org/) to manage our progress and follow the Poetry conventions. See below for some example commands:\n\n```bash\npoetry install # install networkit and co\npoetry run pytest # run tests\n```\n\n\n<!-- ## Algorithm\n```\nf : Graph -> List[Cluster]\n# f : Graph -> List[Graph (labeled)]\n```\n\n```python\n\ns - a - rest_of_community\ns, a - rest_of_community\n\ng : Graph -> List[Cluster]\ndef g(graph):\n    ans = []\n    clusters = f(graph)\n    for c in clusters:\n        subgraph = graph.subgraph(c)\n        cut_info = subgraph.cut() # VieCut\n        if cut_info.is_bad(): # connectivity <= parameter\n            subgraph1, subgraph2 = cut_info.cut_graph(subgraph)\n            ans.extend(g(subgraph1))\n            ans.extend(g(subgraph2))\n        else:\n            ans.append(c)\n    return ans\n```\n\n## Id scheme for each cluster\n\n0 .. n clusters\n1a 1b\n1a0 1a1 1a2\n\n5a6b2\n\n## The formats we need for third-party software\nInput formats\n- edgelist (with continuous ids) # Leiden and IKC\n- metis (with continuous ids) # Viecut\n\nOutput formats\n - CSV from IKC\n - Leiden output (node_id cluster_id)\n - Viecut (standard output, and also the binary labels list)\n\n```\n1a3b6.metis\n```\n\n## Our output format\n\nnode_id cluster_id (the most specific cluster a node belongs to)\n\n```\n1 2\n``` -->',
    'author': 'runeblaze',
    'author_email': 'runeblaze@excite.co.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
