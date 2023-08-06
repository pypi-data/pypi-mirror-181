# FastAPI-Tryton

Adds Tryton support to FastAPI application.

By default transactions are readonly except for PUT, POST, DELETE and PATCH
request methods.
It provides also 2 routing converters `record` and `records`.

Setting the `configure_jinja` flag adds the following filters on jinja
templates: `numberformat`, `dateformat`, `currencyformat` and
`timedeltaformat`. The filters apply the same formatting as Tryton reports.

## Nutshell

TODO: Add examples of use, and docs, all collaboration is welcome!,
but for now you can see test_api.py file where there is examples ;)
