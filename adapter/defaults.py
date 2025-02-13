bolt_length = 19
bolt_size = 5  # M5

base_diameter = 22
base_height = 16

tab_base_width = 15
tab_height = 22
tab_width = 3
tab_spacing = tab_width
tab_hole_diameter = bolt_size
num_tabs = 3

base_thread_size = "3/8 16"
base_thread_depth = 15

nut_diameter = 7.7
nut_outer_diameter = nut_diameter + 4
nut_teeth = 6
nut_depth = 3.7
nut_base_height = (
    nut_depth + bolt_length - num_tabs * tab_width - (num_tabs - 1) * tab_spacing
)
add_nut_holder = True
