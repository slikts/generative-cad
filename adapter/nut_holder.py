import cadquery as cq
from ocp_vscode import show_object

from .defaults import (
    nut_base_height,
    nut_depth,
    nut_diameter,
    nut_outer_diameter,
    nut_teeth,
    tab_hole_diameter,
)


def make_nut_holder(
    outer_diameter,
    base_height,
    nut_diameter,
    nut_teeth,
    hole_diameter,
    nut_depth,
):
    base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(base_height)

    # Create the cog profile - as a pocket
    nut_profile = cq.Workplane("XY").polygon(nut_teeth, nut_diameter).extrude(nut_depth)

    # Create the through-hole for the screw
    screw_hole = cq.Workplane("XY").circle(hole_diameter / 2).extrude(base_height)

    # Subtract the cog profile and screw hole from the base
    result = base.cut(nut_profile).cut(screw_hole)

    return result


if __name__ == "__main__":
    result = make_nut_holder(
        outer_diameter=nut_outer_diameter,
        base_height=nut_base_height,
        nut_diameter=nut_diameter,
        nut_teeth=nut_teeth,
        hole_diameter=tab_hole_diameter,
        nut_depth=nut_depth,
    )
    show_object(result)
