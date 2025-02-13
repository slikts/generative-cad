import cadquery as cq
from ocp_vscode import show_object

from .defaults import tab_base_width, tab_height, tab_hole_diameter, tab_width


def make_tab(tab_width, tab_height, tab_base_width, tab_hole_diameter):
    tab_arc_radius = tab_base_width / 2
    tab_straight_height = tab_height - tab_arc_radius

    tab2d = (
        cq.Workplane("YZ")
        .moveTo(-tab_base_width / 2, 0)
        .lineTo(tab_base_width / 2, 0)
        .lineTo(tab_base_width / 2, tab_straight_height)
        .threePointArc((0, tab_height), (-tab_base_width / 2, tab_straight_height))
        .close()
    )
    tab3d = tab2d.extrude(tab_width)
    tab3d = (
        tab3d.faces(">X")
        .workplane()
        .center(0, tab_height - tab_base_width / 2)
        .hole(tab_hole_diameter)
    )
    return tab3d


if __name__ == "__main__":
    object = make_tab(
        tab_width=tab_width,
        tab_height=tab_height,
        tab_base_width=tab_base_width,
        tab_hole_diameter=tab_hole_diameter,
    )
    show_object(object)
