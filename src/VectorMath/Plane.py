from __future__ import annotations
import numpy as np
from VectorMath.Line import Line
import vectormath as vmath


class Plane:
    origin: vmath.Vector3
    normal: vmath.Vector3

    def __init__(self, origin: vmath.Vector3 = vmath.Vector3(), normal: vmath.Vector3 = vmath.Vector3()):
        self.origin = origin
        self.normal = normal
        if self.normal.length != 0:
            self.normal = self.normal.normalize()

    def new_from_points(self, points: vmath.Vector3Array) -> Plane:
        if len(points) < 3:
            raise ValueError("Not enough points for plane definition.")

        self.origin: vmath.Vector3 = points[0]
        x: vmath.Vector3 = vmath.Vector3(points[1] - self.origin)
        y: vmath.Vector3 = vmath.Vector3(points[2] - self.origin)
        self.normal: vmath.Vector3 = vmath.Vector3(np.cross(x, y)).normalize()

        for p in points[3:]:
            if not self.on_plane(p):
                raise ValueError("The points do not lie in the same plane.")

        return self

    def on_plane(self, point: vmath.Vector3) -> bool:
        if np.dot(self.normal, (point - self.origin)) == 0:
            return True
        return False

    def above_plane(self, point: vmath.Vector3) -> bool:
        return (np.sign(np.dot((point - self.origin), self.normal))) > 0

    def get_line_intersection(self, line: Line) -> vmath.Vector3:
        if self.on_plane(line.p1) and self.on_plane(line.p2):
            raise ValueError("Line lies on plane.")
        if self.above_plane(line.p1) == self.above_plane(line.p2):
            raise ValueError("Plane does not cut line.")

        u = vmath.Vector3(line.p2 - line.p1)
        dot = np.dot(self.origin, u)

        w = vmath.Vector3(line.p1 - self.origin)
        fac = - np.dot(self.origin, w) / dot
        u *= fac
        return vmath.Vector3(line.p1 + u)


if __name__ == "__main__":
    Test = Plane().new_from_points(vmath.Vector3Array([
        vmath.Vector3([1, 0, 0]),
        vmath.Vector3([1, 1, 0]),
        vmath.Vector3([1, 0, 1]),
    ]))
    print("Origin is [1,0,0]: {}".format(Test.origin == vmath.Vector3([1, 0, 0])))
    print("Normal is [1,0,0]: {}".format(Test.origin == vmath.Vector3([1, 0, 0])))

    print("[2,0,0] is above Plane: {}".format(Test.above_plane(vmath.Vector3([2, 0, 0])) == True))
    print("[0,0,0] is below Plane: {}".format(Test.above_plane(vmath.Vector3([0, 0, 0])) == False))

    testLine = Line(vmath.Vector3([0, 0, 0]), vmath.Vector3([2, 2, 2]))
    print("Line cut plane at: {}".format(Test.get_line_intersection(testLine)))
