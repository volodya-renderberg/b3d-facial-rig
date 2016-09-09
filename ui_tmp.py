# <pep8 compliant>

file_data = '''
import bpy

rig_id = "%s"

class FaceLayers(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Face Layers"
    bl_idname = rig_id + "_Face_rig_layers"

    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=19, toggle=True, text='main')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=20, toggle=True, text='mimics')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=21, toggle=True, text='stretch squash')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=24, toggle=True, text='tmp')
        
        row = layout.row(align = True)
        row.operator("facial_rig.on_off_limits_" + rig_id, text = 'Off Eye Limits').action = 'off'
        row.operator("facial_rig.on_off_limits_" + rig_id, text = 'On Eye Limits').action = 'on'
        
class FaceLayers_on_off_limits(bpy.types.Operator):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "On Off Eye Limits"
    bl_idname = "facial_rig.on_off_limits_" + rig_id
    
    action = bpy.props.StringProperty()
    
    def execute(self, context):
        on_off_limits(context, self.action)
    
        self.report({'INFO'}, self.action)
        return{'FINISHED'}
        
def on_off_limits(context, action):
    # name of constraints
    r_cns_name = 'r_eye_limit_rotation'
    l_cns_name = 'l_eye_limit_rotation'
    
    # get bones
    eye_bone_r = context.object.pose.bones['FR_eye_R']
    eye_bone_l = context.object.pose.bones['FR_eye_L']
    
    # get constraints
    r_cns = eye_bone_r.constraints[r_cns_name]
    l_cns = eye_bone_l.constraints[l_cns_name]

    pass
    if action == 'on':
        r_cns.use_limit_x = True
        l_cns.use_limit_x = True
        r_cns.use_limit_z = True
        l_cns.use_limit_z = True
    elif action == 'off':
        r_cns.use_limit_x = False
        l_cns.use_limit_x = False
        r_cns.use_limit_z = False
        l_cns.use_limit_z = False

def register():
    bpy.utils.register_class(FaceLayers)
    bpy.utils.register_class(FaceLayers_on_off_limits)
    
def unregister():
    bpy.utils.unregister_class(FaceLayers)
    bpy.utils.unregister_class(FaceLayers_on_off_limits)
    
register()

'''