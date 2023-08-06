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

class CLIPTextSimilarWords():
    def __init__(self):
        import pickle
        with open(parent_dir + os.path.sep + "clip_similarwords_all.pt", 'rb') as f:
            self.tok_decoder, self.dict = pickle.load(f)

    def __call__(self, key):
        if type(key) == str:
            key += "</w>"
            key = next(k for k, v in self.tok_decoder.items() if v == key)

        return CLIPTextSimilarWordsIter(self, key)


class CLIPTextSimilarWordsIter():
    def __init__(self, sim, key):
        self.sim = sim
        self.key = key
        if key not in sim.dict:
            self.keyi = [].__iter__()
            return
        self.keyi = sim.dict[key].__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        data = next(self.keyi)

        return (self.sim.tok_decoder[self.key].replace("</w>", ""), \
                self.sim.tok_decoder[data[0]].replace("</w>", ""), \
                data[1])

def main():
    if len(sys.argv) < 2:
        print("Usage: clip-similarities [ word_fragment | --all ]")
        exit()

    clipsim = CLIPTextSimilarWords()
    if sys.argv[1] == "--all":
        keys = [sk for sk, s in clipsim.tok_decoder.items()]
    else:
        keys = [sk for sk, s in clipsim.tok_decoder.items() if s.find(sys.argv[1]) >= 0]

    for key in keys:
        for key_token, sim_token, cos_similarity in clipsim(key):
            print("%s -> %s ( cos_similarity: %.2f )"%(key_token, sim_token, cos_similarity))



if __name__ == "__main__": 
    main()

