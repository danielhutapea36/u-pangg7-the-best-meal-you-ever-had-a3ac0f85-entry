#!/usr/bin/env python3
"""The Best Meal You Ever Had — make.fun entry.

Writes one sentence, the best meal we could remember, to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical output.

The sentence: On the shore of Lake Toba, I ate mie gomak in coconut
milk flecked with andaliman, the noodles steaming against the cold
lake wind, and my lips buzzed for an hour afterwards.

Mie gomak is the Batak thick-noodle dish of the Lake Toba highlands:
spaghetti-like noodles in a coconut-milk broth spiced with andaliman,
the citrusy, numbing Batak pepper. The meal is concrete on purpose —
a named dish, a named place, a texture (the noodles steaming against
cold lake wind) and a sensation that outlasts the bowl (lips buzzing
for an hour). Nothing in it is a stock line: no grandmother's kitchen,
no midnight warung, no fogged glasses, no tin roof, no "chased ever
since". The ending is the proof of the meal: the spice was still
working long after the bowl was empty.
"""

import os

# The sentence is a single constant so the choice stays visible in the
# code: the meal is the sentence itself, one specific memory with one
# specific after-effect, and nothing is assembled around it.
_SENTENCE = (
    "On the shore of Lake Toba, I ate mie gomak in coconut milk flecked "
    "with andaliman, the noodles steaming against the cold lake wind, "
    "and my lips buzzed for an hour afterwards."
)

MAX_SENTENCE_CHARS = 200  # competition ceiling for the single sentence


def build_sentence() -> str:
    """Return the one sentence to enter.

    The result must be exactly one sentence: a stray leading or trailing
    space, a sentence that is only white space, or more than one
    sentence would silently break the entry format, so fail loudly
    instead of writing a malformed file.
    """
    sentence = _SENTENCE
    if not sentence.strip():
        raise ValueError("sentence must not be only white space")
    if sentence != sentence.strip():
        raise ValueError("sentence must not start or end with white space")
    if any(ch in "\n\r" for ch in sentence):
        raise ValueError("sentence must be a single line")
    if "  " in sentence:
        raise ValueError("sentence must not contain two spaces in a row")
    if sentence.count(".") != 1 or not sentence.endswith("."):
        raise ValueError("sentence must be exactly one sentence")
    return sentence


def resolve_output_path() -> str:
    """Return the path of the file the sentence is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the sentence to the output file, with no trailing newline.

    The gate requires 1 to 200 characters of UTF-8 text, so the sentence
    is validated here before it is written: one sentence, not only
    white space, and within the limit. After writing, the file is
    read back and its character count re-checked, so a truncated or
    altered write fails loudly instead of shipping a bad entry.
    """
    sentence = build_sentence()
    if not 1 <= len(sentence) <= MAX_SENTENCE_CHARS:
        raise ValueError("sentence must be 1 to 200 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(sentence)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != sentence:
        raise ValueError("written sentence does not match the built sentence")
    if not 1 <= len(written) <= MAX_SENTENCE_CHARS:
        raise ValueError("written sentence is outside 1 to 200 characters")


if __name__ == "__main__":
    main()
