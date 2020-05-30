import bpy 


#from .utils import addon_auto_imports

bl_info = {   ###für export als addon
    "name" : "Blend2RaspLight",
    "author" : "Modicolitor",
    "version" : (0,7),
    "blender" : (2, 82, 0),
    "location" : "View3D > Tools",
    "description" : "Cut your Objects into pieces and get Connectors to fit parts after Printing",
    "category" : "Object"}


from .blend2json import BJ_OT_BlinktElementsGenOperator
from .blend2json import BJ_OT_KeyframesjasonOperator
from .blend2json import BJ_PT_Blend2BlinkUI




classes = (BJ_OT_BlinktElementsGenOperator,
           BJ_OT_KeyframesjasonOperator,
           BJ_PT_Blend2BlinkUI,
            ) 
#classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)
        