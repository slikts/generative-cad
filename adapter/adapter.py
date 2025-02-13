from base import make_base
from defaults import (
    base_diameter,
    base_height,
    base_thread_depth,
    base_thread_diameter,
    num_tabs,
    tab_base_width,
    tab_height,
    tab_hole_diameter,
    tab_spacing,
    tab_width,
)
from ocp_vscode import show_object
from tab_assembly import make_tab_assembly


def make_adapter(
    base_diameter,
    base_height,
    base_thread_diameter,
    base_thread_depth,
    tab_width,
    tab_height,
    tab_base_width,
    tab_hole_diameter,
    tab_spacing,
    num_tabs,
):
    base = make_base(
        base_diameter=base_diameter,
        base_height=base_height,
        base_thread_diameter=base_thread_diameter,
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
    )
    return base.union(tab_assembly)


if __name__ == "__main__":
    adapter = make_adapter(
        base_diameter=base_diameter,
        base_height=base_height,
        base_thread_diameter=base_thread_diameter,
        base_thread_depth=base_thread_depth,
        tab_width=tab_width,
        tab_height=tab_height,
        tab_base_width=tab_base_width,
        tab_hole_diameter=tab_hole_diameter,
        tab_spacing=tab_spacing,
        num_tabs=num_tabs,
    )
    show_object(adapter)
