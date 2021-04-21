import time

from splitcli.experiment.batch_client import BatchClient
from splitcli.experiment.event_result import EventResult

class Experiment(object):
    def __init__(self, sdk_token, feature, comp_treatment="on", key_pattern="user_{position}", traffic_type="user", attributes={}):
        super(Experiment, self).__init__()
        self.sdk_token = sdk_token
        self.split_client = BatchClient(sdk_token)
        self.feature = feature
        self.comp_treatment = comp_treatment
        self.key_pattern = key_pattern
        self.event_results = []
        self.traffic_type = traffic_type
        self.attributes = attributes

    def run(self, sample_size):
        (base_keys, comp_keys) = self.get_samples(sample_size)
        for event_result in self.event_results:
            (base_events, comp_events) = event_result.events(len(base_keys), len(comp_keys))
            self.send_events(event_result, base_events, base_keys)
            self.send_events(event_result, comp_events, comp_keys)
        self.split_client.destroy()

    def get_samples(self, sample_size):
        base_keys = []
        comp_keys = []
        for position in range(sample_size):
            key = self.key(position)
            treatment = self.split_client.get_treatment(key, self.feature, self.attributes)
            if treatment == self.comp_treatment:
                comp_keys.append(key)
            else:
                base_keys.append(key)
        return (base_keys, comp_keys)

    def send_events(self, event_result, events, keys):
        for (key, (count, value)) in zip(keys,events):
            properties = event_result.properties
            if event_result.property_value is not None:
                properties[event_result.property_value] = value
            for _ in range(count):
                time.sleep(.001)
                self.split_client.track(key, self.traffic_type, event_result.event_type, value, properties)

    def key(self, position):
        return self.key_pattern.format(position=position)

    def register(self, eventType, properties={}, property_value=None):
        event_result = EventResult(eventType, properties, property_value=property_value)
        self.event_results.append(event_result)
        return event_result