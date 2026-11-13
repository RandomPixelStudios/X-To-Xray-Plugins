# X To Xray Plugins

Plugins for [X To Xray](https://github.com/RandomPixelStudios/X-To-Xray). Every folder here is one plugin and
appears in the **Plugins** tab of the mod.

**Every developer is responsible for their own plugins, not Random Pixel Studios.**

- [Publish your plugin](publish.md)
- [API reference](docs/api.md)
- [Report a plugin](https://github.com/RandomPixelStudios/X-To-Xray-Plugins/issues/new)

## How it works

- `<id>/modfiles/*.lua` is the plugin, `<id>/info.md` and `<id>/icon.png` are what the game shows.
- Every push to `main` validates all plugins, creates a release `<id>-v<version>` for each new version and
  publishes a signed list that the mod downloads. The mod refuses lists without a valid signature.
- `revoked.json` holds SHA-256 hashes of plugin files that the mod disables everywhere.
