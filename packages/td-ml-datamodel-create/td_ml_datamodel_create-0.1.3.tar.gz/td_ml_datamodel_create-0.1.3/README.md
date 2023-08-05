# td-ml-datamodel-create

## Introduction

This Python Library allows you to define the main JSON params of a Treasure Insights Datamodel in a `config.json` file inside a ***Treasure Workflow Project*** and build datamodel automatically via API.


## Inputs

* `config.json`: the file that contains the needed params for Python code to read from and build the TI Datamodel. See below:

```
{
## -- (name of datamodel)
"model_name":  "datamodel_automated" 
,
## -- (list of tables to be added to datamodel)
"model_tables": [
  {"db":"reporting","name":"table_1"},
  {"db":"reporting","name":"table_2"}
                ] 
,
## -- (list of users to share datamodel with)
"shared_user_list": ["ENTER EMAIL HERE","ENTER EMAIL HERE"] 
,
## -- (list of columns you want to change datatype from raw table to datamodel. Ex. in "date" you provide column names that will be converted to `datetime`)
"change_schema_cols": {"date": ["ENTER_NAME"], "text": ["ENTER_NAME"], "float": ["ENTER NAME"], "bigint": ["ENTER NAME"]}
, 
## -- (if any joins were required you can add a list of table_name:join_key pairs)
"join_relations": {"pairs":
[ 
  {"db1": "reporting", "tb1":"table_1","join_key1":"user_id","db2": "reporting","tb2":"table_2","join_key2":"user_id"},
  {"db1": "reporting", "tb1":"table_1","join_key1":"date","db2": "reporting","tb2":"table_2","join_key2":"date"}
]
                  }
}
```

`Copyright © 2022 Treasure Data, Inc. (or its affiliates). All rights reserved`


