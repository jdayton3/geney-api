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
    "description": "#Description\n##This is the Description",
    "name": "Sample Dataset",
    "id": "sampledataset",
    "uploadDate": 1494195717279
  }
]
```

### GET: `/api/datasets/:id/meta`

##### Query: none

##### Response:

```js
{
  "meta": {
    "variable1": {
      "numOptions": 3,
      "options": ["option1","option2","option3"]
    }
  },
  "genes": {
    "numOptions": 190000,
    "options": null
  }
}
```

If options is null, that means the front end needs to make a query to the backend whenever the user wants to see the page

### GET: `/api/datasets/:id/meta/:metaType/search/:str`

##### Query:

- `:id` ID of dataset
- `:metaType` Either `gene` or one of the meta value types
- `:str` the value to search

##### Response: array of strings that match the search term

```json
["val1", "val2"]
```

### POST: `/api/datasets/:id/samples`

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

### POST: `/api/datasets/:id/download`

##### Query: 	

JSON object with dataset name, selected meta features, download options, and desired genes. An empty list of genes means the user wants ALL genes. Because the browser needs to download the response as a file, we cannot use a standard `XMLHttpRequest`, and instead must use a regular HTML form. This means that the query will a JSON string, and will need to be parsed as such by the server.

Download options:

- fileformats: ["csv","tsv","gct","json"]
- filename: string
- MORE TO COME!

```json
{
  "query": {
    "meta": {
	  "variable1": ["option1","option3"]
    },
    "genes": [],
    "options": {
	  "fileformat": "csv",
	  "filename": "example"
    }
  }
}
```

##### Response:

Set the following headers:

"Content-Type" : "text/`csv`"  
"Content-disposition":"attachment; filename=`example.csv`"
		
(Replace the code sections with the correct values.)

The file to be downloaded will be the response body.

### GET:  `/api/datasets/validate?val=id`

##### Response: `true` or `false`, depending on whether or not that id is available

### PUT: `/api/datasets`

##### Query:

The id, title, description, number of metadata columns, and the file that will be used to create a new dataset.

This will be sent as a [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData) object to accomodate the file upload.

##### Response: 	

Response code 202 on a successful request, to indicate that it is still processing. The user should be notified via email when the dataset has been processed and is ready for querying. The user's information can be obtained from the JWT (which will need authentication anyways).

### PATCH: `/api/datasets/:id/`

##### Query:

JSON object with the new title and description for the dataset

```json
{
  "title": "String",
  "description": "String"
}
```

##### Response: 	

`true` or `false`, depending on the dataset being saved.


## Resources: 

- [Tutorial on APIs, Python, and Flask.](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
- [Helpful tutorial on testing Flask apps](http://flask.pocoo.org/docs/0.12/testing/)

## Notes:
