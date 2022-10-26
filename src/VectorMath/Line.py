import numpy as np
import vectormath as vmath


class Line:
    p1: vmath.Vector3
    p2: vmath.Vector3

    def __len__(self):
        return np.linalg.norm(self.p2 - self.p1)

    def __init__(self, p1: vmath.Vector3, p2: vmath.Vector3):
        self.p1 = p1
        self.p2 = p2


