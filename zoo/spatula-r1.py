import cadquery as cq
from ocp_vscode import show_object


def make_spatula():
    handle_width = 25  # Y direction
    handle_thickness = 15  # Z direction
    handle_length = 100  # X direction
    handle_fillet = 5  # Fillet radius for handle edges

    neck_width = 15  # Y direction
    neck_thickness = 5  # Z direction
    neck_length = 50  # X direction
    neck_fillet = 3  # Fillet radius for neck edges

    head_width = 50  # Y direction
    head_height = 80  # Z direction
    head_thickness = 2  # X direction
    head_fillet_radius = 10  # Fillet radius for head tip

    # Create handle
    handle = (
        cq.Workplane("YZ")
        .rect(handle_width, handle_thickness)
        .extrude(handle_length)
        .edges("|X")  # Select edges parallel to X-axis
        .fillet(handle_fillet)
    )

    # Create neck
    neck = (
        handle.faces(">X")
        .workplane()
        .rect(neck_width, neck_thickness)
        .extrude(neck_length)
        .edges("|X")  # Select edges parallel to X-axis
        .fillet(neck_fillet)
    )

    # Create head with rounded tip
    head = (
        neck.faces(">X")
        .workplane()
        .rect(head_width, head_height)
        .extrude(head_thickness)
        .edges(">X")  # Select edges on the front face of the head
        .fillet(head_fillet_radius)
    )

    # Combine all parts
    spatula = handle.union(neck).union(head)

    return spatula


if __name__ == "__main__":
    object = make_spatula()
    show_object(object)
