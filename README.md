# Chrome Extension `manifest.json` Dataset
> [!CAUTION]
> In April 2025, Google replaced [the API](https://github.com/bored-engineer/chrome-extensions/blob/a341f00b2ad6c1bcd7cb3002605205459a2736c4/.github/workflows/release.yml#L77) that was used to easily collect the `manifest.json` without downloading the entire CRX. As a result, the last complete dataset including manifests was on [2025-04-15](https://github.com/bored-engineer/chrome-extensions/releases/tag/2025-04-15). The automation continues to run daily collecting the list of all chrome extension IDs but no longer includes manifests.

This repository contains [`manifest.json`](https://developer.chrome.com/extensions/manifest) files (as well as associated store metadata) extracted from Chrome extensions from the [Chrome webstore](https://chrome.google.com/webstore/category/extensions). 

This dataset is [automatically updated](./.github/workflows/release.yml) every day. It's meant to be useful for analysis of the Chrome extension ecosystem, such as what permissions are requested, common Content Security Policies, etc.

This repository was directly inspired by [mandatoryprogrammer/chrome-extension-manifests-dataset](https://github.com/mandatoryprogrammer/chrome-extension-manifests-dataset).
