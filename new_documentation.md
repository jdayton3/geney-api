# BioGeney Server API


### get:  `/api/datasets`

##### query:  none

##### response: json array of objects, with the below properties
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

### get: `/api/datasets/:id/meta`

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

### get: `/api/datasets/:id/meta/:metaType/search/:str`

query: 
  * `:id` ID of dataset
  * `:metaType` Either `gene` or one of the meta value types
  * `:str` the value to search

response: array of strings that match the search term

```json
["val1", "val2"]
```

### post: `/api/datasets/:id/samples`

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

### post: `/api/datasets/:id/download`

query: 	

JSON object with dataset name, selected meta features, download options, and desired genes. An empty list of genes means the user wants ALL genes. Because the browser needs to download the response as a file, we cannot use a standard `XMLHttpRequest`, and instead must use a regular HTML form. This means that the query will a JSON string, and will need to be parsed as such by the server.

Download options:
	fileformats: ["csv","tsv","gct","json"]
	Filename: string
	MORE TO COME!

```json
{
  query: {
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

Response:

Set the following headers:

"Content-Type" : "text/`x`"
"Content-disposition":"attachment; filename=`example.csv`"

Then write the file to the response!


### get:  `/api/datasets/validate?val=id`

##### response: `true` or `false`, depending on whether or not that id is available


### put: `/api/datasets`

query:

The id, title, description, number of metadata columns, and the file that will be used to create a new dataset.

This will be sent as a [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData) object to accomodate the file upload.

response: 	

Response code 202 on a successful request, to indicate that it is still processing. The user should be notified via email when the dataset has been processed and is ready for querying. The user's information can be obtained from the JWT (which will need authentication anyways).

### patch: `/api/datasets/:id/`

query:

json object with the new title and description for the dataset

```json
{
  "title": "String",
  "description": "String"
}
```

response: 	

`true` or `false`, depending on the dataset being saved.