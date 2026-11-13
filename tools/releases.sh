#!/usr/bin/env bash
# Usage: releases.sh check|publish releases.json
# Every plugin version gets its own GitHub release "<id>-v<version>" with the Lua file attached.
# A version that was released once can never change: new code needs a new version in the Lua header.
set -euo pipefail
mode="$1"
list="$2"
tmp="$(mktemp -d)"

python3 -c 'import json,sys
for r in json.load(open(sys.argv[1])):
    print("\t".join([r["id"], r["version"], r["tag"], r["file"], r["asset"], r["name"], r["summary"]]))' "$list" |
while IFS=$'\t' read -r id version tag file asset name summary; do
  if gh release view "$tag" >/dev/null 2>&1; then
    rm -f "$tmp/existing"
    gh release download "$tag" --pattern "$asset" --output "$tmp/existing"
    if [ "$(sha256sum < "$tmp/existing")" != "$(sha256sum < "$file")" ]; then
      echo "::error file=$file::$id $version was already released with different code. Raise \"version\" in the Lua header."
      exit 1
    fi
    echo "unchanged $tag"
  elif [ "$mode" = publish ]; then
    cp "$file" "$tmp/$asset"
    notes="$summary"$'\n\n'"Details: https://github.com/$GITHUB_REPOSITORY/tree/main/$id"
    gh release create "$tag" "$tmp/$asset" --title "$name $version" --notes "$notes" --target "$GITHUB_SHA"
    echo "released $tag"
  else
    echo "new release on merge: $tag"
  fi
done
