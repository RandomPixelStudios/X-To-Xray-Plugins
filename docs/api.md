# X To Xray Plugin API

Plugins are single `.lua` files. They run in a sandbox (no files, network or OS access) with a CPU budget per call.
Everything a plugin can do goes through the global table `xtx`. Parts that need a permission only exist when the
plugin declares that permission in its header, so `if xtx.hud then ... end` is a valid check.

```lua
--[[xtoxray
{
  "format": 1,
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "What it does",
  "author": "You",
  "categories": ["Utility"],
  "permissions": ["chat", "hud"]
}
]]
```

## Permissions

| Key | Unlocks |
|---|---|
| `storage` | `xtx.storage` |
| `world.read` | blocks, position, biome, light, world info, world events |
| `world.mine` | `xtx.world.mine` |
| `entities.read` | `xtx.world.entities`, `entity_list`, `players` |
| `render` | `xtx.draw`, event `render` |
| `xray` | `xtx.xray` |
| `chat` | `xtx.chat`, `actionbar`, `title`, `notify` |
| `chat.read` | event `chat_message` |
| `chat.send` | `xtx.send` (1 message per second) |
| `clipboard` | `xtx.copy` |
| `hud` | `xtx.hud`, event `hud` |
| `player.read` | `xtx.player.info`, `inventory`, `effects`, player events |
| `player.control` | `set_look`, `select_slot`, `set_control`, `drop` |
| `input` | `xtx.input` |
| `sound` | `xtx.sound` |
| `options` | `xtx.options` |

## Events: `xtx.on(event, function)`

| Event | Arguments | Permission |
|---|---|---|
| `tick` | – | – |
| `join`, `leave`, `shutdown` | – | – |
| `block_mined` | block id, x, y, z | – |
| `xray_toggle` | active | – |
| `setting_change` | key, value (changed in the settings screen) | – |
| `plugin_message` | channel, payload, from plugin id | – |
| `render` | – | `render` |
| `hud` | – | `hud` |
| `chat_message` | text, `"game"` or `"chat"`; return `false` to hide | `chat.read` |
| `health_change` | new, old | `player.read` |
| `death` | `{x, y, z, dimension}` (nil without `world.read`) | `player.read` |
| `respawn` | – | `player.read` |
| `slot_change` | new, old | `player.read` |
| `level_up` | new, old | `player.read` |
| `food_change` | new, old | `player.read` |
| `held_item_change` | new id, old id | `player.read` |
| `dimension_change` | new, old | `world.read` |
| `biome_change` | new, old | `world.read` |
| `weather_change` | `"clear"`/`"rain"`/`"thunder"` new, old | `world.read` |
| `day_change` | `true` at sunrise, `false` at sunset | `world.read` |

## Limits

A plugin is stopped when it breaks one of these, the game keeps running:

- 5 million steps per call (Lua instructions plus pattern matching steps)
- 128 MiB allocated per call and 64 MiB kept in memory overall
- strings of at most 1 MiB, call depth of at most 400
- `storage`: 1 MiB per file, 16 MiB and 256 files in total

Messages from `plugin_message` can come from any plugin. Never let a message trigger something that needs a
permission (sending chat, mining, moving the player) without checking the sender id.

## Core

| Function | Notes |
|---|---|
| `xtx.log(text)` | game log |
| `xtx.time()` / `xtx.ticks()` / `xtx.fps()` | ms since epoch / ticks since start / current FPS |
| `xtx.screen()` | `"none"`, `"chat"`, `"inventory"`, `"pause"`, `"other"` |
| `xtx.plugin` | `{id, name, version, author, permissions}` |
| `xtx.has_permission(key)` | |
| `xtx.after(ticks, f)`, `xtx.every(ticks, f)`, `xtx.cancel(id)` | timers |
| `xtx.after_seconds(s, f)`, `xtx.every_seconds(s, f)`, `xtx.seconds(s)` | timers in seconds |
| `xtx.once(event, f)` | handler that runs one time |
| `xtx.when(check, f, timeout)` | runs `f(true)` once `check()` is true, `f(false)` on timeout |
| `xtx.throttle(ticks, f)` | wrapped `f` that runs at most once per `ticks` |
| `xtx.command(name, f)` | `/xtx name args` |
| `xtx.subcommands(name, {sub = f, default = f})` | `/xtx name sub args` with usage message |
| `xtx.events.on/emit/off` | events inside your plugin |
| `xtx.broadcast(channel, text)`, `xtx.broadcast_json(channel, table)` | message other plugins |
| `xtx.on_message(channel, f(data, from), as_json)` | receive them (next tick) |
| `xtx.json.encode(v)`, `xtx.json.decode(text)` | |
| `xtx.setting(key)`, `xtx.set_setting(key, value)`, `xtx.setting_ticks(key)` | |

## Settings screen: `xtx.ui`

`toggle(key, label, default)`, `slider(key, label, min, max, default)`, `cycle(key, label, {options}, default)`,
`blocks(key, label, {ids})`, `text(key, label, default)` (max 256 chars), `button(key, label, f)`.

## Helpers: `xtx.util`

`clamp`, `lerp`, `round(v, decimals)`, `distance(x1,y1,z1,x2,y2,z2)`, `distance2d`, `split(s, sep)`, `trim`,
`starts_with`, `ends_with`, `contains(t, v)`, `keys(t)`, `count(t)`, `copy(t)`, `map(t, f)`, `filter(t, f)`,
`short_name(id)`, `pretty_name(id)` ("Diamond Ore"), `format_number(n)` ("1,234"), `format_time(seconds)`,
`format_coords(x, y, z)`, `direction(yaw)` ("North East"), `look_angles(from..., to...)`, `random_choice(t)`.

## Colors: `xtx.color`

Colors are ARGB numbers like `0xFFFF0000`. `rgb(r, g, b, a)`, `hex("#RRGGBB")`, `split(c)`, `with_alpha(c, a)`,
`lerp(c1, c2, t)`, `hsv(h, s, v, a)`, `rainbow(step, speed)`, `health(fraction)` (green to red), and constants
`WHITE BLACK GRAY RED GREEN BLUE YELLOW AQUA PURPLE GOLD SHADOW`.

## Chat and screen (`chat`)

`xtx.chat(text)`, `xtx.actionbar(text)`, `xtx.title(title, subtitle)`, `xtx.notify(title, text)` (toast).
With `chat.send`: `xtx.send(text)` sends a chat message or a `/command`; returns `false` while on cooldown.
With `clipboard`: `xtx.copy(text)`.

## HUD (`hud`)

Basic: `size()`, `text_width(t)`, `text(t, x, y, color, shadow)`, `rect(x1, y1, x2, y2, color)`, `item(id, x, y)`,
`hide(part)`, `show(part)`.
Helpers: `outline(x1, y1, x2, y2, color, thickness)`, `text_centered(t, cx, y, color)`, `text_right(t, right, y, color)`,
`progress(x, y, w, h, value, max, fg, bg)`, `panel(lines, {anchor, x, y, padding, background, border, color})`.
A panel line is a string or `{text, color, item}`; anchors: `top_left`, `top_right`, `bottom_left`, `bottom_right`, `center`.

## World (`world.read`, `entities.read`, `world.mine`)

`block(x, y, z)`, `block_state(x, y, z)` → `{id, air, solid, liquid, hardness, properties}`, `height(x, z)`,
`player()` → x, y, z, `player_block()`, `distance_to(x, y, z)`, `info()` → `{dimension, game_time, day_time, day,
is_day, raining, thundering, singleplayer, server_has_mod, min_y, max_y}`, `light(x, y, z)`, `biome(x, y, z)`,
`looking_at(reach)`, `is_air(x, y, z)`, `each_block(x1, y1, z1, x2, y2, z2, f)`,
`find_blocks(ids, radius ≤ 16, max ≤ 256)` → nearest first `{x, y, z, block, distance}`.
Entities: `entities(radius)`, `entity_list(radius)`, `nearest_entity(radius, kind_or_type)`,
`count_entities(radius, kind_or_type)`, `players()` (tab list names).
Mining: `mine({{x, y, z}, ...}, {silk = "tool"|"always"|"never", durability = 0..10})`.

## Player (`player.read`, `player.control`)

`info()` (health, food, level, xp, held item/count/damage, offhand, position, velocity, flags like `on_ground`,
`in_water`, `flying`...), `inventory()`, `effects()`, `find_item(id)`, `count_item(id)`, `has_effect(id)`.
Control: `set_look(yaw, pitch)`, `look_at(x, y, z)`, `select_slot(0..8)`, `select_item(id)`,
`set_control(name, down)`, `press(name, ticks)`, `drop(all)`.

## Render (`render`)

`box(...)`, `line(...)`, `text(t, x, y, z, color, scale)`, `block(x, y, z, color, on_top)`,
`circle(x, y, z, radius, color, segments)`, `tracer(x, y, z, color)`, `path(points, color)`.

## Storage (`storage`)

`read(name)`, `write(name, text)`, `delete(name)`, `list()`, `exists(name)`, `append(name, line)`,
`read_json(name, fallback)`, `write_json(name, table)`. 1 MiB per file, 16 MiB per plugin.

## Xray, input, sound, options

`xtx.xray`: `active`, `set_active`, `blocks`, `add`, `remove`, `night_vision`, `set_night_vision`,
`render_distance`, `set_render_distance`.
`xtx.input`: `is_down("key.keyboard.g")`, `bind(key, f)`. `xtx.sound.play(id, volume, pitch)`.
`xtx.options.get/set("fov" | "gamma" | "render_distance" | "view_bobbing", value)`.
