[← Back to Main README](../README.md)

# MongoDB Shell (mongosh) Cheat Sheet

## Basic Operations

- **Start MongoDB Shell**: `mongosh "mongodb://<your_connection_string>"`
- **Show Databases**: `show dbs`
- **Use Database**: `use <db_name>`
- **Show Collections**: `show collections`

## CRUD Operations

### Create
- **Create a New Collection**: `db.createCollection('<collection_name>')`
- **Insert a Document**: `db.<collection_name>.insert({<document>})`

### Read
- **Find All Documents in a Collection**: `db.<collection_name>.find()`
- **Find Documents with Conditions**: `db.<collection_name>.find({<condition>})`
- **Count Documents**: `db.<collection_name>.countDocuments({<condition>})`

### Update
- **Update a Document**: `db.<collection_name>.update({<query>}, {$set: {<update>}})`
- **Update Multiple Documents**: `db.<collection_name>.updateMany({<query>}, {$set: {<update>}})`

### Delete
- **Delete a Document**: `db.<collection_name>.deleteOne({<condition>})`
- **Delete Multiple Documents**: `db.<collection_name>.deleteMany({<condition>})`

## Index Management

- **Create an Index**: `db.<collection_name>.createIndex({<field>: <type>})`
- **List Indexes**: `db.<collection_name>.getIndexes()`
- **Drop an Index**: `db.<collection_name>.dropIndex('<index_name>')`

## Aggregation

- **Simple Aggregation**: `db.<collection_name>.aggregate([{$group: {_id: "$<field>", count: {$sum: 1}}}])`

## Administration

- **View Server Status**: `db.serverStatus()`
- **View Current Operations**: `db.currentOp()`
- **Kill an Operation**: `db.killOp(<opId>)`

## Misc

- **Scripting with JavaScript**: Write JavaScript functions and execute them in mongosh.
- **Enable/Disable Profiling**: `db.setProfilingLevel(<level>)`

---

[← Previous: Testing Mongo CRUD API ](./TESTING.md)

