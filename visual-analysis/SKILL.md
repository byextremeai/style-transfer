---
name: visual-analysis
description: >
  Automates product promotional image generation by analyzing reference image styles
  and applying them to product photos using fal.ai nano-banana-2.
  Use this skill whenever the user wants to: generate product lifestyle/promotional images,
  apply a brand style to product photos, create wearing or in-use shots from a product photo,
  run the image generation pipeline, or analyze reference image styles.
  Trigger on phrases like: "brand DNA", "generate product images", "same style", "promotional photo",
  "lifestyle shot", "product image", "reference style", "visual style", "generate images", "run pipeline".
---

# Product Image Generator

Every run starts fresh — always re-analyze reference images and always overwrite `input/prompts.json`.
Never reuse previous prompts. Do not wait for user confirmation between steps.

> **Visual Analysis Reference**: Read `style-analysis.md` for the complete taxonomy of visual dimensions and prompt keywords.

## Pipeline (run in sequence, automatically)

1. Setup workspace → 2. User adds images → 3. Analyze references → 4. Write prompts.json → 5. Run generate.py

---

### Step 1: Setup workspace

```bash
python .claude/skills/style-transfer/visual-analysis/generate.py
```

Creates `input/references/` and `input/products/` folders automatically.

### Step 2: User adds images

Tell the user:
> "Folders are ready:
> - `input/references/` — add 3 to 5 reference images
> - `input/products/` — add product images
>
> Let me know when ready."

Wait for user confirmation before proceeding.

### Step 3: Analyze reference images

Read each image in `input/references/` visually.

Using `style-analysis.md` as taxonomy, extract per image:
- Camera & lens feel (fisheye, telephoto, phone-shot, etc.)
- Camera angle & shot type (low-angle, overhead, eye-level, etc.)
- Color palette and tones
- Lighting style and quality
- Composition and framing
- Mood, atmosphere, energy
- Subject context and environment


### Step 4: Write prompts.json and immediately run generation

**Always overwrite** `input/prompts.json` — never reuse old prompts.

Identify visual categories directly from reference images (do NOT use fixed categories like lifestyle/editorial/aspirational).
Create one prompt per category found. Each prompt must:
- Mirror the exact scene type from that reference (angle, lens, environment, mood)
- Be specific with keywords from `style-analysis.md`
- Be written as an Edit prompt ("transform into...")
- Always end with: `maintaining the product shape and details exactly`
- Include a short English slug `name` for the filename

Write `input/prompts.json`:

```json
{
  "prompts": [
    {
      "name": "urban-lowangle-fisheye-lifestyle",
      "prompt": "transform into low-angle fisheye street lifestyle photo, person wearing the product in front of urban concrete buildings, golden hour warm light, muted earth tones with film grain, dynamic composition, raw urban energy, maintaining the product shape and details exactly"
    },
    {
      "name": "topdown-urban-editorial",
      "prompt": "transform into overhead top-down editorial shot, product styled on urban surface with minimal props, flat diffused daylight, cool neutral tones, clean negative space composition, understated luxury aesthetic, maintaining the product shape and details exactly"
    }
  ]
}
```

**Immediately after writing prompts.json**, run:

```bash
python .claude/skills/style-transfer/visual-analysis/generate.py
```

After generation, report how many images were generated and where (`output/{product-name}/`).

To open output folder on Windows:
```bash
explorer output
```

## Setup (First Time)

```bash
pip install fal-client python-dotenv
```

Add `FAL_KEY=your-key-here` to `.env` in the project root.

## Troubleshooting

- **No FAL_KEY**: Add `FAL_KEY=...` to `.env`
- **Generation failed**: Check fal.ai API status, verify image format (jpg/png/webp)
- **Style not matching**: Use more consistent reference images, or refine prompts in `input/prompts.json` and re-run
