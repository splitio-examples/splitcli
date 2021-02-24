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