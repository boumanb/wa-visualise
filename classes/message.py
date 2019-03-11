class Message:

    def __init__(self, raw, dt_stamp, send_by, message):
        self.raw = raw
        self.dt_stamp = dt_stamp
        self.send_by = send_by
        self.message = message