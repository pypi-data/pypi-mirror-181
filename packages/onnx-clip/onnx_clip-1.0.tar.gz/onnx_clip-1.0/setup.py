# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onnx_clip']

package_data = \
{'': ['*'], 'onnx_clip': ['data/*']}

install_requires = \
['ftfy>=6.0.3,<7.0.0',
 'numpy>=1.18.0,<2.0.0',
 'onnxruntime>=1.4.0',
 'opencv-python-headless>=4.0.1,<5.0.0',
 'pillow>=8.4.0,<9.0.0',
 'regex']

setup_kwargs = {
    'name': 'onnx-clip',
    'version': '1.0',
    'description': 'Replicating CLIP without PyTorch dependencies.',
    'long_description': '# onnx_clip\n\n## About\nThe purpose of this repository is to replicate the functionality of [CLIP](https://github.com/openai/CLIP) without needing the\nvarious `PyTorch` dependencies. We do this by utilising a `.onnx` format of the model, a pure `NumPy` version of the tokenizer, \nand an accurate approximation of the [preprocess function.](https://github.com/openai/CLIP/blob/main/clip/clip.py#L79)\nDue to this final approximation, the output logits do\nnot perfectly match those of `CLIP` but are close enough for our purposes.\n\n## git lfs\nThis repository uses Git LFS for the `clip_model.onnx` file. Make sure to do `git lfs install` before cloning.\n\n## Installation\nTo install, run the following in the root of the repository:\n```bash\npip install .\n```\n\n## Usage\n\nAll you need to do is call the `OnnxClip` model class. An example can be seen below.\n\n```python\nfrom onnx_clip import OnnxClip, softmax\nfrom PIL import Image\n\nimage = Image.open("onnx_clip/data/CLIP.png").convert("RGB")\ntext = ["a photo of a man", "a photo of a woman"]\nonnx_model = OnnxClip()\nlogits_per_image, logits_per_text = onnx_model.predict(image, text)\nprobas = softmax(logits_per_image)\n```\n\n## Building & developing from source\n\n**Note**: The following may give timeout errors due to the filesizes. If so, this can be fixed with poetry version 1.1.13 - see [this related issue.](https://github.com/python-poetry/poetry/issues/6009)\n\n### Install, run, build and publish with Poetry\n\nInstall [Poetry](https://python-poetry.org/docs/)\n```\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\n\nTo setup the project and create a virtual environment run the following command from the project\'s root directory.\n```\npoetry install\n```\n\nTo build a source and wheel distribution of the library run the following command from the project\'s root directory.\n```\npoetry build\n```\n\n#### Instructions to publish the build artifacts for project maintainers\nCopy this into your poetry config.toml file (or create a new one).\n```\n[repositories]\n[repositories.onnx_clip]\nurl = "https://gitlab.com/api/v4/projects/41150990/packages/pypi"\n```\nThe file should be located here on MacOs\n```\n~/Library/Application Support/pypoetry/config.toml\n```\nand here on Linux\n```\n~/.config/pypoetry/config.toml\n```\n\nWith this setup you can now publish a package like so\n```\npoetry publish --repository onnx_clip -u <access_token_name> -p <access_token_key>\n```\nWARNING: Do not publish to the public pypi registry, e.g. always use the --repository option.\nNOTE1: You must generate [an access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)\nwith scope set to api.  \nNOTE2: The push will fail if there is already a package with the same version. You can increment the version using [poetry](https://python-poetry.org/docs/cli/#version)\n```\npoetry version\n```\nor by manually changing the version number in pyproject.toml.\n\n# Help\n\nPlease let us know how we can support: [earlyaccess@lakera.ai](mailto:earlyaccess@lakera.ai).\n\n# LICENSE\nSee the [LICENSE](./LICENSE) file in this repository.\n',
    'author': 'Lakera AI',
    'author_email': 'dev@lakera.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
