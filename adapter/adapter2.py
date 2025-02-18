import cadquery as cq
from ocp_vscode import show_object


def make_rod():
    # Create a round bar with specified dimensions
    rod = (
        cq.Workplane("XY")
        .circle(9.5 / 2)  # Diameter of 9.5mm (radius = diameter/2)
        .extrude(20)  # Length of 20mm
        .edges()
        .chamfer(0.5)  # C1 chamfer on corners
    )
    return rod


if __name__ == "__main__":
    object = make_rod()
    show_object(object)
