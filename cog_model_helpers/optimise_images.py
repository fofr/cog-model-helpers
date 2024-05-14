# Usage:
# 1. Create an instance of OptimiseImages with the desired output format and quality.
#    optimiser = OptimiseImages(given_output_format="jpg", given_output_quality=80)
# 2. Call the optimise_image_files method with a list of file paths to optimise the images.
#    optimiser.optimise_image_files(files=[Path("image1.png"), Path("image2.jpg")])

from cog import Input
from PIL import Image


class OptimiseImages:
    def __init__(self, given_output_format: str, given_output_quality: int):
        self.given_output_format = given_output_format
        self.given_output_quality = given_output_quality

    @staticmethod
    def output_format() -> str:
        return Input(
            description="Format of the output images",
            choices=["webp", "jpg", "png"],
            default="webp",
        )

    @staticmethod
    def output_quality() -> int:
        return Input(
            description="Quality of the output images, from 0 to 100. 100 is best quality, 0 is lowest quality.",
            default=80,
            ge=0,
            le=100,
        )

    def optimise_image_files(self, files=[]):
        if self.given_output_quality < 100 or self.given_output_format in [
            "webp",
            "jpg",
        ]:
            optimised_files = []
            for file in files:
                if file.is_file() and file.suffix in [".jpg", ".jpeg", ".png"]:
                    image = Image.open(file)
                    optimised_file_path = file.with_suffix(
                        f".{self.given_output_format}"
                    )
                    image.save(
                        optimised_file_path,
                        quality=self.given_output_quality,
                        optimize=True,
                    )
                    optimised_files.append(optimised_file_path)
                else:
                    optimised_files.append(file)

            files = optimised_files
