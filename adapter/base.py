import cadquery as cq
from defaults import base_diameter, base_height, base_thread_depth, base_thread_diameter
from ocp_vscode import show_object


def make_base(base_diameter, base_height, base_thread_diameter, base_thread_depth):
    base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)
    base = (
        base.faces("<Z").workplane().hole(base_thread_diameter, depth=base_thread_depth)
    )
    return base


if __name__ == "__main__":
    object = make_base(
        base_diameter=base_diameter,
        base_height=base_height,
        base_thread_diameter=base_thread_diameter,
        base_thread_depth=base_thread_depth,
    )
    show_object(object)
