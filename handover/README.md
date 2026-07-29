# Codex Conversation Handover

`codex_chat_2026-07-29_019fa9b0.tar.gpg` is an AES-256-encrypted snapshot of the Codex session used for the FBFM paper. It contains only the session JSONL at its original relative path under `~/.codex`; no authentication files are included.

The passphrase is transferred separately and must not be committed to this repository.

## Integrity

- Encrypted archive SHA-256: `8251eca74fb441672dfbc67bda53f022ae967889e35e330490973dbbdde7845b`
- Decrypted session SHA-256: `5c0f7497685950343475422e877d5008d9c5ccbeb5a0eed560a6ab5a07d341e6`

## Restore

From the repository root on the destination machine:

```bash
mkdir -p "$HOME/.codex"
gpg --decrypt handover/codex_chat_2026-07-29_019fa9b0.tar.gpg \
  | tar -xvf - -C "$HOME/.codex"
```

Enter the separately supplied passphrase when prompted. The restored session is placed under `~/.codex/sessions/2026/07/29/`.
