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
        print(t.text)
        t.chng_text("something")
        print(t.text)

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


# filename for the uia
bpy.types.Scene.BlinktFilename = bpy.props.StringProperty(
    name="Filename",
    description="Filename of next Jso",
    default=".json"
)


def clampvalue(value):
    if value > 1:
        value = 1
    elif value < 0:
        value = 0

    return value


def get_matinfo(context):
    depsgraph = context.evaluated_depsgraph_get()
    obeval = context.object.evaluated_get(depsgraph)
    emnode = obeval.material_slots[0].material.node_tree.nodes['Emission']

    r = clampvalue(emnode.inputs[0].default_value[0]) * 255
    g = clampvalue(emnode.inputs[0].default_value[1]) * 255
    b = clampvalue(emnode.inputs[0].default_value[2]) * 255

    strength = clampvalue(emnode.inputs[1].default_value)

    return strength, r, g, b


def readoutframedata(context):

    #oricurrentframe = context.scene.frame_current

    frame_start = context.scene.frame_start
    frame_end = context.scene.frame_end

    # set current frame
    context.scene.frame_current = frame_start

    # selected handling

    # go through the range and collect the data
    framelist = []
    while context.scene.frame_current <= frame_end:

        strength, r, g, b = get_matinfo(context)
        print()
        #action = bpy.data.actions["Shader NodetreeAction"]
        ele = {
            "x": context.scene.frame_current,
            "y": strength,
            "r": r,
            "g": g,
            "b": b,


        }
        framelist.append(ele)

        context.scene.frame_current += 1

        '''
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
        '''
        jsonlist = json.dumps(framelist)
        print(jsonlist)

        # path to blendfile + user filename
        filepath = bpy.path.abspath("//") + context.scene.BlinktFilename
        f = open(filepath, "w")
        f.write(jsonlist)
        f.close()


class BJ_OT_KeyframesjasonOperator(bpy.types.Operator):
    bl_idname = "object.bj_ot_keyframesjason"
    bl_label = "BJ_OT_Keyframesjason"

    def execute(self, context):
        data = bpy.data

        #######
        readoutframedata(context)
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

        subcol.prop(context.scene, "BlinktFilename", text="")
        subcol.operator("object.bj_ot_keyframesjason",
                        text="KeyframeToJson", icon="PLUS")
        # subcol.label(text="Adjust")
        #subcol.operator("object.exchangecoup", text="Exchange", icon="FILE_REFRESH")
        # subcol.operator("object.activecoupdefault", text ='Active to Settings', icon ="EXPORT") ### ze

        # return {'FINISHED'}


classes = (BJ_OT_BlinktElementsGenOperator,
           BJ_OT_KeyframesjasonOperator,
           BJ_PT_Blend2BlinkUI)

register, unregister = bpy.utils.register_classes_factory(classes)

# testing non-bound classes in blender


class test():
    def __init__(self):
        self.text = "I'm a non Blender object"

    def chng_text(self, text):
        self.text = text


t = test()

print(t.text)
t.chng_text("something")
print(t.text)
