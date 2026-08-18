#!/usr/bin/env python3
"""Simple OpenAI LLM caller.

Usage:
  python call_openai.py "Tell me a joke"
  python call_openai.py        # prompts for input

Requires: `openai` and `python-dotenv` packages.
Install with: `pip install openai python-dotenv`
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found. Add it to .env or set the environment variable.")
    sys.exit(1)

try:
    from openai import OpenAI
except Exception:
    print("The 'openai' package is required. Install with: pip install openai")
    raise

client = OpenAI(api_key=OPENAI_API_KEY)


def _extract_content_from_choice(choice) -> str:
    # Try a few common shapes to extract the assistant text
    try:
        # new-style: choice.message.content or choice.message['content']
        msg = getattr(choice, "message", None)
        if msg:
            if isinstance(msg, dict):
                return msg.get("content", "").strip()
            # object with attribute
            return getattr(msg, "content", "").strip()
    except Exception:
        pass
    try:
        # older-style: choice.get('text')
        return choice.get("text", "").strip()
    except Exception:
        pass
    # last-resort string conversion
    return str(choice).strip()


def call_llm(prompt: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
    )
    if not getattr(resp, "choices", None):
        return str(resp)
    return _extract_content_from_choice(resp.choices[0])


def main() -> None:
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter prompt: ")

    print("Prompt:", prompt)
    try:
        out = call_llm(prompt)
        print("\nResponse:\n", out)
    except Exception as exc:
        print("Error calling OpenAI:", exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
