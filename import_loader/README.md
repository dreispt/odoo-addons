The output steps available in Pentaho Kettle and Talend have a few limitations.
They do not support XML Ids and the same output step can perform only either 
create or write operations, not both (related to
https://github.com/odoo/odoo/pull/2258).

This module provides a server side proxy model, `import.loader`, that solves
those limitations.
New records created should have a `data` field with the payload to import.
This payload is parsed and then imported into the target model, 
using the `load()` method. This means that serialization rules that apply to 
CSV file import are apply here.

The ETL tools can then perform naive create operations on `import.loader`,
providing a data string with the payload, and this model will do the necessary 
handling and loading.

The payload is string representing a list of rows. 
Each row is a dictionary of field names/values,
and must include an additional `_model` key indicating the target model.

This means that the same payload can load one or more records, 
into one or more models.

Here is an example of a date payload to create or update a new contact:

```
{ "_model": "res.partner"
, "id": "res_partner_eric"
, "name": "Eric"
, "is_company": false
, "user_id/id": "base.user_root"
}
```

A usage example for Pentaho Kettle is provided in the `import_loader_demo.ktr` 
file.
