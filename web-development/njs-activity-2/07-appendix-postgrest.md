# Appendix — How PostgREST works (short version)

Supabase automatically turns every Postgres table into a REST API using **PostgREST**.

Our helper builds a request like:

```text
GET https://YOUR-PROJECT.supabase.co/rest/v1/countries?select=id,name,iso3,regions(name)&order=name.asc
```

with these headers:

```text
apikey: YOUR-ANON-KEY
Authorization: Bearer YOUR-ANON-KEY
```

PostgREST runs the query in Postgres and returns JSON. That is why we do not write our own backend — Supabase gives us one for free.

Useful PostgREST query options we used:

| Option | Example | Meaning |
|---|---|---|
| `select` | `select=id,name,regions(name)` | Choose columns, and embed related tables with `table(columns)` |
| `id=eq.4` | `id=eq.4` | Filter: `id` equals 4 |
| `country_id=eq.4` | `country_id=eq.4` | Filter: `country_id` equals 4 |
| `order` | `order=name.asc` | Sort ascending |

---

[← Part 5](./06-part-5-loading-and-run.md) | [Back to index](./README.md) | [Next: Troubleshooting →](./08-appendix-troubleshooting.md)
