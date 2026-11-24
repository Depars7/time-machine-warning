"""Write one funny time-machine warning label to /output/entry.txt.

Standard library only. The file's content is exactly the label's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be a single line of at most 120
characters, so the label is validated before it is written.
"""

import os

LABEL = (
    "WARNING: Do not high-five your past self. "
    "Paradox damage is not covered under warranty."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(label):
    """The bounty gate: one line, 1-120 characters, non-blank."""
    text = label.strip()
    if not text:
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= 120:
        raise ValueError("entry must be 1-120 characters")
    # Exactly one line: no line breaks anywhere in the label.
    if "\n" in label or "\r" in label:
        raise ValueError("entry must be a single line")
    # The written bytes must be the label itself: no padding and no
    # control characters that could slip a second line past the gate.
    if label != text:
        raise ValueError("entry must not have surrounding whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in label):
        raise ValueError("entry must not contain control characters")
    return text


def write_entry(label):
    """Write the label's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(label.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    label = validate(LABEL)
    write_entry(label)


if __name__ == "__main__":
    main()
