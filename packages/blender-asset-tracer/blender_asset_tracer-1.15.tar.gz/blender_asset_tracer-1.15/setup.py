# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blender_asset_tracer',
 'blender_asset_tracer.blendfile',
 'blender_asset_tracer.cli',
 'blender_asset_tracer.pack',
 'blender_asset_tracer.pack.shaman',
 'blender_asset_tracer.trace']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.11,<3.0']

extras_require = \
{'s3': ['boto3>=1.9,<2.0'], 'zstandard': ['zstandard>=0.15,<0.16']}

entry_points = \
{'console_scripts': ['bat = blender_asset_tracer.cli:cli_main']}

setup_kwargs = {
    'name': 'blender-asset-tracer',
    'version': '1.15',
    'description': 'BAT parses Blend files and produces dependency information. After installation run `bat --help`',
    'long_description': "# Blender Asset Tracer BAT🦇\n\nScript to manage assets with Blender.\n\nBlender Asset Tracer, a.k.a. BAT🦇, is the replacement of\n[BAM](https://developer.blender.org/diffusion/BAM/) and\n[blender-file](https://developer.blender.org/source/blender-file/)\n\nDevelopment is driven by choices explained in [T54125](https://developer.blender.org/T54125).\n\n## Setting up development environment\n\n```\npython3.9 -m venv .venv\n. ./.venv/bin/activate\npip install -U pip\npip install poetry black\npoetry install\nmypy --install-types\n```\n\n\n## Uploading to S3-compatible storage\n\nBAT Pack supports uploading to S3-compatible storage. This requires a credentials file in\n`~/.aws/credentials`. Replace the all-capital words to suit your situation.\n\n    [ENDPOINT]\n    aws_access_key_id = YOUR_ACCESS_KEY_ID\n    aws_secret_access_key = YOUR_SECRET\n\nYou can then send a BAT Pack to the storage using a target `s3:/ENDPOINT/bucketname/path-in-bucket`,\nfor example:\n\n    bat pack my_blendfile.blend s3:/storage.service.cloud/jobs/awesome_work\n\nThis will upload the blend file and its dependencies to `awesome_work/my_blendfile.blend` in\nthe `jobs` bucket.\n\n\n## Paths\n\nThere are two object types used to represent file paths. Those are strictly separated.\n\n1. `bpathlib.BlendPath` represents a path as stored in a blend file. It consists of bytes, and is\n   blendfile-relative when it starts with `//`. It can represent any path from any OS Blender\n   supports, and as such should be used carefully.\n2. `pathlib.Path` represents an actual path, possibly on the local filesystem of the computer\n   running BAT. Any filesystem operation (such as checking whether it exists) must be done using a\n   `pathlib.Path`.\n\nWhen it is necessary to interpret a `bpathlib.BlendPath` as a real path instead of a sequence of\nbytes, BAT first attempts to decode it as UTF-8. If that fails, the local filesystem encoding is\nused. The latter is also no guarantee of correctness, though.\n\n\n## Type checking\n\nThe code statically type-checked with [mypy](http://mypy-lang.org/).\n\nMypy likes to see the return type of `__init__` methods explicitly declared as `None`. Until issue\n[#604](https://github.com/python/mypy/issues/604) is resolved, we just do this in our code too.\n\n\n## Code Example\n\nBAT can be used as a Python library to inspect the contents of blend files, without having to\nopen Blender itself. Here is an example showing how to determine the render engine used:\n\n    #!/usr/bin/env python3.7\n    import json\n    import sys\n    from pathlib import Path\n\n    from blender_asset_tracer import blendfile\n    from blender_asset_tracer.blendfile import iterators\n\n    if len(sys.argv) != 2:\n        print(f'Usage: {sys.argv[0]} somefile.blend', file=sys.stderr)\n        sys.exit(1)\n\n    bf_path = Path(sys.argv[1])\n    bf = blendfile.open_cached(bf_path)\n\n    # Get the first window manager (there is probably exactly one).\n    window_managers = bf.find_blocks_from_code(b'WM')\n    assert window_managers, 'The Blend file has no window manager'\n    window_manager = window_managers[0]\n\n    # Get the scene from the first window.\n    windows = window_manager.get_pointer((b'windows', b'first'))\n    for window in iterators.listbase(windows):\n        scene = window.get_pointer(b'scene')\n        break\n\n    # BAT can only return simple values, so it can't return the embedded\n    # struct 'r'. 'r.engine' is a simple string, though.\n    engine = scene[b'r', b'engine'].decode('utf8')\n    xsch = scene[b'r', b'xsch']\n    ysch = scene[b'r', b'ysch']\n    size = scene[b'r', b'size'] / 100.0\n\n    render_info = {\n        'engine': engine,\n        'frame_pixels': {\n            'x': int(xsch * size),\n            'y': int(ysch * size),\n        },\n    }\n\n    json.dump(render_info, sys.stdout, indent=4, sort_keys=True)\n    print()\n\nTo understand the naming of the properties, look at Blender's `DNA_xxxx.h` files with struct\ndefinitions. It is those names that are accessed via `blender_asset_tracer.blendfile`. The\nmapping to the names accessible in Blender's Python interface can be found in the `rna_yyyy.c`\nfiles.\n\n\n## Code Guidelines\n\nThis section documents some guidelines for the code in BAT.\n\n### Avoiding Late Imports\n\nAll imports should be done at the top level of the file, and not inside\nfunctions. The goal is to ensure that, once imported, a (sub)module of BAT can\nbe used without having to import more parts of BAT.\n\nThis requirement helps to keep Blender add-ons separated, as an add-on can\nimport the modules of BAT it needs, then remove them from `sys.modules` and\n`sys.path` so that other add-ons don't see them. This should reduce problems\nwith various add-ons shipping different versions of BAT.\n\n## Publishing a New Release\n\nFor uploading packages to PyPi, an API key is required; username+password will\nnot work.\n\nFirst, generate an API token at https://pypi.org/manage/account/token/. Then,\nuse this token when publishing instead of your username and password.\n\nAs username, use `__token__`.\nAs password, use the token itself, including the `pypi-` prefix.\n\nSee https://pypi.org/help/#apitoken for help using API tokens to publish. This\nis what I have in `~/.pypirc`:\n\n```\n[distutils]\nindex-servers =\n    bat\n\n# Use `twine upload -r bat` to upload with this token.\n[bat]\n  repository = https://upload.pypi.org/legacy/\n  username = __token__\n  password = pypi-abc-123-blablabla\n```\n\n```\n. ./.venv/bin/activate\npip install twine\n\npoetry build\ntwine check dist/blender_asset_tracer-1.15.tar.gz dist/blender_asset_tracer-1.15-*.whl\ntwine upload -r bat dist/blender_asset_tracer-1.15.tar.gz dist/blender_asset_tracer-1.15-*.whl\n```\n",
    'author': 'Sybren A. Stüvel',
    'author_email': 'sybren@blender.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://developer.blender.org/project/profile/79/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
