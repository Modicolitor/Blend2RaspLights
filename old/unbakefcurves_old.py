
#####################################
# unbake ¿? f-curve to a new action #
#####################################

# Broken!!!!!!!!!!!!
import bpy
obj = bpy.context.object

for c in obj.animation_data.action.fcurves:
    if c.sampled_points and c.select:
        obj.animation_data.action = bpy.data.actions.new(name='Lot_of_Keys')
        fcu = obj.animation_data.action.fcurves.new(
            data_path=c.data_path, index=c.array_index)
        sam = c.sampled_points
        fcu.keyframe_points.add(len(sam))
        for i in range(len(sam)):
            w = fcu.keyframe_points[i]
            w.co = w.handle_left = w.handle_right = sam[i].co
