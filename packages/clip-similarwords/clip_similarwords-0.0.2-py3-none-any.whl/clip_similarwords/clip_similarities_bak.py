# Copyright 2022 Toshimitsu Kimura <lovesyao@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys, os

parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


def main():
    if len(sys.argv) < 2:
        print("Usage: clip-similarities find_word")
        exit()
    from transformers import CLIPTokenizer
    import torch

    tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14") # XXX: should be configurable?
    idx, similarities = torch.load(parent_dir + "/clip_similarities.pt")

    keys = [sk for sk, s in tokenizer.decoder.items() if s.find(sys.argv[1]) >= 0]

    found = torch.zeros(idx.shape[0], dtype=bool, device="cuda")
    for k in keys:
        found |= idx[:, 0] == k
    nz = torch.nonzero(found)

    for i in nz:
        k = idx[i][0] # XXX: why [0]?
        print("%s :: %s :: cossim: %.2f"%(tokenizer.decoder[int(k[0])].replace("</w>", ""), tokenizer.decoder[int(k[1])].replace("</w>", ""), similarities[i].detach().cpu()))

if __name__ == "__main__": 
    main()

# 0m4.881s on RTX 3060 12GB VRAM
