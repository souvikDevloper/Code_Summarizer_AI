#!/usr/bin/env python3
"""
summarize.py – DeepSeek first, OpenRouter fallback.
"""

import os, sys, subprocess, argparse, requests, time
from dotenv import load_dotenv
load_dotenv()

# ---- Keys & URLs -----------------------------------------------------------
DS_KEY   = os.getenv("DEEPSEEK_API_KEY")
DS_URL   = os.getenv("DEEPSEEK_API_URL",  "https://api.deepseek.com/chat/completions")
OR_KEY   = os.getenv("OPENROUTER_API_KEY")
OR_URL   = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
OR_MODEL = os.getenv("OPENROUTER_MODEL",   "deepseek/deepseek-chat:free")

# ---- Helpers ---------------------------------------------------------------
def _post(url, key, body):
    hdr = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    return requests.post(url, headers=hdr, json=body, timeout=60)

def call_llm(prompt, max_tokens=512):
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a senior code-review assistant."},
            {"role": "user",   "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    # Try DeepSeek
    if DS_KEY:
        r = _post(DS_URL, DS_KEY, body)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        if r.status_code != 402:
            sys.exit(f"❌ DeepSeek error: {r.status_code} – {r.text}")

    # Fallback to OpenRouter
    if OR_KEY:
        body["model"] = OR_MODEL
        r = _post(OR_URL, OR_KEY, body)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        if r.status_code == 402:
            sys.exit("❌ Both DeepSeek and OpenRouter free quotas exhausted.")
        sys.exit(f"❌ OpenRouter error: {r.status_code} – {r.text}")

    sys.exit("❌ No valid API key configured for DeepSeek or OpenRouter.")

def load_diff(patch_path):
    if patch_path:
        return open(patch_path, encoding="utf-8").read()
    return subprocess.run(["git", "diff", "HEAD"], text=True, capture_output=True).stdout

def p_summary(diff, n, tone):
    return f"Summarize the following git diff in {n} bullet points with a {tone} tone:\n\n{diff}"

def p_review(diff, n, depth):
    return f"Provide up to {n} code-review comments ({depth} detail) for this git diff:\n\n{diff}"

# ── Public API for FastAPI ──────────────────────────────────────────────────
def summarize(diff: str, args) -> str:
    """Called by FastAPI /api/summarise"""
    return call_llm(p_summary(diff, args.bullets, args.style), args.max_tokens)

def review(diff: str, args) -> str:
    """Called by FastAPI /api/review"""
    return call_llm(p_review(diff, args.comments, args.depth), args.max_tokens)

# ---- CLI entrypoint -------------------------------------------------------
def main():
    import argparse
    cli = argparse.ArgumentParser(description="DeepSeek/OpenRouter diff assistant")
    cli.add_argument("--max-tokens", type=int, default=512)
    sub = cli.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("summarize")
    s.add_argument("--patch")
    s.add_argument("--bullets", type=int, default=3)
    s.add_argument("--style",
        choices=["concise", "detailed", "casual", "formal"],
        default="concise")

    r = sub.add_parser("review")
    r.add_argument("--patch")
    r.add_argument("--comments", type=int, default=5)
    r.add_argument("--depth",
        choices=["brief", "moderate", "thorough"],
        default="moderate")

    args = cli.parse_args()
    diff = load_diff(getattr(args, "patch", None)).strip()
    if not diff:
        sys.exit("No diff found.")

    if args.cmd == "summarize":
        out = call_llm(p_summary(diff, args.bullets, args.style), args.max_tokens)
    else:
        out = call_llm(p_review(diff, args.comments, args.depth), args.max_tokens)
    print("\n" + out)

if __name__ == "__main__":
    main()
