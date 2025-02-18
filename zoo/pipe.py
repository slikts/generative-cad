import cadquery as cq
from ocp_vscode import show_object


def make_pipe():
    # Parameters for the pipe
    outer_diameter = 50.0
    inner_diameter = 40.0
    length = 100.0

    # Create the pipe using CadQuery
    pipe = (
        cq.Workplane("XY")
        .circle(outer_diameter / 2)
        .circle(inner_diameter / 2)
        .extrude(length)
    )

    return pipe


if __name__ == "__main__":
    object = make_pipe()
    show_object(object)
