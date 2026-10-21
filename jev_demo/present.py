import os
import sys
import time


def act(number, title):
    print(f"\n{'=' * 72}\nACT {number}: {title}\n{'=' * 72}")


def timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


def pause():
    """Wait for Enter when presenting live. Skipped with DEMO_NOPAUSE=1 or when there is no terminal."""
    if os.environ.get("DEMO_NOPAUSE") == "1" or not sys.stdin.isatty():
        return
    input("\nPress Enter for the next act...")
