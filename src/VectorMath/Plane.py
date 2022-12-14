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
        """Checks if point is on plane"""
        if np.dot(self.normal, (point - self.origin)) == 0:
            return True
        return False

    def above_plane(self, point: vmath.Vector3) -> bool:
        """Check if point is above plane"""
        return (np.sign(np.dot((point - self.origin), self.normal))) > 0

    """finds intersection point between line and point"""
    def get_line_intersection(self, line: Line) -> vmath.Vector3:
        if self.on_plane(line.p1) and self.on_plane(line.p2):
            raise ValueError("Line lies on plane.")
        if self.above_plane(line.p1) == self.above_plane(line.p2):
            raise ValueError("Plane does not cut line.")

        """Taken from https://stackoverflow.com/questions/5666222/3d-line-plane-intersection"""
        u = vmath.Vector3(line.p2 - line.p1)
        dot = np.dot(self.origin, u)

        w = vmath.Vector3(line.p1 - self.origin)
        fac = - np.dot(self.origin, w) / dot
        u *= fac
        return vmath.Vector3(line.p1 + u)