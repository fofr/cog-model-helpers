from typing import Input, List
from PIL import Image
import os
import subprocess
import torch
import numpy as np
import importlib.resources

FEATURE_EXTRACTOR = "./feature-extractor"
SAFETY_CACHE = "./safety-cache"
SAFETY_URL = "https://weights.replicate.delivery/default/sdxl/safety-1.0.tar"


class SafetyChecker:
    def __init__(self):
        package_name = __name__.split(".")[0]  # Get the top-level package name

        safety_cache = importlib.resources.files(package_name) / "safety-cache"
        if not safety_cache.exists():
            with importlib.resources.path(package_name, "safety-cache") as cache_path:
                subprocess.check_call(
                    ["pget", "-xf", SAFETY_URL, str(cache_path)],
                    close_fds=False,
                )

        with importlib.resources.path(
            package_name, "feature-extractor"
        ) as feature_extractor_path:
            from diffusers.pipelines.stable_diffusion.safety_checker import (
                StableDiffusionSafetyChecker,
            )
            from transformers import CLIPImageProcessor

            self.safety_checker = StableDiffusionSafetyChecker.from_pretrained(
                str(safety_cache), torch_dtype=torch.float16
            ).to("cuda")
            self.feature_extractor = CLIPImageProcessor.from_pretrained(
                str(feature_extractor_path)
            )

    def load_image(self, image_path):
        return Image.open(image_path).convert("RGB")

    def run(self, image_paths):
        images = [self.load_image(image_path) for image_path in image_paths]
        safety_checker_input = self.feature_extractor(images, return_tensors="pt").to(
            "cuda"
        )
        np_images = [np.array(val) for val in images]
        _, is_nsfw = self.safety_checker(
            images=np_images,
            clip_input=safety_checker_input.pixel_values.to(torch.float16),
        )

        for i, nsfw in enumerate(is_nsfw):
            if nsfw:
                print(f"NSFW content detected in image {i}")

        if all(is_nsfw):
            raise Exception(
                "NSFW content detected in all outputs. Try running it again, or try a different prompt."
            )

        return is_nsfw


def predict_disable_safety_checker() -> bool:
    return Input(
        description="Disable the safety checker",
        default=False,
    )


def load():
    return SafetyChecker()


def run(safety_checker, images, disable_safety_checker: bool = False):
    if disable_safety_checker:
        return images
    else:
        has_nsfw_content = safety_checker.run(images)
        if any(has_nsfw_content):
            print("Removing NSFW images")
            images = [f for i, f in enumerate(images) if not has_nsfw_content[i]]

        return images
