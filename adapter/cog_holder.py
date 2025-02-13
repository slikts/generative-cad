import cadquery as cq
from defaults import (
    cog_base_height,
    cog_depth,
    cog_diameter,
    cog_outer_diameter,
    cog_teeth,
    tab_hole_diameter,
)
from ocp_vscode import show_object


def make_cog_holder(
    outer_diameter,
    base_height,
    cog_diameter,
    cog_teeth,
    hole_diameter,
    cog_depth,
):
    base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(base_height)

    # Create the cog profile - as a pocket
    cog_profile = (
        cq.Workplane("XY").polygon(cog_teeth, cog_diameter / 2).extrude(cog_depth)
    )

    # Create the through-hole for the screw
    screw_hole = cq.Workplane("XY").circle(hole_diameter / 2).extrude(base_height)

    # Subtract the cog profile and screw hole from the base
    result = base.cut(cog_profile).cut(screw_hole)

    return result


if __name__ == "__main__":
    result = make_cog_holder(
        outer_diameter=cog_outer_diameter,
        base_height=cog_base_height,
        cog_diameter=cog_diameter,
        cog_teeth=cog_teeth,
        hole_diameter=tab_hole_diameter,
        cog_depth=cog_depth,
    )
    show_object(result)
