import vectormath as vmath
from pydantic import BaseModel
from typing import List


class Point(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0

    def to_vector3(self):
        return vmath.Vector3(self.x, self.y, self.z)


class Polygon(BaseModel):
    points: List[Point]

    def to_vector3array(self):
        plist = []
        for p in self.points:
            plist.append(p.to_vector3())
        return vmath.Vector3Array(plist)


class Plane(BaseModel):
    origin: Point
    normal: Point


class Cut(BaseModel):
    polygon: Polygon
    plane: Plane
    keepAllParts: bool = False
