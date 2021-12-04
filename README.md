# Inventar

### Build using
- [Rancher desktop](https://rancherdesktop.io/)

### Run & test

```
nerdctl compose -f compose.yml up -d --build
nerdctl exec inventar-app pytest
```
