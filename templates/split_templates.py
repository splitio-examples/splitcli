def toggleSplit(comment):
    return rampSplit(0, comment)

def rampSplit(ramp, comment):
    return {
        "treatments": [
            {
                "name": "on"
            },
            {
                "name": "off"
            }
        ],
        "defaultTreatment": "off",
        "baselineTreatment": "off",
        "rules": [],
        "defaultRule": [
            {
                "treatment": "on",
                "size": ramp
            },
            {
                "treatment": "off",
                "size": 100 - ramp
            }
        ],
        "comment": comment
    }

# def movie():
#     return {
#         "name": "movie_filter",
#         # "environment": {
#         #     "id": "f8aa2660-3f31-11eb-be37-12b057418355",
#         #     "name": "Prod-Default"
#         # },
#         # "trafficType": {
#         #     "id": "f8a8ede0-3f31-11eb-be37-12b057418355",
#         #     "name": "user"
#         # },
#         "killed": False,
#         "treatments": [
#             {
#                 "name": "USA",
#                 "description": "USA Filter"
#             },
#             {
#                 "name": "default",
#                 "description": ""
#             }
#         ],
#         "defaultTreatment": "USA",
#         "baselineTreatment": "default",
#         "trafficAllocation": 100,
#         "rules": [],
#         "defaultRule": [
#             {
#                 "treatment": "USA",
#                 "size": 100
#             }
#         ],
#         # "creationTime": 1613767914941,
#         # "lastUpdateTime": 1613768561090
#     }