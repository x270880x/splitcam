# SplitCam SEO data

Ahrefs API automation for keyword research, competitor analysis, and content gap detection.

## Setup

1. Put your Ahrefs API token in env:
   ```bash
   echo 'export AHREFS_TOKEN="your_token_here"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. Edit `targets.txt` — list of domains to analyze.
3. Edit `keywords.txt` — list of keywords to research.

## Run

```bash
cd seo
python3 ahrefs.py
```

Options:
- `python3 ahrefs.py --targets-only`   — domain analysis only
- `python3 ahrefs.py --keywords-only`  — keyword research only

## Output

`data/<domain>.json` — DR + organic traffic + top 50 keywords per domain
`data/keywords-research.json` — volume/KD/CPC for our target keywords
`data/_usage.json` — Ahrefs credits consumed

## Files

- `targets.txt` — domains list (one per line, # for comments)
- `keywords.txt` — keywords list (one per line, # for comments)
- `ahrefs.py` — main script
- `data/` — JSON outputs (gitignored)
- `reports/` — Claude-generated analysis markdown (committed)

## Cost

Each domain analysis ~30-50 credits. Keyword research ~1 credit per keyword.
Workspace limit: 100,000/month (Lite plan). Plenty for several full runs.
