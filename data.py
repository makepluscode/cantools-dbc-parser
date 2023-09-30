class Message:
    name, sender = None, None
    frame_id, length = 0, 0
    is_fd, is_container = False, False

    def __init__(self, name, sender, frame_id, length, is_fd, is_container):
        self.name = name
        self.sender = sender
        self.frame_id = frame_id
        self.length = length
        self.is_fd = is_fd
        self.is_container = is_container


class Signal:
    name, sender = None, None
    receiver = None
    len = 0
    min, max = 0.0, 0.0
    unit = None

    def __init__(self, name, sender, receiver, len, min, max, unit):
        self.name = name
        self.sender = sender
        self.receiver = receiver
        self.len = len
        self.min = min
        self.max = max
        self.unit = unit
