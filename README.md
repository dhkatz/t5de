# T5DE

![T5DE Workflow](https://github.com/dhkatz/t5de/actions/workflows/t5de.yml/badge.svg)
[![](https://dcbadge.vercel.app/api/server/5zkJuKZVTK?style=flat)](https://discord.gg/5zkJuKZVTK)

A modified IMVU client that unlocks useful features.

**Features**

* Unlocked `*hiresnob` and `*hiresnobg` in shop
* New room filters: 'Non-Empty' and '1 Person'
* Use any product with `*use <id>` command
    - Note: Only other users with modified clients will see clothes
    worn this way. Furniture can be seen by mobile users as well.
* Removed IMVU tracking features
  - Stop IMVU from fingerprinting your device
  - Stop crashes from sending reports to IMVU
* Removed annoying 'Shop Together' upsell ads
* See AP products regardless of status

# Install

Download the latest release from the [Releases](https://github.com/dhkatz/t5de/releases) section.

# Build

You can also build the client yourself by cloning the repository.

**Requirements**

* Python 2.7
* NSIS

**Building**

```
python -m pip install -r requirements.txt
python -m t5de
makensis ./scripts/install.nsi
```

**Installing**

Run the generated `T5DE-*.exe`

**Development**

**Patches**

The client is modified using a patch system. Patches are stored in the `patches` directory.

There are currently three types of patches:

* `interface` - Patches the interface, any HTML, CSS, or JS files which affect the UI
* `python` - Patches the actual client Python code, any Python files which affect the client
* `checksum` - Patches the checksums of the client files, used to bypass the client update system

**Patching**

Writing a patch is as simple as creating a new file in the `patches` directory.

Your patch must inherit from either `InterfacePatch`, `PythonPatch`, or `ChecksumPatch` 
depending on the type of patch you are writing. You may also inherit from `Patch` if you want to create a custom patch type.
Theoretically you could even inherit from multiple patch types, but make sure to call `super()` in the correct order.
