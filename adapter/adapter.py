from ocp_vscode import show_object

from .base import make_base
from .defaults import (
    add_nut_holder,
    base_diameter,
    base_height,
    base_thread_depth,
    base_thread_size,
    num_tabs,
    tab_base_width,
    tab_height,
    tab_hole_diameter,
    tab_spacing,
    tab_width,
)
from .tab_assembly import make_tab_assembly


def make_adapter(
    base_diameter,
    base_height,
    base_thread_size,
    base_thread_depth,
    tab_width,
    tab_height,
    tab_base_width,
    tab_hole_diameter,
    tab_spacing,
    num_tabs,
    nut_holder,
):
    base = make_base(
        base_diameter=base_diameter,
        base_height=base_height,
        base_thread_size=base_thread_size,
        base_thread_depth=base_thread_depth,
    )
    tab_assembly = make_tab_assembly(
        tab_width=tab_width,
        tab_height=tab_height,
        tab_base_width=tab_base_width,
        tab_hole_diameter=tab_hole_diameter,
        tab_spacing=tab_spacing,
        base_height=base_height,
        num_tabs=num_tabs,
        add_nut_holder=nut_holder,
    )
    return base.union(tab_assembly)


if __name__ == "__main__":
    adapter = make_adapter(
        base_diameter=base_diameter,
        base_height=base_height,
        base_thread_size=base_thread_size,
        base_thread_depth=base_thread_depth,
        tab_width=tab_width,
        tab_height=tab_height,
        tab_base_width=tab_base_width,
        tab_hole_diameter=tab_hole_diameter,
        tab_spacing=tab_spacing,
        num_tabs=num_tabs,
        nut_holder=add_nut_holder,
    )
    show_object(adapter)
