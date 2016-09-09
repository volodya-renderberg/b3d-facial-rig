#
#
#
#

bl_info = {
	"name": "Facial Rig",
	"description": "Automatic rigging from building-block components, interface for settings",
	"author": "Volodya Renderberg",
	"version": (1, 0),
	"blender": (2, 76, 0),
	"location": "View3d tools panel",
	"warning": "", # used for warning icon and text in addons panel
	"category": "Rigging"}

if "bpy" in locals():
    import importlib
    #importlib.reload(tmp_armature_create)
    #importlib.reload(face_rig_create)
    importlib.reload(ui)
else:
    #from . import tmp_armature_create
    #from . import face_rig_create
    from . import ui

import bpy


##### REGISTER #####

def register():
	#bpy.utils.register_module(__name__)
    #tmp_armature_create.register()
    ui.register()
	
def unregister():
	#tmp_armature_create.unregister()
	ui.unregister()
	#bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
    register()

