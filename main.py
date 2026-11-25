#!/usr/bin/env python3
"""news-image-20261125: sum up 25 November 2026's world news in one image.

Running this entrypoint copies the bundled illustration (entry.png) into
the output directory. It is fully deterministic: no network, no clock,
no randomness, no environment-dependent behaviour beyond the output dir.
"""
import hashlib
import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(src):
        print("error: %s not found next to main.py" % IMAGE_NAME, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if sha256_of(src) != sha256_of(dst):
        print("error: copied image failed integrity check", file=sys.stderr)
        return 1
    print("news-image-20261125: wrote %s (%d bytes, sha256 %s)"
          % (dst, size, sha256_of(dst)))
    print("One image summing up 25 November 2026: Ukraine's sea strike, "
          "Hormuz tensions, the Huawei verdict and CIA cyberattack, and "
          "Thanksgiving in Washington.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
