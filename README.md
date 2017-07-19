# Geney Server API

[Main repository](https://github.com/srp33/Geney).

### GET:  `/api/datasets`

##### Query:  none

##### Response: json array of objects, with the below properties

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

### GET: `/api/meta/id`

##### Query: none

##### Response:

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

### GET: `/api/meta/id/gene?search=str`

##### Query: 	

- `search`: string to search for in the list of genes

##### Response:

```json
["gene1","gene2"]
```

### GET: `/api/meta/id/metaType/var1?search=str`

##### Query: 

- `search`: string to match `metaType[var1]`

##### Response: array of strings that match the search term

```json
["val1", "val2"]
```

### POST: `/api/id/samples`

##### Query:

JSON object with dataset name and selected meta features

```json
{
  "meta": {
    "variable1": ["option1","option3"]
  }
}
```

##### Response: 	

JSON object containing the number of samples matched by the filters

```json
{
  "samples": 65
}
```

### POST: `/api/id/download`

##### Query: 	

JSON object with dataset name, selected meta features, download options, and desired genes. An empty list of genes means the user wants ALL genes.

Download options:

- fileformats: ["csv","tsv","gct","json"]
- filename: string
- MORE TO COME!

```json
{
  "meta": {
    "variable1": ["option1","option3"]
  },
  "options": {
    "fileformat": "csv",
    "filename": "example"
  },
  "genes": []
}
```

##### Response:

Set the following headers:

"Content-Type" : "text/`csv`"  
"Content-disposition":"attachment; filename=`example.csv`"
		
(Replace the code sections with the correct values.)

The file to be downloaded will be the response body.

## Resources: 

- [Tutorial on APIs, Python, and Flask.](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
- [Helpful tutorial on testing Flask apps](http://flask.pocoo.org/docs/0.12/testing/)

## Notes: