# Maybe a web interface for SqlTutorial book exercises

## Notes
### Standard SQL clauses to fetch table description in Postgres:
[Stack Overflow Source](https://stackoverflow.com/a/5273757/2223106)
`select column_name, data_type, character_maximum_length, column_default, is_nullable
from INFORMATION_SCHEMA.COLUMNS where table_name = 'employee';`

```
select n.nspname as schema_name,
       t.relname as table_name,
       c.conname as constraint_name
from pg_constraint c
  join pg_class t on c.conrelid = t.oid
  join pg_namespace n on t.relnamespace = n.oid
where t.relname = 'employee';
```

### Add constraint to table column with ALTER:
```
ALTER TABLE employee ALTER COLUMN emp_id ADD GENERATED ALWAYS AS IDENTITY;
```

### Manually run these commands before runnin `python admin.py tables --confirm`

- `CREATE TYPE customer_type AS ENUM('I', 'B');`
- `CREATE TYPE account_status AS ENUM('ACTIVE','CLOSED','FROZEN');`
- `CREATE TYPE txn_type_cd AS ENUM('DBT','CDT');`

### Create a function you can reuse to truncate all tables in a db:

```sql
--src: https://stackoverflow.com/a/2829485/2223106
CREATE OR REPLACE FUNCTION truncate_tables(username IN VARCHAR) RETURNS void AS $$
DECLARE
    statements CURSOR FOR
        SELECT tablename FROM pg_tables
        WHERE tableowner = username AND schemaname = 'public';
BEGIN
    FOR stmt IN statements LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

USAGE: `SELECT truncate_tables('MYUSER');`

### Book References:
- https://resources.oreilly.com/examples/9780596007270
