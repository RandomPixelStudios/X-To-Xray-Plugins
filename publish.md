# Publish your plugin

This guide takes you from an idea to a plugin that everyone can install from the **Plugins** tab of X To Xray. You only need a text editor and a free GitHub account.

## 1. Write the plugin

A plugin is one Lua file. Create `my-plugin.lua`. The file name must match the `id`:

```lua
--[[xtoxray
{
  "format": 1,
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "Tells you how many blocks you mined",
  "author": "YourName",
  "categories": ["Utility"],
  "permissions": ["chat"]
}
]]

local mined = 0

xtx.on("block_mined", function(block, x, y, z)
  mined = mined + 1
  xtx.chat("Blocks mined: " .. mined)
end)
```

Header rules:

- The header must be the very first thing in the file.
- `id`: 2 to 32 characters using `a-z`, `0-9`, `_` and `-`.
- `version`: letters, digits, `.` and `_` only.
- `permissions`: list only what your plugin needs. See the [API list](README.md#api).

## 2. Test it

1. Start Minecraft with X To Xray and open the config menu.
2. Open the **Plugins** tab and drag your `.lua` file onto the window.
3. Open **Installed** and click **Allow**.
4. Try your plugin in a world. Errors appear in the game log.

## 3. Add it with a pull request

A pull request asks the maintainers to add your file to the official list. You can do everything on the GitHub website:

1. Sign in to GitHub and open the [plugins folder](https://github.com/RandomPixelStudios/X-To-Xray-Plugins/tree/main/plugins).
2. Click **Add file**, then **Upload files**. If GitHub asks you to fork the repository, accept.
3. Drag in `my-plugin.lua`. Add nothing else: only `.lua` files are allowed in this folder.
4. Choose **Create a new branch** if GitHub offers it, then click **Propose changes**.
5. Check the summary and click **Create pull request**.
6. Describe what your plugin does and why it needs its permissions, then click **Create pull request** again.

## 4. Wait for the review

- An automatic check validates your file. If it shows a red cross, open **Details**, fix the problem, and upload the file again to the same branch.
- A maintainer reads your code and may ask for changes.
- After the merge, your plugin appears in the Plugins tab of every player once their plugin list refreshes (the next time they start the game).

## 5. Publish an update

1. Change your code and raise `version` in the header.
2. Open your file in the plugins folder, click the pencil icon, and replace the content.
3. Click **Commit changes**, then **Propose changes**, and create a pull request as before.

Players see an **Update** button after the merge. They review the permissions again before updating.

## Rules

Plugins are rejected if they:

- hide what they do or use deliberately unreadable code,
- request permissions they do not need,
- damage worlds or mine blocks without the player expecting it,
- give an advantage on servers that do not allow it,
- copy another author's work without permission.

If a published plugin turns out to be harmful, it is blocked for all players.

## Need help?

[Open an issue](https://github.com/RandomPixelStudios/X-To-Xray-Plugins/issues) and describe your problem.
