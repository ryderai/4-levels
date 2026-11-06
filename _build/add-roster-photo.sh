#!/bin/bash
# Add one athlete photo to the 4Levels roster.
# Usage (from the site folder):  bash _build/add-roster-photo.sh <slug> "<photo URL>"
# Saves the original in ../4Levels-roster-photos/, then makes assets/img/roster/<slug>.jpg:
# cropped to 4:5 (portrait, like the cards), max 800px wide, JPEG.
set -e
cd "$(dirname "$0")/.."
slug="$1"; url="$2"
[ -n "$slug" ] && [ -n "$url" ] || { echo "usage: add-roster-photo.sh <slug> <url>"; exit 1; }
src=../4Levels-roster-photos; mkdir -p "$src" assets/img/roster
curl -fsSL -o "$src/$slug-original" "$url"
w=$(sips -g pixelWidth  "$src/$slug-original" | awk '/pixelWidth/{print $2}')
h=$(sips -g pixelHeight "$src/$slug-original" | awk '/pixelHeight/{print $2}')
th=$(( w * 5 / 4 ))
if [ "$h" -ge "$th" ]; then ch=$th; cw=$w; else ch=$h; cw=$(( h * 4 / 5 )); fi
sips -s format jpeg -s formatOptions 84 -c "$ch" "$cw" "$src/$slug-original" --out "assets/img/roster/$slug.jpg" >/dev/null
[ "$cw" -gt 800 ] && sips -Z 1000 "assets/img/roster/$slug.jpg" >/dev/null
echo "made assets/img/roster/$slug.jpg from ${w}x${h} (crop ${cw}x${ch})"
