class TrackingClient(object):
    def __init__(self):
        super(TrackingClient, self).__init__()
        self.events = []
        self.keys = {}
    
    def track(self, key, traffic_type, event_type, value, properties, valueProp=None):
        self.events.append((key, traffic_type, event_type, value, properties))
        track = self.keys.get(key, {})
        track['count'] = track.get('count', 0) + 1
        if valueProp is None:
            track['sum'] = track.get('sum', 0) + value
        elif properties.contains(valueProp):
            track['sum'] = track.get('sum', 0) + properties.get(valueProp)
        self.keys[key] = track
    
    def rate_mean(self, sample):
        return self.mean(sample, lambda x: 1)
    
    def count_mean(self, sample):
        return self.mean(sample, lambda x: x['count'])
    
    def sum_mean(self, sample):
        return self.mean(sample, lambda x: x['sum'])
    
    def average_mean(self, sample):
        return self.mean(sample, lambda x: x['sum'] / x['count'])

    def mean(self, sample, extractor):
        distribution = map(extractor, self.keys.values())
        return sum(distribution) / sample