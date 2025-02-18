import cadquery as cq
from ocp_vscode import show_object


def make_spatula():
    # Spatula Parameters
    # Handle dimensions
    handle_length = 150.0  # mm
    handle_width = 20.0  # mm
    handle_thickness = 5.0  # mm

    # Head dimensions
    head_length = 80.0  # mm
    head_width = 100.0  # mm
    head_thickness = 3.0  # mm
    head_fillet = 10.0  # mm

    # --- Create the Handle ---
    handle = cq.Workplane("XY").box(handle_length, handle_width, handle_thickness)

    # --- Create the Head ---
    # First, create a 2D rectangular profile
    head_profile = cq.Workplane("XY").rect(head_length, head_width, centered=True)

    # Extrude the profile to form a solid, then fillet the vertical edges.
    # You can adjust the edge selection (here we select edges parallel to the Z-axis).
    head = head_profile.extrude(head_thickness).edges("|Z").fillet(head_fillet)

    # --- Position the Head ---
    # Translate the head so that it attaches smoothly to one end of the handle.
    # Adjust the translation along the X-axis so that the head overlaps slightly with the handle.
    head = head.translate(
        (
            (handle_length / 2) + (head_length / 2) - 5,  # X-offset (overlap by 5mm)
            0,  # Y-offset
            (handle_thickness - head_thickness) / 2,  # Center in Z
        )
    )

    return handle.union(head)


if __name__ == "__main__":
    object = make_spatula()
    show_object(object)
