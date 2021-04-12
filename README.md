# T5DE

![T5DE Workflow](https://github.com/dhkatz/t5de/actions/workflows/t5de.yml/badge.svg)

A modified IMVU client that unlocks useful features.

**Features**

* Unlocked `*hiresnob` and `*hiresnobg` in shop
* New room filters: 'Non-Empty' and '1 Person'
* Use any product with `*use <id>` command
    - Note: Only other users with modified clients will see clothes
    worn this way. Furniture can be seen by mobile users as well.
* Removed IMVU tracking features
  - Stops IMVU from fingerprinting your device
  - Stops crashes from sending reports to IMVU
* Removed annoying 'Shop Together' upsell ads
* See AP products regardless of status

# Install

Download the latest release from the [Releases]() section.

# Build

You can also build the client yourself by cloning the repository.

**Requirements**

* Python 2.7
* NSIS

**Building**

```
python -m pip install -r requirements.txt
makensis install.nsi
```

**Installing**

Run the generated `T5DE-*.exe`
