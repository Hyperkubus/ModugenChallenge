from fastapi import FastAPI
from ApiModels import cut
from VectorMath.Plane import Plane
from VectorMath.Polygon import Polygon

app = FastAPI()


@app.post("/cut")
async def get_cut(json: cut.Cut):
    polygon = Polygon(json.polygon.to_vector3array())
    plane = Plane(json.plane.origin.to_vector3(), json.plane.normal.to_vector3())
    keep = json.keepAllParts
    cut_data = polygon.cut(plane)
    if not keep:
        return str(cut_data[0])
    return "[" + str(cut_data[0]) + ", " + str(cut_data[1]) + "]"
