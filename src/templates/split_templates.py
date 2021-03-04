def toggle_split(comment):
    return ramp_split(0, comment)

def ramp_split(ramp, comment):
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