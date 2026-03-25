"""
Product Image Generator
-----------------------
Generates product images using style prompts crafted from reference image analysis.

Reference images are analyzed by Claude — only product images are sent to fal.ai.
Prompts must be saved to input/prompts.json before running.

prompts.json format:
  {
    "prompts": [
      {"name": "urban-lowangle-fisheye-lifestyle", "prompt": "..."},
      {"name": "topdown-urban-editorial", "prompt": "..."}
    ]
  }

Output filename format:
  {product}_{timestamp}_{category-name}.png
  e.g. cap_20240315_143022_urban-lowangle-fisheye-lifestyle.png
"""

import os
import sys
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import fal_client

load_dotenv()

BASE_DIR = Path.cwd()
INPUT_DIR = BASE_DIR / "input"
REFERENCES_DIR = INPUT_DIR / "references"
PRODUCTS_DIR = INPUT_DIR / "products"
PROMPTS_FILE = INPUT_DIR / "prompts.json"
OUTPUT_DIR = BASE_DIR / "output"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def setup_workspace():
    for folder in [REFERENCES_DIR, PRODUCTS_DIR, OUTPUT_DIR]:
        if not folder.exists():
            folder.mkdir(parents=True)
            print(f"  Created: {folder.relative_to(BASE_DIR)}")


def load_prompts() -> list[dict]:
    if not PROMPTS_FILE.exists():
        print(f"\nFAIL No prompts found at input/prompts.json")
        print(f"  Run visual analysis first to generate prompts.")
        sys.exit(1)
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    prompts = data.get("prompts", [])
    if not prompts:
        print(f"\nFAIL prompts.json is empty.")
        sys.exit(1)
    print(f"  Loaded {len(prompts)} prompt(s) from input/prompts.json")
    return prompts


def get_images(folder: Path) -> list[Path]:
    return [f for f in folder.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]


def generate_product_images(
    product_path: Path,
    prompts: list[dict],
    output_dir: Path,
    timestamp: str,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    print(f"\n  Uploading: {product_path.name}")
    product_url = fal_client.upload_file(str(product_path))

    for i, entry in enumerate(prompts, 1):
        name = entry.get("name", f"style-{i:02d}")
        prompt = entry.get("prompt", "")
        print(f"  Generating ({i}/{len(prompts)}) {name}...")
        try:
            result = fal_client.run(
                "fal-ai/nano-banana-2/edit",
                arguments={
                    "prompt": prompt,
                    "image_urls": [product_url],
                    "aspect_ratio": "4:5",
                    "resolution": "1K",
                    "num_images": 1,
                },
            )
            image_url = result["images"][0]["url"]
            filename = f"{product_path.stem}_{timestamp}_{name}.png"
            output_path = output_dir / filename
            urllib.request.urlretrieve(image_url, output_path)
            generated.append(output_path)
            print(f"  OK Saved: {output_path.name}")
        except Exception as e:
            print(f"  FAIL ({name}): {e}")

    return generated


def run():
    if not os.getenv("FAL_KEY"):
        print("FAIL FAL_KEY not set. Add it to .env")
        sys.exit(1)

    print("\n[*] Setting up workspace...")
    setup_workspace()

    product_paths = get_images(PRODUCTS_DIR)

    if not product_paths:
        print(f"\nFAIL No product images found in input/products/")
        print(f"  Add product images and run again.")
        sys.exit(1)

    print(f"  Products: {len(product_paths)} image(s)")

    prompts = load_prompts()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    total = len(product_paths)
    print(f"\n[>] Processing {total} product(s)\n" + "-" * 40)

    all_generated = []
    for idx, product in enumerate(product_paths, 1):
        print(f"\n[{idx}/{total}] {product.name}")
        output_subdir = OUTPUT_DIR / product.stem
        generated = generate_product_images(product, prompts, output_subdir, timestamp)
        all_generated.extend(generated)

    print("\n" + "-" * 40)
    print(f"[OK] Done! {len(all_generated)} images generated")
    print(f"   Saved to: output/")


if __name__ == "__main__":
    run()
