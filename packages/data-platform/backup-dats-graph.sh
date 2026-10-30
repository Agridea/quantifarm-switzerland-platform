#!/bin/sh
# Dumps the DATs and DAT translations named graphs from Fuseki as Turtle,
# for disaster recovery (not a per-CRUD backup - see dat_change_log/undo
# in toolkit-dashboard for that).
#
# Usage:
#   ./backup-dats-graph.sh
#
# Env vars (all optional):
#   TRIPLE_STORE_ENDPOINT   default: http://localhost:3030
#   DATS_GRAPH_URI                  default: https://quantifarm.eu/graphs/dats
#   DATS_TRANSLATIONS_GRAPH_URI     default: https://quantifarm.eu/graphs/dats-translations
#   BACKUP_DIR                      default: ./backups
#   RETENTION_DAYS                  default: 30 (older *.ttl files are deleted)

set -eu

ENDPOINT="${TRIPLE_STORE_ENDPOINT:-http://localhost:3030}"
DATS_GRAPH="${DATS_GRAPH_URI:-https://quantifarm.eu/graphs/dats}"
DATS_TRANSLATIONS_GRAPH="${DATS_TRANSLATIONS_GRAPH_URI:-https://quantifarm.eu/graphs/dats-translations}"
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

backup_graph() {
  GRAPH_NAME="$1"
  GRAPH_URI="$2"
  GRAPH_BACKUP_DIR="$BACKUP_DIR/$GRAPH_NAME"

  mkdir -p "$GRAPH_BACKUP_DIR"

  TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
  OUT_FILE="$GRAPH_BACKUP_DIR/${GRAPH_NAME}-${TIMESTAMP}.ttl"
  TMP_FILE="${OUT_FILE}.tmp"

  if ! HTTP_CODE=$(curl -sS -o "$TMP_FILE" -w '%{http_code}' \
    -H "Accept: text/turtle" \
    "${ENDPOINT}/quantifarm/data?graph=${GRAPH_URI}"); then
    echo "backup failed for $GRAPH_NAME: could not contact Fuseki" >&2
    rm -f "$TMP_FILE"
    return 1
  fi

  if [ "$HTTP_CODE" != "200" ]; then
    echo "backup failed for $GRAPH_NAME: Fuseki returned HTTP $HTTP_CODE" >&2
    rm -f "$TMP_FILE"
    return 1
  fi

  if [ ! -s "$TMP_FILE" ]; then
    echo "backup failed for $GRAPH_NAME: empty response from Fuseki" >&2
    rm -f "$TMP_FILE"
    return 1
  fi

  mv "$TMP_FILE" "$OUT_FILE"
  echo "backup written: $OUT_FILE ($(wc -l < "$OUT_FILE") lines)"

  # Rotate only this graph's backups.
  find "$GRAPH_BACKUP_DIR" -name "${GRAPH_NAME}-*.ttl" -type f -mtime +"$RETENTION_DAYS" -print -delete
}

# Keep the graph requests sequential so each backup is completed before the next starts.
backup_graph "dats" "$DATS_GRAPH"
backup_graph "dats-translations" "$DATS_TRANSLATIONS_GRAPH"
