import math

import cadquery as cq
from ocp_vscode import show_object


def make_bearing():
    # Convert inches to mm
    shaft_diameter = 0.75 * 25.4

    # Bearing parameters
    outer_diameter = shaft_diameter * 2.2  # Common ratio for bearings
    bearing_width = shaft_diameter * 0.8
    ball_diameter = (outer_diameter - shaft_diameter) * 0.25
    num_balls = 8

    # Create inner race
    inner_race = (
        cq.Workplane("XY")
        .circle(shaft_diameter / 2 + ball_diameter / 4)
        .extrude(bearing_width)
    )

    # Create outer race
    outer_race = (
        cq.Workplane("XY")
        .circle(outer_diameter / 2)
        .circle(outer_diameter / 2 - ball_diameter / 2)
        .extrude(bearing_width)
    )

    # Create balls
    balls = []
    for i in range(num_balls):
        angle = (2 * math.pi * i) / num_balls
        radius = (outer_diameter / 2 + shaft_diameter / 2) / 2
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        ball = (
            cq.Workplane("XY")
            .sphere(ball_diameter / 2)
            .translate((x, y, bearing_width / 2))
        )
        balls.append(ball)

    # Combine all balls
    all_balls = balls[0]
    for ball in balls[1:]:
        all_balls = all_balls.union(ball)

    # Final assembly
    bearing = inner_race.union(outer_race).union(all_balls)

    return bearing


if __name__ == "__main__":
    object = make_bearing()
    show_object(object)
