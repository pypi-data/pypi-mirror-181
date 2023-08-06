import os
import sys
from ..base import Inference
from PIL import Image
import torch
from torch import cuda
from .nets.clip_prefix_caption import GPT2Tokenizer, clip, ClipCaptionModel, generate2, generate_beam
from ...checkpoint import PretrainedCheckpoint


class ClipPrefixCaption(Inference):
    pretrained = {
        "Conceptual_captions": PretrainedCheckpoint("clip_prefix_caption.pt",
                                                    gdrive="14pXWwB4Zm82rsDdvbGguLfx9F8aM7ovT"),
        "COCO_captions": PretrainedCheckpoint("coco_clip_prefix_caption.pt",
                                              gdrive="1IdaBtMSvtyzF0ByVaBHtvM0JYSXRExRX")
    }

    def __init__(self,
                 name="Conceptual_captions",
                 use_beam_search=False,
                 device='cuda' if cuda.is_available() else 'cpu'):
        super(ClipPrefixCaption, self).__init__()
        self.device = device
        self.clip_model, self.preprocess = clip.load("ViT-B/32", device=device, jit=False)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        self.prefix_length = 10

        model = ClipCaptionModel(self.prefix_length)
        model.load_state_dict(self.pretrained[name].load(map_location=self.device))
        model = model.eval()
        model = model.to(device)
        self.model = model
        self.use_beam_search = use_beam_search

    def inference(self, image: Image.Image):

        image = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            prefix = self.clip_model.encode_image(image).to(self.device, dtype=torch.float32)
            prefix_embed = self.model.clip_project(prefix).reshape(1, self.prefix_length, -1)
        if self.use_beam_search:
            generated_text_prefix = generate_beam(self.model,
                                                  self.tokenizer,
                                                  embed=prefix_embed)[0]
        else:
            generated_text_prefix = generate2(self.model,
                                              self.tokenizer,
                                              embed=prefix_embed)

        return {
            "text": generated_text_prefix
        }
