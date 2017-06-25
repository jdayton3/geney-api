# BioGeney Server API

## [Glorious tutorial on APIs, Python, and Flask.](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)

[Helpful tutorial on testing Flask apps](http://flask.pocoo.org/docs/0.12/testing/)

### get:  `/api/datasets`

##### query:  none

##### response: json array of objects, with the below properties

```js
[
  {
    "numMetaTypes": 1,
    "numSamples": 123,
    "numGenes": 3,
    "description": "<h1>Description</h1>",
    "name": "Sample Dataset",
    "id": "sampledataset"
  }
]
```

### get: `/api/meta/id`

##### query: `none`

##### response:

```js
{
    "meta": {
        "variable1": {
            numOptions: 3,
            options: ["option1","option2","option3"]
    },
    "genes": {
        numOptions: 190000,
        options: null
}
```

If options is null, that means the front end needs to make a query to the backend whenever the user wants to see the page

### get: `/api/meta/id/gene?search=str`

query: 	

search: string of users typed in search

response:

```json
["gene1","gene2"]
```

### get: `/api/meta/id/metaType/var1?search=str`

query: 

search: string to match `metaType[var1]`

response: array of strings that match the search term

```json
["val1", "val2"]
```

### post: `/api/id/samples`

query:

json object with dataset name and selected meta features

```json
{
  "meta": {
    "variable1": ["option1","option3"]
  }
}
```

response: 	

number of samples matched by the filters

```json
{
  "samples": 65
}
```

### post: `/api/id/download`

query: 	

JSON object with dataset name, selected meta features, download options, and desired genes. An empty list of genes means the user wants ALL genes.

Download options:
	fileformats: ["csv","tsv","gct","json"]
	Filename: string
	MORE TO COME!

```json
{
  "meta": {
    "variable1": ["option1","option3"]
  },
  "options": {
    "fileformat": "csv",
    "filename": "example"
  }
  "genes": []
}
```

Response:

Set the following headers:

"Content-Type" : "text/`x`"
"Content-disposition":"attachment; filename=`example.csv`"
		
Replace the code sections with the correct values.

## Notes:

Maybe it's better to have a data_access::DataObj object that has a Flask object?