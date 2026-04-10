class HashRecord:
    def __init__(self):
        self.id = None
        self.pi = None
        self.u = 0
        self.d = 0
        self.c = 0
        self.t = 0
        self.p0 = None
        self.l = 0

    def __str__(self):
        id_str = str(self.id) if self.id else ""
        pi_str = str(self.pi) if self.pi else ""
        p0_str = str(self.p0) if self.p0 is not None else ""
        return f"{id_str:12} | {p0_str:4} | {self.l:1} | {self.u:1} | {self.d:1} | {self.t:1} | {self.c:1} | {pi_str}"
