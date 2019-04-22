#

import bpy
from .tmp_armature_create import TMP_create  # 
from .face_rig_create import passport  # 
from .face_rig_create import face_armature  # 
from .face_rig_create import face_shape_keys  # 
from .face_rig_create import eye_limits  #
from .face_rig_create import export_to_unity
from .face_rig_create import BROWS_VERTEX_GROUPS
from .face_rig_create import BROWS_SHAPE_KEYS_FOR_HAND_MAKE
import webbrowser
import json

class G(object):
	import_single_panel = False
	import_single_from_all_panel = False
	recalculate_single_brows_vtx_group_panel = False
	edit_brows_shape_keys_panel = False
	insert_inbetween_panel = False
	insert_inbetween_target = ''
	insert_inbetween_exists = []
	
	targets_list = [('None',)*3]
	brows_vtx_list = [('None',)*3]
	brows_shape_keys_for_hand_make_list = [('None',)*3]
	
	#face_armature = face_armature()
	#face_shape_keys = face_shape_keys()
	#export_to_unity = export_to_unity()
	
	def rebild_targets_list(self, context):
		###
		G.targets_list = []
		list_shape_keys = get_data_class().get_list_shape_keys(context, only_origin = 0)
		for key in list_shape_keys:
			G.targets_list.append((key,)*3)
		###
		G.brows_vtx_list = []
		for key in BROWS_VERTEX_GROUPS:
			G.brows_vtx_list.append((key,)*3)
		###
		G.brows_shape_keys_for_hand_make_list = []
		for key in BROWS_SHAPE_KEYS_FOR_HAND_MAKE:
			G.brows_shape_keys_for_hand_make_list.append((key,)*3)
		###
		set_targets_list()

def set_targets_list():
	bpy.types.Scene.my_num_of_between = bpy.props.IntProperty(name = 'Num of Between:', min = 1, default = 1)
	bpy.types.Scene.my_targets_list_enum = bpy.props.EnumProperty(items = G.targets_list, name = 'Targets', update = None)
	bpy.types.Scene.brows_vtx_list = bpy.props.EnumProperty(items = G.brows_vtx_list, name = 'Vertex_Groups:', update = None)
	bpy.types.Scene.brows_shape_keys_for_hand_make_list_enum = bpy.props.EnumProperty(items = G.brows_shape_keys_for_hand_make_list, name = 'Targets', update = None)

def set_props():
	bpy.types.WindowManager.weight_inbetween = bpy.props.FloatProperty(name="weight_inbetween", min = 0.0, max = 1.0, default=0.5, update = None)
	bpy.types.WindowManager.method = bpy.props.BoolProperty(name='between adjacent', default = True, update = None)

class get_data_class():
	def __init__(self):
		self.data = []
			
	def get_list_shape_keys(self, context,  only_origin = 1):
		fshk = face_shape_keys()
		#central_sh_keys = ['jaw_open_C', 'jaw_side_R', 'lip_side.r', 'jaw_fwd', 'jaw_back', 'lip_down', 'lip_raise', 'lip_funnel', 'lip_close']
		central_sh_keys = fshk.central_sh_keys
		#print('\n'*3, face_shape_keys().central_side_shape_keys)
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
	bl_options = {'DEFAULT_CLOSED'}
		
	def draw(self, context):
		layout = self.layout

		#layout.label("Mesh Passport")
		col = layout.column(align=1)
		col.operator("face_rig.help",icon = 'QUESTION', text = 'Manual').path = 'https://sites.google.com/site/blenderfacialrig/user-manual'
		col.operator("face_rig.help",icon = 'QUESTION', text = 'Youtube(ru)').path = 'https://www.youtube.com/playlist?list=PLaF5hl1yUd9UYmvyRC51C-C0TulaA2SnT'

class FACIALRIG_MakeRig(bpy.types.Panel):
	bl_idname = "face_rig.tools_panel"
	bl_label = "Make Rig"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	layout = 'MAKE_RIG'
	bl_options = {'DEFAULT_CLOSED'}
		
	mesh_keys = face_armature.mesh_passp_bones.keys()
	
	def draw(self, context):
		self.mesh_keys = face_armature().mesh_passp_bones.keys()
		#passport_data=passport().reload_passport_data()
		passport_ob = passport()
		#passport_ob.reload_passport_data()
		passport_data=passport_ob.passport_data
		layout = self.layout
		
		#Armature Passport
		layout.label("Armature Passport")
		col = layout.column(align=1)
		for key in passport_ob.ARMATURE_PASSPORT_KEYS:
			row = col.row(align=True)
			if key.endswith('_bone'):
				button_text = '%s (pose bone)' % key
			else:
				button_text = key
			row.operator("passport.object_add", text = button_text).key_passp = 'armature_passport.%s' % key
			if passport_data.get('armature_passport') and passport_data['armature_passport'].get(key):
				try:
					row.label(json.dumps(passport_data['armature_passport'].get(key)))
				except Exception as e:
					print('key', e)
					row.label('--')
			else:
				row.label('--')

		# Mesh Passport
		layout.label("Mesh Passport")
		col_passp = layout.column(align=1)
		#col_passp.operator("passport.object_add", text = 'body').key_passp = 'body'
		mesh_keys = list(self.mesh_keys)
		mesh_keys.append('body')
		for key in sorted(mesh_keys):
			row = col_passp.row(align=True)
			row.operator("passport.object_add", text = key).key_passp = 'mesh_passport.%s' % key
			if passport_data.get('mesh_passport') and passport_data['mesh_passport'].get(key):
				try:
					row.label(json.dumps(passport_data['mesh_passport'].get(key)))
				except Exception as e:
					print('key', e)
					row.label('--')
			else:
				row.label('--')
		#layout.operator("passport.object_add", text = 'Print Passport').key_passp = ''

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
	bl_label = "Shape Keys: Create, Edit"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	layout = 'Shape_Keys'
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		layout = self.layout
		
		layout.label("Create:")
		col = layout.column(align=1)
		col.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Shape Keys').action = 'create_shape_keys'
		col.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Autolid').action = 'create_autolid'
		#col.operator("insert.inbetween", icon='SHAPEKEY_DATA', text = 'Add Inbetween')
		col.operator("shape_key.insert_inbetween_panel", icon='SHAPEKEY_DATA', text = 'Insert Inbetween:')
		if G.insert_inbetween_panel:
			#target
			col.label('Target: %s' % G.insert_inbetween_target)
			#weight
			wm = context.window_manager
			col.prop(wm, 'weight_inbetween')
			col.prop(wm, 'method')
			#exists
			col.label('Exists Inbetweens:')
			if G.insert_inbetween_exists:
				for weight in G.insert_inbetween_exists:
					col.label(str(weight))
			row = col.row(align = True)
			row.operator('shape_key.insert_inbetween', text = 'Insert')
			row.operator('shape_key.insert_inbetween_close_panel', text = 'close')
		
		layout.label("Edit Shape Keys:")
		col = layout.column(align=1)
		col.operator("shape_key.generate", icon='SHAPEKEY_DATA', text = 'Central To Side').action = 'central_to_side'
		col.operator('shape_key.edit_brows_shape_keys_open_panel', icon='SHAPEKEY_DATA', text = 'Edit Brows Shape Keys:').action = 'open'
		
		if G.edit_brows_shape_keys_panel:
			col.prop(context.scene, "brows_shape_keys_for_hand_make_list_enum")
			col.operator('shape_key.brows_edit_shape_keys').action = 'copy_from_central'
			col.operator('shape_key.brows_edit_shape_keys', text = 'to Calculate TMP Vertex Group').action = 'vertex_group'
			col.operator('shape_key.brows_edit_shape_keys', text = 'Bake Shape Key: follow these "Central to Side"').action = 'bake'
			col.operator('shape_key.edit_brows_shape_keys_open_panel', text = 'close').action = 'close'
				
		layout.label("Recalculate Vertex Groups:")
		col = layout.column(align=1)
		col.operator("shape_key.generate", icon='GROUP_VERTEX', text = '(Lower, Middle) Recalculation All').action = 'recalculation'
		col.operator("shape_key.brows_all_vertex_groups", icon='GROUP_VERTEX', text = '(Brows) Recalculation All').target = 'all'
		col.operator('shape_key.single_vertex_groups_open_panel', icon='GROUP_VERTEX', text = '(Brows) Recalculation Single:').action = 'open'
		
		if G.recalculate_single_brows_vtx_group_panel:
			for name in face_shape_keys().brows_vertex_groups:
				row = col.row(align=1)
				row.label(name)
				row.operator("shape_key.brows_all_vertex_groups", icon='GROUP_VERTEX', text = 'To Recalculate').target = name
			row = col.row(align=1)
			row.operator('shape_key.single_vertex_groups_open_panel', text = 'close').action = 'close'
			
class FACIALRIG_Shape_Keys_Sculpt(bpy.types.Panel):
	bl_idname = "shape_keys.sculpt"
	bl_label = "Shape Keys: Sculpt"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		layout = self.layout
		layout.label("Sculpt Shape Keys:")
		col = layout.column(align = 1)
		list_shape_keys = get_data_class().get_list_shape_keys(context, only_origin = 0)
		for key in list_shape_keys:
			row = col.row(align = True)
			row.operator("shape_key.edit", icon='SHAPEKEY_DATA', text = key).target = key
			if key in face_shape_keys().helps_list and face_shape_keys().helps_list[key]:
				row.operator('face_rig.help', icon = 'QUESTION', text = '').path = face_shape_keys().helps_list[key]
		
		
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
		
		#eye_limits.import_export
		col = layout.column(align = 1)
		col.operator("eye_limits.import_export", text = 'Export Eye/Jaw Limits').action = 'export'
		col.operator("eye_limits.import_export", text = 'Import Eye/Jaw Limits').action = 'import'
		
#game engine
class FACIALRIG_to_game_engine(bpy.types.Panel):
	bl_idname = "faceial_rig.to_game_engine"
	bl_label = "To Game Engine"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Facial Rig"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		layout = self.layout
		
		col = layout.column(align = 1)
		col.operator("to_game_engine.clear")
		
class TO_GAME_ENGINE_clear(bpy.types.Operator):
	bl_idname = "to_game_engine.clear"
	bl_label = "Export to Unity"
	
	directory = bpy.props.StringProperty(subtype="DIR_PATH")
	
	def execute(self, context):
		# export metadata
		res, mes = export_to_unity().export_meta_data(context, self.directory)
		if not res:
			self.report({'WARNING'}, mes)
			return{'FINISHED'}
		
		# clear shape_keys
		res, mes = export_to_unity().clear_shape_keys(context)
		if not res:
			self.report({'WARNING'}, mes)
			return{'FINISHED'}
		# clear control
		res, mes = export_to_unity().clear_control(context)
		if not res:
			self.report({'WARNING'}, mes)
			return{'FINISHED'}
		
		# save_blend_file
		res, mes = export_to_unity().save_blend_file(context, self.directory)
		if not res:
			self.report({'WARNING'}, mes)
			return{'FINISHED'}
		
		self.report({'INFO'}, 'Ok!')
		return{'FINISHED'}
	
	def invoke(self, context, event):
		wm = context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

class FACE_rig_help(bpy.types.Operator):
	bl_idname = "face_rig.help"
	bl_label = "Help"
	path = bpy.props.StringProperty()

	def execute(self, context):
		'''
		if self.action == 'manual':
			webbrowser.open_new_tab('https://sites.google.com/site/blenderfacialrig/user-manual')
		elif self.action == 'youtube_ru':
			webbrowser.open_new_tab('https://www.youtube.com/playlist?list=PLaF5hl1yUd9UYmvyRC51C-C0TulaA2SnT')
		'''
		webbrowser.open_new_tab(self.path)
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
			if self.key_passp.startswith('mesh_passport.'):
				passport().select_object_to_passport(context, 'mesh_passport', self.key_passp.replace('mesh_passport.' , ''))
			elif self.key_passp.startswith('armature_passport.'):
				passport().select_object_to_passport(context, 'armature_passport', self.key_passp.replace('armature_passport.' , ''))
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
		result = face_armature().linear_jaw_driver_create(context)
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
		res, message = face_shape_keys().create_edit_brows_vertes_groups(context, self.target)
		if not res:
			self.report({'WARNING'}, message)
		else:
			self.report({'INFO'}, message)
		return{'FINISHED'}
		
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

class SHAPE_keys_single_vertex_groups_open_panel(bpy.types.Operator):
	bl_idname = "shape_key.single_vertex_groups_open_panel"
	bl_label = "(Brows) Recalculate Single Vertex Group"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'open':
			G().rebild_targets_list(context)
			G.recalculate_single_brows_vtx_group_panel = True
		elif self.action == 'close':
			G.recalculate_single_brows_vtx_group_panel = False
		return {'FINISHED'}
	
class SHAPE_keys_edit_brows_shape_keys_open_panel(bpy.types.Operator):
	bl_idname = "shape_key.edit_brows_shape_keys_open_panel"
	bl_label = "Edit Brows Shape Keys Open Panel"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'open':
			G().rebild_targets_list(context)
			G.edit_brows_shape_keys_panel = True
		elif self.action == 'close':
			G.edit_brows_shape_keys_panel = False
		return {'FINISHED'}
	
class SHAPE_keys_brows_edit_shape_keys(bpy.types.Operator):
	bl_idname = "shape_key.brows_edit_shape_keys"
	bl_label = "Copy From Central Shape Key"
	
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		target = context.scene.brows_shape_keys_for_hand_make_list_enum
		if self.action == 'copy_from_central':
			res, mess = face_shape_keys().edit_brows_copy_from_central(context, target)
			if res:
				self.report({'INFO'}, mess)
			else:
				self.report({'WARNING'}, mess)
		elif self.action == 'vertex_group':
			res, mess = face_shape_keys().create_edit_brows_tmp_vertes_groups(context, target)
			if res:
				self.report({'INFO'}, mess)
			else:
				self.report({'WARNING'}, mess)
		elif self.action == 'bake':
			res, mess = face_shape_keys().bake_brows_shape_key(context, target)
			if res:
				self.report({'INFO'}, mess)
			else:
				self.report({'WARNING'}, mess)
			pass
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
	
class EYE_limits_import_export(bpy.types.Operator):
	bl_idname = "eye_limits.import_export"
	bl_label = "You Are Sure?"
	action = bpy.props.StringProperty()
	
	def execute(self, context):
		if self.action == 'export':
			res, mess = eye_limits().export_limits()
			if not res:
				self.report({'WARNING'}, mess)
			else:
				self.report({'INFO'}, mess)
		else:
			res, mess = eye_limits().import_limits()
			if not res:
				self.report({'WARNING'}, mess)
			else:
				self.report({'INFO'}, mess)
		return{'FINISHED'}
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
class INSERT_inbetween(bpy.types.Operator):
	bl_idname = "insert.inbetween"
	bl_label = "Insert Inbetween"
	
	##### get list shape keys
	central_sh_keys = ['jaw_open_C', 'jaw_fwd', 'jaw_back', 'lip_down', 'lip_raise', 'lip_funnel', 'lip_close']
	list_sh_keys = []
	try:
		keys = face_shape_keys.central_side_shape_keys.keys()
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
	
class SHAPE_keys_insert_inbetween_panel(bpy.types.Operator):
	bl_idname = "shape_key.insert_inbetween_panel"
	bl_label = "Insert Inbetween"
	
	##### get list shape keys
	central_sh_keys = face_shape_keys.central_sh_keys#['jaw_open_C', 'jaw_fwd', 'jaw_back', 'lip_down', 'lip_raise', 'lip_funnel', 'lip_close']
	list_sh_keys = []
	try:
		keys = face_shape_keys.central_side_shape_keys.keys()
		list_sh_keys = list(keys)
		list_sh_keys = list_sh_keys + central_sh_keys
		# finish
		list_sh_keys.sort()
	except:
		pass
	#####
	target_list = []
	for key in list_sh_keys:
		target_list.append((key, key, key))
	
	target = bpy.props.EnumProperty(name="Shape Key", items = target_list)
	#num = bpy.props.IntProperty(name="Num Inbetween Keys")
	
	def execute(self, context):
		#print(self.num, self.target)
		#result = face_shape_keys().insert_in_between(context, self.target, (self.num + 1))
		#if not result[0]:
		#	self.report({'WARNING'}, result[1])
		#get exists list
		res, mess = face_shape_keys().get_inbetween_exists(context, self.target)
		if not res:
			self.report({'WARNING'}, mess)
		else:
			G.insert_inbetween_exists = mess
			if G.insert_inbetween_exists:
				G.insert_inbetween_exists.sort()
		
		G.insert_inbetween_panel = True
		G.insert_inbetween_target = self.target
		
		return {'FINISHED'}

	def invoke(self, context, event):
		self.num = 1
		wm = context.window_manager
		return wm.invoke_props_dialog(self)
	
class SHAPE_keys_insert_inbetween(bpy.types.Operator):
	bl_idname = "shape_key.insert_inbetween"
	bl_label = "You Are Sure?"
	
	def execute(self, context):
		weight = context.window_manager.weight_inbetween
		method = context.window_manager.method
		weight_exists = G.insert_inbetween_exists
		target = G.insert_inbetween_target
		
		res, mess = face_shape_keys().insert_inbetween(context, target, weight, weight_exists, method)
		if not res:
			self.report({'WARNING'}, mess)
		else:
			self.report({'INFO'}, mess)
		G.insert_inbetween_panel = False
		return {'FINISHED'}
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

class SHAPE_keys_insert_inbetween_close_panel(bpy.types.Operator):
	bl_idname = "shape_key.insert_inbetween_close_panel"
	bl_label = "close"
	
	def execute(self, context):
		G.insert_inbetween_panel = False
		return {'FINISHED'}
	
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
	bpy.utils.register_class(FACIALRIG_Shape_Keys_Sculpt)
	bpy.utils.register_class(FACIALRIG_import_export)
	bpy.utils.register_class(FACIALRIG_to_game_engine)
	bpy.utils.register_class(TMP_armature_create)
	bpy.utils.register_class(PASSPORT_add_object)
	bpy.utils.register_class(FACE_rig_generate)
	bpy.utils.register_class(FACE_rig_linear_jaw_driver)
	bpy.utils.register_class(CLEAR_skin)
	bpy.utils.register_class(LATTICE_deform)
	bpy.utils.register_class(SHAPE_keys)
	bpy.utils.register_class(SHAPE_keys_brows_all_vertex_groups)
	bpy.utils.register_class(SHAPE_keys_single_vertex_groups_open_panel)
	bpy.utils.register_class(SHAPE_keys_edit_brows_shape_keys_open_panel)
	bpy.utils.register_class(SHAPE_keys_brows_edit_shape_keys)
	bpy.utils.register_class(EYE_limits)
	bpy.utils.register_class(EYE_limits_import_export)
	bpy.utils.register_class(EDIT_SHAPE_keys)
	bpy.utils.register_class(INSERT_inbetween)
	bpy.utils.register_class(SHAPE_keys_insert_inbetween_panel)
	bpy.utils.register_class(SHAPE_keys_insert_inbetween)
	bpy.utils.register_class(SHAPE_keys_insert_inbetween_close_panel)
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
	bpy.utils.register_class(TO_GAME_ENGINE_clear)
	
	###
	set_targets_list()
	set_props()
	
def unregister():
	bpy.utils.unregister_class(FACIALRIG_Help)
	bpy.utils.unregister_class(FACIALRIG_MakeRig)
	bpy.utils.unregister_class(FACIALRIG_ShapeKeys)
	bpy.utils.unregister_class(FACIALRIG_Shape_Keys_Sculpt)
	bpy.utils.unregister_class(FACIALRIG_import_export)
	bpy.utils.unregister_class(FACIALRIG_to_game_engine)
	bpy.utils.unregister_class(TMP_armature_create)	
	bpy.utils.unregister_class(PASSPORT_add_object)	
	bpy.utils.unregister_class(FACE_rig_generate)
	bpy.utils.unregister_class(FACE_rig_linear_jaw_driver)
	bpy.utils.unregister_class(CLEAR_skin)	
	bpy.utils.unregister_class(LATTICE_deform)	
	bpy.utils.unregister_class(SHAPE_keys)
	bpy.utils.unregister_class(SHAPE_keys_brows_all_vertex_groups)
	bpy.utils.unregister_class(SHAPE_keys_single_vertex_groups_open_panel)
	bpy.utils.unregister_class(SHAPE_keys_edit_brows_shape_keys_open_panel)
	bpy.utils.unregister_class(SHAPE_keys_brows_edit_shape_keys)
	bpy.utils.unregister_class(EYE_limits)
	bpy.utils.unregister_class(EYE_limits_import_export)
	bpy.utils.unregister_class(EDIT_SHAPE_keys)	
	bpy.utils.unregister_class(INSERT_inbetween)
	bpy.utils.unregister_class(SHAPE_keys_insert_inbetween_panel)
	bpy.utils.unregister_class(SHAPE_keys_insert_inbetween)
	bpy.utils.unregister_class(SHAPE_keys_insert_inbetween_close_panel)
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
	bpy.utils.unregister_class(TO_GAME_ENGINE_clear)
