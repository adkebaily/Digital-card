"""Build the encrypted business card for GitHub Pages and its QR code.

profile.json (your details) and secret.key stay on your computer: both are git-ignored.
The page in docs/ only contains the encrypted data; the key is in the QR link after "#",
which browsers never send to the server.

Usage:
    pip install cryptography segno
    python build.py              # rebuild, same key -> the printed QR keeps working
    python build.py --new-key    # revoke: old QR codes stop working, a new one is made
"""
import base64
import json
import os
import shutil
import sys
from pathlib import Path

import segno
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE_URL = "https://adkebaily.github.io/Digital-card/"
ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
KEY_FILE = ROOT / "secret.key"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


if "--new-key" in sys.argv or not KEY_FILE.exists():
    KEY_FILE.write_text(b64url(AESGCM.generate_key(bit_length=128)))
key_txt = KEY_FILE.read_text().strip()
key = base64.urlsafe_b64decode(key_txt + "=" * (-len(key_txt) % 4))

profile = (ROOT / "profile.json").read_text(encoding="utf-8")
json.loads(profile)  # fail early on a typo
iv = os.urandom(12)
payload = b64url(iv + AESGCM(key).encrypt(iv, profile.encode(), None))

DOCS.mkdir(exist_ok=True)
html = (ROOT / "template.html").read_text(encoding="utf-8").replace("__PAYLOAD__", payload)
(DOCS / "index.html").write_text(html, encoding="utf-8")
shutil.copy(ROOT / "template-404.html", DOCS / "404.html")
(DOCS / ".nojekyll").touch()

url = f"{BASE_URL}#k={key_txt}"
qr_dir = ROOT / "qr"
qr_dir.mkdir(exist_ok=True)
qr = segno.make(url, error="h")
qr.save(qr_dir / "qr.svg", scale=10, border=2, dark="#0b0d12", light=None)
qr.save(qr_dir / "qr.png", scale=20, border=2, dark="#0b0d12", light="#ffffff")

print(f"built docs/index.html\ncard link: {url}\nQR code:   qr/qr.svg, qr/qr.png")
