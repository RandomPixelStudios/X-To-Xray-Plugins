# X To Xray Plugins

The official plugin list for [X To Xray](https://github.com/RandomPixelStudios/X-To-Xray). Plugins merged here appear in the **Plugins** tab of the mod.

Plugins are Lua scripts in a sandbox. They have no access to files, network, Java or Minecraft internals, only to the [`xtx` API](docs/api.md). Jar files are refused.

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

**[Read the step-by-step publishing guide](publish.md)**, including how to create a pull request.

## API

**[Read the full API reference](docs/api.md)**: HUD, drawing, player, world, input, sound, game options, Xray, timers, commands, storage and more.

## Limits

Every call has a CPU budget. A plugin that exceeds it, or has 5 errors, is stopped.

## Security

- `main` is signed into `index.json` by GitHub Actions; the mod has the public key built in and refuses unsigned, altered or older lists.
- Review what a plugin does: the sandbox stops access to the computer, but a plugin with `world.mine` can still wreck a world.
- **Bad plugin:** add the SHA-256 of its file to `revoked.json`.
- **Stolen key:** a new key requires a new mod release. Rotate `INDEX_SIGNING_KEY` and update `PUBLIC_KEY` in `PluginRepository.java`.

## Disclaimer

Plugins are created by third parties and are used at your own risk. Random Pixel Studios does not guarantee that any plugin is safe, correct or free of errors, even after review. To the extent permitted by law, Random Pixel Studios is not responsible for damage caused by plugins, including lost worlds, lost data or problems with your computer.
