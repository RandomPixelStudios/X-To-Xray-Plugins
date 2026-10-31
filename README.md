# X To Xray Plugins

The official plugin list for [X To Xray](https://github.com/RandomPixelStudios/X-To-Xray). Plugins merged here appear in the **Plugins** tab of the mod.

Plugins are Lua scripts in a sandbox. They have no access to files, network, Java or Minecraft internals, only to the `xtx` API below. Jar files are refused.

## Write a plugin

A plugin is one file, `plugins/<id>.lua`, starting with a JSON header:

```lua
--[[xtoxray
{
  "format": 1,
  "id": "mined-counter",
  "name": "Mined Counter",
  "version": "1.0.0",
  "description": "Tells you how many blocks you mined",
  "author": "YourName",
  "categories": ["Utility"],
  "permissions": ["chat"]
}
]]

local mined = 0
xtx.ui.slider("every", "Message Every", 1, 100, 10)

xtx.on("block_mined", function(block, x, y, z)
  mined = mined + 1
  if mined % xtx.setting("every") == 0 then
    xtx.chat("Blocks mined: " .. mined)
  end
end)
```

**[Read the step-by-step publishing guide](PUBLISHING.md)**, including how to create a pull request.

## API

| Function | Permission |
|---|---|
| `xtx.log(text)` | none |
| `xtx.on(event, fn)`: `tick`, `block_mined(block, x, y, z)`, `xray_toggle(active)`, `render` | `render` for `render` |
| `xtx.setting(key)` | none |
| `xtx.ui.toggle(key, label, default)` | none |
| `xtx.ui.slider(key, label, min, max, default)` | none |
| `xtx.ui.cycle(key, label, options, default)` | none |
| `xtx.ui.blocks(key, label, ids)` | none |
| `xtx.chat(text)` (only you see it) | `chat` |
| `xtx.storage.read(name)`, `.write(name, text)`, `.delete(name)` | `storage` |
| `xtx.world.block(x, y, z)`, `xtx.world.player()` | `world.read` |
| `xtx.world.entities(radius)` | `entities.read` |
| `xtx.world.mine({{x=,y=,z=}, ...}, {silk="tool"\|"always"\|"never", durability=n})` | `world.mine` |
| `xtx.draw.box(minX, minY, minZ, maxX, maxY, maxZ, color, onTop)` | `render` |
| `xtx.xray.active()`, `.blocks()`, `.add(id)`, `.remove(id)` | `xray` |

World functions return nothing on servers without the X To Xray server side.

## Limits

Every call has a CPU budget. A plugin that exceeds it, or has 5 errors, is stopped.

## Security

- `main` is signed into `index.json` by GitHub Actions; the mod has the public key built in and refuses unsigned, altered or older lists.
- Review what a plugin does: the sandbox stops access to the computer, but a plugin with `world.mine` can still wreck a world.
- **Bad plugin:** add the SHA-256 of its file to `revoked.json`.
- **Stolen key:** a new key requires a new mod release. Rotate `INDEX_SIGNING_KEY` and update `PUBLIC_KEY` in `PluginRepository.java`.
