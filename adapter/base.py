import cadquery as cq
from ocp_vscode import show_object

from .defaults import base_diameter, base_height, base_thread_depth, base_thread_size
from .vendor.Thread import thread, threads


def make_base(base_diameter, base_height, base_thread_size, base_thread_depth):
    base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

    if base_thread_size and base_thread_depth:
        if isinstance(base_thread_size, str):
            thread_spec = threads[base_thread_size]
            base = (
                base.faces("<Z")
                .workplane()
                .hole(thread_spec.Dmajor, depth=base_thread_depth)
            )
            threaded = thread(base_thread_size, base_thread_depth, location="internal")
            base = base.union(threaded)
        else:
            base = (
                base.faces("<Z")
                .workplane()
                .hole(base_thread_size, depth=base_thread_depth)
            )

    return base


if __name__ == "__main__":
    object = make_base(
        base_diameter=base_diameter,
        base_height=base_height,
        base_thread_size=base_thread_size,
        base_thread_depth=base_thread_depth,
    )
    show_object(object)
