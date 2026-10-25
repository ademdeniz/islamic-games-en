#!/bin/sh
# Tests supabase/schema.sql, waiver.sql, tracking.sql, parents.sql, homework.sql and adab.sql on a throwaway Postgres (needs Docker running; container bz-pgtest from postgres:16-alpine).
set -e
cd "$(dirname "$0")/.."
docker exec bz-pgtest psql -U postgres -c 'drop database if exists schematest' -c 'create database schematest' >/dev/null
docker exec bz-pgtest mkdir -p /tmp/sb
docker cp supabase/schema.sql bz-pgtest:/tmp/sb/schema.sql
docker cp supabase/test_schema.sql bz-pgtest:/tmp/sb/test_schema.sql
docker cp supabase/waiver.sql bz-pgtest:/tmp/sb/waiver.sql
docker cp supabase/test_waiver.sql bz-pgtest:/tmp/sb/test_waiver.sql
docker cp supabase/tracking.sql bz-pgtest:/tmp/sb/tracking.sql
docker cp supabase/test_tracking.sql bz-pgtest:/tmp/sb/test_tracking.sql
docker cp supabase/parents.sql bz-pgtest:/tmp/sb/parents.sql
docker cp supabase/test_parents.sql bz-pgtest:/tmp/sb/test_parents.sql
docker cp supabase/homework.sql bz-pgtest:/tmp/sb/homework.sql
docker cp supabase/test_homework.sql bz-pgtest:/tmp/sb/test_homework.sql
docker cp supabase/adab.sql bz-pgtest:/tmp/sb/adab.sql
docker cp supabase/test_adab.sql bz-pgtest:/tmp/sb/test_adab.sql
docker exec bz-pgtest psql -q -t -A -U postgres -d schematest -f /tmp/sb/test_schema.sql -f /tmp/sb/test_waiver.sql -f /tmp/sb/test_tracking.sql -f /tmp/sb/test_parents.sql -f /tmp/sb/test_homework.sql -f /tmp/sb/test_adab.sql 2>&1 | sed 's/^psql:[^ ]* //' | grep -vE 'does not exist, skipping|already exists, skipping|^$|^[0-9a-f-]{36}$|^[A-Z2-9]{6}$'
