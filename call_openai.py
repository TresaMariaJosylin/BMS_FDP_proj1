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
    import openai
except Exception as e:
    print("The 'openai' package is required. Install with: pip install openai")
    raise

openai.api_key = OPENAI_API_KEY


def call_llm(prompt: str) -> str:
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
    )
    # handle common response shapes
    choice = resp.choices[0]
    # new ChatCompletion returns message
    if hasattr(choice, 'message'):
        return choice.message.get('content', '').strip()
    # fallback for older/other shapes
    return choice.get('text', '').strip()


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
