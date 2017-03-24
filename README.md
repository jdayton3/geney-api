# Geney API

## GET requests

get:  `/api/datasets`

query:  none

response:  json array of strings, each the name of a dataset

```
["Sample Dataset","Sample Dataset 1"]
```

get:  `/api/meta/x`

query: 	none

response:  metadata for dataset "x" if "x" exists, else 404. x is the name of the dataset lowercase without spaces
```
{  
  "info":{  
    "numMetaTypes":1,
    "numSamples":123,
    "numGenes":3,
    "description":"<h1>Description</h1>",
    "title":"Sample Dataset"
  },
  "meta":{  
    "variable1":[  
      "option1",
      "option2",
      "option3"
    ]
  },
  "genes":[  
    "gene1",
    "gene2",
    "gene3"
  ]
}
```

## POST requests

post:  `/api/samples`

query:  json object with dataset name and selected meta features

```
{  
  "dataset":"sampledataset",
  "meta":{  
    "variable1":[  
      "option1",
      "option3"
    ]
  }
}
```

response:  number of samples matched by the filters

```
{  
  "samples":65
}
```

post:  `/api/download`

query:  JSON object with dataset name, selected meta features, download options, and desired genes. An empty list of genes means the user wants ALL genes.

Download options:

- fileformats: ["csv","tsv","gct","json"]
- Filename: string
- MORE TO COME!

```
{  
  "dataset":"sampledataset",
  "meta":{  
    "variable1":[  
      "option1",
      "option3"
    ]
  },
  "options":{  
    "fileformat":"csv",
    "filename":"example"
  },
  "genes":[  

  ]
}
```

Response:  Set the following headers:

```
Content-Type : text/x
Content-disposition: attachment; filename=example.csv
```

And somehow serve the file.

_Replace `x` and `example.csv` with the correct values._

