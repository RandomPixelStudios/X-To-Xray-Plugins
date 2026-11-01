# Plugin API reference

For X To Xray **2026.31** and newer, on Minecraft 26.1 to 26.3. New to plugins? Start with the [publishing guide](../publish.md).

Everything goes through the global table `xtx`. A function only exists if the plugin lists its permission in the header, so calling it without one fails with `attempt to index nil` or `attempt to call nil`.

## Contents

[Permissions](#permissions) · [Events](#events) · [Core](#core) · [Settings menu](#settings-menu) · [HUD](#hud) · [Drawing in the world](#drawing-in-the-world) · [Chat and screen messages](#chat-and-screen-messages) · [Player](#player) · [World](#world) · [Input](#input) · [Sound](#sound) · [Game options](#game-options) · [Xray](#xray) · [Storage](#storage) · [Limits](#limits) · [What plugins cannot do](#what-plugins-cannot-do)

## Permissions

| Permission | Unlocks |
|---|---|
| `storage` | `xtx.storage` |
| `chat` | `xtx.chat`, `xtx.actionbar`, `xtx.title` |
| `chat.read` | the `chat_message` event |
| `hud` | `xtx.hud`, the `hud` event |
| `render` | `xtx.draw`, the `render` event |
| `player.read` | `xtx.player.info`, `xtx.player.inventory` |
| `player.control` | `xtx.player.set_look`, `.select_slot`, `.set_control` |
| `world.read` | `xtx.world.block`, `.player`, `.info`, `.light`, `.biome`, `.looking_at` |
| `world.mine` | `xtx.world.mine` |
| `entities.read` | `xtx.world.entities`, `.entity_list` |
| `input` | `xtx.input` |
| `sound` | `xtx.sound` |
| `options` | `xtx.options` |
| `xray` | `xtx.xray` |

## Events

Register with `xtx.on(event, function)`.

| Event | Arguments | Notes |
|---|---|---|
| `tick` | none | 20 times per second, also in menus |
| `block_mined` | `block, x, y, z` | You broke a block. Not fired for blocks broken by `xtx.world.mine` |
| `xray_toggle` | `active` | |
| `hud` | none | Every frame. The only place where `xtx.hud` drawing works |
| `render` | none | Every frame. Use `xtx.draw` here |
| `join` / `leave` | none | Entering or leaving a world or server |
| `shutdown` | none | The game closes or the plugin is stopped. Save your data here |
| `chat_message` | `text, kind` | `kind` is `"chat"` or `"game"`. Return `false` to hide the message. Needs `chat.read` |

## Core

No permission needed.

| Function | Description |
|---|---|
| `xtx.log(text)` | Writes to the game log |
| `xtx.after(ticks, fn)` | Runs `fn` once. Returns a timer id |
| `xtx.every(ticks, fn)` | Runs `fn` repeatedly. Returns a timer id |
| `xtx.cancel(id)` | Stops a timer |
| `xtx.command(name, fn)` | Adds `/xtx <name> <arguments>`. `fn` receives the arguments as one string. `/xtx` alone lists all commands |
| `xtx.time()` | Current time in milliseconds |
| `xtx.json.encode(value)` | Table to JSON text |
| `xtx.json.decode(text)` | JSON text to table |

Lua's `string`, `table`, `math` and `bit32` libraries are available.

## Settings menu

Each widget appears in the plugin's own tab of the config menu. Values are saved for you.

| Function | Description |
|---|---|
| `xtx.ui.toggle(key, label, default)` | On or off |
| `xtx.ui.slider(key, label, min, max, default)` | Whole numbers |
| `xtx.ui.cycle(key, label, options, default)` | Choose one of a list |
| `xtx.ui.blocks(key, label, ids)` | Block list |
| `xtx.setting(key)` | Reads a value |
| `xtx.set_setting(key, value)` | Changes a value |

## HUD

Permission: `hud`. Colors are `0xAARRGGBB`; an alpha of `00` is invisible.

| Function | Description |
|---|---|
| `xtx.hud.text(text, x, y, color, shadow)` | Draws text, at most 80 characters |
| `xtx.hud.rect(x1, y1, x2, y2, color)` | Draws a filled rectangle |
| `xtx.hud.item(id, x, y)` | Draws an item such as `"minecraft:diamond"` |
| `xtx.hud.size()` | Returns screen width and height |
| `xtx.hud.text_width(text)` | Width of a text |
| `xtx.hud.hide(part)` / `xtx.hud.show(part)` | Hides or restores a vanilla part |

Parts: `hotbar`, `health`, `armor`, `food`, `air`, `mount_health`, `experience_bar`, `experience_level`, `crosshair`, `effects`, `boss_bar`, `scoreboard`, `chat`, `player_list`, `subtitles`, `title`, `overlay_message`, `held_item_tooltip`.

```lua
xtx.hud.hide("hotbar")
xtx.on("hud", function()
  xtx.hud.text("Hello!", 5, 5, 0xFFFFD700)
end)
```

## Drawing in the world

Permission: `render`. Call inside the `render` event. Up to 4096 shapes per frame.

| Function | Description |
|---|---|
| `xtx.draw.box(minX, minY, minZ, maxX, maxY, maxZ, color, onTop)` | Box outline |
| `xtx.draw.line(x1, y1, z1, x2, y2, z2, color, width)` | Line |
| `xtx.draw.text(text, x, y, z, color, scale)` | Floating text above a block position |

## Chat and screen messages

Only you see these. Plugins cannot send chat messages or commands to a server.

| Function | Permission |
|---|---|
| `xtx.chat(text)` | `chat` |
| `xtx.actionbar(text)` | `chat` |
| `xtx.title(title, subtitle)` | `chat` |

## Player

| Function | Permission | Description |
|---|---|---|
| `xtx.player.info()` | `player.read` | Table with `name`, `health`, `max_health`, `armor`, `food`, `saturation`, `air`, `level`, `xp_progress`, `selected_slot`, `held_item`, `on_ground`, `sneaking`, `sprinting`, `creative`, `spectator`. Also `x`, `y`, `z`, `yaw`, `pitch` where world access is allowed |
| `xtx.player.inventory()` | `player.read` | List of `{slot, id, count, damage, max_damage}` |
| `xtx.player.set_look(yaw, pitch)` | `player.control` | Turns your view |
| `xtx.player.select_slot(slot)` | `player.control` | Hotbar slot 0 to 8 |
| `xtx.player.set_control(name, down)` | `player.control` | `forward`, `back`, `left`, `right`, `jump`, `sneak`, `sprint`, `attack`, `use`. Does nothing while a menu is open. Released when the plugin stops |

## World

World functions return nothing on servers without the X To Xray server side.

| Function | Permission | Returns |
|---|---|---|
| `xtx.world.block(x, y, z)` | `world.read` | Block id |
| `xtx.world.player()` | `world.read` | `x, y, z` |
| `xtx.world.info()` | `world.read` | `{dimension, game_time, raining, thundering}` |
| `xtx.world.light(x, y, z)` | `world.read` | Light level |
| `xtx.world.biome(x, y, z)` | `world.read` | Biome id |
| `xtx.world.looking_at(reach)` | `world.read` | `{block, x, y, z, face}` or nil. Reach is 5 by default, at most 128 |
| `xtx.world.entities(radius)` | `entities.read` | List of `{kind, min_x, min_y, min_z, max_x, max_y, max_z}` |
| `xtx.world.entity_list(radius)` | `entities.read` | List of `{id, type, kind, name, x, y, z, distance, health, max_health}`. Radius is at most 256 |
| `xtx.world.mine(blocks, options)` | `world.mine` | Breaks `{{x=,y=,z=}, ...}`, at most 1024. Options: `silk` is `"tool"`, `"always"` or `"never"`; `durability` is 0 to 10 per extra block |

`kind` is `player`, `hostile`, `friendly` or `other`.

## Input

Permission: `input`. Key names look like `key.keyboard.h`. Keys always read as not pressed while a menu or the chat is open, so plugins cannot read what you type.

| Function | Description |
|---|---|
| `xtx.input.is_down(key)` | Whether the key is held |
| `xtx.input.bind(key, fn)` | Runs `fn` each time the key is pressed |

## Sound

Permission: `sound`.

`xtx.sound.play(id, volume, pitch)` plays a sound such as `"minecraft:ui.button.click"`. Volume is 0 to 1, pitch is 0.5 to 2.

## Game options

Permission: `options`.

`xtx.options.get(name)` and `xtx.options.set(name, value)` work with `fov`, `gamma`, `render_distance` and `view_bobbing`.

## Xray

Permission: `xray`.

| Function | Description |
|---|---|
| `xtx.xray.active()` / `.set_active(on)` | Reads or switches Xray. Refused on servers without the server side |
| `xtx.xray.blocks()` | Whitelist as a list of ids |
| `xtx.xray.add(id)` / `.remove(id)` | Changes the whitelist |
| `xtx.xray.night_vision()` / `.set_night_vision(on)` | Night vision setting |
| `xtx.xray.render_distance()` / `.set_render_distance(n)` | Xray distance, 1 to 64 |

## Storage

Permission: `storage`. Private text files for your plugin, up to 1 MiB each and 16 MiB in total.

`xtx.storage.read(name)`, `xtx.storage.write(name, text)`, `xtx.storage.delete(name)`. Names cannot contain paths.

## Limits

- Every call has a CPU budget. A plugin that exceeds it, or has 5 errors, is stopped.
- 256 timers, 64 commands, 64 key binds, 32 settings.
- 4096 HUD calls per frame.
- Text you display is cut to 80 characters and formatting codes are removed.

## What plugins cannot do

Plugins cannot access files outside their storage, the network, Java or Minecraft internals. They cannot send chat messages or commands to servers, read keys while you type, or add new blocks, items or menus. This is deliberate: it is what keeps plugins from being able to harm your computer or your accounts.
