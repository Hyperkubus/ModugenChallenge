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


if __name__ == "__main__":
    points = [[0, 0, 0], [10, 0, 0], [4, 5, 0], [10, 10, 0], [0, 10, 0]]
    polygon = Polygon(vmath.Vector3Array(points))
    plane = Plane(vmath.Vector3([5, 0, 0]), vmath.Vector3([1, 0, 0]))
    cut_data = polygon.cut(plane)
    print(cut_data[0])
    print(cut_data[1])
