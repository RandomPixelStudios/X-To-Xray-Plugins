#!/usr/bin/env python3
"""Validates plugins/*.lua and, with --out, writes index.json. Plugins are never executed here."""
import argparse, datetime, json, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYS = {"format", "id", "name", "version", "description", "author", "permissions", "categories"}
PERMISSIONS = {"storage", "world.read", "world.mine", "entities.read", "render", "xray", "chat"}
HEADER = "--[[xtoxray"
MAX_BYTES = 256 * 1024


def validate(path):
    raw = path.read_text(encoding="utf-8")
    if len(raw.encode("utf-8")) > MAX_BYTES:
        raise ValueError("larger than 256 KiB")
    end = raw.find("]]")
    if not raw.startswith(HEADER) or end < 0:
        raise ValueError("missing plugin header")
    m = json.loads(raw[len(HEADER):end])
    if m.keys() - KEYS or {"format", "id", "name", "version"} - m.keys():
        raise ValueError("missing or unknown header fields")
    if m["format"] != 1:
        raise ValueError("format must be 1")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,31}", m["id"]) or path.stem != m["id"]:
        raise ValueError("id is invalid or differs from the file name")
    if not re.fullmatch(r"[0-9A-Za-z._]{1,32}", m["version"]):
        raise ValueError("version may only contain letters, digits, '.' and '_'")
    if set(m.get("permissions", [])) - PERMISSIONS:
        raise ValueError("unknown permission")
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    args = parser.parse_args()
    plugins, failed = [], False
    for path in (ROOT / "plugins").iterdir():
        if path.suffix != ".lua":
            print(f"FAIL {path.name}: only .lua files are allowed")
            failed = True
    for path in sorted((ROOT / "plugins").glob("*.lua")):
        try:
            plugins.append(validate(path))
            print(f"OK   {path.name}")
        except Exception as e:
            print(f"FAIL {path.name}: {e}")
            failed = True
    revoked = json.loads((ROOT / "revoked.json").read_text())
    if not all(re.fullmatch(r"[0-9a-f]{64}", h) for h in revoked):
        print("FAIL revoked.json: entries must be sha256 hashes")
        failed = True
    if failed:
        sys.exit(1)
    if args.out:
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
        index = {"sequence": int(os.environ["GITHUB_RUN_NUMBER"]), "expires": expires.strftime("%Y-%m-%dT%H:%M:%SZ"), "revoked": revoked, "plugins": plugins}
        pathlib.Path(args.out).write_text(json.dumps(index, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
