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

# worked on RTX 3060 VRAM 12GB
import torch
import transformers
import time
from tqdm import tqdm


class CLIPTextToTextSimilarWordsGen(transformers.CLIPTextModel):
    def __init__(self, config: transformers.CLIPTextConfig):
        super().__init__(config)

    @torch.no_grad()
    def forward(self, variant_prompts):
        similarities = torch.empty(0, dtype=torch.half, device="cuda")#torch.cuda.HalfTensor()
        idx = torch.empty(0, dtype=torch.int64, device="cuda")
        tokens = torch.full((64, 77), 49407, dtype=torch.int64, device="cuda")
        tokens[:, 0] = 49406
        variant_embeddings = torch.empty((variant_prompts.shape[0], 77*768), dtype=torch.half, device="cuda")

        for i in tqdm(range(0, variant_prompts.shape[0], 64)):
            tokens[:, 1] = variant_prompts[i:i+64]
            variant_embeddings[i:i+64] = super().forward(tokens)[0].flatten(1)

#        print(variant_embeddings.shape)

        # https://www.h4pz.co/blog/2021/4/2/batch-cosine-similarity-in-pytorch-or-numpy-jax-cupy-etc
        variant_embeddings_norm = torch.linalg.norm(variant_embeddings, dim=1, keepdim=True)
        variant_embeddings_norm2 = torch.linalg.norm(variant_embeddings.T, dim=0, keepdim=True)
#        print(variant_embeddings_norm.shape)
#        print(variant_embeddings_norm2.shape)

        y = torch.matmul(variant_embeddings, variant_embeddings.T)
#        print(y.shape)
        del variant_embeddings

        x = torch.matmul(variant_embeddings_norm, variant_embeddings_norm2)
#        print(x.shape)

        t = (y / x).T # 転置不要のはず
        del y
        del x
        mask = t >= 0.85
        nz = torch.nonzero(mask)
#        print(t[mask].shape) # 閾値 0.85 で torch.Size([1833429])、閾値 0.80 で torch.Size([8399651])
        return (nz, t[mask])

if __name__ == '__main__':
    model_path = "/home/nazo/.cache/huggingface/diffusers/models--CompVis--stable-diffusion-v1-4____/snapshots/a304b1ab1b59dd6c3ba9c40705c29c6de4144096/"
    #model_path = "/home/nazo/.cache/huggingface/diffusers/Anything-V3.0/"
    model_path += "text_encoder/"

    tokenizer = transformers.CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")
    arr = [sk for sk, s in tokenizer.decoder.items() if s[-4:] == "</w>"]
    #arr = [sk for sk, s in tokenizer.decoder.items() if s == "kitty</w>"]
    if len(arr) % 64 != 0:
        arr += [49407] * (64 - (len(arr) % 64)) # padding
    assert(len(arr) % 64 == 0)
    variant_prompts = torch.cuda.LongTensor(arr)

    f = CLIPTextToTextSimilarWordsGen.from_pretrained(model_path).to("cuda").half()
    idx, similarities = f(variant_prompts)
    idx = variant_prompts[idx]
    torch.save((idx, similarities), "clip_similarwords.pt")

#    print(idx)
#    print(similarities)

#    similarities = similarities.detach().cpu().numpy()
#    variant_prompts = variant_prompts.detach().cpu().numpy()
#
#    import regex as re
#    for i, k in enumerate(idx):
#         print("%s :: %s :: cossim: %.2f"%(tokenizer.decoder[variant_prompts[k[0]]], tokenizer.decoder[variant_prompts[k[1]]].replace("</w>", ""), similarities[i]))

