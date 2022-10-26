from __future__ import annotations
import vectormath as vmath
from VectorMath.Plane import Plane
from VectorMath.Line import Line
from typing import List


class Polygon:
    points: vmath.Vector3Array

    def __init__(self, points: vmath.Vector3Array):
        self.points = points

    def cut(self, plane: Plane) -> List[Polygon]:
        new_points: List[vmath.Vector3] = []
        discard: List[vmath.Vector3] = []
        for i in range(1, len(self.points)+1):
            p0 = self.points[i - 1]
            if i == len(self.points):
                p1 = self.points[0]
            else:
                p1 = self.points[i]

            p0abovePlane = plane.above_plane(p0)
            p1abovePlane = plane.above_plane(p1)

            if not p0abovePlane:
                discard.append(p0)
            else:
                new_points.append(p0)

            if not p0abovePlane == p1abovePlane:
                intersection = plane.get_line_intersection(Line(p0, p1))
                new_points

            if plane.above_plane(p0):
                new_points.append(p0)
                if not plane.above_plane(p1):
                    intersection = plane.get_line_intersection(Line(p0, p1))
                    new_points.append(intersection)
                    discard.append(intersection)
            elif plane.above_plane(p1):
                discard.append(p0)
                intersection = plane.get_line_intersection(Line(p0, p1))
                new_points.append(intersection)
                discard.append(intersection)
            else:
                discard.append(p0)

        return [Polygon(vmath.Vector3Array(new_points)), Polygon(vmath.Vector3Array(discard))]

    def __str__(self) -> str:
        data = ""
        for p in self.points:
            data += "{" + "\"x\": {}, \"y\": {}, \"z\": {}".format(p.x, p.y, p.z) + "},"

        return "[" + data[:-1] + "]"