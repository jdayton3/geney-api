class APIObj:
    def __init__(self):
        self.datasets = [
            {
                "id": 1,
                "name": "Sample Dataset 1",
                "numMetaTypes": 2,
                "numSamples": 123,
                "numGenes": 3,
                "description": "<h1>Sample Dataset</h1>"
            },
            {
                "id": 2,
                "name": "Sample Dataset 2",
                "numMetaTypes": 2,
                "numSamples": 1234,
                "numGenes": 35,
                "description": "<h1>Sample Dataset TWO</h1>"
            },
        ]
        self.meta = {
            "1" : {
                "meta": {
                    "var1": {
                        "numOptions": 3,
                        "options": [
                            "opt1",
                            "opt2",
                            "opt3",
                        ]
                    },
                    "var2": {
                        "numOptions": 10,
                        "options": None
                    },
                },
                "genes": {
                    "numOptions": 200,
                    "options": None
                }
            },
            "2" : {
                "meta": {
                    "var1": {
                        "numOptions": 3,
                        "options": [
                            "opt1",
                            "opt2",
                            "opt3",
                        ]
                    },
                    "var2": {
                        "numOptions": 2,
                        "options": [
                            "opt1",
                            "opt2",
                        ]
                    },
                },
                "genes": {
                    "numOptions": 300,
                    "options": None
                }
            }
        }

        self.samples = {
            "samples": 65
        }

        self.genes = ["AF10", "ALOX12", "ARHGEF12", "RNT", "AXL", "BAX", "BCL3", "CL6", "BTG1", "AV1", "CBFB", "DC23", "DH17", "CDX2", "CEBPA", "CLC", "R1", "CREBBP", "EK", "DLEU1", "DLEU2", "GFR", "ETS1", "EVI2A", "EVI2B", "OXO3A", "FUS", "LI2", "MPS", "HOX11", "OXA9", "RF1", "IT", "AF4", "LCP1", "LDB1", "LMO1", "LMO2", "LYL1", "ADH5", "LL3", "LLT2", "LLT3", "MOV10L1", "TCP1", "YC", "NFKB2", "OTCH1", "NOTCH3", "PM1", "UP214", "NUP98", "BX1", "BX2", "BX3", "BXP1", "ITX2", "PML", "AB7", "GS2", "RUNX1", "ET", "P140", "AL1", "AL2", "TCL1B", "TCL6", "THRA", "TRA", "NFN1A1"]


    # Given an array and a search string, return a new array containing
    # all values containing the search string.
    def find(self, arr, search):
        retArr = []
        for x in arr:
            if len(retArr) >= 10:
                break
            if search in x:
                retArr.append(x)
        return retArr

    # Search the genes array for genes matching the `search` term
    def searchGenes(self, search):
        return self.find(self.genes, search)
