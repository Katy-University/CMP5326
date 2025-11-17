# make_test_wallets.py
# Safe, synthetic testnet wallet files for teaching only.
# No private keys, no seeds, NO REAL FUNDS.

import os
from textwrap import dedent

OUT_DIR = "."  # change if you want a specific folder

# A few example *testnet* addresses (public only) — harmless strings for lab use
TESTNET_ADDRESSES = [
    "mipcBbFg9gMiCh81Kj8tqqdgoZub1ZJRfn",   # legacy-like (example)
    "2N2JD6wb56AfK4tfmM6PwdVmoYk2dCKf4Br",  # P2SH-like
    "tb1qexampletestnetaddress0000000000000" # bech32-like placeholder
]

def make_wallet_dat(path, addresses, size_bytes=64*1024):
    header = dedent("""\
        TESTNET WALLET.DAT PLACEHOLDER
        This file is created for educational lab use only.
        It contains NO private keys or seeds.
        Do NOT use with real funds.
        ---- BEGIN ADDRESSES ----
        """)
    footer = "\n---- END ADDRESSES ----\n"
    body = "\n".join(addresses) + "\n"
    payload = (header + body + footer).encode("utf-8")
    # pad with repeating pattern to reach a plausible size
    pad = b"\x00" * max(0, size_bytes - len(payload))
    with open(path, "wb") as f:
        f.write(payload + pad)
    print(f"Wrote {os.path.abspath(path)} ({os.path.getsize(path)} bytes)")

def make_electrum_json(path, addresses):
    # Minimal Electrum-like JSON with only public addresses & metadata
    import json
    data = {
        "keystore": {
            "type": "watching",
            "addresses": addresses
        },
        "wallet_type": "standard",
        "label": "Testnet Teaching Wallet (no keys)",
        "seed_version": None
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {os.path.abspath(path)} ({os.path.getsize(path)} bytes)")

if __name__ == "__main__":
    out1 = os.path.join(OUT_DIR, "wallet.dat")
    out2 = os.path.join(OUT_DIR, "electrum_testnet_wallet.json")
    make_wallet_dat(out1, TESTNET_ADDRESSES, size_bytes=64*1024)
    make_electrum_json(out2, TESTNET_ADDRESSES)
