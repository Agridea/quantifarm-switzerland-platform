# QuantiFarm Data Plaform

This is the source code repository of the QuantiFarm Data Platform.

The main components are the following:

- `triple-store`: Triple store for storing DAT information and test case assessment data.
  - This triple store will be queried by the various *tool web services*, which are not yet included in this prototype.
- `dats-loader`: A loader that reads data about DATs from various source, e.g. an export from FAIRshare, converts them into triples, and loads it into the triple store.
- `testcase-loader`: A loader (ETL) of test case data that reads data from a JSON testcase file, maps it to QCSM-conform RDF, and loads it into the triple store.

It should be noted that the loaders (`*-loader` services) should write triples to __their own graph__. This way, when source data for a loader is updated, it is trivial to replace any existing data using the SPARQL Graph Store Protocol (handled by the loaders).

## Implementation status

There is a version of the data platform deployed on TNO's Azure cloud servers. This is the production instance of the original **QuantiFarm EU** project, from which this Swiss solution was derived.

- The central data storage on the Azure cloud servers is not available from the outside, but only from the QuantiFarm toolkit server.

## Running the platform (for developing locally)

### Environment variables
First, create a `.env` file in this directory and put the following in it:

```
SPARQL_QUERY_ENDPOINT=http://triple-store:3030/quantifarm/query
TRIPLE_STORE_ENDPOINT=http://triple-store:3030
```

### Prepare source data
The FAIRshare data file that contains all DAT information can be found at `./dats-loader/fairshare-dats....json`. Other sources of DATs are DATs collected for the cost-benefit tool in `./dats-loader/cost-benefit....xls` and `testcase-dats.xls`.

### Starting the platform

To start the platform and run the triplestore and loader(s) locally, run the following:

```bash
docker compose up
```

The triplestore should be available at:

- http://localhost:3030/quantifarm/query
  - The triple store's endpoint for SPARQL 1.1 Query (with ARQ extensions)
  - To be used by the tool web services
- http://localhost:3030/quantifarm/update
  - The triple store's endpoint for SPARQL 1.1 Update (with ARQ extensions)
  - To be used by the loaders
- http://localhost:3030/quantifarm/data
  - The triple store's endpoint for SPARQL Graph Store Protocol and Quad extensions
  - To be used by the loaders and tool web services
- http://localhost:3030/quantifarm/get
  - The triple store's endpoint for SPARQL Graph Store Protocol and Quad extensions (read-only)
  - To be used by the tool web services

To receive data from the triple store, you can, for example, do the following:

```bash
# receive and write all of the data in the fairshare graph to a Turtle file.
curl localhost:3030/quantifarm/data?graph=https://quantifarm.eu/graphs/dats --header "Accept: text/turtle" > dats-graph.ttl
```

To (re)load the data with the loaders, they can simply be run as a Docker Compose service:

```bash
# this will overwrite the data that it previously wrote, if any
docker compose up dats-loader
```

## Backing up the DATs graph

Since the `toolkit-dashboard`'s DAT-management UI allows admins to edit the `dats` graph
directly, daily Turtle dumps of the `dats` and `dats-translations` graphs are kept for
disaster recovery (separate from the per-change undo history stored in the
toolkit-dashboard's `dat_change_log` table). The graphs are backed up sequentially by one
service invocation.

**Run manually / test:**

```bash
cd packages/data-platform
docker compose --profile loaders up dats-backup
```

This writes `backups/dats/dats-<timestamp>.ttl` and
`backups/dats-translations/dats-translations-<timestamp>.ttl`, then deletes backups older
than `RETENTION_DAYS` (default 30, override via `DATS_BACKUP_RETENTION_DAYS` in `.env`).

**Schedule on the production Linux server** (cron is normally already installed/running there):

```bash
crontab -e
# daily at 03:00
0 3 * * * cd /path/to/packages/data-platform && docker compose --profile loaders up dats-backup >> backups/dats-backup.log 2>&1
```

**Restore from a backup** (full graph replace — only for disaster recovery, use the
toolkit-dashboard's Undo feature for reverting a single change instead):

```bash
curl -X PUT -H "Content-Type: text/turtle" \
  --data-binary @backups/dats/dats-2026-10-01_030000.ttl \
  "http://localhost:3030/quantifarm/data?graph=https://quantifarm.eu/graphs/dats"

# Restore the DAT translations graph
curl -X PUT -H "Content-Type: text/turtle" \
  --data-binary @backups/dats-translations/dats-translations-2026-10-01_030000.ttl \
  "http://localhost:3030/quantifarm/data?graph=https://quantifarm.eu/graphs/dats-translations"
```

## Rebuilding the triple store image
*Note that in production Fuseki also runs as the `triple-store` Docker container; the loaders reach it via `TRIPLE_STORE_ENDPOINT=http://triple-store:3030` in the `.env`.*

For local development, the `triple-store` serves as the data storage.

Since it can take quite some time to build the `triple-store` image, it is recommended to not build it locally, but to pull it from the registry with `docker compose pull triple-store`.
