from defaults import (
    add_nut_holder,
    base_height,
    num_tabs,
    nut_base_height,
    nut_depth,
    nut_diameter,
    nut_outer_diameter,
    nut_teeth,
    tab_base_width,
    tab_height,
    tab_hole_diameter,
    tab_spacing,
    tab_width,
)
from nut_holder import make_nut_holder
from ocp_vscode import show_object
from tab import make_tab


def make_tab_assembly(
    tab_width,
    tab_height,
    tab_base_width,
    tab_hole_diameter,
    tab_spacing,
    base_height,
    num_tabs,
    add_nut_holder,
):
    if num_tabs < 1:
        raise ValueError("Number of tabs must be at least 1")

    tab = make_tab(
        tab_width=tab_width,
        tab_height=tab_height,
        tab_base_width=tab_base_width,
        tab_hole_diameter=tab_hole_diameter,
    )

    total_spacing = tab_width + tab_spacing
    total_width = (num_tabs * tab_width) + ((num_tabs - 1) * tab_spacing)
    start_x = -total_width / 2

    assembly = None
    for i in range(num_tabs):
        x_pos = start_x + (i * total_spacing)
        current_tab = tab.translate((x_pos, 0, base_height))

        if assembly is None:
            assembly = current_tab
        else:
            assembly = assembly.union(current_tab)

    if add_nut_holder:
        cog = make_nut_holder(
            outer_diameter=nut_outer_diameter,
            base_height=nut_base_height,
            nut_diameter=nut_diameter,
            nut_teeth=nut_teeth,
            hole_diameter=tab_hole_diameter,
            nut_depth=nut_depth,
        )
        # Position the cog holder in front of the first tab's hole
        cog = cog.rotate((0, 0, 0), (1, 0, 0), 90)
        cog = cog.rotate((0, 0, 0), (0, 0, 1), 90)
        cog = cog.translate(
            (
                start_x - nut_base_height,
                0,
                base_height + tab_height - tab_base_width / 2,
            )
        )
        assembly = assembly.union(cog)

    return assembly


if __name__ == "__main__":
    object = make_tab_assembly(
        tab_width=tab_width,
        tab_height=tab_height,
        tab_base_width=tab_base_width,
        tab_hole_diameter=tab_hole_diameter,
        tab_spacing=tab_spacing,
        base_height=base_height,
        num_tabs=num_tabs,
        add_nut_holder=add_nut_holder,
    )
    show_object(object)
