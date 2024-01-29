import bpy

#Read the data
filepath = r'F:\Blender_Projects\tutorial.txt'

data = dict()
with open(filepath, 'r') as txt_file:
    for idx, line in enumerate(txt_file.readlines()):
        if idx > 0:
            line = line.rstrip('\n')
            day = line.split(',')[0]
            hours_worked = line.split(',')[1]
            
            data[idx] = {
                'label': day,
                'value': hours_worked
            }

# Clean up scene     
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj)

text_thickness = 2
bevel_depth = 0.01
text_offset = 0.6

max_value = -999999
min_value = 999999
# Visualize data
for idx, data_entry in enumerate(data):
    # Create a bar
    height = float(data[data_entry]['value'])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,idx,0))
    bpy.ops.transform.resize(value=(1, 1, height), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
    bpy.ops.transform.translate(value=(0, 0, height/2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)

    # Label the bar
    label = data[data_entry]['label']
    bpy.ops.object.text_add(enter_editmode=True, location=(text_offset, idx-0.5, 0))
    bpy.ops.font.delete(type='PREVIOUS_WORD')
    bpy.ops.font.text_insert(text=label)
    bpy.ops.object.editmode_toggle()
    
    bpy.context.object.data.bevel_depth = bevel_depth
    bpy.ops.transform.resize(value=(1, 1, text_thickness), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)

    max_value = max(height, max_value)
    min_value = min(height, max_value)
    

# Tick marks on bar charts just quick and dirty with cubes
amount_of_ticks = 10
tick_thickness = 0.1
tick_offset = -2
letter_width = -0.5
step = (max_value - min_value) / (amount_of_ticks - 2)

for i in range(amount_of_ticks):
    # Put a cube
    current_value  = min_value + (i * step)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,tick_offset, current_value))
    bpy.ops.transform.resize(value=(1, 1, tick_thickness), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)

    # Put a number
    num_pos_z = current_value + (tick_thickness/2) + (bevel_depth * text_thickness)
    value_string = str(round(current_value, 2))
    
    bpy.ops.object.text_add(enter_editmode=True, location=(0,tick_offset + (len(value_string) * letter_width) - 0.125, num_pos_z))
    bpy.ops.font.delete(type='PREVIOUS_WORD')
    bpy.ops.font.text_insert(text=value_string)
    bpy.ops.object.editmode_toggle()
    
    bpy.context.object.data.bevel_depth = bevel_depth
    bpy.ops.transform.resize(value=(1, 1, text_thickness), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)

    bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)