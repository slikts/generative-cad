from defaults import (
    base_height,
    num_tabs,
    tab_base_width,
    tab_height,
    tab_hole_diameter,
    tab_spacing,
    tab_width,
)
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
    )
    show_object(object)
