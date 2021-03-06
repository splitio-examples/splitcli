def set_configuration(definition, treatment_name, configuration):
    for treatment in definition["treatments"]:
        if treatment["name"] == treatment_name:
            treatment["configurations"] = configuration
            return definition
    raise ValueError("Treatment does not exist: " + treatment_name)

def set_segments(definition, treatment_name, segments):
    for treatment in definition["treatments"]:
        if treatment["name"] == treatment_name:
            treatment["segments"] = segments
            return definition
    raise ValueError("Treatment does not exist: " + treatment_name)

def set_keys(definition, treatment_name, keys):
    for treatment in definition["treatments"]:
        if treatment["name"] == treatment_name:
            treatment["keys"] = keys
            return definition
    raise ValueError("Treatment does not exist: " + treatment_name)

def ramp_default_rule(definition, treatment_map):
    treatments = []
    for treatment,size in treatment_map.items():
        treatments.append(bucket(treatment, size))
    definition['defaultRule'] = treatments
    return definition

def new_split(treatments, baseline):
    comment = "Created via Split CLI"
    return build_split(comment, treatments, baseline)

def simple_treatments(treatments):
    return list(map(lambda x: {"name":x},treatments))

def bucket(treatment, size=100):
    return {"treatment":treatment, "size":size}

def build_split(comment, treatments=["on","off"], baseline="off", default_rule=None, rules=[]):
    if default_rule is None:
        default_rule = [bucket(baseline)]
    return {
        "treatments": simple_treatments(treatments),
        "defaultTreatment": baseline,
        "baselineTreatment": baseline,
        "rules": rules,
        "defaultRule": default_rule,
        "comment": comment
    }