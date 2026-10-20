# Digital business card

QR-code business card hosted on GitHub Pages (`docs/`).

The page only contains **encrypted** data (AES-GCM). The decryption key is in the QR link after `#k=`:
browsers never send that part to the server, and it is not in this repository. Without the QR code, the page shows "Not found".

## Edit the card
1. Edit `profile.json` (on your computer, git-ignored).
2. `pip install cryptography segno` then `python build.py`
3. Commit + push `docs/`: GitHub Pages updates in about a minute. The QR code stays the same.

## Revoke a QR code
`python build.py --new-key`, push, and use the new QR code from `qr/`. Old QR codes stop working.

Keep `secret.key` and `profile.json` safe: without them you can rebuild the card, but not with the same QR code.
