import cadquery as cq
from ocp_vscode import show_object


def make_bracket():
    # Bracket dimensions
    length = 80.0
    width = 40.0
    height = 40.0
    thickness = 3.0
    hole_diameter = 6.0
    hole_margin = 10.0

    # Create base L bracket
    bracket = (
        cq.Workplane("XY")
        .box(length, width, thickness)
        .faces(">Z")
        .workplane()
        .transformed(offset=(0, width / 2))
        .box(length, thickness, height)
    )

    # Add mounting holes in horizontal face
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints(
            [
                (-length / 2 + hole_margin, -width / 2 + hole_margin),
                (length / 2 - hole_margin, -width / 2 + hole_margin),
            ]
        )
        .hole(hole_diameter)
    )

    # Add mounting holes in vertical face
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints(
            [
                (-length / 2 + hole_margin, height / 2 - hole_margin),
                (length / 2 - hole_margin, height / 2 - hole_margin),
            ]
        )
        .hole(hole_diameter)
    )

    return bracket


if __name__ == "__main__":
    object = make_bracket()
    show_object(object)
