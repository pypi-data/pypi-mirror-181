The clip_similarwords is the implementation of finding similar 1-token words of OpenAI's [CLIP](https://github.com/openai/CLIP) in less than one second. 

OpenAI's CLIP uses text-image similarities so its text-text similarities may also be text's typical image similarities unlike [WordNet](https://en.wikipedia.org/wiki/WordNet) or other synonym dictionaries.

Note that, for speed and storage reason (PyPI is limited to 60MB), the words composed by 2 or more tokens are not supported. 

Installation
============
clip_similarwords is easily installable via pip command:
```bash
pip install clip_similarwords
```
or
```bash
pip install git+https://github.com/nazodane/clip_similarwords.git
```

Usage of the command
====================
```bash
~/.local/bin/clip-similarwords [ word_fragment | --all ]
```

Usage of the module
===================
```python
from clip_similarwords import CLIPTextSimilarWords
clipsim = CLIPTextSimilarWords()
for key_token, sim_token, cos_similarity in clipsim("cat"):
    print("%s -> %s ( cos_similarity: %.2f )"%(key_token, sim_token, cos_similarity))
```

Requirements for model uses
===========================
* Linux (should also works on other environmets)

no PyTorch nor CUDA are required.

Requirements for model generation
=================================
* Linux
* Python 3.10 or later
* PyTorch 1.13 or later
* CUDA 11.7 or later
* DRAM 16GB or higher
* RTX 3060 12GB or higher

The patches and informations on other enviroments are surely welcome!

License
=======
The codes are under MIT License. The model was converted under Japanese law.
