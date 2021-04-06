import time

from splitcli.experiment.batch_client import BatchClient
from splitcli.experiment.event_result import EventResult

class Experiment(object):
    def __init__(self, sample, feature, comp_treatment="on", key_pattern="user_{position}", traffic_type="user"):
        super(Experiment, self).__init__()
        self.feature = feature
        self.comp_treatment = comp_treatment
        self.sample = sample
        self.key_pattern = key_pattern
        self.event_results = []
        self.traffic_type = traffic_type

    def register(self, eventType, properties={}, property_value=None):
        event_result = EventResult(eventType, properties, self.sample, property_value=property_value)
        self.event_results.append(event_result)
        return event_result

    def key(self, position):
        return self.key_pattern.format(position=position)

    def run(self, sdk_token):
        batch_client = BatchClient(sdk_token)
        base_sample = 0
        comp_sample = 0
        for position in range(self.sample):
            key = self.key(position)
            treatment = batch_client.get_treatment(key, self.feature)
            if treatment == self.comp_treatment:
                comp_sample += 1
            else:
                base_sample += 1

        for event_result in self.event_results:
            base_events = event_result.base_events(base_sample)
            comp_events = event_result.comp_events(comp_sample)

            base_pos = 0
            comp_pos = 0

            for position in range(self.sample):
                key = self.key(position)
                treatment = batch_client.get_treatment(key, self.feature)
                if treatment == self.comp_treatment:
                    if comp_pos >= len(comp_events):
                        print(str(len(comp_events)) + " | " + str(comp_sample) + " | " + str(comp_pos))
                    (count, value) = comp_events[comp_pos]
                    
                    properties = event_result.properties
                    if event_result.property_value is not None:
                        properties[event_result.property_value] = value
                    self.track(batch_client, key, self.traffic_type, event_result.event_type, properties, count, value)
                    comp_pos += 1
                else:
                    if base_pos >= len(base_events):
                        print(str(len(base_events)) + " | " + str(base_sample) + " | " + str(base_pos))
                    (count, value) = base_events[base_pos]

                    properties = event_result.properties
                    if event_result.property_value is not None:
                        properties[event_result.property_value] = value
                    self.track(batch_client, key, self.traffic_type, event_result.event_type, properties, count, value)
                    base_pos += 1
        
        batch_client.destroy()
    
    def track(self, split_client, key, traffic_type, event_type, properties, event_count, event_value):
        for _ in range(event_count):
            time.sleep(.001)
            split_client.track(key, traffic_type, event_type, event_value, properties)