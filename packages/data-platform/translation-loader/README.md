# Translation loader

Pre-translates the free-text fields of DATs (name, title, description, keywords,
sectors, benefits, cost structure, digital form, functionalities) into German,
French and Italian using the **DeepL API**, and stores the results as
language-tagged literals in their own graph:
`https://quantifarm.eu/graphs/dats-translations`.

It also pre-translates the small, repeating controlled vocabulary used in testcase
graphs (indicator/parameter names, product types) into
`https://quantifarm.eu/graphs/testcase-translations`. Unlike DAT free text, this
vocabulary is tiny (a few dozen unique values, even though it repeats across
hundreds of testcase/parcel/year combinations), so it's cheap to translate and runs
automatically alongside the DAT job (unless `TRANSLATE_ONLY_DAT` is set, in which
case it's skipped to keep single-DAT test runs focused).

This replaces translating DAT fields on the fly at request time (as
`packages/recommendation-tool/src/translation.py` used to do with MyMemory/Google
Translate): the recommendation-tool can simply look up the pre-computed
`@de`/`@fr`/`@it` literal for a given subject/predicate instead.

## Incremental behaviour

Every run:
1. Reads the current translatable literals from `https://quantifarm.eu/graphs/dats`.
2. Reads the existing translations already stored in
   `https://quantifarm.eu/graphs/dats-translations`.
3. Only translates (subject, predicate, language) combinations that are **not yet**
   present in the translations graph, then merges the new triples into the graph
   before writing it back.

So re-running this after `dats-loader` picked up new DATs only translates the new
DATs (or newly added fields) - it never re-translates (and never re-spends DeepL
quota on) anything already translated.

## Environment variables

| Variable              | Required | Description                                                                 |
| ---------------------- | -------- | ---------------------------------------------------------------------------- |
| `TRIPLE_STORE_ENDPOINT` | no       | Base URL of the Fuseki store (default `http://localhost:3030`)              |
| `DEEPL_API_KEY`         | yes*     | DeepL API key. *Not required when `DRY_RUN=true`.                           |
| `TARGET_LANGUAGES`      | no       | Comma-separated target languages (default `de,fr,it`)                       |
| `TRANSLATE_ONLY_DAT`    | no       | Restrict the run to a single DAT: bare slug (e.g. `gaiasense`) or full URI. |
| `DRY_RUN`               | no       | If `true`: only logs how many literals would be translated, no API calls, no writes. |

## Running this (outside of Docker)

(assumes you are in a bash shell, such as in Linux, macOS or WSL)

- Have Python 3.11 installed
- Create and activate a virtualenv, then install the QuantiFarm common modules and
  this module (same as for `dats-loader`, see its README).
- Try it out on a single DAT first, without needing a DeepL key yet:

```bash
TRANSLATE_ONLY_DAT=gaiasense DRY_RUN=true python -m translation_loader
```

- Once you have a `DEEPL_API_KEY`, translate that same single DAT for real:

```bash
DEEPL_API_KEY=... TRANSLATE_ONLY_DAT=gaiasense python -m translation_loader
```

- Once that looks good, run it for all DATs by simply omitting
  `TRANSLATE_ONLY_DAT`:

```bash
DEEPL_API_KEY=... python -m translation_loader
```

## Running this as a Docker Compose service

```bash
# add DEEPL_API_KEY (and optionally TRANSLATE_ONLY_DAT / DRY_RUN) to
# packages/data-platform/.env, then:
docker compose up translation-loader
```
