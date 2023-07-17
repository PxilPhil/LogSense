event_map = dict()
class EventData:
    def __init__(self, timestamp, change, value, is_event):
        self.timestamp = timestamp
        self.change = change
        self.value = value
        self.is_event = is_event
