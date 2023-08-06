# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transformers_inference_toolkit']

package_data = \
{'': ['*']}

install_requires = \
['accelerate>=0.14.0,<0.15.0',
 'deepspeed>=0.7.4,<0.8.0',
 'onnx>=1.12.0,<2.0.0',
 'onnxruntime-gpu>=1.13.1,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'transformers-inference-toolkit',
    'version': '0.1.1',
    'description': 'A collection of helper methods to simplify optimization and inference of Huggingface Transformers-based models',
    'long_description': '# Transformers Inference Toolkit\n[![PyPI](https://img.shields.io/pypi/v/transformers-inference-toolkit)](https://pypi.org/project/transformers-inference-toolkit/)\n[![](https://img.shields.io/badge/%E2%96%BA-%20Changelog-blue)](https://github.com/feratur/transformers-inference-toolkit/blob/main/CHANGELOG.md)\n\n🤗 [Transformers](https://github.com/huggingface/transformers) library provides great API for manipulating pre-trained NLP (as well as CV and Audio-related) models. However, preparing 🤗 Transformers models for use in production usually requires additional effort. The purpose of `transformers-inference-toolkit` is to get rid of boilerplate code and to simplify automatic optimization and inference process of Huggingface Transformers models.\n\n## Installation\nUsing `pip`:\n```bash\npip install transformers-inference-toolkit\n```\n\n## Optimization\nThe original 🤗 Transformers library includes `transformers.onnx` package, which can be used to convert PyTorch or TensorFlow models into [ONNX](https://onnx.ai/) format. This Toolkit extends this functionality by giving the user an opportunity to automatically [optimize ONNX model graph](https://onnxruntime.ai/docs/performance/graph-optimizations.html) - this is similar to what 🤗 [Optimum](https://github.com/huggingface/optimum) library does, but 🤗 Optimum currently has limited support for locally stored pre-trained models as well as for models of less popular architectures (for example, [MPNet](https://github.com/microsoft/MPNet)).\n\nAside from ONNX conversion the Toolkit also supports resaving PyTorch models with half-precision and setting up [DeepSpeed Inference](https://www.deepspeed.ai/tutorials/inference-tutorial/).\n\n### Prerequisite\nThe Toolkit expects your pretrained model (in PyTorch format) and tokenizer to be saved (using `save_pretrained()` method) inside a common parent directory in `model` and `tokenizer` folders respectively. This is how a file structure of `toxic-bert` model should look like:\n```bash\ntoxic-bert\n├── model\n│\xa0\xa0 ├── config.json\n│\xa0\xa0 └── pytorch_model.bin\n└── tokenizer\n    ├── merges.txt\n    ├── special_tokens_map.json\n    ├── tokenizer_config.json\n    └── vocab.json\n```\n\n### How to use\nMost of the popular Transformer model architectures (like BERT and its variations) can be converted with a single command:\n```python\nfrom transformers_inference_toolkit import (\n    Feature,\n    OnnxModelType,\n    OnnxOptimizationLevel,\n    optimizer,\n)\n\noptimizer.pack_onnx(\n    input_path="toxic-bert",\n    output_path="toxic-bert-optimized",\n    feature=Feature.SEQUENCE_CLASSIFICATION,\n    for_gpu=True,\n    fp16=True,\n    optimization_level=OnnxOptimizationLevel.FULL,\n)\n```\nIf your model architecture is not supported out-of-the-box (described [here](https://huggingface.co/docs/transformers/serialization)) you can try writing a custom OnnxConfig class:\n```python\nfrom collections import OrderedDict\nfrom transformers.onnx import OnnxConfig\n\nclass MPNetOnnxConfig(OnnxConfig):\n    @property\n    def default_onnx_opset(self):\n        return 14\n\n    @property\n    def inputs(self):\n        dynamic_axis = {0: "batch", 1: "sequence"}\n        return OrderedDict(\n            [\n                ("input_ids", dynamic_axis),\n                ("attention_mask", dynamic_axis),\n            ]\n        )\n\noptimizer.pack_onnx(\n    input_path="all-mpnet-base-v2",\n    output_path="all-mpnet-base-v2-optimized",\n    feature=Feature.DEFAULT,\n    custom_onnx_config_cls=MPNetOnnxConfig,\n)\n```\nONNX is not the only option, it is also possible to resave the model for future inference simply using PyTorch (`optimizer.pack_transformers()` method, `force_fp16` argument to save in half-precision) or [DeepSpeed Inference](https://www.deepspeed.ai/tutorials/inference-tutorial/) (`optimizer.pack_deepspeed()` method):\n```python\noptimizer.pack_deepspeed(\n    input_path="gpt-neo",\n    output_path="gpt-neo-optimized",\n    feature=Feature.CAUSAL_LM,\n    replace_with_kernel_inject=True,\n    mp_size=1,\n)\n```\nAfter calling `optimizer` methods the model and tokenizer would be saved at `output_path`. The output directory will also contain `metadata.json` file that is necessary for the `Predictor` object (described below) to correctly load the model:\n```bash\ntoxic-bert-optimized\n├── metadata.json\n├── model\n│\xa0\xa0 ├── config.json\n│\xa0\xa0 └── model.onnx\n└── tokenizer\n    ├── special_tokens_map.json\n    ├── tokenizer.json\n    └── tokenizer_config.json\n```\n## Prediction\nAfter model and tokenizer are packaged using one of the `optimizer` methods, it is possible to initialize a `Predictor` object:\n```python\n>>> from transformers_inference_toolkit import Predictor\n>>> \n>>> predictor = Predictor("toxic-bert-optimized", cuda=True)\n>>> print(predictor("I hate this!"))\n{\'logits\': array([[ 0.02940369, -7.0195312 , -4.7890625 , -6.0664062 , -5.625     ,\n        -6.09375   ]], dtype=float32)}\n```\nThe `Predictor` object can be simply called with tokenizer arguments (similar to 🤗 Transformers `pipeline`s, `return_tensors` argument can be omitted, `padding` and `truncation` are `True` by default). For text generation tasks `Predictor.generate()` method (with [generation arguments](https://huggingface.co/docs/transformers/main_classes/text_generation)) can be used:\n```python\n>>> predictor = Predictor("gpt-neo-optimized", cuda=True)\n>>> predictor.generate(\n...     "Tommy: Hi Mark!",\n...     do_sample=True,\n...     top_p=0.9,\n...     num_return_sequences=3,\n...     max_new_tokens=5,\n... )\n[\'Tommy: Hi Mark!\\nMadelyn: Hello\', \'Tommy: Hi Mark! It’s so\', \'Tommy: Hi Mark! How are you?\\n\']\n```\n',
    'author': 'Alexey Burlakov',
    'author_email': 'feraturdev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/feratur/transformers-inference-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
