class APIObj:
    def __init__(self):
        self.datasets = ["Sample Dataset", "Sample Dataset 1"]
        self.meta = {
            "sampledataset": {
                "info": {
                    "numMetaTypes": 1,
                    "numSamples": 123,
                    "numGenes": 3,
                    "description": "<h1>Description</h1>",
                    "title": "Sample Dataset"
                },
                "meta": {
                    "variable1": ["option1","option2","option3"]
                },
                "genes": ["gene1","gene2","gene3"]
            },
            "sampledataset1": {
                "info": {
                    "numMetaTypes": 1,
                    "numSamples": 123,
                    "numGenes": 3,
                    "description": "<h1>Description</h1>",
                    "title": "Sample Dataset"
                },
                "meta": {
                    "variable1": ["option1","option2","option3"]
                },
                "genes": ["gene1","gene2","gene3"]
            }
        }

        self.samples = {
            "samples": 65
        }
