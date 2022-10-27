from __future__ import annotations

import vectormath
import vectormath as vmath
from VectorMath.Plane import Plane
from VectorMath.Line import Line
from typing import List


class Polygon:
    points: vmath.Vector3Array

    def __init__(self, points: vmath.Vector3Array):
        self.points = points

    def cut(self, plane: Plane) -> List[Polygon | None]:
        new_points: List[vmath.Vector3] = []
        discard: List[vmath.Vector3] = []
        for i in range(1, len(self.points) + 1):
            p0 = self.points[i - 1]
            if i == len(self.points):
                p1 = self.points[0]
            else:
                p1 = self.points[i]
            '''
            p0_above_plane = plane.above_plane(p0)
            p1_above_plane = plane.above_plane(p1)

            if not p0_above_plane:
                discard.append(p0)
                if p1_above_plane:
                    intersection = plane.ge
            else:
                new_points.append(p0)

            if not p0_above_plane == p1_above_plane:
                intersection = plane.get_line_intersection(Line(p0, p1))
                new_points
'''
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

        keep = None
        drop = None
        if len(new_points) > 0:
            keep = Polygon(vmath.Vector3Array(new_points))
        if len(discard) > 0:
            drop = Polygon(vmath.Vector3Array(discard))

        return [keep, drop]

    def __str__(self) -> str:
        data = ""
        for p in self.points:
            data += "{" + "\"x\": {}, \"y\": {}, \"z\": {}".format(p.x, p.y, p.z) + "},"

        return "[" + data[:-1] + "]"


def test___init__():
    points = vectormath.Vector3Array([
        vmath.Vector3([0, 0, 0]),
        vmath.Vector3([1, 0, 0]),
        vmath.Vector3([1, 1, 0]),
        vmath.Vector3([0, 1, 0]),
    ])
    poly = Polygon(points)
    assert (poly.points == points).all()


def test_cut_with_all_points_below_plane():
    polygon = Polygon(vmath.Vector3Array([
        vmath.Vector3([0, 0, 0]),
        vmath.Vector3([1, 0, 0]),
        vmath.Vector3([1, 1, 0]),
        vmath.Vector3([0, 1, 0])
    ]))
    plane = Plane(vmath.Vector3([2, 0, 0]), vmath.Vector3([1, 0, 0]))
    expectation = [
        None,
        Polygon(vmath.Vector3Array([
            vmath.Vector3([0, 0, 0]),
            vmath.Vector3([1, 0, 0]),
            vmath.Vector3([1, 1, 0]),
            vmath.Vector3([0, 1, 0])
        ]))
    ]
    assert (polygon.cut(plane)[0] == expectation[0])
    assert (polygon.cut(plane)[1].points == expectation[1].points).all()


def test_cut_with_all_points_above_plane():
    polygon = Polygon(vmath.Vector3Array([
        vmath.Vector3([0, 0, 0]),
        vmath.Vector3([1, 0, 0]),
        vmath.Vector3([1, 1, 0]),
        vmath.Vector3([0, 1, 0])
    ]))
    plane = Plane(vmath.Vector3([-1, 0, 0]), vmath.Vector3([1, 0, 0]))
    expectation = [
        Polygon(vmath.Vector3Array([
            vmath.Vector3([0, 0, 0]),
            vmath.Vector3([1, 0, 0]),
            vmath.Vector3([1, 1, 0]),
            vmath.Vector3([0, 1, 0])
        ])),
        None
    ]
    assert (polygon.cut(plane)[0].points == expectation[0].points).all()
    assert (polygon.cut(plane)[1] == expectation[1])


def test_cut_with_half_the_points_above_plane():
    polygon = Polygon(vmath.Vector3Array([
        vmath.Vector3([0, 0, 0]),
        vmath.Vector3([1, 0, 0]),
        vmath.Vector3([1, 1, 0]),
        vmath.Vector3([0, 1, 0])
    ]))
    plane = Plane(vmath.Vector3([0.5, 0, 0]), vmath.Vector3([1, 0, 0]))
    expectation = [
        Polygon(vmath.Vector3Array([
            vmath.Vector3([0.5, 0, 0]),
            vmath.Vector3([1, 0, 0]),
            vmath.Vector3([1, 1, 0]),
            vmath.Vector3([0.5, 1, 0])
        ])),
        Polygon(vmath.Vector3Array([
            vmath.Vector3([0, 0, 0]),
            vmath.Vector3([0.5, 0, 0]),
            vmath.Vector3([0.5, 1, 0]),
            vmath.Vector3([0, 1, 0])
        ]))
    ]
    assert (polygon.cut(plane)[0].points == expectation[0].points).all()
    assert (polygon.cut(plane)[1].points == expectation[1].points).all()
