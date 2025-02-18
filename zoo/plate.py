import cadquery as cq
from ocp_vscode import show_object


def make_mounting_plate():
    # Convert inches to mm (CadQuery works in mm)
    length = 10 * 25.4
    width = 6 * 25.4
    thickness = 0.25 * 25.4
    corner_hole_dia = 0.25 * 25.4
    center_hole_dia = 4 * 25.4
    corner_fillet = 0.125 * 25.4

    # Offset from edges for corner holes
    hole_offset = 0.5 * 25.4

    # Create base plate
    plate = (
        cq.Workplane("XY")
        .box(length, width, thickness)
        .edges("|Z")
        .fillet(corner_fillet)
    )

    # Add corner holes
    plate = (
        plate.faces(">Z")
        .workplane()
        .pushPoints(
            [
                (length / 2 - hole_offset, width / 2 - hole_offset),
                (length / 2 - hole_offset, -width / 2 + hole_offset),
                (-length / 2 + hole_offset, width / 2 - hole_offset),
                (-length / 2 + hole_offset, -width / 2 + hole_offset),
            ]
        )
        .hole(corner_hole_dia)
    )

    # Add center hole
    plate = plate.faces(">Z").workplane().hole(center_hole_dia)

    return plate


if __name__ == "__main__":
    mounting_plate = make_mounting_plate()
    show_object(mounting_plate)
