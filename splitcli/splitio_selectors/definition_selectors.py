import json

from splitcli.split_apis import definitions_api, segments_api
from splitcli.templates import split_templates
from splitcli.ux import menu

def manage_definition(workspace, split, environment):
    while True:
        definition = get_definition_operator(workspace["name"], environment["name"], split["name"])
        if definition == None:
            (treatments, baseline) = select_treatments()
            create_definition_operator(workspace["id"], environment["name"], split["name"], treatments, baseline)
        else:
            title = "Managing " + split["name"] + " in " + environment["name"]

            options = []
            options.append({"option_name": "Show full definition JSON", "operation": lambda: show_definition_json(definition)})
            options.append({"option_name": "Target keys", "operation": lambda: target_keys(workspace, split, environment, definition)})
            options.append({"option_name": "Target segments", "operation": lambda: target_segments(workspace, split, environment, definition)})
            options.append({"option_name": "Ramp split", "operation": lambda: ramp_split(workspace, split, environment, definition)})
            if definition.get("killed", False):
                options.append({"option_name": "Restore", "operation": lambda: restore_definition(workspace, split, environment)})
            else:
                options.append({"option_name": "Kill", "operation": lambda: kill_definition(workspace, split, environment)})
            options.append({"option_name": "Delete definition", "go_back": True, "operation": lambda: delete_definition(workspace, split, environment)})
            options.append({"option_name": "Go back", "go_back": True})

            show_definition(definition)
            _, go_back = menu.select_operation(title, options)
            if go_back:
                return

def select_treatments():
    title = "Select Treatments"
    options = [
        {"option_name": "Simple Rollout - on & off treatments", "operation": lambda: (["on", "off"], "off")},
        {"option_name": "Custom & Multivariant - create any treatments needed", "operation": lambda: input_treatments()}
    ]
    selection,_ = menu.select_operation(title, options)
    return selection

def input_treatments():
    treatments = menu.input_list("Add treatment name", treatments_validator)
    baseline,_ = menu.select("Select baseline treatment", treatments)
    return (treatments, baseline)

def treatments_validator(treatments):
    if len(treatments) < 2:
        return menu.error_message("At least two treatments are required")
    else:
        return None

def show_definition_json(definition):
    menu.info_message(json.dumps(definition, indent=4))

def show_definition(definition):
    output = ""

    # Targeting Lists
    for treatment in definition.get("treatments",[]):
        treatment_name = treatment["name"]
        segments = treatment.get("segments",[])
        if(len(segments) > 0):
            segment_string = ", ".join(segments)
            output += f"\nTargeting '{treatment_name}' to segments: {segment_string}"
        keys = treatment.get("keys",[])
        if(len(keys) > 0):
            key_string = ", ".join(keys)
            output += f"\nTargeting '{treatment_name}' to keys: {key_string}"
    
    # Traffic Allocation
    default_treatment = definition["defaultTreatment"]
    allocation = definition.get("trafficAllocation",100)
    if allocation < 100:
        output += f"\nAllocating {allocation}% of traffic to {default_treatment}"
    
    # Rules
    for rule in definition.get("rules",[]):
        rule_string = json.dumps(rule, indent=4)
        output += f"\n{rule_string}"
    
    # Default Rule
    buckets = []
    for bucket in definition.get("defaultRule",[]):
        treatment = bucket["treatment"]
        size = bucket["size"]
        buckets.append(f"{size}% {treatment}")
    bucket_string = ", ".join(buckets)
    output += f"\nDefault Rule: {bucket_string}"
    
    if definition.get("killed",False):
        output += f"\n\nThis Split has been killed. Serving '{default_treatment}' to all keys"
        menu.warn_message(output)
    else:
        menu.info_message(output)

def delete_definition(workspace, split, environment):
    title = "Are you sure?"
    options = [
        {"option_name": "Yes", "operation": lambda: definitions_api.delete(
            workspace["id"], environment["name"], split["name"])},
        {"option_name": "No", "go_back": True}
    ]
    menu.select_operation(title, options)

def target_keys(workspace, split, environment, definition):
    try:
        treatments = map(lambda x: x['name'], definition['treatments'])
        treatment,_ = menu.select("Which treatment are you targeting", treatments)
        keys = menu.input_list("Provide a key to add to list")
        split_data = split_templates.set_keys(definition, treatment, keys)
        definitions_api.full_update(workspace["id"], environment["name"], split["name"], split_data)
    except Exception as exc:
        menu.error_message("Could not add keys to split\n" + str(exc))

def target_segments(workspace, split, environment, definition):
    try:
        traffic_type_name = split['trafficType']['name']
        segments = segments_api.list_segments_environment(workspace['id'], environment['name'])
        segments = list(filter(lambda x: x['trafficType']['name'] == traffic_type_name, segments))
        segment_names = list(map(lambda x: x['name'], segments))
        
        treatment = menu.select("Which treatment are you targeting", definition['treatments'], name_field="name")
        default = treatment.get("segments",[])
        result = menu.checkbox("Select segments to target", segment_names, default)

        split_data = split_templates.set_segments(definition, treatment["name"], result)
        definitions_api.full_update(workspace["id"], environment["name"], split["name"], split_data)
    except Exception as exc:
        menu.error_message("Could not update split\n" + str(exc))

def ramp_split(workspace, split, environment, definition):
    try:
        total_ramp = 0
        treatment_map = {}
        default_treatment = definition['defaultTreatment']
        for treatment in definition['treatments']:
            treatment_name = treatment['name']
            if treatment_name != default_treatment:
                while True:
                    ramp_percent = int(menu.text_input("Ramp percentage for " + treatment_name))
                    if total_ramp + ramp_percent > 100:
                        menu.error_message("Total ramp percentage must be less than 100: remaining=" + (100-total_ramp))
                    else:
                        treatment_map[treatment_name] = ramp_percent
                        total_ramp += ramp_percent
                        break
        treatment_map[default_treatment] = 100 - total_ramp
        split_data = split_templates.ramp_default_rule(definition, treatment_map)
        definitions_api.full_update(workspace["id"], environment["name"], split["name"], split_data)
    except Exception as exc:
        menu.error_message("Could not update split\n" + str(exc))


# Operators

def get_definition_operator(workspace_id, environment_name, split_name, expected=False):
    try:
        return definitions_api.get(workspace_id, environment_name, split_name)
    except Exception as exc:
        if expected:
            menu.error_message("Definition does not exist:" + str(exc))
        return None

def create_definition_operator(workspace_id, environment_name, split_name, treatments=["on", "off"], baseline="off"):
    try:
        split_data = split_templates.new_split(treatments, baseline)
        definitions_api.create(workspace_id, environment_name, split_name, split_data)
    except Exception as exc:
        menu.error_message("Could not create split\n" + str(exc))

def kill_definition(workspace, split, environment):
    try:
        definitions_api.kill(workspace["id"], environment["name"], split["name"])
        menu.success_message(f"You killed " + split["name"] + " in " + environment["name"] + ". RIP.")
    except Exception as exc:
        menu.error_message("Could not kill split\n" + str(exc))

def restore_definition(workspace, split, environment):
    try:
        definitions_api.restore(workspace["id"], environment["name"], split["name"])
        menu.success_message(f"You restored " + split["name"] + " in " + environment["name"] + ". It's Alive!!")
    except Exception as exc:
        menu.error_message("Could not restore split\n" + str(exc))

def ramp_split_operator(workspace_id, environment_name, split_name, ramp_percent=None, treatment_map=None):
    try:
        # Validate Inputs
        if ramp_percent is not None and treatment_map is not None:
            raise ValueError("Either ramp_percent or treatment_map must be set, currently both")
        
        # Get current definition
        definition = get_definition_operator(workspace_id, environment_name, split_name, expected=True)
        if definition is None:
            raise ValueError("Definition not found")

        if ramp_percent is not None:
            # Set Ramp Percent
            treatment_map = {}
            treatments = definition["treatments"]
            if len(definition["treatments"]) != 2:
                raise ValueError("Definition must have two treatments to use ramp_percent")
            default_treatment = definition['defaultTreatment']
            for treatment in treatments:
                treatment_name = treatment['name']
                if treatment_name != default_treatment:
                    treatment_map[treatment_name] = ramp_percent
            treatment_map[default_treatment] = 100 - ramp_percent
        elif treatment_map is None:
            raise ValueError("Either ramp_percent or treatment_map must be set, currently neither")
    
        # Update Split
        split_data = split_templates.ramp_default_rule(definition, treatment_map)
        definitions_api.full_update(workspace_id, environment_name, split_name, split_data)
    except Exception as exc:
        menu.error_message("Could not update split\n" + str(exc))

def target_segments_operator(workspace_id, environment_name, split_name, treatment_name, segment_names):
    try:
        # Get current definition
        definition = get_definition_operator(workspace_id, environment_name, split_name, expected=True)
        if definition is None:
            raise ValueError("Definition not found")
        split_data = split_templates.set_segments(definition, treatment_name, segment_names)
        definitions_api.full_update(workspace_id, environment_name, split_name, split_data)
    except Exception as exc:
        menu.error_message("Could not update split\n" + str(exc))