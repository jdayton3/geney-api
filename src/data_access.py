class DataObj:
    def __init__(self):
        self.datasets = [
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
        self.meta = {
            "sampledataset" : {
                "meta": {
                    "variable1": {
                        "numOptions": 3,
                        "options": [
                            "option1",
                            "option2",
                            "option3",
                        ]
                    },
                    "var1": {
                        "numOptions": 4,
                        "options": [
                            "val1",
                            "val2",
                            "thing3",
                            "thing4",
                        ]
                    }
                },
                "genes": {
                    "numOptions": 190000,
                    "options": None
                }
            }
        }

        self.samples = {
            "samples": 123
        }

        self.genes = ['gene1', 'gene2', "AF10", "ALOX12", "ARHGEF12", "RNT", "AXL", "BAX", "BCL3", "CL6", "BTG1", "AV1", "CBFB", "DC23", "DH17", "CDX2", "CEBPA", "CLC", "R1", "CREBBP", "EK", "DLEU1", "DLEU2", "GFR", "ETS1", "EVI2A", "EVI2B", "OXO3A", "FUS", "LI2", "MPS", "HOX11", "OXA9", "RF1", "IT", "AF4", "LCP1", "LDB1", "LMO1", "LMO2", "LYL1", "ADH5", "LL3", "LLT2", "LLT3", "MOV10L1", "TCP1", "YC", "NFKB2", "OTCH1", "NOTCH3", "PM1", "UP214", "NUP98", "BX1", "BX2", "BX3", "BXP1", "ITX2", "PML", "AB7", "GS2", "RUNX1", "ET", "P140", "AL1", "AL2", "TCL1B", "TCL6", "THRA", "TRA", "NFN1A1"]

    def get_datasets(self):
        return self.datasets
        
    def get_meta(self, dataset):
        return self.meta[dataset]

    def search_genes(self, gene):
        return self.find(self.genes, gene)

    def num_samples(self, dataset_id, variables):
        n_samples = self.samples["samples"]
        if variables != {}:
            for k in variables.keys():
                n_samples *= len(variables[k])
                n_samples /= 3
        return n_samples

    # Given an array and a search string, return a new array containing
    # all values containing the search string.
    def find(self, arr, search):
        retArr = []
        for x in arr:
            # if len(retArr) >= 10:
            #     break
            if search in x:
                retArr.append(x)
        return retArr
