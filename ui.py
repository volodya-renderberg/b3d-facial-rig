#

import bpy
from .tmp_armature_create import TMP_create  # 
from .face_rig_create import passport  # 
from .face_rig_create import face_armature  # 
from .face_rig_create import face_shape_keys  # 
from .face_rig_create import eye_limits  # 
import webbrowser

class G(object):
	import_single_panel = False
	import_single_from_all_panel = False
	recalculate_single_brows_vtx_group_panel = False
	
	targets_list = [('None',)*3]
	brows_vtx_list = [('None',)*3]
	
	face_armature = face_armature()
	face_shape_keys = face_shape_keys()
	
	def rebild_targets_list(self, context):
		###
		G.targets_list = []
		list_shape_keys = get_data_class().get_list_shape_keys(context, only_origin = 0)
		for key in list_shape_keys:
			G.targets_list.append((key,)*3)
		###
		G.brows_vtx_list = []
		for key in G.face_shape_keys.brows_vertex_groups:
			G.brows_vtx_list.append((key,)*3)
		###
		set_targets_list()

def set_targets_list():
	bpy.types.Scene.my_num_of_between = bpy.props.IntProperty(name = 'Num of Between:', min = 1, default = 1)
	bpy.types.Scene.my_targets_list_enum = bpy.props.EnumProperty(items = G.targets_list, name = 'Targets:', update = None)
	bpy.types.Scene.brows_vtx_list = bpy.props.EnumProperty(items = G.brows_vtx_list, name = 'Vertex_Groups:', update = None)

class get_data_class():
	def __init__(self):
		self.data = []
			
	def get_list_shape_keys(self, context,  only_origin = 1):
		central_sh_keys = ['jaw_open_C', 'jaw_side_R', 'lip_side.r', 'jaw_fwd', 'jaw_back', 'lip_down', 'lip_raise', 'lip_funnel', 'lip_close']
		#print('\n'*3, face_shape_keys().central_side_shape_keys)
		fshk = face_shape_keys()
		try:
			keys = fshk.central_side_shape_keys.keys()
			list_sh_keys = list(keys)
			list_sh_keys = list_sh_keys + central_sh_keys
			if not only_origin:
				inbetweens_keys = passport().read_passport(context, 'list_of_inbetweens')
				if inbetweens_keys[0]:
					list_inbetweens = []
					for key in inbetweens_keys[1]:
						for k in inbetweens_keys[1][key]:
							list_inbetweens.append(key + str(round(k, 2)).replace('0', ''))
					list_sh_keys = list_sh_keys + list_inbetweens
			# finish
			list_sh_keys.sort()
			return list_sh_keys
		except:
			return(self.data)
		
class FACIALRIG_Help(bpy.types.Panel):
	bl_idname = "face_rig.help_panel"
	bl_label = "Help"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	layout = 'HELP'
	#bl_options = {'DEFAULT_CLOSED'}
		
	def draw(self, context):
		layout = self.layout

		#layout.label("Mesh Passport")
		col = layout.column(align=1)
		col.operator("face_rig.help",icon = 'QUESTION', text = 'Manual').action = 'manual'
		col.operator("face_rig.help",icon = 'QUESTION', text = 'Youtube(ru)').action = 'youtube_ru'

class FACIALRIG_MakeRig(bpy.types.Panel):
	bl_idname = "face_rig.tools_panel"
	bl_label = "Make Rig"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	layout = 'MAKE_RIG'
	bl_options = {'DEFAULT_CLOSED'}
		
	mesh_keys = face_armature().mesh_passp_bones.keys()
	
	def draw(self, context):
		#mesh_keys = ['body', 'eye_r', 'eye_l', 'tongue']
		layout = self.layout

		layout.label("Mesh Passport")
		col_passp = layout.column(align=1)
		col_passp.operator("passport.object_add", text = 'body').key_passp = 'body'
		for key in self.mesh_keys:
			col_passp.operator("passport.object_add", text = key).key_passp = key
		layout.operator("passport.object_add", text = 'Print Passport').key_passp = ''

		layout.label("Armature")
		col = layout.column(align=1)
		col.operator("face_rig.tmp_create", icon='OUTLINER_OB_ARMATURE', text = 'Create Meta Rig')
		col.operator("face_rig.generate", icon='OUTLINER_OB_ARMATURE', text = 'Face Rig Generate')
		col.operator("face_rig.linear_jaw_driver", icon='OUTLINER_OB_ARMATURE', text = 'Add Linear Driver For Jaw')
		row = col.row(align = True)
		row.operator('face_rig.toggle_deform_bone', text = 'Off Deform').action = 'off'
		row.operator('face_rig.toggle_deform_bone', text = 'On Deform').action = 'on'
		col.operator("face_rig.clear_skin", icon='MOD_ARMATURE', text = 'Clear Body Skin').mesh = 'BODY'
		col.operator("body_weight.paint", icon='WPAINT_HLT', text = 'Jaw Paint').target = 'FR_jaw'
		
		layout.label("Lattice")
		colmn = layout.column(align=1)
		colmn.operator("lattice.deform_generate", icon='OUTLINER_OB_LATTICE', text = 'Create Lattice Deform')
		row = colmn.row(align = True)
		row.operator('facial_rig.toggle_lattice_visible', text = 'Unhide Lattice').action = 'on'
		row.operator('facial_rig.toggle_lattice_visible', text = 'Hide Lattice').action = 'off'
		colmn.operator("body_weight.paint", icon='WPAINT_HLT', text = 'Str_Sq Paint').target = 'str_squash'
		colmn.operator("body_weight.paint", icon='WPAINT_HLT', text = 'Eye_R Paint').target = 'lattice_eye_r'
		colmn.operator("body_weight.paint", icon='WPAINT_HLT', text = 'Eye_L Paint').target = 'lattice_eye_l'
		colmn.operator("edit.lattice", icon='OUTLINER_OB_LATTICE', text = 'Recalculate Eye Weight')
		
		layout.label("Eye Limits")
		col_lim = layout.column(align=1)
		col_lim.operator("eye_limits.set_limits", text = 'Set Start').action = 'start'
		col_lim.operator("eye_limits.set_limits", text = 'Set Low').action = 'low'
		col_lim.operator("eye_limits.set_limits", text = 'Set Up').action = 'up'
		col_lim.operator("eye_limits.set_limits", text = 'Set Right').action = 'right'
		col_lim.operator("eye_limits.set_limits", text = 'Apply').action = 'apply'

		layout.label("Position of Controls")
		col_pos = layout.column(align = 1)
		col_pos.operator("lock.controls", icon='NONE', text = 'Unlock Root').action = 'unlock'
		col_pos.operator("lock.controls", icon='NONE', text = 'Lock Root').action = 'lock'
		
		col_key = layout.column(align = 1)
		col_key.operator("lock.controls", icon='NONE', text = 'Keyframe Root Cnt').action = 'keying'
		
class FACIALRIG_ShapeKeys(bpy.types.Panel):
	bl_idname = "shape_keys.add_edit"
	bl_label = "Shape Keys"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	layout = 'Shape_Keys'
	
	def draw(self, context):
		layout = self.layout
		
		layout.label("Create")
		col_shk = layout.column(align=1)
		col_shk.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Shape Keys').action = 'create_shape_keys'
		col_shk.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Autolid').action = 'create_autolid'
		col_shk.operator("insert.inbetween", icon='SHAPEKEY_DATA', text = 'Add Inbetween')
		
		layout.label("Edit Shape Keys")
		col_eshk = layout.column(align=1)
		col_eshk.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Central To Side').action = 'central_to_side'
		col_eshk.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Recalculation Vertex Groups').action = 'recalculation'
		
		layout.label("Brows Shape Keys")
		col = layout.column(align=1)
		col.operator("shape_key.brows_all_vertex_groups", icon='SHAPEKEY_DATA', text = 'Recalculation All Vertex Groups').target = 'all'
		col.operator('shape_key.single_vertex_groups_open_panel').action = 'open'
		
		if G.recalculate_single_brows_vtx_group_panel:
			for name in G.face_shape_keys.brows_vertex_groups:
				row = col.row(align=1)
				row.label(name)
				row.operator("shape_key.brows_all_vertex_groups", icon='SHAPEKEY_DATA', text = 'To Recalculate').target = name
			row = col.row(align=1)
			row.operator('shape_key.single_vertex_groups_open_panel', text = 'close').action = 'close'
		
		layout.label("Sculpt Shape Keys")
		col_shk_list = layout.column(align = 1)
		list_shape_keys = get_data_class().get_list_shape_keys(context, only_origin = 0)
		for key in list_shape_keys:
			col_shk_list.operator("shape_key.edit", icon='SHAPEKEY_DATA', text = key).target = key
			
		
		
class FACIALRIG_import_export(bpy.types.Panel):
	bl_idname = "faceial_rig.import_export"
	bl_label = "Export/Import Data"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		layout = self.layout
		# singl
		col = layout.column(align = 1)
		col.operator("export.single_vertex_data", icon='SHAPEKEY_DATA', text = 'Export Single Shape')
		col.operator("import.single_data_open_panel", icon='SHAPEKEY_DATA', text = 'Import Single Shape').action = 'open'
		
		if G.import_single_panel:
			layout.label('Set import options:')
			#layout.prop(context.scene, "my_num_of_between")
			layout.prop(context.scene, "my_targets_list_enum")
			
			row = layout.row(align = True)
			row.operator("import.single_vertex_data", text = 'Import')
			row.operator("import.single_data_open_panel", text = 'Close').action = 'close'
					
		
		col = layout.column(align = 1)
		col.operator("export.all_shape_keys_data", icon='SHAPEKEY_DATA', text = 'Export All Shapes')
		col.operator("import.all_shape_keys_data", icon='SHAPEKEY_DATA', text = 'Import All Shapes')
		col.operator("facial_rig.import_single_sk_from_all_panel", icon='SHAPEKEY_DATA').action = 'open'
		
		if G.import_single_from_all_panel:
			layout.label('Select Target:')
			layout.prop(context.scene, "my_targets_list_enum")
			
			row = layout.row(align = True)
			row.operator("facial_rig.import_single_sk_from_all", text = 'Import')
			row.operator("facial_rig.import_single_sk_from_all_panel", text = 'Close').action = 'close'
		
		col = layout.column(align = 1)
		col.operator("export.all_vertex_groups", icon='GROUP_VERTEX', text = 'Export All Vertex Group')
		col.operator("import.all_vertex_groups", icon='GROUP_VERTEX', text = 'Import All Vertex Group')
		

class FACE_rig_help(bpy.types.Operator):
	bl_idname = "face_rig.help"
	bl_label = "Help"
	action = bpy.props.StringProperty()

	def execute(self, context):
		print('***** help')
		if self.action == 'manual':
			webbrowser.open_new_tab('https://sites.google.com/site/blenderfacialrig/user-manual')
		elif self.action == 'youtube_ru':
			webbrowser.open_new_tab('https://www.youtube.com/playlist?list=PLaF5hl1yUd9UYmvyRC51C-C0TulaA2SnT')
		return{'FINISHED'}
				
class TMP_armature_create(bpy.types.Operator):
	bl_idname = "face_rig.tmp_create"
	bl_label = "Are You Sure?"
	#country = bpy.props.StringProperty()

	def execute(self, context):
		print('hellow world')
		#TMP_create().create_bones(context)
		result = TMP_create().test_exists(context)
		if result:
			self.report({'WARNING'}, '****** TMP armature already exists!')
			bpy.ops.rebild.tmp_armature('INVOKE_DEFAULT')
		else:
			TMP_create().create_bones(context)
		return{'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
class PASSPORT_add_object(bpy.types.Operator):
	bl_idname = "passport.object_add"
	bl_label = "Passport"
	key_passp = bpy.props.StringProperty()

	def execute(self, context):
		if self.key_passp == '':
			print('\n'*3,'='*6,'mesh passport:', '='*6)
			passport().print_passport(context, 'mesh_passport')
		else:	
			print('add obj in passport:', self.key_passp)
			passport().select_object_to_passport(context, 'mesh_passport', self.key_passp)
		return{'FINISHED'}
	
class FACE_rig_generate(bpy.types.Operator):
	bl_idname = "face_rig.generate"
	bl_label = "Are You Sure?"
	
	def execute(self, context):
		print('***** face rig generate')
		result = face_armature().armature_create(context)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return{'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
#face_rig.linear_jaw_driver
class FACE_rig_linear_jaw_driver(bpy.types.Operator):
	bl_idname = "face_rig.linear_jaw_driver"
	bl_label = "Are You Sure?"
	
	def execute(self, context):
		result = G.face_armature.linear_jaw_driver_create(context)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		else:
			self.report({'INFO'}, result[1])
		
		return{'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
class CLEAR_skin(bpy.types.Operator):
	bl_idname = "face_rig.clear_skin"
	bl_label = "Clear Skin"
	mesh = bpy.props.StringProperty()

	def execute(self, context):
		print('***** clear skin')
		result = face_armature().clear_skin(context, as_ = self.mesh)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return{'FINISHED'}
		
class FACIALRIG_toggle_deform_bone(bpy.types.Operator):
	bl_idname = "face_rig.toggle_deform_bone"
	bl_label = "Toggle Bone Deform"
	action = bpy.props.StringProperty()

	def execute(self, context):
		result, data = face_armature().toggle_deform_bone(context, self.action)
		if not result:
			self.report({'WARNING'}, data)
		else:
			self.report({'INFO'}, data)
		return{'FINISHED'}
	
class LATTICE_deform(bpy.types.Operator):
	bl_idname = "lattice.deform_generate"
	bl_label = "Are You Sure?"
	#mesh = bpy.props.StringProperty()

	def execute(self, context):
		print('***** Lattice Deform Generate')
		result = face_armature().stretch_squash_controls(context)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return{'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
		
#facial_rig.toggle_lattice_visible
class FACIALRIG_toggle_lattice_visible(bpy.types.Operator):
	bl_idname = "facial_rig.toggle_lattice_visible"
	bl_label = "Toggle Lattice Visible"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		result, data = face_armature().toggle_lattice_visible(context, self.action)
		if not result:
			self.report({'WARNING'}, data)
			return{'FINISHED'}
		else:
			self.report({'INFO'}, data)
		return{'FINISHED'}
	
class WEIGHT_paint(bpy.types.Operator):
	bl_idname = "body_weight.paint"
	bl_label = "Weight Paint"
	target = bpy.props.StringProperty()

	def execute(self, context):
		print('***** Lattice Deform Generate')
		result = face_armature().edit_body_weight(context, self.target)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return{'FINISHED'}
	
class SHAPE_keys(bpy.types.Operator):
	bl_idname = "shape_key.generate"
	bl_label = "Are You Sure?"
	
	action = bpy.props.StringProperty()

	def execute(self, context):
		print('***** Shape Keys')
		if self.action == 'create_shape_keys':
			result = face_shape_keys().create_shape_keys(context)
			if not result[0]:
				self.report({'WARNING'}, result[1])
		elif self.action == 'create_autolid':
			result = face_shape_keys().autolids_base(context)
			if not result[0]:
				self.report({'WARNING'}, result[1])
		elif self.action == 'central_to_side':
			result = face_shape_keys().copy_central_to_side_shape_keys(context)
			if not result[0]:
				self.report({'WARNING'}, result[1])
		elif self.action == 'recalculation':
			face_shape_keys().create_edit_vertes_groups(context)
		elif self.action == 'inbetween':
			pass
		return{'FINISHED'}
		
	def invoke(self, context, event):
		#wm = context.window_manager.fileselect_add(self)
		#return {'RUNNING_MODAL'}
		return context.window_manager.invoke_props_dialog(self)

class SHAPE_keys_brows_all_vertex_groups(bpy.types.Operator):
	bl_idname = "shape_key.brows_all_vertex_groups"
	bl_label = "Are You Sure?"
	
	target = bpy.props.StringProperty()
	
	def execute(self, context):
		res, message = G.face_shape_keys.create_edit_brows_vertes_groups(context, self.target)
		if not res:
			self.report({'WARNING'}, message)
		else:
			self.report({'INFO'}, message)
		return{'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

class SHAPE_keys_single_vertex_groups_open_panel(bpy.types.Operator):
	bl_idname = "shape_key.single_vertex_groups_open_panel"
	bl_label = "Recalculate Single Vertex Group"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'open':
			G().rebild_targets_list(context)
			G.recalculate_single_brows_vtx_group_panel = True
		elif self.action == 'close':
			G.recalculate_single_brows_vtx_group_panel = False
		return {'FINISHED'}
	
class EDIT_SHAPE_keys(bpy.types.Operator):
	bl_idname = "shape_key.edit"
	bl_label = "Shape Keys"
	target = bpy.props.StringProperty()

	def execute(self, context):
		print('***** Edit Shape Keys')
		result = face_shape_keys().edit_shape_keys(context, self.target)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return{'FINISHED'}
	
class EYE_limits(bpy.types.Operator):
	bl_idname = "eye_limits.set_limits"
	bl_label = "Eye Limits"
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'start':
			print('***** Eye Limits Start')
			eye_limits().get_start_position()
		elif self.action == 'low':
			print('***** Eye Limits Low')
			eye_limits().get_low_position()
		elif self.action == 'up':
			print('***** Eye Limits UP')
			eye_limits().get_up_position()
		elif self.action == 'right':
			print('***** Eye Limits Right')
			eye_limits().get_right_position()
		elif self.action == 'apply':
			print('***** Eye Limits Apply')
			eye_limits().apply_limits()
		return{'FINISHED'}
	
class INSERT_inbetween(bpy.types.Operator):
	bl_idname = "insert.inbetween"
	bl_label = "Insert Inbetween"
	
	##### get list shape keys
	central_sh_keys = ['jaw_open_C', 'jaw_fwd', 'jaw_back', 'lip_down', 'lip_raise', 'lip_funnel', 'lip_close']
	fshk = face_shape_keys()
	list_sh_keys = []
	try:
		keys = fshk.central_side_shape_keys.keys()
		list_sh_keys = list(keys)
		list_sh_keys = list_sh_keys + central_sh_keys
		# finish
		list_sh_keys.sort()
	except:
		pass
	#####

	num = bpy.props.IntProperty(name="Num Inbetween Keys")
			
	target_list = []
	for key in list_sh_keys:
		target_list.append((key, key, key))
	target = bpy.props.EnumProperty(name="Shape Key", items = target_list)
	
	def execute(self, context):
		print(self.num, self.target)
		result = face_shape_keys().insert_in_between(context, self.target, (self.num + 1))
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return {'FINISHED'}

	def invoke(self, context, event):
		self.num = 1
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
	
class EDIT_lattice(bpy.types.Operator):
	bl_idname = "edit.lattice"
	bl_label = "Edit Lattice"
	######
	interpolation_list = []
	for key in ['cosinus','linear']:
		interpolation_list.append((key, key, key))
	######
	num = bpy.props.FloatProperty(name="Distance")
	interpolation = bpy.props.EnumProperty(name="Interpolation", items = interpolation_list)
	
	def execute(self, context):
		#print(self.num, self.target)
		result = face_armature().edit_eye_global_lattice(context, self.num, self.interpolation)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return {'FINISHED'}
	
	def invoke(self, context, event):
		self.num = 1.5
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
	
class REBILD_tmp_armature(bpy.types.Operator):
	bl_idname = "rebild.tmp_armature"
	bl_label = "Tmp armature already exists, to rebuild it?"
	
	def execute(self, context):
		TMP_create().create_bones(context)
		return {'FINISHED'}
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
	
class Export_single_data(bpy.types.Operator):
	bl_idname = "export.single_vertex_data"
	bl_label = "Export Single Date"
	
	def execute(self, context):
		result, data = face_shape_keys().export_single_vertex_data(context)
		if not result:
			self.report({'WARNING'}, data)
		else:
			self.report({'INFO'}, data)
		return {'FINISHED'}
		
class Export_all_shape_keys_data(bpy.types.Operator):
	bl_idname = "export.all_shape_keys_data"
	bl_label = "Export All Shape Keys Data"
	
	def execute(self, context):
		result, data = face_shape_keys().export_all_shape_key_data(context)
		if not result:
			self.report({'WARNING'}, data)
		else:
			self.report({'INFO'}, data)
		return {'FINISHED'}

class Export_all_vertex_groups(bpy.types.Operator):
	bl_idname = "export.all_vertex_groups"
	bl_label = "Export All Vertex Groups"
	
	def execute(self, context):
		result, data = face_shape_keys().export_all_vertex_groups(context)
		if not result:
			self.report({'WARNING'}, data)
		else:
			self.report({'INFO'}, data)
		return {'FINISHED'}


class IMPORT_single_data_open_panel(bpy.types.Operator):
	bl_idname = "import.single_data_open_panel"
	bl_label = "Import Single Date"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'open':
			G().rebild_targets_list(context)
			G.import_single_panel = True
		elif self.action == 'close':
			G.import_single_panel = False
		return {'FINISHED'}
		
class IMPORT_single_data(bpy.types.Operator):
	bl_idname = "import.single_vertex_data"
	bl_label = "Are You Sure?"
	
	def execute(self, context):
		#num = context.scene.my_num_of_between
		target = context.scene.my_targets_list_enum
		
		result = face_shape_keys().import_single_vertex_data(context, target)
		if not result[0]:
			self.report({'WARNING'}, result[1])
			return {'FINISHED'}
		else:
			self.report({'INFO'}, result[1])
		
		G.import_single_panel = False
		return {'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
		
'''
class IMPORT_single_data(bpy.types.Operator):
	bl_idname = "import.single_vertex_data"
	bl_label = "Import Single Date"
	
	# get list shape keys
	list_sh_keys = get_data_class().get_list_shape_keys(bpy.context, only_origin = 0)
	#list_sh_keys.sort()
	#
	
	target_list = []
	for key in list_sh_keys:
		target_list.append((key, key, key))
	target = bpy.props.EnumProperty(name="Shape Key", items = target_list)
	
		
	def execute(self, context):
		print(self.num, self.target)
		result = face_shape_keys().import_single_vertex_data(context, self.target)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return {'FINISHED'}

	def invoke(self, context, event):
		self.num = 1
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
'''
		
class Import_all_shape_keys_data(bpy.types.Operator):
	bl_idname = "import.all_shape_keys_data"
	bl_label = "Are You Sure?"
	
	def execute(self, context):
		result = face_shape_keys().import_all_shape_key_data(context)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return {'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
		
class FACIALRIG_import_single_sk_from_all_panel(bpy.types.Operator):
	bl_idname = "facial_rig.import_single_sk_from_all_panel"
	bl_label = "Import Single From All"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'open':
			G().rebild_targets_list(context)
			G.import_single_from_all_panel = True
		elif self.action == 'close':
			G.import_single_from_all_panel = False
		return {'FINISHED'}


class FACIALRIG_import_single_sk_from_all(bpy.types.Operator):
	bl_idname = "facial_rig.import_single_sk_from_all"
	bl_label = "Are You Sure?"
	
	def execute(self, context):
		target = context.scene.my_targets_list_enum
		result, data = face_shape_keys().import_single_sk_from_all(context, target)
		if not result:
			self.report({'WARNING'}, data)
			return {'FINISHED'}
		else:
			self.report({'INFO'}, data)
		
		G.import_single_from_all_panel = False
		return {'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
		
class IMPORT_all_vertex_groups(bpy.types.Operator):
	bl_idname = "import.all_vertex_groups"
	bl_label = "Are You Sure?"
	
	def execute(self, context):
		result = face_shape_keys().import_all_vertex_groups(context)
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return {'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
class LOCK_controls(bpy.types.Operator):
	bl_idname = "lock.controls"
	bl_label = "Lock Controls"
	action = bpy.props.StringProperty()

	def execute(self, context):
		print('***** face rig generate') #keyframe_to_root_cnt
		if self.action == 'lock':
			result = face_armature().lock_cnt_root(context, True)
		elif self.action == 'unlock':
			result = face_armature().lock_cnt_root(context, False)
		elif self.action == 'keying':
			result = face_armature().keyframe_to_root_cnt(context)
		
		if not result[0]:
			self.report({'WARNING'}, result[1])
		return{'FINISHED'}
	
def register():
	bpy.utils.register_class(FACIALRIG_Help)
	bpy.utils.register_class(FACIALRIG_MakeRig)
	bpy.utils.register_class(FACIALRIG_ShapeKeys)
	bpy.utils.register_class(FACIALRIG_import_export)
	bpy.utils.register_class(TMP_armature_create)
	bpy.utils.register_class(PASSPORT_add_object)
	bpy.utils.register_class(FACE_rig_generate)
	bpy.utils.register_class(FACE_rig_linear_jaw_driver)
	bpy.utils.register_class(CLEAR_skin)
	bpy.utils.register_class(LATTICE_deform)
	bpy.utils.register_class(SHAPE_keys)
	bpy.utils.register_class(SHAPE_keys_brows_all_vertex_groups)
	bpy.utils.register_class(SHAPE_keys_single_vertex_groups_open_panel)
	bpy.utils.register_class(EYE_limits)
	bpy.utils.register_class(EDIT_SHAPE_keys)
	bpy.utils.register_class(INSERT_inbetween)
	bpy.utils.register_class(EDIT_lattice)
	bpy.utils.register_class(REBILD_tmp_armature)
	bpy.utils.register_class(WEIGHT_paint)
	bpy.utils.register_class(Export_single_data)
	bpy.utils.register_class(IMPORT_single_data)
	bpy.utils.register_class(IMPORT_single_data_open_panel)
	bpy.utils.register_class(Export_all_shape_keys_data)
	bpy.utils.register_class(Import_all_shape_keys_data)
	bpy.utils.register_class(Export_all_vertex_groups)
	bpy.utils.register_class(IMPORT_all_vertex_groups)
	bpy.utils.register_class(LOCK_controls)
	bpy.utils.register_class(FACE_rig_help)
	bpy.utils.register_class(FACIALRIG_import_single_sk_from_all_panel)
	bpy.utils.register_class(FACIALRIG_import_single_sk_from_all)
	bpy.utils.register_class(FACIALRIG_toggle_deform_bone)
	bpy.utils.register_class(FACIALRIG_toggle_lattice_visible)
	
	###
	set_targets_list()
	
def unregister():
	bpy.utils.unregister_class(FACIALRIG_Help)
	bpy.utils.unregister_class(FACIALRIG_MakeRig)
	bpy.utils.unregister_class(FACIALRIG_ShapeKeys)
	bpy.utils.unregister_class(FACIALRIG_import_export)
	bpy.utils.unregister_class(TMP_armature_create)	
	bpy.utils.unregister_class(PASSPORT_add_object)	
	bpy.utils.unregister_class(FACE_rig_generate)
	bpy.utils.unregister_class(FACE_rig_linear_jaw_driver)
	bpy.utils.unregister_class(CLEAR_skin)	
	bpy.utils.unregister_class(LATTICE_deform)	
	bpy.utils.unregister_class(SHAPE_keys)
	bpy.utils.unregister_class(SHAPE_keys_brows_all_vertex_groups)
	bpy.utils.unregister_class(SHAPE_keys_single_vertex_groups_open_panel)
	bpy.utils.unregister_class(EYE_limits)	
	bpy.utils.unregister_class(EDIT_SHAPE_keys)	
	bpy.utils.unregister_class(INSERT_inbetween)	
	bpy.utils.unregister_class(EDIT_lattice)	
	bpy.utils.unregister_class(REBILD_tmp_armature)	
	bpy.utils.unregister_class(WEIGHT_paint)	
	bpy.utils.unregister_class(Export_single_data)	
	bpy.utils.unregister_class(IMPORT_single_data)
	bpy.utils.unregister_class(IMPORT_single_data_open_panel)
	bpy.utils.unregister_class(Export_all_shape_keys_data)	
	bpy.utils.unregister_class(Import_all_shape_keys_data)	
	bpy.utils.unregister_class(Export_all_vertex_groups)	
	bpy.utils.unregister_class(IMPORT_all_vertex_groups)	
	bpy.utils.unregister_class(LOCK_controls)	
	bpy.utils.unregister_class(FACE_rig_help)
	bpy.utils.unregister_class(FACIALRIG_import_single_sk_from_all_panel)
	bpy.utils.unregister_class(FACIALRIG_import_single_sk_from_all)
	bpy.utils.unregister_class(FACIALRIG_toggle_deform_bone)
	bpy.utils.unregister_class(FACIALRIG_toggle_lattice_visible)
