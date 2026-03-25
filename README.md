# Style Transfer — Product Image Generator

Automate product promotional image generation by analyzing reference image styles and applying them to product photos using fal.ai.

---

## Getting Started

### 1. Install Antigravity

Go to [antigravity.google](https://antigravity.google/) and install Antigravity.

Then open the Extensions panel, search for `Claude Code`, and click **Install**.

---

### 2. Download from GitHub

```
https://github.com/byextremeai/style-transfer
```

Click **Code → Download ZIP** and extract, or clone:

```bash
git clone https://github.com/byextremeai/style-transfer.git
```

---

### 3. Place the Files

Move the extracted `style-transfer` folder into your Claude Code project under `.claude/skills/`:

```
your-project/
└── .claude/
    └── skills/
        └── style-transfer/          ← place it here
            └── visual-analysis/
                ├── SKILL.md
                ├── scripts/
                │   └── generate.py
                └── references/
                    └── style-analysis.md
```

---

### 4. Install Python

If Python is not installed:

1. Go to [python.org](https://python.org) → click **Download Python**
2. During installation, check **"Add Python to PATH"**
3. Restart your terminal after installation

Verify:

```bash
python --version
```

---

### 5. Install Dependencies

Run this in your terminal (any directory):

```bash
pip install fal-client python-dotenv
```

---

### 6. Get a FAL API Key

1. Go to [fal.ai](https://fal.ai) → Sign up
2. Dashboard → **API Keys** → **Create new key**
3. Copy the key
4. Dashboard → **Billing** → Add a card and top up credits

---

### 7. Set Up .env

Create a `.env` file in your project root (same level as the `.claude` folder):

```
FAL_KEY=your-api-key-here
```

> Never commit `.env` to git.

---

## Usage

### 1. Open your project in Antigravity

### 2. Start the skill

Talk to Claude to get started:

> "Generate product images"
> "Create images in the reference style"

### 3. Add your images

Claude will automatically create the input folders. Once ready, add your images:

- `input/references/` — 3 to 5 reference style images
- `input/products/` — your product images

Then let Claude know and it will analyze the references, generate prompts, and run the pipeline automatically.

### 4. View results

Find the generated images in the `output/` folder.

---

## Troubleshooting

- **No FAL_KEY**: Make sure `.env` exists in the project root with `FAL_KEY=...`
- **Generation failed**: Check fal.ai API status and verify image format (jpg / png / webp)
- **Style not matching**: Use more consistent reference images, or ask Claude to regenerate
