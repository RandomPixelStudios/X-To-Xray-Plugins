#!/usr/bin/env python3
"""Validates every plugin folder and, with --out, writes index.json. Plugins are never executed here.

Layout of one plugin:
    <id>/modfiles/<anything>.lua   the plugin itself, exactly one .lua file
    <id>/info.md                   name, developer, date, summary and the long description
    <id>/icon.png                  optional, square PNG up to 256x256 and 64 KiB
"""
import argparse, base64, datetime, hashlib, json, os, pathlib, re, struct, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = os.environ.get("GITHUB_REPOSITORY", "RandomPixelStudios/X-To-Xray-Plugins")
NOT_PLUGINS = {".git", ".github", "tools", "docs"}
HEADER_KEYS = {"format", "id", "name", "version", "description", "author", "permissions", "categories"}
PERMISSIONS = {"storage", "world.read", "world.mine", "entities.read", "render", "xray", "chat", "chat.read", "chat.send",
               "clipboard", "hud", "player.read", "player.control", "input", "sound", "options"}
INFO_REQUIRED = {"name", "developer", "updated", "summary"}
INFO_KEYS = INFO_REQUIRED | {"category", "license"}
HEADER = "--[[xtoxray"
MAX_LUA = 256 * 1024
MAX_ICON = 64 * 1024
MAX_DESCRIPTION = 8000


def read_header(path):
    data = path.read_bytes()
    if len(data) > MAX_LUA:
        raise ValueError("Lua file is larger than 256 KiB")
    raw = data.decode("utf-8")  # exact bytes, so the hash matches the released file
    end = raw.find("]]")
    if not raw.startswith(HEADER) or end < 0:
        raise ValueError("Lua file must start with the --[[xtoxray header")
    header = json.loads(raw[len(HEADER):end])
    if header.keys() - HEADER_KEYS or {"format", "id", "name", "version"} - header.keys():
        raise ValueError("missing or unknown header fields")
    if header["format"] != 1:
        raise ValueError("format must be 1")
    if not re.fullmatch(r"[0-9A-Za-z._]{1,32}", header["version"]):
        raise ValueError("version may only contain letters, digits, '.' and '_'")
    unknown = set(header.get("permissions", [])) - PERMISSIONS
    if unknown:
        raise ValueError(f"unknown permission: {', '.join(sorted(unknown))}")
    return raw, header


def read_info(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = re.fullmatch(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not match:
        raise ValueError("info.md must start with a --- block (see README)")
    info = {}
    for line in match.group(1).split("\n"):
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        key = key.strip().lower()
        if not sep or key not in INFO_KEYS:
            raise ValueError(f"info.md: unknown line '{line.strip()}'")
        info[key] = value.strip()
    missing = INFO_REQUIRED - {k for k, v in info.items() if v}
    if missing:
        raise ValueError(f"info.md is missing: {', '.join(sorted(missing))}")
    try:
        datetime.date.fromisoformat(info["updated"])
    except ValueError:
        raise ValueError("info.md: updated must be a date like 2026-11-13")
    for key, limit in (("name", 40), ("developer", 40), ("summary", 200), ("license", 40)):
        if len(info.get(key, "")) > limit:
            raise ValueError(f"info.md: {key} is longer than {limit} characters")
    description = match.group(2).strip()
    if len(description) > MAX_DESCRIPTION:
        raise ValueError(f"info.md: the description is longer than {MAX_DESCRIPTION} characters")
    categories = [c.strip() for c in info.get("category", "").split(",") if c.strip()][:4]
    return {
        "name": info["name"],
        "developer": info["developer"],
        "updated": info["updated"],
        "summary": info["summary"],
        "description": description,
        "categories": categories,
        "license": info.get("license", ""),
    }


def read_icon(path):
    data = path.read_bytes()
    if len(data) > MAX_ICON:
        raise ValueError("icon.png is larger than 64 KiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("icon.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if width != height or not 16 <= width <= 256:
        raise ValueError("icon.png must be square, between 16x16 and 256x256")
    return base64.b64encode(data).decode("ascii")


def validate(folder):
    plugin_id = folder.name
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,31}", plugin_id):
        raise ValueError("folder name must be the plugin id (a-z, 0-9, '-', '_', 2 to 32 characters)")
    allowed = {"modfiles", "info.md", "icon.png"}
    extra = sorted(p.name for p in folder.iterdir() if p.name not in allowed)
    if extra:
        raise ValueError(f"only modfiles/, info.md and icon.png belong here, found: {', '.join(extra)}")
    modfiles = folder / "modfiles"
    files = sorted(modfiles.iterdir()) if modfiles.is_dir() else []
    if len(files) != 1 or files[0].suffix != ".lua" or not files[0].is_file():
        raise ValueError("modfiles/ must contain exactly one .lua file")
    source, header = read_header(files[0])
    if header["id"] != plugin_id:
        raise ValueError(f"the id in the Lua header ('{header['id']}') must equal the folder name")
    if not (folder / "info.md").is_file():
        raise ValueError("info.md is missing")
    details = read_info(folder / "info.md")
    if (folder / "icon.png").exists():
        details["icon"] = read_icon(folder / "icon.png")
    details["version"] = header["version"]
    details["sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    details["source"] = f"https://github.com/{REPO}/tree/main/{plugin_id}"
    details["release"] = f"{plugin_id}-v{header['version']}"
    return plugin_id, source, header, details


def plugin_folders():
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name not in NOT_PLUGINS and not p.name.startswith("."))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="write index.json here")
    parser.add_argument("--releases", help="write a JSON list of releases to create here")
    args = parser.parse_args()
    sources, details, releases, failed = [], {}, [], False
    for folder in plugin_folders():
        try:
            plugin_id, source, header, info = validate(folder)
            sources.append(source)
            details[plugin_id] = info
            lua = next((folder / "modfiles").iterdir())
            releases.append({"id": plugin_id, "version": header["version"], "tag": info["release"], "file": str(lua.relative_to(ROOT)),
                             "asset": f"{plugin_id}-{header['version']}.lua", "name": info["name"], "summary": info["summary"],
                             "sha256": info["sha256"]})
            print(f"OK   {folder.name} {header['version']}")
        except Exception as e:
            print(f"FAIL {folder.name}: {e}")
            failed = True
    revoked = json.loads((ROOT / "revoked.json").read_text())
    if not all(re.fullmatch(r"[0-9a-f]{64}", h) for h in revoked):
        print("FAIL revoked.json: entries must be sha256 hashes")
        failed = True
    if failed:
        sys.exit(1)
    if args.out:
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
        # A timestamp only grows, so clients that remember the last sequence never reject a new index.
        index = {"sequence": int(time.time()), "expires": expires.strftime("%Y-%m-%dT%H:%M:%SZ"), "revoked": revoked,
                 "plugins": sources, "details": details}
        pathlib.Path(args.out).write_text(json.dumps(index, indent=1), encoding="utf-8")
    if args.releases:
        pathlib.Path(args.releases).write_text(json.dumps(releases), encoding="utf-8")


if __name__ == "__main__":
    main()
