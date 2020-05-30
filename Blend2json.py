import json
import bpy

#from .utils import addon_auto_imports

bl_info = {  # für export als addon
    "name": "Blend2RaspLight",
    "author": "Modicolitor",
    "version": (0, 7),
    "blender": (2, 82, 0),
    "location": "View3D > Tools",
    "description": "Cut your Objects into pieces and get Connectors to fit parts after Printing",
    "category": "Object"}

# some JSON:
# x = json.loads() #####loads existing json string


# make 8 cubes make material


# make library of rgb values

# y = json.dumps(x) #python object to json string

# Operator
class BJ_OT_BlinktElementsGenOperator(bpy.types.Operator):

    bl_idname = "object.blinktelementsgen"
    bl_label = "BlinktElementsGen"

    def execute(self, context):
        data = bpy.data

        matbool = True

        mat = bpy.data.materials.get("BlinktPixel")
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="BlinktPixel")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links

            for node in nodes:
                nodes.remove(node)

            #nodeVal = nodes.new('ShaderNodeValue')
            #nodeVal.location = (-300,0)

            nodeEm = nodes.new('ShaderNodeEmission')

            nodeOut = nodes.new('ShaderNodeOutputMaterial')
            nodeOut.location = (300, 0)

            #links.new(nodeVal.outputs[0], nodeEm.inputs[1])
            links.new(nodeEm.outputs[0], nodeOut.inputs[0])

        for x in range(8):
            bpy.ops.mesh.primitive_cube_add(
                size=2, enter_editmode=False, location=(x*2.5, 0, 0))
            obj = context.object
            if obj.data.materials:
                # assign to 1st material slot
                obj.data.materials[0] = mat
            else:
             #  no slots
                obj.data.materials.append(mat)

        data.materials['BlinktPixel'].node_tree.nodes['Emission'].inputs[1].keyframe_insert(
            data_path="default_value", frame=1)

        return {'FINISHED'}


class BJ_OT_KeyframesjasonOperator(bpy.types.Operator):
    bl_idname = "object.bj_ot_keyframesjason"
    bl_label = "BJ_OT_Keyframesjason"

    def execute(self, context):
        data = bpy.data
        action = bpy.data.actions["Shader NodetreeAction"]
        keyframelist = []
        for fcu in action.fcurves:
            #print(fcu.data_path + " channel " + str(fcu.array_index))
            for keyframe in fcu.keyframe_points:
                ele = {
                    "x": keyframe.co.x,
                    "y": keyframe.co.y,
                    "r": data.materials["BlinktPixel"].node_tree.nodes["Emission"].inputs[0].default_value[0] * 255,
                    "g": data.materials["BlinktPixel"].node_tree.nodes["Emission"].inputs[0].default_value[1] * 255,
                    "b": data.materials["BlinktPixel"].node_tree.nodes["Emission"].inputs[0].default_value[2] * 255,


                }
                keyframelist.append(ele)

        jsonlist = json.dumps(keyframelist)
        print(jsonlist)

        f = open("Blend2BlinkTest.json", "w")
        f.write(jsonlist)
        f.close()

        #######

        return {'FINISHED'}


# UI
class BJ_PT_Blend2BlinkUI(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Blend2RaspLights"
    bl_category = "Blend2RaspLights"

    # schreibe auf den Bildschirm

    def draw(self, context):

        data = bpy.data

        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0,
                                even_columns=False, even_rows=False, align=True)
        col = flow.column()
        row = layout.row()

        #col.template_ID(PUrP, "CenterObj", filter='AVAILABLE')

        subcol = col.column()
        #subcol.label(text="Coupling Mode")
        # subcol.label(text="AddingCouplings")

        subcol.operator("object.blinktelementsgen",
                        text="Make Blinkt! Pixels", icon="PLUS")  # zeige button an
        subcol.operator("object.bj_ot_keyframesjason",
                        text="KeyframeToJson", icon="PLUS")
        # subcol.label(text="Adjust")
        #subcol.operator("object.exchangecoup", text="Exchange", icon="FILE_REFRESH")
        # subcol.operator("object.activecoupdefault", text ='Active to Settings', icon ="EXPORT") ### ze

        # return {'FINISHED'}
