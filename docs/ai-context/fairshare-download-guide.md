# Download and Update FairShare Data

## 1. Generate FairShare Export Manually

```powershell
cd packages/data-platform/dats-loader
py -c "from dats_loader.__main__ import check_fairshare; check_fairshare()"
```

This writes `data.json` in the current directory without modifying the triple store.

## 2. Rename the File

```powershell
Rename-Item data.json fairshare-dats-2026-09-24.json
```

## 3. Configure the Loader

The loader expects `fairshare-dats-06-2024.json` by default. Either:

- **Option A**: Rename the new file to `fairshare-dats-06-2024.json`, or
- **Option B**: Set the environment variable `FAIRSHARE_FILE_PATH` to the new filename

## 4. Validation

Before loading, verify that the API still returns the expected fields:

- `name`, `title`, `desc`
- `launchYear`, `updateYear`
- `keywords`, `sector`, `benefits`
- `languages`, `countries`
- `providerName`

## 5. Load into the Triple Store

After export and validation:

```powershell
cd packages/data-platform
docker compose build dats-loader
docker compose up dats-loader
```

## 6. Downstream Updates

> **Important**: After loading, the `recommendation-tool` must be restarted to pick up the updated DATs.

---

*QuantiFarm Switzerland | Data Platform | FairShare Update Guide*
