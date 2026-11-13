# Publish your plugin

Plugins you add here appear in the **Plugins** tab of [X To Xray](https://github.com/RandomPixelStudios/X-To-Xray).
You need a text editor and a free GitHub account.

> **Every developer is responsible for their own plugins.** Random Pixel Studios checks that a plugin follows the
> rules below, but does not take responsibility for what plugins do.

## 1. Create your folder

The folder name is your plugin id: lowercase letters, digits, `-` and `_`, 2 to 32 characters.

```
my-plugin/
├── modfiles/
│   └── my-plugin.lua   your plugin, exactly one .lua file
├── icon.png            optional: square PNG, 16x16 to 256x256, at most 64 KiB
└── info.md             what X To Xray shows about your plugin
```

## 2. Write the plugin

`modfiles/my-plugin.lua` starts with a header. The `id` must equal the folder name:

```lua
--[[xtoxray
{
  "format": 1,
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "permissions": ["chat"]
}
]]

local mined = 0
xtx.on("block_mined", function(block, x, y, z)
  mined = mined + 1
  xtx.chat("Blocks mined: " .. mined)
end)
```

Everything a plugin can do is described in the [API reference](docs/api.md). Plugins run in a sandbox without
access to files, the network or Minecraft internals. Ask only for the permissions you need: players see them before
they install.

## 3. Write info.md

X To Xray **always** shows the data from `info.md`, not from the Lua header:

```markdown
---
name: My Plugin
developer: YourName
updated: 2026-11-13
summary: One sentence that tells players what the plugin does.
category: Mining, Utility
license: MIT
---

## What it adds

Everything below the second `---` is the long description on the plugin page.

- Lists, **bold** text and `## headings` are shown.
```

| Field | Required | |
|---|---|---|
| `name` | yes | up to 40 characters |
| `developer` | yes | your name, up to 40 characters |
| `updated` | yes | date of your last change, `YYYY-MM-DD` |
| `summary` | yes | up to 200 characters |
| `category` | no | up to 4, separated by commas |
| `license` | no | for example `MIT` |

## 4. Open a pull request

Fork this repository, add your folder and open a pull request. A check validates your plugin automatically. After
the merge, GitHub releases your plugin as `my-plugin-v1.0.0` and it shows up in the game within minutes.

## Updates

Replace the Lua file in `modfiles/`, raise `"version"` in its header and set `updated` in `info.md`. A version that
was released once can never change, so the check fails if you change the code without raising the version.

## Reporting a plugin

If a plugin misbehaves, use **Report this plugin** on its page in the game, or
[open an issue](https://github.com/RandomPixelStudios/X-To-Xray-Plugins/issues/new). Plugins that break the rules
are removed and blocked in the game.
