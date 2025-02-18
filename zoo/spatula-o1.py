import cadquery as cq
from ocp_vscode import show_object


def make_spatula():
    handle_length = 100.0  # Length of the spatula handle
    handle_width = 20.0  # Width of the spatula handle
    handle_thickness = 5.0  # Thickness of the spatula handle

    blade_length = 80.0  # Length of the blade
    blade_width_base = 60.0  # Width of the blade near the handle
    blade_width_tip = 80.0  # Width of the blade at the tip
    blade_thickness = 2.0  # Thickness of the blade

    fillet_radius = 2.0  # Radius for filleting handle edges
    chamfer_size = 1.0  # Chamfer size for blade edges

    # -----------------------------
    # Handle
    # -----------------------------
    handle = (
        cq.Workplane("XY")
        .rect(handle_width, handle_thickness, centered=True)
        .extrude(handle_length)
        # Fillet edges along the length for comfort
        .edges("|Z")
        .fillet(fillet_radius)
    )

    # -----------------------------
    # Blade
    # -----------------------------
    # We start creating the blade on a plane offset by 'handle_length' in Z,
    # so that it attaches to the end of the handle.

    blade = (
        cq.Workplane("XY")
        .workplane(offset=handle_length)  # Move up in Z to the handle's end
        .rect(blade_width_base, blade_thickness, centered=True)
        .workplane(
            offset=blade_length, invert=True
        )  # Offset again to create the tip cross-section
        .rect(blade_width_tip, blade_thickness, centered=True)
        .loft(combine=True)  # Loft between the two rectangles
        # Add a slight chamfer to the edges
        # .edges(">Z")
        # .chamfer(0.5)
        # .edges("<Z")
        # .chamfer(chamfer_size)
    )

    return handle.union(blade)


if __name__ == "__main__":
    object = make_spatula()
    show_object(object)
