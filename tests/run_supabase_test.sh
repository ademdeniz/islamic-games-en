#!/bin/sh
# Tests supabase/schema.sql on a throwaway Postgres (needs Docker running; container bz-pgtest from postgres:16-alpine).
set -e
cd "$(dirname "$0")/.."
docker exec bz-pgtest psql -U postgres -c 'drop database if exists schematest' -c 'create database schematest' >/dev/null
docker exec bz-pgtest mkdir -p /tmp/sb
docker cp supabase/schema.sql bz-pgtest:/tmp/sb/schema.sql
docker cp supabase/test_schema.sql bz-pgtest:/tmp/sb/test_schema.sql
docker exec bz-pgtest psql -q -t -A -U postgres -d schematest -f /tmp/sb/test_schema.sql 2>&1 | sed 's/^psql:[^ ]* //' | grep -vE 'does not exist, skipping|already exists, skipping|^$|^[0-9a-f-]{36}$|^[A-Z2-9]{6}$'
