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

class CLIPTextToTextSimilarWords():
    def __init__(self):
        from transformers import CLIPTokenizer
        global torch
        import torch
        self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14") # XXX: should be configurable?
        self.idx, self.similarities = torch.load(parent_dir + "/clip_similarwords.pt")

    def __call__(self, keys):
        found = torch.zeros(self.idx.shape[0], dtype=bool, device="cuda")
        for k in keys:
            found |= self.idx[:, 0] == k
        nz = torch.nonzero(found)

        return CLIPTextToTextSimilarWordsIter(self, nz)


class CLIPTextToTextSimilarWordsIter():
    def __init__(self, sim, nz):
        self.sim = sim
        self.nzi = nz.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        i = next(self.nzi)
        k = self.sim.idx[i][0] # XXX: why [0]?
        return (self.sim.tokenizer.decoder[int(k[0])].replace("</w>", ""), \
                self.sim.tokenizer.decoder[int(k[1])].replace("</w>", ""), \
                self.sim.similarities[i].detach().cpu())

def main():
    if len(sys.argv) < 2:
        print("Usage: clip-similarities find_word")
        exit()

    clipsim = CLIPTextToTextSimilarWords()
    keys = [sk for sk, s in clipsim.tokenizer.decoder.items() if s.find(sys.argv[1]) >= 0]

    for key_token, sim_token, cos_similarity in clipsim(keys):
        print("%s -> %s ( cos_similarity: %.2f )"%(key_token, sim_token, cos_similarity))



if __name__ == "__main__": 
    main()

# 0m4.881s on RTX 3060 12GB VRAM
