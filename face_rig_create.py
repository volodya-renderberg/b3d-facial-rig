#
import os
import bpy
import math
import json

from .ui_tmp import file_data

class G(object):
	user_text_name = 'current_task'
	rig_name = 'rig'

class passport:
	'''
	self.read_passport(dict_name)  return: (True, Dict) ore (False, Comment)
	'''
	
	def __init__(self):
		self.text_name = 'rig_meta_data'
		try:
			self.text = bpy.data.texts[self.text_name]
		except:
			pass
			#self.text = bpy.data.texts.new(self.text_name)
			
	def make_passport(self):
		try:
			self.text = bpy.data.texts[self.text_name]
		except:
			self.text = bpy.data.texts.new(self.text_name)
			
	def print_passport(self, context, dict_name):
		passp = self.read_passport(context, dict_name)
		if passp[0]:
			for key in passp[1]:
				print(key, ':', passp[1][key])
		else:
			print(passp[1])
	
	def read_passport(self, context, dict_name):
		try:
			string = self.text.as_string()
		except:
			return(False, '****** Not Passport')
		if string:
			data = json.loads(string)
			try:
				work_dict = data[dict_name]
			except:
				return(False, ('****** ' + dict_name + ' not found in \"rig_meta_data\"!'))
			
			return(True, work_dict)
						
		else:
			#print('****** \"rig_meta_data\" is empty!')
			return(False, '****** \"rig_meta_data\" is empty!')
				
		
	def select_object_to_passport(self, context, dict_name, key):
		self.make_passport()
		objects = bpy.context.selected_objects
		obj_names = []
		for obj in objects:
			obj_names.append(obj.name)
		
		string = self.text.as_string()
		if string:
			data = json.loads(string)
			try:
				work_dict = data[dict_name]
			except:
				work_dict = {}
		
		else:
			data = {}
			work_dict = {}
		
		work_dict[key] = obj_names
		data[dict_name] = work_dict
		
		self.text.clear()
		self.text.write(json.dumps(data, sort_keys=True, indent=4))
		
		return(True, 'all right!')
		
	def string_add_to_passport(self, context, dict_name, name):
		self.make_passport()
		string = self.text.as_string()
		if string:
			data = json.loads(string)
			try:
				work_dict = data[dict_name]
			except:
				work_dict = []
		
		else:
			data = {}
			work_dict = []
		
		if not name in work_dict:
			work_dict.append(name)
		data[dict_name] = work_dict
		
		self.text.clear()
		self.text.write(json.dumps(data, sort_keys=True, indent=4))
		
	def key_data_add_to_passport(self, context, dict_name, key, data):
		self.make_passport()
		string = self.text.as_string()
		if string:
			global_dict = json.loads(string)
			try:
				work_dict = global_dict[dict_name]
			except:
				work_dict = {}
		
		else:
			global_dict = {}
			work_dict = {}
		
		# append data
		work_dict[key]= data
		global_dict[dict_name] = work_dict
		
		# write text block
		self.text.clear()
		self.text.write(json.dumps(global_dict, sort_keys=True, indent=4))
		

class face_armature:
	def __init__(self):
		self.label_tmp_bones = ['vtx_lip_grp_set', 'vtx_brow_m_set', 'vtx_brow_in_set', 'vtx_brow_out_set', 'vtx_nose_set']
		self.label_bones = ['jaw', 'upper_jaw', 'lower_jaw', 'eye_L','eye_R','tongue_base', 'tongue_middle', 'tongue_end', 'ear_L','ear_R']
		self.tongue_label = ['tongue_base', 'tongue_middle', 'tongue_end']
		self.def_label = self.tongue_label + ['eye_L','eye_R', 'jaw']
		self.eye_label = ['eye_L','eye_R']
		
		self.tmp_bones = [
		('FRTMP_lip_M', 'FOUR_SIDE', ''),	
		('FRTMP_lip_R', 'FOUR_SIDE', ''),	
		('FRTMP_lip_L', 'FOUR_SIDE', ''),	
		#('FRTMP_lip_up_raise_R', 'LINE', ''),	
		('FRTMP_lip_up_raise_R', 'LINE_DUBBLE', ''),	
		#('FRTMP_lip_up_raise_L', 'LINE', ''),	
		('FRTMP_lip_up_raise_L', 'LINE_DUBBLE', ''),	
		#('FRTMP_lip_low_depress_R', 'LINE', ''),	
		('FRTMP_lip_low_depress_R', 'LINE_DUBBLE', ''),	
		#('FRTMP_lip_low_depress_L', 'LINE', ''),	
		('FRTMP_lip_low_depress_L', 'LINE_DUBBLE', ''),	
		('FRTMP_lip_up_roll_R', 'LINE_DUBBLE', ''),	
		('FRTMP_lip_up_roll_M', 'LINE_DUBBLE', ''),
		('FRTMP_lip_up_roll_L', 'LINE_DUBBLE', ''),	
		('FRTMP_lip_low_roll_R', 'LINE_DUBBLE', ''),	
		('FRTMP_lip_low_roll_M', 'LINE_DUBBLE', ''),	
		('FRTMP_lip_low_roll_L', 'LINE_DUBBLE', ''),	
		('FRTMP_lips_pinch_R', 'LINE', ''),	
		('FRTMP_lips_pinch_L', 'LINE', ''),	
		#('FRTMP_lip_up_sqz_R', 'LINE', ''),	
		#('FRTMP_lip_up_sqz_L', 'LINE', ''),	
		#('FRTMP_lip_low_sqz_R', 'LINE', ''),	
		#('FRTMP_lip_low_sqz_L', 'LINE', ''),	
		('FRTMP_nose_R', 'THREE_SIDE', ''),	
		('FRTMP_nose_L', 'THREE_SIDE', ''),	
		('FRTMP_cheek_R', 'FOUR_SIDE', ''),	
		('FRTMP_cheek_L', 'FOUR_SIDE', ''),	
		('FRTMP_brow_out_R', 'LINE_DUBBLE', ''),	
		('FRTMP_brow_mid_R', 'LINE_DUBBLE', ''),	
		('FRTMP_brow_in_R', 'LINE_DUBBLE', ''),	
		('FRTMP_brow_out_L', 'LINE_DUBBLE', ''),	
		('FRTMP_brow_mid_L', 'LINE_DUBBLE', ''),	
		('FRTMP_brow_in_L', 'LINE_DUBBLE', ''),
		('FRTMP_brow_gather_R', 'LINE', ''),
		('FRTMP_brow_gather_L', 'LINE', ''),
		('FRTMP_blink_R', 'FOUR_SIDE2', ''),	
		('FRTMP_blink_L', 'FOUR_SIDE2', ''),	
		('FRTMP_pupil_R', 'LINE_DUBBLE', ''),	
		('FRTMP_pupil_L', 'LINE_DUBBLE', ''),
		('FRTMP_eye_global_R', 'CIRCLE', ''),
		('FRTMP_eye_global_L', 'CIRCLE', ''),
		# side panel
		('FRTMP_lips', 'FOUR_SIDE2', ''),
		('FRTMP_cheeks', 'FOUR_SIDE2', ''),
		('FRTMP_jaw_back_fwd', 'LINE_DUBBLE', ''),
		('FRTMP_funnel', 'LINE', ''),
		#('FRTMP_lip_up_raise', 'LINE', ''),
		('FRTMP_lip_up_raise', 'LINE_DUBBLE', ''),
		#('FRTMP_lip_low_depress', 'LINE', ''),
		('FRTMP_lip_low_depress', 'LINE_DUBBLE', ''),
		('FRTMP_nose', 'THREE_SIDE2', ''),
		#('FRTMP_lip_up_sqz', 'LINE', ''),
		#('FRTMP_lip_low_sqz', 'LINE', ''),
		('FRTMP_lips_pinch', 'LINE', ''),
		('FRTMP_lips_close', 'LINE', ''),
		('FRTMP_lip_up_roll', 'LINE_DUBBLE', ''),
		('FRTMP_lip_low_roll', 'LINE_DUBBLE', ''),
		]
		
		# mesh_passport - bones to skin
		self.mesh_passp_bones = {
		'eye_r':('FR_eye_R',),
		'eye_l':('FR_eye_L',),
		'highlight_R':('FR_eye_R',),
		'highlight_L':('FR_eye_L',),
		'tongue':('FR_tongue_base', 'FR_tongue_middle', 'FR_tongue_end'),
		'upper_jaw':('FR_upper_jaw',),
		'lower_jaw':('FR_lower_jaw',),
		}
		
		# vertexes edjes
		self.circle_verts = (
		(0.0, 0.0, 0),
		(0.59999999999999987, 0.19999999999999996, 0),
		(0.79999999999999993, 0.39999999999999991, 0),
		(0.91651513899116788, 0.59999999999999987, 0),
		(0.9797958971132712, 0.79999999999999982, 0),
		(1.0, 0.99999999999999978, 0),
		(0.97979589711327131, 1.1999999999999997, 0),
		(0.91651513899116821, 1.3999999999999997, 0),
		(0.80000000000000027, 1.5999999999999996, 0),
		(0.60000000000000053, 1.7999999999999996, 0),
		(2.9802322387695312e-08, 1.9999999999999996, 0),
		(-0.43588989435406728, 1.8999999999999999, 0),
		(-0.71414284285428498, 1.7, 0),
		(-0.86602540378443871, 1.5, 0),
		(-0.95393920141694577, 1.2999999999999998, 0),
		(-0.99498743710661997, 1.0999999999999996, 0),
		(-0.99498743710661985, 0.89999999999999958, 0),
		(-0.95393920141694555, 0.69999999999999962, 0),
		(-0.86602540378443849, 0.49999999999999967, 0),
		(-0.71414284285428453, 0.29999999999999949, 0),
		(-0.43588989435406589, 0.099999999999999312, 0),
		)
		self.circle_edges = (
		(0,1),
		(1,2),
		(2,3),
		(3,4),
		(4,5),
		(5,6),
		(6,7),
		(7,8),
		(8,9),
		(9,10),
		(10,11),
		(11,12),
		(12,13),
		(13,14),
		(14,15),
		(15,16),
		(16,17),
		(17,18),
		(18,19),
		(19,20),
		(20,0),
		)
	
	@staticmethod
	def z_up(m):
		up = (0,0,1)
		X = (-1, 0, 0)
		Y = (m[1][0], m[1][1], m[1][2])
		a = X
		b = Y
		#a × b = {aybz - azby; azbx - axbz; axby - aybx}
		Z = ((a[1]*b[2] - a[2]*b[1]), (a[2]*b[0] - a[0]*b[2]), (a[0]*b[1] - a[1]*b[0]))
		m[0][0] = X[0]
		m[0][1] = X[1]
		m[0][2] = X[2]
		m[2][0] = Z[0]
		m[2][1] = -Z[1]
		m[2][2] = Z[2]
		return m
	
	def armature_create(self, context):
		pass
		# ******************** constants *********************************
		eye_ik_extending = 5
		bbone_ratio = 10
		
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])

		# ******************** copy-create bones **************************
		# -- names
		face_tmp_name = 'face_rig_tmp'
		#rig_name = 'rig'

		# -- tmp data
		face_obj = None
		try:
			face_obj = bpy.data.objects[face_tmp_name]
		except:
			return(False, '****** Tmp Armature Not Found!')
		face_arm = face_obj.data

		# -- tmp to EDIT mode
		scene = bpy.context.scene
		scene.objects.active = face_obj
		bpy.ops.object.mode_set(mode = 'EDIT')
		
		# -- go to laers
		layer = [False]*20
		layer[19] = True
		face_obj.layers = layer

		heads = {}
		tails = {}
		heads_tmp = {}
		tails_tmp = {}

		# -- get tmp bones position
		for label in self.label_bones:
			try:
				bone = face_arm.edit_bones[('FRTMP_' + label)]
			except:
				print('***** not found ' + label)
				continue
			else:
				heads[label] = (bone.head[0],bone.head[1],bone.head[2])
				tails[label] = (bone.tail[0], bone.tail[1], bone.tail[2])

		for label in self.label_tmp_bones:
			try:
				name = 'FRTMP_' + label
				bone = face_arm.edit_bones[name]
			except:
				print('***** not found ' + name)
				continue
			else:
				heads_tmp[label] = (bone.head[0],bone.head[1],bone.head[2])
				tails_tmp[label] = (bone.tail[0], bone.tail[1], bone.tail[2])
		
		tails_global = tails
		
		# -- get jaw_tmp position
		j_t_b = face_arm.edit_bones['FRTMP_jaw_control']
		jaw_tmp_location = [(j_t_b.head[0], j_t_b.head[1], j_t_b.head[2],), (j_t_b.tail[0], j_t_b.tail[1], j_t_b.tail[2])]

		# -- tmp to OBJECT mode
		scene.objects.active = face_obj
		bpy.ops.object.mode_set(mode = 'OBJECT', toggle=True)

		# -- rig data
		rig_obj = None
		try:
			rig_obj = bpy.data.objects[G.rig_name]
		except:
			return(False, '****** Rig Not Found!')
		rig_arm = rig_obj.data
		
		# ------------ add properties for jaw setting ------------------
		bpy.types.Armature.jaw_open =  bpy.props.FloatProperty(name = "jaw_open", default = 1.0,min = 0.0, max = 180)
		rig_arm.jaw_open = 0.58
		bpy.types.Armature.jaw_side =  bpy.props.FloatProperty(name = "jaw_side", default = 1.0,min = 0.0, max = 180)
		rig_arm.jaw_side = 0.2
		bpy.types.Armature.jaw_incline =  bpy.props.FloatProperty(name = "jaw_incline", default = 1.0,min = 0.0, max = 180)
		rig_arm.jaw_incline = 0.06
		bpy.types.Armature.jaw_fwd =  bpy.props.FloatProperty(name = "jaw_fwd", default = 1.0,min = 0.0, max = 100)
		rig_arm.jaw_fwd = 0.03
		bpy.types.Armature.jaw_back =  bpy.props.FloatProperty(name = "jaw_back", default = 1.0,min = 0.0, max = 100)
		rig_arm.jaw_back = 0.015
		
		# ------------ create all cnt ------------------
		self.create_all_cnt(bpy.context)

		# -- rig to EDIT mode
		scene.objects.active = rig_obj
		result = None
		while result != {'FINISHED'}:
			result = bpy.ops.object.mode_set(mode = 'EDIT', toggle=True)
		bpy.ops.object.mode_set(mode = 'EDIT', toggle=True)
		bpy.ops.object.mode_set(mode = 'EDIT', toggle=True)
		
		# -- set layers
		layer = [False]*32
		layer[29] = True
		cnt_layer = [False]*32
		cnt_layer[19] = True
		tmp_layer = [False]*32
		tmp_layer[24] = True
		rig_arm.layers[19] = True

		# -- create tmp_bones
		for label in self.label_tmp_bones:
			bname = 'FR_' + label
			###### -- test exists face_rig
			try:
				rig_arm.edit_bones[bname]
			except:
				pass
			else:
				return(False, '***** face rig already exist!')
			######
			bone = rig_arm.edit_bones.new(bname)
			bone.head = (heads_tmp[label][0], heads_tmp[label][1], heads_tmp[label][2])
			bone.tail = (tails_tmp[label][0], tails_tmp[label][1], tails_tmp[label][2])
			bone.roll = 0.0000
			bone.layers = tmp_layer
			bone.use_connect = False
			bone.use_deform = False
			bone.parent = rig_arm.edit_bones['DEF-head']

		# -- create bones
		for label in self.label_bones:
			if label == 'jaw':
				head = (heads[label][0], heads[label][1], heads[label][2])
				tail = (tails[label][0], tails[label][1], tails[label][2])
				x = (tail[0] - head[0])*0.1 + head[0]
				y = (tail[1] - head[1])*0.1 + head[1]
				z = (tail[2] - head[2])*0.1 + head[2]
				middle = (x,y,z)
				y_fwd_tail = (tail[1] - y)/2.0 + y
				fwd_tail = (x, y_fwd_tail, z)
				
				# Jaw Back-Forward
				bone = rig_arm.edit_bones.new('FWD_jaw')
				bone.layers = layer
				#bone.head = middle
				bone.head = head
				bone.tail = fwd_tail
				bone.roll = 0.0000
				bone.use_connect = False
				bone.use_deform = False
				bone.parent = rig_arm.edit_bones['DEF-head']
				'''
				# Jaw Incline
				bone = rig_arm.edit_bones.new('INCL_jaw')
				bone.layers = layer
				bone.head = head
				bone.tail = middle
				bone.roll = 0.0000
				bone.use_connect = False
				bone.use_deform = False
				bone.parent = rig_arm.edit_bones['FWD_jaw']
				'''
				# Jaw Open
				bone = rig_arm.edit_bones.new('FR_jaw')
				#bone.head = middle
				bone.head = head
				bone.tail = tail
				bone.roll = 0.0000
				#bone.use_connect = True
				bone.use_connect = False
				#bone.parent = rig_arm.edit_bones['INCL_jaw']
				bone.parent = rig_arm.edit_bones['FWD_jaw']

			else:
				bname = 'FR_' + label
				bone = rig_arm.edit_bones.new(bname)
				bone.head[:] = heads[label][0], heads[label][1], heads[label][2]
				bone.tail[:] = tails[label][0], tails[label][1], tails[label][2]
				bone.roll = 0.0000
				bone.use_connect = False
				bone.parent = rig_arm.edit_bones['DEF-head']

			# b-bone size
			x = heads[label][0] - tails[label][0]
			y = heads[label][1] - tails[label][1]
			z = heads[label][2] - tails[label][2]
			dist = (x**2 + y**2 + z**2)**0.5
			bone.bbone_x = dist/bbone_ratio
			bone.bbone_z = dist/bbone_ratio

			# tongue parametres
			if label in self.tongue_label:
				bone.bbone_segments = 7
				bone.use_inherit_scale = False
			# layers
			if label in self.def_label:
				bone.layers = layer
			else:
				bone.layers = cnt_layer

		# -- PARENT TONGUE
		try:
			tbone = rig_arm.edit_bones['FR_tongue_base']
		except:
			pass
		else:
			tbone.use_connect = False
			tbone.parent = rig_arm.edit_bones['FR_jaw']
		# --
		try:
			tbone = rig_arm.edit_bones['FR_tongue_middle']
		except:
			pass
		else:
			tbone.use_connect = True
			tbone.parent = rig_arm.edit_bones['FR_tongue_base']
		# --
		try:
			tbone = rig_arm.edit_bones['FR_tongue_end']
		except:
			pass
		else:
			tbone.use_connect = True
			tbone.parent = rig_arm.edit_bones['FR_tongue_middle']

		# -- PARENT JAW
		try:
			tbone = rig_arm.edit_bones['FR_upper_jaw']
		except:
			pass
		else:
			tbone.use_connect = False
			tbone.parent = rig_arm.edit_bones['DEF-head']
		# --	
		try:
			tbone = rig_arm.edit_bones['FR_lower_jaw']
		except:
			pass
		else:
			tbone.use_connect = False
			tbone.parent = rig_arm.edit_bones['FR_jaw']


		# ********************** create control ***********************

		# JAW ******************************************  jaw_tmp_location

		# -- create goints
		jaw_root_bone = rig_arm.edit_bones.new('jaw.cnt.root')
		jaw_root_bone.head = (0,0,0)
		jaw_root_bone.tail = (0,0,1)
		jaw_root_bone.layers = cnt_layer
		jaw_root_bone.parent = rig_arm.edit_bones['DEF-head']
		jaw_root_bone.use_deform = False
		jaw_root_bone.hide_select = True
		jaw_bone = rig_arm.edit_bones.new('jaw.cnt')
		jaw_bone.head = (0,0,0.8)
		jaw_bone.tail = (0,0,1)
		jaw_bone.layers = cnt_layer
		jaw_bone.parent = rig_arm.edit_bones['jaw.cnt.root']
		jaw_bone.use_deform = False

		# -- create mesh ------ 
		cat1 = jaw_tmp_location[1][0] - jaw_tmp_location[0][0]
		cat2 = jaw_tmp_location[1][1] - jaw_tmp_location[0][1]
		cat3 = jaw_tmp_location[1][2] - jaw_tmp_location[0][2]
		len_ = (cat1**2 + cat2**2 + cat3**2)**0.5

		layer_mesh = [False]*20
		layer_mesh[19] = True

		y = 0.2
		x = 1.0
		verts1 = ((-x,-y,0), (-x, 1, 0), (x,1,0), (x,-y,0))
		edges1 = ((0,1), (1,2), (2,3), (3,0))
		faces1 = []
		origin1 = (0,0,0)
		name1 = 'jaw.cnt.root.mesh'
		ob1 = self.createMesh(name1, origin1, verts1, edges1, faces1)
		ob1.location = (jaw_tmp_location[0][0], jaw_tmp_location[0][1], jaw_tmp_location[0][2])
		ob1.scale = (len_, len_, len_)
		ob1.layers = layer_mesh
		ob1.rotation_euler = (1.5708,0,0)
		verts2 = ((-1,-1,0), (-1, 1, 0), (1,1,0), (1,-1,0))
		edges2 = ((0,1), (1,2), (2,3), (3,0))
		faces2 = []
		origin2 = (0,0,0)
		name2= 'jaw.cnt.mesh'
		ob2 = self.createMesh(name2, origin2, verts2, edges2, faces2)
		ob2.rotation_euler = (1.5708,0,0)
		ob2.location = (jaw_tmp_location[0][0], jaw_tmp_location[0][1], (jaw_tmp_location[0][2] + len_*0.8))
		ob2.scale = ((len_*0.2), (len_*0.2), (len_*0.2))
		ob2.layers = layer_mesh

		# TONGUE ********************************************
		# -- create control bones
		for label in self.tongue_label:
			bone = rig_arm.edit_bones[('FR_' + label)]
			# --- bone propites
			#bone.bbone_segments = 7
			# --- create cnt bones
			tails = (bone.tail[0], bone.tail[1], bone.tail[2])
			bone_ = rig_arm.edit_bones.new(label)
			bone_.head[:] = tails[0], tails[1], tails[2]
			''' # old
			if label == 'tongue_end':
				bone_.tail[:] = tails[0], (tails[1] - 0.025), tails[2]
			else:
				bone_.tail[:] = tails[0], tails[1], (tails[2] + 0.025)
			'''
			# new
			bone_.tail[:] = tails[0], (tails[1] - 0.025), tails[2]
			bone_.roll = 0.0000
			bone_.use_deform = False
			bone_.use_connect = False
			bone_.parent = rig_arm.edit_bones['FR_jaw']
			bone_.layers = cnt_layer
			# b-bone size
			bone_.bbone_x = 0.0025
			bone_.bbone_z = 0.0025

			if label == 'tongue_end':
				# -- create end_tongue
				bone_ = rig_arm.edit_bones.new('end_tongue')
				bone_.head[:] = tails[0], tails[1], tails[2]
				bone_.tail[:] = tails[0], (tails[1] - 0.01), tails[2]
				bone_.roll = 0.0000
				bone_.use_deform = False
				bone_.use_connect = True
				bone_.parent = rig_arm.edit_bones['FR_' + label]
				bone_.layers = layer
				# b-bone size
				bone_.bbone_x = 0.001
				bone_.bbone_z = 0.001

			# create mesh
			verts2 = ((-0.5,-0.5,0), (0, 0.5, 0), (0.5,-0.5,0))
			edges2 = ((0,1), (1,2), (2,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= label + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh		

		# EYE_IK
		# -- make eye_r,l
		for label in self.eye_label:
			a = rig_arm.edit_bones[('FR_' + label)].head
			b = rig_arm.edit_bones[('FR_' + label)].tail
			x = (b[0] - a[0])*eye_ik_extending + a[0]
			y = (b[1] - a[1])*eye_ik_extending + a[1]
			z = (b[2] - a[2])*eye_ik_extending + a[2]

			bone = rig_arm.edit_bones.new(label)
			bone.head = (x,y,z)
			bone.tail = (x, y, (z + 0.03))
			bone.use_deform = False

			# create mesh
			verts = ((0,-0.5,0), (0, 0.5, 0), (-0.5,0,0), (0.5,0,0))
			edges = ((0,1), (2,3))
			faces = []
			origin = (0,0,0)
			name= label + '.mesh'
			cnt_mesh = self.createMesh(name, origin, verts, edges, faces)
			cnt_mesh.layers = layer_mesh

		# -- make eye_ik
		bone = rig_arm.edit_bones.new('eye_ik')
		y = rig_arm.edit_bones[self.eye_label[0]].head[1]
		z = rig_arm.edit_bones[self.eye_label[0]].head[2]
		bone.head = (0, y, z)
		bone.tail = (0, y, (z + 0.03))
		bone.use_deform = False
		bone.parent = rig_arm.edit_bones['DEF-head']

		# -- create mesh
		verts = ((0,-1,0), (-1,0,0), (0, 1, 0), (1,0,0), (0,-0.5,0), (0, 0.5,0), (-0.5,0,0), (0.5,0,0))
		edges = ((0,1), (1,2), (2,3), (3,0), (4,5), (6,7))
		faces = []
		origin = (0,0,0)
		name= 'eye_ik.mesh'
		cnt_mesh = self.createMesh(name, origin, verts, edges, faces)
		cnt_mesh.layers = layer_mesh

		# -- make eye_ik driver bones
		bone_root = rig_arm.edit_bones.new('eye_ik_root_parent')
		bone_root.head = bone.head
		bone_root.tail = bone.tail
		bone_root.parent = rig_arm.edit_bones['root']

		# -- eye_ik parents, properties
		bone0 = rig_arm.edit_bones[self.eye_label[0]]
		bone1 = rig_arm.edit_bones[self.eye_label[1]]
		bone0.parent = rig_arm.edit_bones['eye_ik']
		bone0.use_inherit_scale = False
		bone0.layers = cnt_layer
		bone1.parent = rig_arm.edit_bones['eye_ik']
		bone1.use_inherit_scale = False
		bone1.layers = cnt_layer

		# -- tongue, jaw axes
		# -- -- tongue Z_up
		for label in self.tongue_label:
			bone = rig_arm.edit_bones[('FR_' + label)]
			tail = (bone.tail[0], bone.tail[1], bone.tail[2])
			matrix = bone.matrix
			z_up_matrix = self.z_up(matrix)
			bone.matrix = z_up_matrix
			bone.tail = tail
			
		# -- -- JAW Z_up
		jaw_bone = rig_arm.edit_bones['FR_jaw']
		tail = (jaw_bone.tail[0], jaw_bone.tail[1], jaw_bone.tail[2])
		matrix = jaw_bone.matrix
		z_up_matrix = self.z_up(matrix)
		jaw_bone.matrix = z_up_matrix
		jaw_bone.tail = tail
		
		# -- -- ather Z_up
		bpy.ops.armature.select_all(action='DESELECT')
		
		rig_arm.edit_bones['end_tongue'].select = True
		#rig_arm.edit_bones['FR_jaw'].select = True
		#rig_arm.edit_bones['INCL_jaw'].select = True
		
		bpy.ops.armature.calculate_roll(type = 'GLOBAL_POS_Z')
		bpy.ops.armature.select_all(action='DESELECT')
		
		#rig_arm.edit_bones['tongue_end'].select = True
		#bpy.ops.armature.calculate_roll(type = 'POS_X')


		# ******** POSE bone EDIT *********
		bpy.ops.object.mode_set(mode = 'POSE')

		# -- Bone group create
		group_1 = rig_obj.pose.bone_groups.new(name="Face.cnts")
		group_1.color_set = 'THEME03'

		# ==== EAR edit
		r_ear_bones = rig_obj.pose.bones['FR_ear_R']
		l_ear_bones = rig_obj.pose.bones['FR_ear_L']
		# --- group
		r_ear_bones.bone_group = group_1
		l_ear_bones.bone_group = group_1
		# --- create mesh
		verts_r = ((0,-1,0), (-1,0,0), (0, 1, 0), (-0.2,-0.5,0), (-0.7,0,0), (-0.2, 0.5,0))
		edges_r = ((0,1), (1,2), (2,0), (3,4), (4,5), (5,3))
		verts_l = ((0,-1,0), (1,0,0), (0, 1, 0), (0.2,-0.5,0), (0.7,0,0), (0.2, 0.5,0))
		edges_l = ((0,1), (1,2), (2,0), (3,4), (4,5), (5,3))
		faces = []
		origin = (0,0,0)
		name_r= 'ear_R.mesh'
		name_l= 'ear_L.mesh'
		r_mesh = self.createMesh(name_r, origin, verts_r, edges_r, faces)
		l_mesh = self.createMesh(name_l, origin, verts_l, edges_l, faces)
		r_mesh.layers = layer_mesh
		l_mesh.layers = layer_mesh
		# --- apply mesh
		r_ear_bones.custom_shape = r_mesh
		l_ear_bones.custom_shape = l_mesh

		# ==== TEETH edit FR_upper_jaw
		up_teeth_bones = rig_obj.pose.bones['FR_upper_jaw']
		low_teeth_bones = rig_obj.pose.bones['FR_lower_jaw']
		# --- group
		up_teeth_bones.bone_group = group_1
		low_teeth_bones.bone_group = group_1
		# --- create mesh
		verts = ((-0.5,1,-0.05), (-0.5,1,0.05), (0.5, 1, 0.05), (0.5,1,-0.05))
		edges = ((0,1), (1,2), (2,3), (3,0))
		faces = []
		origin = (0,0,0)
		name_up= 'FR_upper_jaw.mesh'
		name_low= 'FR_lower_jaw.mesh'
		up_mesh = self.createMesh(name_up, origin, verts, edges, faces)
		low_mesh = self.createMesh(name_low, origin, verts, edges, faces)
		up_mesh.layers = layer_mesh
		low_mesh.layers = layer_mesh
		# --- apply mesh
		up_teeth_bones.custom_shape = up_mesh
		low_teeth_bones.custom_shape = low_mesh

		# ==== EYE_ik create constraint
		rig_obj.data.bones['eye_ik_root_parent'].hide = True
		# -- eye_ik add properties
		bpy.types.PoseBone.bodyParent =  bpy.props.FloatProperty(name = "bodyParent", default = 0.0, min = 0.0, max = 1.0)
		# -- eye_ik loc scale 
		bone_pose = rig_obj.pose.bones['eye_ik']
		bone_pose.lock_scale[1] = True
		bone_pose.lock_scale[2] = True
		bone_pose.bodyParent = 0.0
		# -- eye_ik mesh 
		bone_pose.custom_shape = bpy.data.objects['eye_ik.mesh']
		# -- eye_ik create loc constraint
		cns = bone_pose.constraints.new('COPY_LOCATION')
		cns.target = rig_obj
		cns.subtarget = 'eye_ik_root_parent'

		fcurve = cns.driver_add('influence')
		drv = fcurve.driver
		drv.type = 'AVERAGE'
		drv.show_debug_info = True

		var = drv.variables.new()
		var.name = 'var'
		var.type = 'SINGLE_PROP'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.bone_target = 'eye_ik'
		targ.data_path = 'pose.bones["eye_ik"]["bodyParent"]'

		# -- eye_ik create loc constraint
		cns_r = bone_pose.constraints.new('COPY_ROTATION')
		cns_r.target = rig_obj
		cns_r.subtarget = 'eye_ik_root_parent'

		fcurve = cns_r.driver_add('influence')
		drv = fcurve.driver
		drv.type = 'AVERAGE'
		drv.show_debug_info = True

		var = drv.variables.new()
		var.name = 'var'
		var.type = 'SINGLE_PROP'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.bone_target = 'eye_ik'
		targ.data_path = 'pose.bones["eye_ik"]["bodyParent"]'

		# -- eye_ik create AIM constraint and apply mesh
		for label in self.eye_label:
			bone_pose = rig_obj.pose.bones[('FR_' + label)]
			cns = bone_pose.constraints.new('TRACK_TO')
			cns.target = rig_obj
			cns.subtarget = label
			cns.track_axis = 'TRACK_Y'
			cns.up_axis = 'UP_Z'
			# --- group
			rig_obj.pose.bones[label].bone_group = group_1
			# --- mesh
			cnt_pose = rig_obj.pose.bones[(label)]
			mesh = bpy.data.objects[(label + '.mesh')]
			cnt_pose.custom_shape = mesh

		# ==== JAW cnt EDIT
		# -- custom shape
		jaw_root_pose = rig_obj.pose.bones['jaw.cnt.root']
		jaw_root_pose.custom_shape = ob1
		jaw_cnt_pose = rig_obj.pose.bones['jaw.cnt']
		jaw_cnt_pose.custom_shape = ob2

		# -- group
		jaw_cnt_pose.bone_group = group_1

		# -- location
		cat1 = jaw_tmp_location[1][0] - jaw_tmp_location[0][0]
		cat2 = jaw_tmp_location[1][1] - jaw_tmp_location[0][1]
		cat3 = jaw_tmp_location[1][2] - jaw_tmp_location[0][2]
		len_ = (cat1**2 + cat2**2 + cat3**2)**0.5
		jaw_root_pose.location = (jaw_tmp_location[0][0], jaw_tmp_location[0][2], -jaw_tmp_location[0][1])
		jaw_root_pose.scale = (len_, len_, len_)
		# -- loc control
		jaw_cnt_pose.lock_location[2] = True
		jaw_cnt_pose.lock_rotation = (True, True, True)
		jaw_cnt_pose.lock_rotation_w = True
		jaw_cnt_pose.lock_scale = (True, True, True)
		# -- limit location constraint
		cns = jaw_cnt_pose.constraints.new('LIMIT_LOCATION')
		cns.owner_space = 'LOCAL'
		cns.use_transform_limit = True
		cns.use_min_x = True
		cns.min_x = -1
		cns.use_max_x = True
		cns.max_x = 1
		cns.use_min_y = True
		cns.min_y = -1
		cns.use_max_y = True
		cns.max_y = 0
		cns.use_min_z = True
		cns.min_z = 0
		cns.use_max_z = True
		cns.max_z = 0
		
		# -------- JAW DRIVERS -----------
		cnt_name = 'cnt'
		open_name = 'jaw_open'
		side_name = 'jaw_side'
		incline_name = 'jaw_incline'
		fwd_name = 'jaw_fwd'
		back_name = 'jaw_back'
		# -- affect to jaw - FWD JAW
		# --- f curve
		fcurve = rig_obj.pose.bones['FWD_jaw'].driver_add('location', 1)
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = '%s * %s if %s>0 else %s * %s' % (cnt_name, fwd_name, cnt_name, cnt_name, back_name)
		drv.show_debug_info = True
		# --- var
		var = drv.variables.new()
		var.name = cnt_name
		var.type = 'TRANSFORMS'
		# --- targ
		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = 'jaw_back_fwd'
		targ.transform_space = 'LOCAL_SPACE'
		# --- var2
		var2 = drv.variables.new()
		var2.name = fwd_name
		var2.type = 'SINGLE_PROP'
		# --- var2.targ
		targ = var2.targets[0]
		targ.id_type = 'ARMATURE'
		targ.id = rig_arm
		targ.data_path = '["%s"]' % fwd_name
		# --- var3
		var3 = drv.variables.new()
		var3.name = back_name
		var3.type = 'SINGLE_PROP'
		# --- var3.targ
		targ = var3.targets[0]
		targ.id_type = 'ARMATURE'
		targ.id = rig_arm
		targ.data_path = '["%s"]' % back_name

		# -- affect to jaw - OPEN JAW
		# set ratation mode
		jaw_bone = rig_obj.pose.bones['FR_jaw']
		jaw_bone.rotation_mode = 'XZY'
		# --- f curve
		fcurve = jaw_bone.driver_add('rotation_euler', 0)
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = '%s * %s' % (cnt_name, open_name)
		drv.show_debug_info = True
		# --- var
		var = drv.variables.new()
		var.name = cnt_name
		var.type = 'TRANSFORMS'
		# --- var.targ 
		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = 'jaw.cnt'
		targ.transform_space = 'LOCAL_SPACE'
		# --- var2
		var2 = drv.variables.new()
		var2.name = open_name
		var2.type = 'SINGLE_PROP'
		# --- var2.targ
		targ = var2.targets[0]
		targ.id_type = 'ARMATURE'
		targ.id = rig_arm
		targ.data_path = '["%s"]' % open_name

		'''
		# --- modifires
		fmod = fcurve.modifiers[0]
		fmod.mode = 'POLYNOMIAL'
		fmod.poly_order = 1
		fmod.coefficients = (0.0, 0.3)
		'''

		# -- affect to jaw - SIDE JAW
		# --- f curve
		fcurve = jaw_bone.driver_add('rotation_euler', 2)
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = '%s * %s' % (cnt_name, side_name)
		drv.show_debug_info = True
		# --- var
		var = drv.variables.new()
		var.name = cnt_name
		var.type = 'TRANSFORMS'
		# --- targ
		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_X'
		targ.bone_target = 'jaw.cnt'
		targ.transform_space = 'LOCAL_SPACE'
		# --- var2
		var2 = drv.variables.new()
		var2.name = side_name
		var2.type = 'SINGLE_PROP'
		# --- var2.targ
		targ = var2.targets[0]
		targ.id_type = 'ARMATURE'
		targ.id = rig_arm
		targ.data_path = '["%s"]' % side_name

		'''
		# --- modifires
		fmod = fcurve.modifiers[0]
		fmod.mode = 'POLYNOMIAL'
		fmod.poly_order = 1
		fmod.coefficients = (0.0, 0.1)
		'''

		# -- affect to jaw - INCLINE JAW
		# --- f curve
		fcurve = jaw_bone.driver_add('rotation_euler', 1)
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = '%s * %s' % (cnt_name, incline_name)
		drv.show_debug_info = True
		# --- var
		var = drv.variables.new()
		var.name = cnt_name
		var.type = 'TRANSFORMS'
		# --- targ
		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_X'
		targ.bone_target = 'jaw.cnt'
		targ.transform_space = 'LOCAL_SPACE'
		# --- var2
		var2 = drv.variables.new()
		var2.name = incline_name
		var2.type = 'SINGLE_PROP'
		# --- var2.targ
		targ = var2.targets[0]
		targ.id_type = 'ARMATURE'
		targ.id = rig_arm
		targ.data_path = '["%s"]' % incline_name

		'''
		# --- modifires
		fmod = fcurve.modifiers[0]
		fmod.mode = 'POLYNOMIAL'
		fmod.poly_order = 1
		fmod.coefficients = (0.0, 0.03)
		'''

		# ==== TONGUE add control attribute
		bpy.types.PoseBone.autoScaleTongue =  bpy.props.FloatProperty(name = "autoScaleTongue", default = 1.0,min = 0.0, max = 1.0)
		bpy.types.PoseBone.scaleFactor =  bpy.props.FloatProperty(name = "scaleFactor", default = 1.0,min = 0.0, max = 3.0)
		bpy.types.PoseBone.smoothTongue =  bpy.props.FloatProperty(name = "smoothTongue", default = 1.0,min = 0.0, max = 2.0)
		pose = rig_obj.pose.bones['tongue_end']
		pose.autoScaleTongue = 1.0
		pose.scaleFactor = 1.0
		pose.smoothTongue = 1.0

		for i, label in enumerate(self.tongue_label, 0):
			bone_pose = rig_obj.pose.bones['FR_' + label]
			bone = rig_arm.bones['FR_' + label]
			cnt_pose = rig_obj.pose.bones[label]

			# -- mesh
			mesh_name = label + '.mesh'
			cnt_pose.custom_shape = bpy.data.objects[mesh_name]

			# -- group
			cnt_pose.bone_group = group_1
			
			# -- cnt properties
			cnt_pose.lock_scale[1] = True
			cnt_pose.rotation_mode = 'YXZ'
			if label != 'tongue_end':
				cnt_pose.lock_rotation[0] = True
				cnt_pose.lock_rotation[2] = True

			# -- bone properties
			bone_pose.rotation_mode = 'YXZ'

			# --- add driver bbone_in
			fcurve = bone.driver_add('bbone_in')
			drv = fcurve.driver
			drv.type = 'AVERAGE'
			drv.show_debug_info = True

			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'

			targ = var.targets[0]
			targ.id = rig_obj
			targ.bone_target = 'tongue_end'
			targ.data_path = 'pose.bones[\"tongue_end\"][\"smoothTongue\"]'

			# --- add driver bbone_out
			fcurve = bone.driver_add('bbone_out')
			drv = fcurve.driver
			drv.type = 'AVERAGE'
			drv.show_debug_info = True

			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'

			targ = var.targets[0]
			targ.id = rig_obj
			targ.bone_target = 'tongue_end'
			targ.data_path = 'pose.bones[\"tongue_end\"][\"smoothTongue\"]'

			# --- to stretch constraint
			cns = bone_pose.constraints.new('STRETCH_TO')
			cns.target = rig_obj
			cns.subtarget = label
			
			# --- add driver
			fcurve = cns.driver_add('bulge')
			
			drv = fcurve.driver
			drv.type = 'AVERAGE'
			drv.show_debug_info = True
			
			var = drv.variables.new()
			var.name = 'var'
			var.type = 'SINGLE_PROP'

			targ = var.targets[0]
			targ.id = rig_obj
			targ.bone_target = 'tongue_end'
			targ.data_path = 'pose.bones[\"tongue_end\"][\"scaleFactor\"]'

			# --- scale constraint
			if i >0:
				# -- add copy_scale constraint
				sc_cns = bone_pose.constraints.new('COPY_SCALE')
				sc_cns.target = rig_obj
				sc_cns.subtarget = self.tongue_label[i-1]
				sc_cns.use_x = True
				sc_cns.use_y = False
				sc_cns.use_z = True
				sc_cns.target_space = 'LOCAL'
				sc_cns.owner_space  = 'LOCAL'
				# -- add driver to copy_scale constraint
				fcurve = sc_cns.driver_add('influence')
				drv = fcurve.driver
				drv.type = 'SCRIPTED'
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'SINGLE_PROP'

				targ = var.targets[0]
				targ.id = rig_obj
				targ.bone_target = 'tongue_end'
				targ.data_path = 'pose.bones[\"tongue_end\"][\"autoScaleTongue\"]'

				drv.expression = '1 - var'

				# -- add driver to Y rotate
				fcurve = bone_pose.driver_add('rotation_euler', 1)
				drv = fcurve.driver
				drv.type = 'AVERAGE'
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig_obj
				targ.transform_type = 'ROT_Y'
				targ.bone_target = self.tongue_label[(i-1)]
				targ.transform_space = 'LOCAL_SPACE'

		# add constraint to 'end_tongue'
		pose_end = rig_obj.pose.bones['end_tongue']
		r_cns = pose_end.constraints.new('COPY_ROTATION')
		r_cns.target = rig_obj
		r_cns.subtarget = 'tongue_end'
		r_cns.use_x = True
		r_cns.use_y = True
		r_cns.use_z = True
		r_cns.use_offset = False
		r_cns.target_space = 'WORLD'
		r_cns.owner_space  = 'WORLD'

		# ------------ Create Armature Deformer ------- self.mesh_passp_bones
		
		for key in mesh_passport:
			for mesh_name in mesh_passport[key]:
				try:
					mesh = bpy.data.objects[mesh_name]
				except:
					print(('****** ' + mesh_name + ' not found!'))
					continue
				# -- test exists armature
				list_modif = mesh.modifiers
				exists_armature = False
				for modif in list_modif:
					if modif.type == 'ARMATURE':
						exists_armature = True
				# -- create ARMATURE modifiers
				if not exists_armature:
					modif_name = mesh_name + '_armature'
					armature = mesh.modifiers.new(name = modif_name, type = 'ARMATURE')
					armature.object = rig_obj
				# vtx groups
				if key == 'tongue':
					for i,vtx_group_name in enumerate(self.mesh_passp_bones[key]):
						vtx_group = mesh.vertex_groups.new(vtx_group_name)
						a = tails_global['tongue_end'][1]
						b = (tails_global['tongue_middle'][1] + heads['tongue_middle'][1])/2
						c = heads['tongue_base'][1]
						if i == 0:
							for vtx in mesh.data.vertices:
								weight = 0
								dist = vtx.co[1]
								if dist > b and dist <= c:
									weight = (math.cos(math.pi*((dist-a)/(b-a))) + 1)/2
								elif dist >c:
									weight = 1
								elif dist == b:
									weight = 0
								vtx_group.add([vtx.index], weight, 'REPLACE')
						elif i == 1:
							for vtx in mesh.data.vertices:
								weight = 0
								dist = vtx.co[1]
								if dist > a and dist <= b:
									weight = (math.cos(math.pi*((dist-a)/(b-a)) + math.pi) + 1)/2
								elif dist >b and dist < c:
									weight = (math.cos(math.pi*((dist-b)/(c-b))) + 1)/2
								elif dist == a:
									weight = 0
								vtx_group.add([vtx.index], weight, 'REPLACE')
						elif i == 2:
							for vtx in mesh.data.vertices:
								weight = 0
								dist = vtx.co[1]
								if dist >= a and dist < b:
									weight = (math.cos(math.pi*((dist-a)/(b-a))) + 1)/2
								elif dist < a:
									weight = 1
								else:
									weight = 0
								vtx_group.add([vtx.index], weight, 'REPLACE')
				elif key == 'body':
					vtx_group_name = 'FR_jaw'
					if not vtx_group_name in mesh.vertex_groups.keys():
						vtx_group = mesh.vertex_groups.new(vtx_group_name)
							
				else:
					try:
						vtx_group_name = self.mesh_passp_bones[key][0]
					except:
						continue
					vtx_group = mesh.vertex_groups.new(vtx_group_name)
					for vtx in mesh.data.vertices:
						vtx_group.add([vtx.index], 1.0, 'REPLACE')
				
				# parent mesh
				mesh.parent = rig_obj
				mesh.parent_type = 'OBJECT'
						
		'''
		# ------------ create all cnt ------------------
		self.create_all_cnt(bpy.context)
		'''
		# ------------ create edit vertex groups -------
		face_shape_keys().create_edit_vertes_groups(bpy.context)
		
		# ------------ create lattice (str/sq, eye_global) ----------
		bpy.context.scene.objects.active = rig_obj
		bpy.ops.object.mode_set(mode = 'OBJECT')
		self.stretch_squash_lattice(bpy.context)
		
		# ------------ create face ui ----------------
		face_ui = self.create_face_ui()
		print(face_ui[1])

		return(True, ('*'*10 + ' face rig created'))
		
		
	def toggle_deform_bone(self, context, action):
		pass
		# get ARMATURE
		ob = context.object
		if ob.type != 'ARMATURE':
			return(False, 'The selected object is not "ARMATURE"')
		bpy.ops.object.mode_set(mode = 'POSE')
		
		exclusions = ['jaw', 'ear_L', 'ear_R']
		for label in self.label_bones:
			if label in exclusions:
				continue
			else:
				name = 'FR_' + label
				if not name in ob.pose.bones:
					print(('Not Bone with name: ' + name))
					continue
				bone = ob.data.bones[name]
				if action == 'on':
					bone.use_deform = True
				elif action == 'off':
					bone.use_deform = False
		return(True, ('Use Deform ' + action))
		
	def clear_skin(self, context, as_ = 'BODY'):
		pass
		#mesh = bpy.context.object
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		
		if as_ == 'BODY':
			# get mesh
			try:
				mesh = bpy.data.objects[mesh_passport['body'][0]]
			except:
				return(False, '***** Not key \"body\" in mesh_passport')
			else:
				#return(mesh)
				pass
			
			# mesh to EDIT mode
			bpy.context.scene.objects.active = mesh
			bpy.ops.object.mode_set(mode='EDIT')
					
			#bpy.ops.object.mode_set(mode='OBJECT')
			head_vtx_grp = mesh.vertex_groups['DEF-head']
			exclusions = ['jaw', 'ear_L', 'ear_R']
			for label in self.label_bones:
				if label in exclusions:
					continue
				else:
					name = 'FR_' + label
					try:
						vtx_grp = mesh.vertex_groups[name]
					except:
						print(('NO  ' + name))
					else:
						for vtx in mesh.data.vertices:
							'''
							try:
								vtx_weight = vtx_grp.weight(vtx.index)
							except:
								continue
							else:
								try:
									head_vtx_weight = vtx_grp.weight(vtx.index)
								except:
									head_vtx_weight = 0.0
								vtx_weight = vtx_grp.weight(vtx.index)
								weight = vtx_weight + head_vtx_weight
								head_vtx_grp.add([vtx.index], weight, 'REPLACE')
								vtx_grp.add([vtx.index], 0.0, 'REPLACE')
							'''
						index = vtx_grp.index
						mesh.vertex_groups.active_index = index
						bpy.ops.object.vertex_group_select()
						mesh.vertex_groups.remove(vtx_grp)
						
			# apply vertex to head
			
			index = bpy.context.object.vertex_groups['DEF-head'].index
			mesh.vertex_groups.active_index = index
			bpy.ops.object.vertex_group_assign()
			
			return(True, 'All Right!')
			
		elif as_ == 'UPPER_JAW':
			# get mesh
			try:
				mesh = bpy.data.objects[mesh_passport['upper_jaw'][0]]
			except:
				return(False, '***** Not key \"body\" in mesh_passport')
			else:
				#return(mesh)
				pass
			
			# mesh to EDIT mode
			bpy.context.scene.objects.active = mesh
			bpy.ops.object.mode_set(mode='EDIT')
			
			exclusions = 'upper_jaw'
			for vtx_grp in list(mesh.vertex_groups):
				if vtx_grp.name != ('FR_' + exclusions):
					mesh.vertex_groups.remove(vtx_grp)

		elif as_ == 'LOWER_JAW':
			# get mesh
			try:
				mesh = bpy.data.objects[mesh_passport['lower_jaw'][0]]
			except:
				return(False, '***** Not key \"body\" in mesh_passport')
			else:
				#return(mesh)
				pass
			
			# mesh to EDIT mode
			bpy.context.scene.objects.active = mesh
			bpy.ops.object.mode_set(mode='EDIT')
			
			exclusions = 'lower_jaw'
			for vtx_grp in list(mesh.vertex_groups):
				if vtx_grp.name != ('FR_' + exclusions):
					mesh.vertex_groups.remove(vtx_grp)

		elif as_ == 'EYE_R':
			bpy.ops.object.mode_set(mode='EDIT')
			exclusions = 'eye_R'
			for vtx_grp in list(mesh.vertex_groups):
				if vtx_grp.name != ('FR_' + exclusions):
					mesh.vertex_groups.remove(vtx_grp)

		elif as_ == 'EYE_L':
			bpy.ops.object.mode_set(mode='EDIT')
			exclusions = 'eye_L'
			for vtx_grp in list(mesh.vertex_groups):
				if vtx_grp.name != ('FR_' + exclusions):
					mesh.vertex_groups.remove(vtx_grp)

		elif as_ == 'TONGUE':
			bpy.ops.object.mode_set(mode='EDIT')
			exclusions = ['tongue']
			for vtx_grp in list(mesh.vertex_groups):
				if vtx_grp.name.replace('FR_', '') in tongue_label:
					continue
				else:
					mesh.vertex_groups.remove(vtx_grp)

		# finale		
		bpy.ops.object.mode_set(mode='OBJECT')

	def bone_controls_create(self, context, tmp_name, parent, type = 'LINE', color = 'YELLOW'):
		colors = ('YELLOW', 'GREEN')
		types = ('LINE', 'LINE_DUBBLE', 'THREE_SIDE','THREE_SIDE2', 'FOUR_SIDE', 'FOUR_SIDE2', 'CIRCLE')
		if not (color in colors):
			print('****** color can be only from the list: ', colors)
			return False, ('****** color can be only from the list: ', colors)
		if not (type in types):
			print('****** type can be only from the list: ', types)
			return False, ('****** type can be only from the list: ', types)
		# -- TMP rig to EDIT mode
		scene = bpy.context.scene
		tmp_rig = bpy.data.objects['face_rig_tmp']
		scene.objects.active = tmp_rig
		bpy.ops.object.mode_set(mode = 'EDIT')

		# -- get TMP Position
		tmp_bone = tmp_rig.data.edit_bones[tmp_name]
		head = (tmp_bone.head[0], tmp_bone.head[1], tmp_bone.head[2])
		tail = (tmp_bone.tail[0], tmp_bone.tail[1], tmp_bone.tail[2])

		# -- TMP rig to OBJECT mode
		bpy.ops.object.mode_set(mode = 'OBJECT')

		# -- rig to EDIT mode
		rig_obj = bpy.data.objects['rig']
		scene.objects.active = rig_obj
		bpy.ops.object.mode_set(mode = 'EDIT')

		# -- CREATE BONES
		# -- bone layers
		cnt_layer = [False]*32
		cnt_layer[20] = True

		rig_arm = rig_obj.data
		root_name = tmp_name.replace('FRTMP_','') + '.root'
		name = tmp_name.replace('FRTMP_','')
		# -- -- root bone
		root_bone = rig_arm.edit_bones.new(root_name)
		root_bone.head = (0,0,0)
		root_bone.tail = (0,0,1)
		#root_bone.parent = rig_arm.edit_bones['DEF-head']
		# parent bone (new version)
		try:
			root_bone.parent = rig_arm.edit_bones[parent]
		except:
			try:
				root_bone.parent = rig_arm.edit_bones['DEF-head']
			except:
				pass
		root_bone.show_wire = True
		root_bone.layers = cnt_layer
		root_bone.hide_select = True
		root_bone.use_deform = False
		# -- -- cnt bone
		if type == 'THREE_SIDE' or type == 'THREE_SIDE2':
			k = 0.4
		else:
			k = 0.3
		# +++++
		if type == 'LINE_DUBBLE' or type == 'FOUR_SIDE'  or type == 'FOUR_SIDE2':
			cnt_bone = rig_arm.edit_bones.new(name)
			cnt_bone.head = (0,0,1)
			cnt_bone.tail = (0,0,1.5)
			cnt_bone.parent = root_bone
			cnt_bone.show_wire = True
			cnt_bone.layers = cnt_layer
		# +++++	
		elif type == 'CIRCLE':
			cnt_bone = rig_arm.edit_bones.new(name)
			cnt_bone.head = (0,0,0)
			cnt_bone.tail = (0,0,1)
			cnt_bone.parent = root_bone
			cnt_bone.show_wire = True
			cnt_bone.layers = cnt_layer

		else:
			cnt_bone = rig_arm.edit_bones.new(name)
			cnt_bone.head = (0,0,0)
			cnt_bone.tail = (0,0,k)
			cnt_bone.parent = root_bone
			cnt_bone.show_wire = True
			cnt_bone.layers = cnt_layer
		cnt_bone.use_deform = False

		# -- Bone group create
		# cnt Group
		if color == 'YELLOW':
			try:
				b_group = rig_obj.pose.bone_groups["Face.yellow.cnts"]
			except:
				b_group = rig_obj.pose.bone_groups.new(name="Face.yellow.cnts")
			b_group.color_set = 'THEME09'
		elif color == 'GREEN':
			try:
				b_group = rig_obj.pose.bone_groups["Face.green.cnts"]
			except:
				b_group = rig_obj.pose.bone_groups.new(name="Face.green.cnts")
			b_group.color_set = 'THEME03'
		# root Group
		try:
			b_group_root = rig_obj.pose.bone_groups["Face.gray.cnts"]
		except:
			b_group_root = rig_obj.pose.bone_groups.new(name="Face.gray.cnts")
		b_group_root.color_set = 'THEME13'

		if type == 'LINE':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			verts1 = ((0,0,0), (0, 1, 0))
			edges1 = ((0,1), (1,0))
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			verts2 = ((-0.5,-0.5,0), (-0.5, 0.5, 0), (0.5,0.5,0), (0.5,-0.5,0))
			edges2 = ((0,1), (1,2), (2,3), (3,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		elif type == 'LINE_DUBBLE':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			#verts1 = ((0,-1,0), (0, 1, 0)) # old version
			verts1 = ((0,0,0), (0, 2, 0))
			edges1 = ((0,1), (1,0))
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			verts2 = ((-0.5,-0.5,0), (-0.5, 0.5, 0), (0.5,0.5,0), (0.5,-0.5,0))
			edges2 = ((0,1), (1,2), (2,3), (3,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		elif type == 'THREE_SIDE':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			verts1 = ((0,0,0), (0, 1, 0), (-1, 0, 0), (1, 0, 0))
			edges1 = ((0,1), (2,3))
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			#verts2 = ((-0.5,-0.5,0), (-0.5, 0.5, 0), (0.5,0.5,0), (0.5,-0.5,0)) # old
			verts2 = ((-1,-0.5,0), (-1, 0.5, 0), (1,0.5,0), (1,-0.5,0))
			edges2 = ((0,1), (1,2), (2,3), (3,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		elif type == 'THREE_SIDE2':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			verts1 = ((-1,0,0), (-1, 1, 0), (1, 1, 0), (1, 0, 0))
			edges1 = ((0,1), (1,2), (2,3), (3,0))
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			#verts2 = ((-0.5,-0.5,0), (-0.5, 0.5, 0), (0.5,0.5,0), (0.5,-0.5,0)) # old 
			verts2 = ((-1,-0.5,0), (-1, 0.5, 0), (1,0.5,0), (1,-0.5,0))
			edges2 = ((0,1), (1,2), (2,3), (3,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		elif type == 'FOUR_SIDE':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			verts1 = ((0,0,0), (0, 2, 0), (-1, 1, 0), (1, 1, 0))
			edges1 = ((0,1), (2,3))
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			verts2 = ((-0.5,-0.5,0), (-0.5, 0.5, 0), (0.5,0.5,0), (0.5,-0.5,0))
			edges2 = ((0,1), (1,2), (2,3), (3,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		elif type == 'FOUR_SIDE2':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			verts1 = ((-1,0,0), (-1, 2, 0), (1, 2, 0), (1, 0, 0))
			edges1 = ((0,1), (1,2), (2,3), (3,0))
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			verts2 = ((-0.5,-0.5,0), (-0.5, 0.5, 0), (0.5,0.5,0), (0.5,-0.5,0))
			edges2 = ((0,1), (1,2), (2,3), (3,0))
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		elif type == 'CIRCLE':
			# -- CREATE MESH
			layer_mesh = [False]*20
			layer_mesh[19] = True
			# -- root mesh
			verts1 = self.circle_verts
			edges1 = self.circle_edges
			faces1 = []
			origin1 = (0,0,0)
			name1 = root_name + '.mesh'
			root_mesh = self.createMesh(name1, origin1, verts1, edges1, faces1)
			root_mesh.layers = layer_mesh
			# -- cnt mesh
			verts2 = verts1
			edges2 = edges1
			faces2 = []
			origin2 = (0,0,0)
			name2= name + '.mesh'
			cnt_mesh = self.createMesh(name2, origin2, verts2, edges2, faces2)
			cnt_mesh.layers = layer_mesh
		else:
			return False, '****** not Types!'

		# -- EDIT BONES
		# -- rig to POSE mode
		scene.objects.active = rig_obj
		bpy.ops.object.mode_set(mode = 'POSE')

		# -- get coordinates
		cat1 = tail[0] - head[0]
		cat2 = tail[1] - head[1]
		cat3 = tail[2] - head[2]
		len_cnt = (cat1**2 + cat2**2 + cat3**2)**0.5
		if cat3 != 0:
			rotateZ = -1*(math.atan(cat1/cat3))
		else:
			if cat1>0:
				rotateZ = 3.1415936/2*-1
			else:
				rotateZ = 3.1415936/2
		if cat3<0:
			rotateZ = rotateZ + 3.1415936
		#print('cat1',cat1 , 'cat2', cat2)
		if cat1 != 0:
			rotateX = -1*(math.atan(cat2/cat1)) #+ 3.1415936/2
		else:
			rotateX = 0

		if cat1 < 0 and cat2 > 0:
			rotateX = -1 * rotateX
		elif cat1 < 0 and cat2 < 0:
			rotateX = -1 * rotateX

		# -- set position of bone // custom_shape
		# -- -- root bone
		pose_root = rig_obj.pose.bones[root_name]
		pose_root.rotation_mode = 'XYZ'
		pose_root.location = (head[0], head[2], head[1]*-1)
		# +++++
		if type == 'LINE_DUBBLE' or type == 'FOUR_SIDE'  or type == 'FOUR_SIDE2' or type == 'CIRCLE':
			pose_root.scale = (len_cnt/2, len_cnt/2, len_cnt/2)
		elif type == 'THREE_SIDE' or type == 'THREE_SIDE2':
			pose_root.scale = (len_cnt/2, len_cnt, len_cnt)
		else:
			pose_root.scale = (len_cnt, len_cnt, len_cnt)
		pose_root.rotation_euler[2] = rotateZ
		pose_root.rotation_euler[0] = rotateX
		pose_root.custom_shape = root_mesh
		pose_root.bone_group = b_group_root

		# -- -- cnt bone
		pose_cnt = rig_obj.pose.bones[name]
		pose_cnt.custom_shape = cnt_mesh
		pose_cnt.bone_group = b_group

		if type == 'LINE':
			# -- loc control
			pose_cnt.lock_location[0] = True
			pose_cnt.lock_location[2] = True
			pose_cnt.lock_rotation = (True, True, True)
			pose_cnt.lock_rotation_w = True
			pose_cnt.lock_scale = (True, True, True)
			# -- limit location constraint
			cns = pose_cnt.constraints.new('LIMIT_LOCATION')
			cns.owner_space = 'LOCAL'
			cns.use_transform_limit = True
			cns.use_min_x = True
			cns.min_x = 0
			cns.use_max_x = True
			cns.max_x = 0
			cns.use_min_y = True
			cns.min_y = 0
			cns.use_max_y = True
			cns.max_y = 1
			cns.use_min_z = True
			cns.min_z = 0
			cns.use_max_z = True
			cns.max_z = 0
		elif type == 'LINE_DUBBLE':
			# -- loc control
			pose_cnt.lock_location[0] = True
			pose_cnt.lock_location[2] = True
			pose_cnt.lock_rotation = (True, True, True)
			pose_cnt.lock_rotation_w = True
			pose_cnt.lock_scale = (True, True, True)
			# -- limit location constraint
			cns = pose_cnt.constraints.new('LIMIT_LOCATION')
			cns.owner_space = 'LOCAL'
			cns.use_transform_limit = True
			cns.use_min_x = True
			cns.min_x = 0
			cns.use_max_x = True
			cns.max_x = 0
			cns.use_min_y = True
			cns.min_y = -1
			cns.use_max_y = True
			cns.max_y = 1
			cns.use_min_z = True
			cns.min_z = 0
			cns.use_max_z = True
			cns.max_z = 0
		elif type == 'THREE_SIDE' or type == 'THREE_SIDE2':
			# -- loc control
			pose_cnt.lock_location[2] = True
			pose_cnt.lock_rotation = (True, True, True)
			pose_cnt.lock_rotation_w = True
			pose_cnt.lock_scale = (True, True, True)
			# -- limit location constraint
			cns = pose_cnt.constraints.new('LIMIT_LOCATION')
			cns.owner_space = 'LOCAL'
			cns.use_transform_limit = True
			cns.use_min_x = True
			cns.min_x = -1
			cns.use_max_x = True
			cns.max_x = 1
			cns.use_min_y = True
			cns.min_y = 0
			cns.use_max_y = True
			cns.max_y = 1
			cns.use_min_z = True
			cns.min_z = 0
			cns.use_max_z = True
			cns.max_z = 0
		elif type == 'FOUR_SIDE'  or type == 'FOUR_SIDE2':
			# -- loc control
			pose_cnt.lock_location[2] = True
			pose_cnt.lock_rotation = (True, True, True)
			pose_cnt.lock_rotation_w = True
			pose_cnt.lock_scale = (True, True, True)
			# -- limit location constraint
			cns = pose_cnt.constraints.new('LIMIT_LOCATION')
			cns.owner_space = 'LOCAL'
			cns.use_transform_limit = True
			cns.use_min_x = True
			cns.min_x = -1
			cns.use_max_x = True
			cns.max_x = 1
			cns.use_min_y = True
			cns.min_y = -1
			cns.use_max_y = True
			cns.max_y = 1
			cns.use_min_z = True
			cns.min_z = 0
			cns.use_max_z = True
			cns.max_z = 0
		elif type == 'CIRCLE':
			# -- loc control
			pose_cnt.lock_location[2] = True
			pose_cnt.lock_rotation = (True, True, True)
			pose_cnt.lock_rotation_w = True
			pose_cnt.lock_scale = (True, True, True)

		else:
			return False, '****** not limits'

		# -- Mesh Position
		# +++++
		if type == 'LINE_DUBBLE' or type == 'FOUR_SIDE'  or type == 'FOUR_SIDE2':
			root_mesh.scale = (len_cnt/2, len_cnt/2, len_cnt/2)
		else:
			root_mesh.scale = (len_cnt, len_cnt, len_cnt)
		root_mesh.location = head
		root_mesh.rotation_euler = (90/57.29577, -1*rotateZ, -1*rotateX)
		# +++++
		if type == 'LINE_DUBBLE' or type == 'FOUR_SIDE'  or type == 'FOUR_SIDE2':
			cnt_mesh.scale = (len_cnt*k/2, len_cnt*k/2, len_cnt*k/2)
		elif type == 'THREE_SIDE' or type == 'THREE_SIDE2':
			cnt_mesh.scale = (len_cnt*k/2, len_cnt*k, len_cnt*k)
			root_mesh.scale = (len_cnt/2, len_cnt, len_cnt)
		elif type == 'CIRCLE':
			cnt_mesh.scale = (len_cnt/2, len_cnt/2, len_cnt/2)
			root_mesh.scale = (len_cnt/2, len_cnt/2, len_cnt/2)
		else:
			cnt_mesh.scale = (len_cnt*k, len_cnt*k, len_cnt*k)
		cnt_mesh.location = head
		cnt_mesh.rotation_euler = (90/57.29577, -1*rotateZ, -1*rotateX)

		return cnt_bone, pose_cnt, name
	
	def createMesh(self, name, origin, verts, edges, faces):
		pass
		# Create mesh and object
		me = bpy.data.meshes.new(name+'Mesh')
		ob = bpy.data.objects.new(name, me)
		ob.location = origin
		ob.show_name = True
		# Link object to scene
		bpy.context.scene.objects.link(ob)

		# Create mesh from given verts, edges, faces. Either edges or
		# faces should be [], or you ask for problems
		me.from_pydata(verts, edges, faces)

		# Update mesh with new data
		me.update(calc_edges=True)
		return ob
	
	def create_all_cnt(self, context):
		tmp_rig = bpy.data.objects['face_rig_tmp']
		layer = [False]*20
		layer[0] = True
		tmp_rig.layers = layer

		for tmp in self.tmp_bones:
			#result = bone_controls_create(bpy.context, tmp[0], tmp[2], type = tmp[1], color = 'GREEN')
			result = self.bone_controls_create(bpy.context, tmp[0], tmp[2], type = tmp[1])
			#print(result)

		layer = [False]*20
		layer[9] = True
		tmp_rig.layers = layer
		
	def stretch_squash_lattice(self, context):
		pass
		# ****** GET HEAD POS
		# start - tmp rig in active layer
		tmp_rig = bpy.data.objects['metarig']
		rig = bpy.data.objects[G.rig_name]
		layer = [False]*20
		layer[0] = True
		tmp_rig.layers = layer
		
		# get position
		bpy.context.scene.objects.active = tmp_rig
		bpy.ops.object.mode_set(mode = 'EDIT')
		
		head_bones = tmp_rig.data.edit_bones['head']
		head = head_bones.head
		tail = head_bones.tail
		#print(head, tail)
				
		# finale - tmp rig in back layer
		bpy.context.scene.objects.active = tmp_rig
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		layer = [False]*20
		layer[9] = True
		tmp_rig.layers = layer
		
		# ****** CREATE HEAD LATTICE
		try:
			latt = bpy.data.lattices['lattice_stretch_squash']
		except:
			latt = bpy.data.lattices.new('lattice_stretch_squash')
			latt.points_w = 3
		ob = bpy.data.objects.new('lattice_str_sq', latt)
		bpy.context.scene.objects.link(ob)
		ob.parent = rig
				
		# ****** POSITION LATTICE
		# -- get center position
		center = [0,0,0]
		center[0] = tail[0] - (tail[0] - head[0])/2
		center[1] = tail[1] - (tail[1] - head[1])/2
		center[2] = tail[2] - (tail[2] - head[2])/2
		
		# -- get rotation
		z = abs(tail[2] - head[2])
		y = abs(tail[1] - head[1])
		alf = math.atan(y/z)
		print('alf: ', alf)
		
		# -- get scale
		len = (z**2 + y**2)**0.5
				
		# -- set position
		ob.location = center
		# -- set rotation
		if (tail[1] - head[1]) > 0:
			ob.rotation_euler[0] = -alf
		elif (tail[1] - head[1]) == 0:
			ob.rotation_euler[0] = 0
		else:
			ob.rotation_euler[0] = alf
		# -- set scale
		ob.scale[0] = len*1.2
		ob.scale[1] = len*1.2
		ob.scale[2] = len*0.6
		
		# ********** EYE LATTICE ****************
		# -- eye_r
		try:
			latt_r = bpy.data.lattices['lattice_eye_r']
		except:
			latt_r = bpy.data.lattices.new('latt_eye_r')
			ob_r = bpy.data.objects.new('lattice_eye_r', latt_r)
			bpy.context.scene.objects.link(ob_r)
			ob_r.parent = rig
			ob_r.parent_type = 'BONE'
			ob_r.parent_bone = 'FR_eye_R'
			
		# -- eye_l
		try:
			latt_l = bpy.data.lattices['lattice_eye_l']
		except:
			latt_l = bpy.data.lattices.new('latt_eye_l')
			ob_l = bpy.data.objects.new('lattice_eye_l', latt_l)
			bpy.context.scene.objects.link(ob_l)
			ob_l.parent = rig
			ob_l.parent_type = 'BONE'
			ob_l.parent_bone = 'FR_eye_L'
		
		# **** LATTICE position
		bpy.context.scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'POSE')
		
		# -- R
		length = rig.pose.bones['FR_eye_R'].length
		ob_r.scale = (length*2, length*2, length*2)
		ob_r.location[1] = -length
		
		# -- L
		length = rig.pose.bones['FR_eye_L'].length
		ob_l.scale = (length*2, length*2, length*2)
		ob_l.location[1] = -length
				
		
	def stretch_squash_controls(self, context):
		pass
		###### EXISTS MESH
		meshes = passport().read_passport(context, 'mesh_passport')
		if not meshes[0]:
			return(False, meshes[1])
		try:
			eye_mesh_r = bpy.data.objects[meshes[1]['eye_r'][0]]
		except:
			return(False, '****** \"eye_r\" Not Found!')
		try:
			eye_mesh_l = bpy.data.objects[meshes[1]['eye_l'][0]]
		except:
			return(False, '****** \"eye_l\" Not Found!')
		try:
			body_mesh = bpy.data.objects[meshes[1]['body'][0]]
		except:
			return(False, '****** \"body\" Not Found!')
		######         'str_squash'
		
		###### EXISTS LATTICE modifiers  ====== 'body_eye_r_lattice', 'body_eye_l_lattice', 'str_sq_lattice'
		if 'str_sq_lattice' in body_mesh.modifiers.keys():
			return(False, '****** Lattice deformation already exists!')
		######
		
		scene = bpy.context.scene
		try:
			latt = bpy.data.objects['lattice_str_sq']
		except:
			#print('****** "Str Sq Lattice" Not Found!')
			return(False, '****** "Str Sq Lattice" Not Found!')
		# get Latt_r
		try:
			latt_r = bpy.data.objects['lattice_eye_r']
		except:
			latt_r = False
			
		# get Latt_l
		try:
			latt_l = bpy.data.objects['lattice_eye_l']
		except:
			latt_l = False
						
		# -- Lattice -> OBJECT
		scene.objects.active = latt
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		# -- get Lattice points pos
		location = latt.location
		rotate = latt.rotation_euler
		scale = latt.scale
		
		# GET
		# [8], [9], [10], [11]
		up_points = []
		for i in [8,9,10,11]:
			local = latt.data.points[i].co
			y_st = local[1] * scale[1]
			z_st = local[2] * scale[2]
			lenth = (y_st**2 + z_st**2)**0.5
			# -- -- get x
			global_x = local[0] * scale[0] + location[0]
			# -- -- get y
			#gamm = math.pi/2 - (math.acos(z_st/lenth) + rotate[0])
			if local[1]>0:
				gamm = math.pi/2 - (math.acos(z_st/lenth) - rotate[0])
				global_y = lenth*math.cos(gamm) + location[1]
			else:
				gamm = math.pi/2 - (math.acos(z_st/lenth) + rotate[0])
				global_y = location[1] - lenth*math.cos(gamm)
			# -- -- get z
			global_z = location[2] + lenth*math.sin(gamm)
			up_points.append((global_x, global_y, global_z))
			
		# 4, 5, 6, 7
		mid_points = []
		for i in [4,5,6,7]:
			local = latt.data.points[i].co
			y_st = local[1] * scale[1]
			z_st = local[2] * scale[2]
			lenth = (y_st**2 + z_st**2)**0.5
			# -- -- get x
			global_x = local[0] * scale[0] + location[0]
			# -- -- get y
			#gamm = math.pi/2 - (math.acos(z_st/lenth) + rotate[0])
			if local[1]>0:
				gamm = math.pi/2 - (math.acos(z_st/lenth) - rotate[0])
				global_y = lenth*math.cos(gamm) + location[1]
			else:
				gamm = math.pi/2 - (math.acos(z_st/lenth) + rotate[0])
				global_y = location[1] - lenth*math.cos(gamm)
			# -- -- get z
			global_z = location[2] + lenth*math.sin(gamm)
			mid_points.append((global_x, global_y, global_z))
			
		# 0, 1, 2, 3
		low_points = []
		for i in [0,1,2,3]:
			local = latt.data.points[i].co
			y_st = local[1] * scale[1]
			z_st = local[2] * scale[2]
			lenth = (y_st**2 + z_st**2)**0.5
			# -- -- get x
			global_x = local[0] * scale[0] + location[0]
			# -- -- get y
			#gamm = math.pi/2 - (math.acos(z_st/lenth) + rotate[0])
			if local[1]>0:
				gamm = math.pi/2 - (math.acos(z_st/lenth) - rotate[0])
				global_y = lenth*math.cos(gamm) + location[1]
			else:
				gamm = math.pi/2 - (math.acos(z_st/lenth) + rotate[0])
				global_y = location[1] - lenth*math.cos(gamm)
			# -- -- get z
			global_z = location[2] + lenth*math.sin(gamm)
			low_points.append((global_x, global_y, global_z))
		
		# -- rig -> EDIT
		try:
			rig = bpy.data.objects[G.rig_name]
		except:
			#print('****** "rig" Not Found!')
			return(False, '****** "rig" Not Found!')
			
		scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'EDIT')
		
		# get FR_eye_R, FR_eye_L position
		eye_r_edit = rig.data.edit_bones['FR_eye_R']
		eye_r_head = eye_r_edit.head
		eye_l_edit = rig.data.edit_bones['FR_eye_L']
		eye_l_head = eye_l_edit.head
		
		# -- layers
		cnt_layer = [False]*32
		cnt_layer[21] = True
		deform_layer = [False]*32
		deform_layer[29] = True
		layer_mesh = [False]*20
		layer_mesh[19] = True
		# -- groups
		group = rig.pose.bone_groups.new(name="Face.red.cnts")
		group.color_set = 'THEME01'
		
		# -- create UP_bones
		up_head = [0,0,0]
		up_head[0] = (up_points[0][0] + up_points[1][0] + up_points[2][0] + up_points[3][0])/4
		up_head[1] = (up_points[0][1] + up_points[1][1] + up_points[2][1] + up_points[3][1])/4
		up_head[2] = (up_points[0][2] + up_points[1][2] + up_points[2][2] + up_points[3][2])/4
		up_tail = [0,0,0]
		up_tail[0] = (up_points[0][0] + up_points[1][0])/2
		up_tail[1] = (up_points[0][1] + up_points[1][1])/2
		up_tail[2] = (up_points[0][2] + up_points[1][2])/2
		# -- --  bones
		up_name = 'up_str_sq'
		up_bone = rig.data.edit_bones.new(up_name)
		up_bone.parent = rig.data.edit_bones['DEF-head']
		up_bone.use_deform = False
		up_bone.layers = cnt_layer
		up_bone.head = up_head
		up_bone.tail = up_tail
						
		# -- create MIDDL_bones
		mid_head = [0,0,0]
		mid_head[0] = (mid_points[0][0] + mid_points[1][0] + mid_points[2][0] + mid_points[3][0])/4
		mid_head[1] = (mid_points[0][1] + mid_points[1][1] + mid_points[2][1] + mid_points[3][1])/4
		mid_head[2] = (mid_points[0][2] + mid_points[1][2] + mid_points[2][2] + mid_points[3][2])/4
		mid_tail = [0,0,0]
		mid_tail[0] = (mid_points[0][0] + mid_points[1][0])/2
		mid_tail[1] = (mid_points[0][1] + mid_points[1][1])/2
		mid_tail[2] = (mid_points[0][2] + mid_points[1][2])/2
		# -- --  bones
		mid_name = 'mid_str_sq'
		mid_bone = rig.data.edit_bones.new(mid_name)
		mid_bone.parent = rig.data.edit_bones['DEF-head']
		mid_bone.use_deform = False
		mid_bone.layers = cnt_layer
		mid_bone.head = mid_head
		mid_bone.tail = mid_tail
				
		# -- rig -> POSE
		scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'POSE')
		
		# groups
		rig.pose.bones[up_name].bone_group = group
		rig.pose.bones[mid_name].bone_group = group
		
		# meshes
		points = []
		for point in self.circle_verts:
			points.append((point[0], point[1] - 1, point[2]))
		# -- up
		up_mesh = self.createMesh('up_str_sq_mesh', (0,0,0), points, self.circle_edges, [])
		up_pose = rig.pose.bones[up_name]
		up_pose.custom_shape = up_mesh
		up_mesh.layers = layer_mesh
		up_mesh.location = up_head
		up_mesh.rotation_euler[0] = rotate[0]
		up_mesh.scale = (up_pose.length, up_pose.length, up_pose.length)
		# -- mid
		mid_mesh = self.createMesh('mid_str_sq_mesh', (0,0,0), points, self.circle_edges, [])
		mid_pose = rig.pose.bones[mid_name]
		mid_pose.custom_shape = mid_mesh
		mid_mesh.layers = layer_mesh
		mid_mesh.location = mid_head
		mid_mesh.rotation_euler[0] = rotate[0]
		mid_mesh.scale = (mid_pose.length, mid_pose.length, mid_pose.length)
		
		# -- EYE LATTICE DEFORM
		if latt_r:
			# Basis shape_key
			latt_r.shape_key_add(name='Basis', from_mix=True)
			
			tsk = {
			'up':([0,1,2,3,4,5,6,7], 2, 0.1, 'LOC_Y', 'eye_global_R', 1),
			'side':([0,1,2,3,4,5,6,7], 0, 0.1, 'LOC_X', 'eye_global_R', -1)
			}
			
			for key in tsk:
				shkey = latt_r.shape_key_add(name=key, from_mix=True)
				shkey.slider_min = -10
				shkey.slider_max = 10
				for i in tsk[key][0]:
					shkey.data[i].co[tsk[key][1]] += tsk[key][2]

				# driver
				f_curve = shkey.driver_add('value')
				drv = f_curve.driver
				drv.type = 'SCRIPTED'
				drv.expression = 'var*' + str(tsk[key][5])
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig
				targ.transform_type = tsk[key][3]
				targ.bone_target = tsk[key][4]
				targ.transform_space = 'LOCAL_SPACE'
				
			sck = {
			'sc_up':(([0,1,2,3],[4,5,6,7]), 2, 1, 'SCALE_Y', 'eye_global_R', -1),
			'sc_side':(([0,2,4,6], [1,3,5,7]), 0, 1, 'SCALE_X', 'eye_global_R', -1),
			}
			for key in sck:
				shkey = latt_r.shape_key_add(name=key, from_mix=True)
				shkey.slider_min = -10
				shkey.slider_max = 10
				for i in sck[key][0][0]:
					shkey.data[i].co[sck[key][1]] += sck[key][2]
				for i in sck[key][0][1]:
					shkey.data[i].co[sck[key][1]] -= sck[key][2]

				# driver
				f_curve = shkey.driver_add('value')
				drv = f_curve.driver
				drv.type = 'SCRIPTED'
				drv.expression = '1 + ' + 'var*' + str(sck[key][5])
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig
				targ.transform_type = sck[key][3]
				targ.bone_target = sck[key][4]
				targ.transform_space = 'LOCAL_SPACE'
		else:
			print('**** Not Found', latt_r)
			
		if latt_l:
			# Basis shape_key
			latt_l.shape_key_add(name='Basis', from_mix=True)
			
			tsk = {
			'up':([0,1,2,3,4,5,6,7], 2, 0.1, 'LOC_Y', 'eye_global_L', 1),
			'side':([0,1,2,3,4,5,6,7], 0, 0.1, 'LOC_X', 'eye_global_L', -1)
			}
			
			for key in tsk:
				shkey = latt_l.shape_key_add(name=key, from_mix=True)
				shkey.slider_min = -10
				shkey.slider_max = 10
				for i in tsk[key][0]:
					shkey.data[i].co[tsk[key][1]] += tsk[key][2]

				# driver
				f_curve = shkey.driver_add('value')
				drv = f_curve.driver
				drv.type = 'SCRIPTED'
				drv.expression = 'var*' + str(tsk[key][5])
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig
				targ.transform_type = tsk[key][3]
				targ.bone_target = tsk[key][4]
				targ.transform_space = 'LOCAL_SPACE'
				
			sck = {
			'sc_up':(([0,1,2,3],[4,5,6,7]), 2, 1, 'SCALE_Y', 'eye_global_L', -1),
			'sc_side':(([0,2,4,6], [1,3,5,7]), 0, 1, 'SCALE_X', 'eye_global_L', -1),
			}
			for key in sck:
				shkey = latt_l.shape_key_add(name=key, from_mix=True)
				shkey.slider_min = -10
				shkey.slider_max = 10
				for i in sck[key][0][0]:
					shkey.data[i].co[sck[key][1]] += sck[key][2]
				for i in sck[key][0][1]:
					shkey.data[i].co[sck[key][1]] -= sck[key][2]

				# driver
				f_curve = shkey.driver_add('value')
				drv = f_curve.driver
				drv.type = 'SCRIPTED'
				drv.expression = '1 + ' + 'var*' + str(sck[key][5])
				drv.show_debug_info = True

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig
				targ.transform_type = sck[key][3]
				targ.bone_target = sck[key][4]
				targ.transform_space = 'LOCAL_SPACE'
			
		else:
			print('**** Not Found', latt_l)
		
		# -- STR SQUASH LATTICE DEFORM  # [vertex, num_oska, delta_diatance, loc, name_of_bone, expression_factor]
		tsk = {
		'up_up':([8,9,10,11],2, 2, 'LOC_Z', up_name, -1),
		'up_l':([8,9,10,11], 0, 1, 'LOC_X', up_name, 1),	
		'up_f':([8,9,10,11], 1, 1, 'LOC_Y', up_name, -1),
		'mid_up':([4,5,6,7],2, 2, 'LOC_Z', mid_name, -1),
		'mid_l':([4,5,6,7], 0, 1, 'LOC_X', mid_name, 1),
		'mid_f':([4,5,6,7], 1, 1, 'LOC_Y', mid_name, -1),
		}
		
		latt.shape_key_add(name='Basis', from_mix=True)
		for key in tsk:
			shkey = latt.shape_key_add(name=key, from_mix=True)
			shkey.slider_min = -10
			shkey.slider_max = 10
			for i in tsk[key][0]:
				shkey.data[i].co[tsk[key][1]] += tsk[key][2]
				
			# driver
			f_curve = shkey.driver_add('value')
			drv = f_curve.driver
			drv.type = 'SCRIPTED'
			drv.expression = 'var*' + str(tsk[key][5])
			drv.show_debug_info = True

			var = drv.variables.new()
			var.name = 'var'
			var.type = 'TRANSFORMS'

			targ = var.targets[0]
			targ.id = rig
			targ.transform_type = tsk[key][3]
			targ.bone_target = tsk[key][4]
			targ.transform_space = 'LOCAL_SPACE'
			
		sck = {
		'up_sc_f':(([8,9],[10,11]), 1, 1, 'SCALE_Y', up_name, -1),
		'up_sc_side':(([8,10],[9,11]), 0, 1, 'SCALE_X', up_name, -1),
		'mid_sc_f':(([4,5],[6,7]), 1, 1, 'SCALE_Y', mid_name, -1),
		'mid_sc_side':(([4,6],[5,7]), 0, 1, 'SCALE_X', mid_name, -1),
		}
		for key in sck:
			shkey = latt.shape_key_add(name=key, from_mix=True)
			shkey.slider_min = -10
			shkey.slider_max = 10
			for i in sck[key][0][0]:
				shkey.data[i].co[sck[key][1]] += sck[key][2]
			for i in sck[key][0][1]:
				shkey.data[i].co[sck[key][1]] -= sck[key][2]
				
			# driver
			f_curve = shkey.driver_add('value')
			drv = f_curve.driver
			drv.type = 'SCRIPTED'
			drv.expression = '1 + ' + 'var*' + str(sck[key][5])
			drv.show_debug_info = True

			var = drv.variables.new()
			var.name = 'var'
			var.type = 'TRANSFORMS'

			targ = var.targets[0]
			targ.id = rig
			targ.transform_type = sck[key][3]
			targ.bone_target = sck[key][4]
			targ.transform_space = 'LOCAL_SPACE'
				
		# -- rig -> OBJECT
		scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		# ****** Hide Parent LATTICE
		# hide
		latt.hide = True
		# parent
		matrix = latt.matrix_world
		latt.parent = rig
		latt.parent_type = 'BONE'
		latt.parent_bone = 'DEF-head'
		latt.matrix_world = matrix
		if latt_r:
			# hide
			latt_r.hide = True
			# parent
			matrix = latt_r.matrix_world
			latt_r.parent = rig
			latt_r.parent_type = 'BONE'
			latt_r.parent_bone = 'DEF-head'
			latt_r.matrix_world = matrix
		if latt_l:
			# hide
			latt_l.hide = True
			# parent
			matrix = latt_l.matrix_world
			latt_l.parent = rig
			latt_l.parent_type = 'BONE'
			latt_l.parent_bone = 'DEF-head'
			latt_l.matrix_world = matrix
		
						
		# ****** ADD LATTICE TO MESH
		# ***** EYE R
		if latt_r:
			for name in meshes[1]['eye_r']:
				try:
					mesh = bpy.data.objects[name]
				except:
					print('****** mesh ', name, 'not_found!')
					continue
				r_latt = mesh.modifiers.new(name = name, type = 'LATTICE')
				r_latt.object = latt_r

			body_r_latt = body_mesh.modifiers.new(name = 'body_eye_r_lattice', type = 'LATTICE')
			body_r_latt.object = latt_r

			body_vtx_name = 'lattice_eye_r'
			if body_vtx_name in body_mesh.vertex_groups.keys():
				body_r_latt.vertex_group = body_vtx_name
			else:
				vtx_mesh_r_grp = body_mesh.vertex_groups.new(body_vtx_name)
				body_r_latt.vertex_group = body_vtx_name

			r = (latt_r.scale[0] + latt_r.scale[1] + latt_r.scale[2])/6
			loc = eye_r_head
			k = 1.5
			for v in body_mesh.data.vertices:
				dist = ((v.co[0] - loc[0])**2 + (v.co[1] - loc[1])**2 + (v.co[2] - loc[2])**2)**0.5
				if dist>(r * k):
					vtx_mesh_r_grp.add([v.index], 0.0, 'REPLACE')
				elif dist<r:
					vtx_mesh_r_grp.add([v.index], 1.0, 'REPLACE')
				else:
					a = r
					b = r*k
					weight = math.cos(math.pi*((dist-a)/(b-a)))
					vtx_mesh_r_grp.add([v.index], weight, 'REPLACE')

		# ***** EYE L
		if latt_l:
			'''
			l_latt = eye_mesh_l.modifiers.new(name = 'eye_l_lattice', type = 'LATTICE')
			l_latt.object = latt_l
			'''
			for name in meshes[1]['eye_l']:
				try:
					mesh = bpy.data.objects[name]
				except:
					print('****** mesh ', name, 'not_found!')
					continue
				l_latt = mesh.modifiers.new(name = name, type = 'LATTICE')
				l_latt.object = latt_l

			body_l_latt = body_mesh.modifiers.new(name = 'body_eye_l_lattice', type = 'LATTICE')
			body_l_latt.object = latt_l

			body_vtx_name = 'lattice_eye_l'
			if body_vtx_name in body_mesh.vertex_groups.keys():
				body_l_latt.vertex_group = body_vtx_name
			else:
				vtx_mesh_l_grp = body_mesh.vertex_groups.new(body_vtx_name)
				body_l_latt.vertex_group = body_vtx_name

			r = (latt_l.scale[0] + latt_l.scale[1] + latt_l.scale[2])/6
			loc = eye_l_head
			k = 1.5
			for v in body_mesh.data.vertices:
				dist = ((v.co[0] - loc[0])**2 + (v.co[1] - loc[1])**2 + (v.co[2] - loc[2])**2)**0.5
				if dist>(r * k):
					vtx_mesh_l_grp.add([v.index], 0.0, 'REPLACE')
				elif dist<r:
					vtx_mesh_l_grp.add([v.index], 1.0, 'REPLACE')
				else:
					a = r
					b = r*k
					weight = math.cos(math.pi*((dist-a)/(b-a)))
					vtx_mesh_l_grp.add([v.index], weight, 'REPLACE')

		# **** STR SQUASH
		for key in meshes[1]:
			for i,name in enumerate(meshes[1][key]):
				try:
					mesh = bpy.data.objects[meshes[1][key][i]]
				except:
					print('****** ', meshes[1][key][i], ' Not Found!')
					continue
				mesh_latt = mesh.modifiers.new(name = 'str_sq_lattice', type = 'LATTICE')
				mesh_latt.object = latt
				# get vertex_group
				if 'str_squash' in mesh.vertex_groups.keys():
					mesh_latt.vertex_group = 'str_squash'
				'''
				# moove modifier
				bpy.context.scene.objects.active = mesh
				bpy.ops.object.modifier_move_up(modifier = 'str_sq_lattice')
				'''
		return(True, 'All right!')
		
	def toggle_lattice_visible(self, context, action):
		lattice_list = ['lattice_str_sq', 'lattice_eye_r','lattice_eye_l']
		
		for name in lattice_list:
			if name in bpy.data.objects:
				if action == 'on':
					bpy.data.objects[name].hide = False
				elif action == 'off':
					bpy.data.objects[name].hide = True
			else:
				print((name + ' Not Found! ***'))
		
		if action == 'on':
			message = 'Unhide Lattice!'
		else:
			message = 'Hide Lattice!'
		return(True, message)
			
	def edit_eye_global_lattice(self, context, k, metod):
		pass
		# get Latt_r
		try:
			latt_r = bpy.data.objects['lattice_eye_r']
		except:
			latt_r = False
			
		# get Latt_l
		try:
			latt_l = bpy.data.objects['lattice_eye_l']
		except:
			latt_l = False
			
		# -- rig -> EDIT
		try:
			rig = bpy.data.objects[G.rig_name]
		except:
			#print('****** "rig" Not Found!')
			return(False, '****** \"rig\" Not Found!')
		
		scene = bpy.context.scene
		scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'EDIT')
			
		# get FR_eye_R, FR_eye_L position
		eye_r_edit = rig.data.edit_bones['FR_eye_R']
		eye_r_head = eye_r_edit.head
		eye_l_edit = rig.data.edit_bones['FR_eye_L']
		eye_l_head = eye_l_edit.head
		
		# ****** Edit Lattice deform
		meshes = passport().read_passport(context, 'mesh_passport')
		if meshes[0]:
			# get body mesh
			try:
				body_mesh = bpy.data.objects[meshes[1]['body'][0]]
			except:
				print('****** ', meshes[1]['body'][0], ' Not Found!')
				return
			# ***** EYE R
			if latt_r:
				# get vertex group
				try:
					vtx_mesh_r_grp = body_mesh.vertex_groups['lattice_eye_r']
				except:
					return(False, '****** \"lattice_eye_r\" vertex group Not Found!')
				else:
					r = (latt_r.scale[0] + latt_r.scale[1] + latt_r.scale[2])/6
					loc = eye_r_head
					for v in body_mesh.data.vertices:
						dist = ((v.co[0] - loc[0])**2 + (v.co[1] - loc[1])**2 + (v.co[2] - loc[2])**2)**0.5
						if dist>(r * k):
							vtx_mesh_r_grp.add([v.index], 0.0, 'REPLACE')
						elif dist<r:
							vtx_mesh_r_grp.add([v.index], 1.0, 'REPLACE')
						else:
							a = r
							b = r*k
							if metod == 'cosinus':
								weight = math.cos(math.pi*((dist-a)/(b-a)))
							elif metod == 'linear':
								weight = 1 - (a-dist)/(a-b)
							vtx_mesh_r_grp.add([v.index], weight, 'REPLACE')
			
			# ***** EYE L
			if latt_l:
				# get vertex group
				try:
					vtx_mesh_l_grp = body_mesh.vertex_groups['lattice_eye_l']
				except:
					return(False, '****** \"lattice_eye_l\" vertex group Not Found!')
				else:
					r = (latt_l.scale[0] + latt_l.scale[1] + latt_l.scale[2])/6
					loc = eye_l_head
					#k = 1.5
					for v in body_mesh.data.vertices:
						dist = ((v.co[0] - loc[0])**2 + (v.co[1] - loc[1])**2 + (v.co[2] - loc[2])**2)**0.5
						if dist>(r * k):
							vtx_mesh_l_grp.add([v.index], 0.0, 'REPLACE')
						elif dist<r:
							vtx_mesh_l_grp.add([v.index], 1.0, 'REPLACE')
						else:
							a = r
							b = r*k
							if metod == 'cosinus':
								weight = math.cos(math.pi*((dist-a)/(b-a)))
							elif metod == 'linear':
								weight = 1 - (a-dist)/(a-b)
							vtx_mesh_l_grp.add([v.index], weight, 'REPLACE')
							
		scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'POSE')
		return(True, 'All Right!')
	
	def edit_body_weight(self, context, vtx_grp_name):
		pass
		#vtx_grp_name = 'str_squash'
		
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			return(False, mesh_passport[1])
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			return(False, '***** Not key \"body\" in mesh_passport')
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		# 
		vertex_groups = ob.vertex_groups.keys()
		index = 0
		for i, g in enumerate(vertex_groups):
			if g == vtx_grp_name:
				index = i
				break
		        
		if index:
			scene = bpy.context.scene
			scene.objects.active = ob
			ob.vertex_groups.active_index = index
			bpy.ops.object.mode_set(mode = 'WEIGHT_PAINT')
			return(True, '****** all right!')
		else:
			return(False, '****** This key not found!')
		
	
	def create_face_ui(self):
		try:
			rig_id = bpy.data.objects[G.rig_name].data.get("rig_id")
		except:
			return(None, '****** not \"rig_id\"')

		if "face_ui.py" in bpy.data.texts:
			script = bpy.data.texts["face_ui.py"]
			script.clear()
		else:
			script = bpy.data.texts.new("face_ui.py")

		script.write(file_data % rig_id)
		script.use_module = True
		
		# Run UI script
		exec(script.as_string(), {})
		
		return(True, 'create face ui - all right!')
	
	def lock_cnt_root(self, context, boolean):
		rig = bpy.context.object
		if rig.type != 'ARMATURE':
			return(False, '*** the selected object is not ARMATURE')
		
		bones = bpy.context.selected_pose_bones
		for bone in bones:
			#bone = bpy.context.active_pose_bone
			name = bone.name

			if name[-5:] == '.root':
				root_name = name
			else:
				root_name = name + '.root'

			#root_bone = rig.pose.bones[root_name]

			bpy.context.scene.objects.active = rig
			bpy.ops.object.mode_set(mode = 'EDIT')

			try:
				root_bone = rig.data.edit_bones[root_name]
				root_bone.hide_select = boolean
			except:
				bpy.ops.object.mode_set(mode = 'POSE')
				#return(False, '*** Root Bones not found!')
				print(name,'*** Root Bones not found!')
				continue

			bpy.ops.object.mode_set(mode = 'POSE')
			
		# fin	
		return(True, 'all right!')
	
	def keyframe_to_root_cnt(self, context):
		try:
			rig = bpy.data.objects[G.rig_name]
		except:
			return(False, '****** object \"rig\" not found!')
		context.scene.objects.active = rig
		bpy.ops.object.mode_set(mode = 'POSE')
		
		for name in self.tmp_bones + [('FRTMP_jaw.cnt',)]:
			# get root
			root_name = name[0].replace('FRTMP_', '') + '.root'
			try:
				root_bone = rig.pose.bones[root_name]
			except:
				print('****** get \"root_bone\" problem with >>', name)
				continue
			
			# insert keyframe
			root_bone.keyframe_insert('rotation_euler', frame = 1)
			root_bone.keyframe_insert('location', frame = 1)
			root_bone.keyframe_insert('scale', frame = 1)
		return(True, 'finish')
	
	def linear_jaw_driver_create(self, context):
		pass
		# get obj
		rig_obj = bpy.context.object
		if rig_obj.type != 'ARMATURE':
			return(False, '*** the selected object is not ARMATURE')
		rig_arm = rig_obj.data
		
		if not 'FR_jaw' in rig_obj.pose.bones:
			return(False, '"FR_jaw" Not Found!')
		# set ratation mode
		jaw_bone = rig_obj.pose.bones['FR_jaw']
		open_name = 'jaw_open'
		x_name = 'x'
		max_name = 'max'
		# --- f curve
		fcurve = jaw_bone.driver_add('scale', 1)
		drv = fcurve.driver
		drv.type = 'SCRIPTED'
		drv.expression = '1-(1 - cos(%s/2))*sin(abs(%s)*pi/%s)' % (max_name, x_name, max_name)
		drv.show_debug_info = True
		# --- var
		var = drv.variables.new()
		var.name = x_name
		var.type = 'TRANSFORMS'
		# --- var.targ 
		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'ROT_X'
		targ.bone_target = 'FR_jaw'
		targ.transform_space = 'LOCAL_SPACE'
		# --- var2
		var2 = drv.variables.new()
		var2.name = max_name
		var2.type = 'SINGLE_PROP'
		# --- var2.targ
		targ = var2.targets[0]
		targ.id_type = 'ARMATURE'
		targ.id = rig_arm
		targ.data_path = '["%s"]' % open_name
		
		return(True, 'Line Driver created for Jaw!')
		
class face_shape_keys:
	def __init__(self):
		self.low_num = 2
		self.up_num = 2
		self.out_num = 1
		self.in_num = 1
		
		self.label_tmp_bones = ['vtx_lip_grp_set', 'vtx_brow_m_set', 'vtx_brow_in_set', 'vtx_brow_out_set', 'vtx_nose_set']
		
		self.ather_shape_keys_data_list = [
		('eye_r', 'pupil_extension_r', 'pupil_R', 'LOC_Y', 1, ''),
		('eye_r', 'pupil_pinch_r', 'pupil_R', 'LOC_Y', -1, ''),
		('eye_l', 'pupil_extension_l', 'pupil_L', 'LOC_Y', 1, ''),
		('eye_l', 'pupil_pinch_l', 'pupil_L', 'LOC_Y', -1, ''),
		]
		
		self.face_shape_keys_data_list = [
		('jaw_fwd', 'jaw_back_fwd', 'LOC_Y', 1, 'head_blend.m'),
		('jaw_back', 'jaw_back_fwd', 'LOC_Y', -1, 'head_blend.m'),
		('lip_down', 'lip_M', 'LOC_Y', -1, 'head_blend.m'),
		('lip_raise', 'lip_M', 'LOC_Y', 1 , 'head_blend.m'),
		('lip_side.r', 'lip_M', 'LOC_X', -1 , 'head_blend.m'),
		('lip_side.l', 'lip_M', 'LOC_X',  1 , 'head_blend.m'),
		('lip_smile', 'lips', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_smile.r', 'lip_R', 'LOC_Y', 1, 'lip_blend.r'), 
		('lip_smile.l', 'lip_L', 'LOC_Y', 1, 'lip_blend.l'), 
		('lip_frown', 'lips', 'LOC_Y', -1, 'head_blend.m'), 
		('lip_frown.r', 'lip_R', 'LOC_Y', -1, 'lip_blend.r'), 
		('lip_frown.l', 'lip_L', 'LOC_Y', -1, 'lip_blend.l'), 
		('lip_stretch', 'lips', 'LOC_X', -1, 'head_blend.m'), 
		('lip_stretch.r', 'lip_R', 'LOC_X', -1, 'lip_blend.r'), 
		('lip_stretch.l', 'lip_L', 'LOC_X', 1, 'lip_blend.l'), 
		('lip_pucker', 'lips', 'LOC_X', 1, 'head_blend.m'), 
		('lip_pucker.r', 'lip_R', 'LOC_X', 1, 'lip_blend.r'), 
		('lip_pucker.l', 'lip_L', 'LOC_X', -1, 'lip_blend.l'), 
		('lip_upper_raiser', 'lip_up_raise', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_upper_raiser.r', 'lip_up_raise_R', 'LOC_Y', 1, 'lip_blend.r'), 
		('lip_upper_raiser.l', 'lip_up_raise_L', 'LOC_Y', 1, 'lip_blend.l'), 
		('lip_lower_depressor', 'lip_low_depress', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_lower_depressor.r', 'lip_low_depress_R', 'LOC_Y', 1, 'lip_blend.r'), 
		('lip_lower_depressor.l', 'lip_low_depress_L', 'LOC_Y', 1, 'lip_blend.l'), 
		('lip_upper_roll', 'lip_up_roll', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_upper_roll.r', 'lip_up_roll_R', 'LOC_Y', 1, 'lip_roll_blend.r'), 
		('lip_upper_roll.l', 'lip_up_roll_L', 'LOC_Y', 1, 'lip_roll_blend.l'), 
		('lip_upper_roll.m', 'lip_up_roll_M', 'LOC_Y', 1, 'lip_roll_blend.m'), 
		# new
		('lip_upper_roll_in', 'lip_up_roll', 'LOC_Y', -1, 'head_blend.m'), 
		('lip_upper_roll_in.r', 'lip_up_roll_R', 'LOC_Y', -1, 'lip_roll_blend.r'), 
		('lip_upper_roll_in.l', 'lip_up_roll_L', 'LOC_Y', -1, 'lip_roll_blend.l'), 
		('lip_upper_roll_in.m', 'lip_up_roll_M', 'LOC_Y', -1, 'lip_roll_blend.m'),
		# -- 
		('lip_lower_roll', 'lip_low_roll', 'LOC_Y', -1, 'head_blend.m'), 
		('lip_lower_roll.r', 'lip_low_roll_R', 'LOC_Y', -1, 'lip_roll_blend.r'), 
		('lip_lower_roll.l', 'lip_low_roll_L', 'LOC_Y', -1, 'lip_roll_blend.l'), 
		('lip_lower_roll.m', 'lip_low_roll_M', 'LOC_Y', -1, 'lip_roll_blend.m'), 
		# new
		('lip_lower_roll_in', 'lip_low_roll', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_lower_roll_in.r', 'lip_low_roll_R', 'LOC_Y', 1, 'lip_roll_blend.r'), 
		('lip_lower_roll_in.l', 'lip_low_roll_L', 'LOC_Y', 1, 'lip_roll_blend.l'), 
		('lip_lower_roll_in.m', 'lip_low_roll_M', 'LOC_Y', 1, 'lip_roll_blend.m'), 
		# --
		('lip_close', 'lips_close', 'LOC_Y', 1, 'head_blend.m', 'jaw.cnt', 'LOC_Y', -1), 
		('lip_pinch', 'lips_pinch', 'LOC_Y', 1, 'head_blend.m', 'jaw.cnt', 'LOC_Y', -0.4), 
		('lip_pinch.r', 'lips_pinch_R', 'LOC_Y', 1, 'lip_blend.r', 'jaw.cnt', 'LOC_Y', -0.4), 
		('lip_pinch.l', 'lips_pinch_L', 'LOC_Y', 1, 'lip_blend.l', 'jaw.cnt', 'LOC_Y', -0.4), 
		#('lip_upper_sqz', 'lip_up_sqz', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_upper_sqz', 'lip_up_raise', 'LOC_Y', -1, 'head_blend.m'), 
		#('lip_upper_sqz.r', 'lip_up_sqz_R', 'LOC_Y', 1, 'lip_blend.r'), 
		('lip_upper_sqz.r', 'lip_up_raise_R', 'LOC_Y', -1, 'lip_blend.r'), 
		#('lip_upper_sqz.l', 'lip_up_sqz_L', 'LOC_Y', 1, 'lip_blend.l'), 
		('lip_upper_sqz.l', 'lip_up_raise_L', 'LOC_Y', -1, 'lip_blend.l'), 
		#('lip_lower_sqz', 'lip_low_sqz', 'LOC_Y', 1, 'head_blend.m'), 
		('lip_lower_sqz', 'lip_low_depress', 'LOC_Y', -1, 'head_blend.m'), 
		#('lip_lower_sqz.r', 'lip_low_sqz_R', 'LOC_Y', 1, 'lip_blend.r'), 
		('lip_lower_sqz.r', 'lip_low_depress_R', 'LOC_Y', -1, 'lip_blend.r'), 
		#('lip_lower_sqz.l', 'lip_low_sqz_L', 'LOC_Y', 1, 'lip_blend.l'), 
		('lip_lower_sqz.l', 'lip_low_depress_L', 'LOC_Y', -1, 'lip_blend.l'), 
		('lip_funnel', 'funnel', 'LOC_Y', 1, 'head_blend.m'), 
		('nose_sneer', 'nose', 'LOC_Y', 1, 'head_blend.m'), 
		('nose_sneer.r', 'nose_R', 'LOC_Y', 1, 'nose_blend.r'), 
		('nose_sneer.l', 'nose_L', 'LOC_Y', 1, 'nose_blend.l'), 
		('nostril_dilator', 'nose', 'LOC_X', -1, 'head_blend.m'), 
		('nostril_dilator.r', 'nose_R', 'LOC_X', -1, 'nose_blend.r'), 
		('nostril_dilator.l', 'nose_L', 'LOC_X', 1, 'nose_blend.l'), 
		('nostril_compressor', 'nose', 'LOC_X', 1, 'head_blend.m'), 
		('nostril_compressor.r', 'nose_R', 'LOC_X', 1, 'nose_blend.r'), 
		('nostril_compressor.l', 'nose_L', 'LOC_X', -1, 'nose_blend.l'), 
		('cheek_puff', 'cheeks', 'LOC_X', -1, 'head_blend.m'), 
		('cheek_puff.r', 'cheek_R', 'LOC_X', -1, 'lip_blend.r'), 
		('cheek_puff.l', 'cheek_L', 'LOC_X', 1, 'lip_blend.l'), 
		('cheek_suck', 'cheeks', 'LOC_X', 1, 'head_blend.m'), 
		('cheek_suck.r', 'cheek_R', 'LOC_X', 1, 'lip_blend.r'), 
		('cheek_suck.l', 'cheek_L', 'LOC_X', -1, 'lip_blend.l'), 
		('cheek_sqz', 'cheeks', 'LOC_Y', -1, 'head_blend.m'), 
		('cheek_sqz.r', 'cheek_R', 'LOC_Y', -1, 'lip_blend.r'), 
		('cheek_sqz.l', 'cheek_L', 'LOC_Y', -1, 'lip_blend.l'), 
		('cheek_raise', 'cheeks', 'LOC_Y', 1, 'head_blend.m'), 
		('cheek_raise.r', 'cheek_R', 'LOC_Y', 1, 'head_blend.r'), 
		('cheek_raise.l', 'cheek_L', 'LOC_Y', 1, 'head_blend.l'),
		('brow_raiser', '', '', '', 'head_blend.m'),
		('brow_raiser_out.r', 'brow_out_R', 'LOC_Y', 1, 'brow_out_blend.r'),
		('brow_raiser_mid.r', 'brow_mid_R', 'LOC_Y', 1, 'brow_m_blend.r'),
		('brow_raiser_in.r', 'brow_in_R', 'LOC_Y', 1, 'brow_in_blend.r'),
		('brow_raiser_out.l', 'brow_out_L', 'LOC_Y', 1, 'brow_out_blend.l'),
		('brow_raiser_mid.l', 'brow_mid_L', 'LOC_Y', 1, 'brow_m_blend.l'),
		('brow_raiser_in.l', 'brow_in_L', 'LOC_Y', 1, 'brow_in_blend.l'),
		('brow_lower', '', '', '', 'head_blend.m'),
		('brow_lower_out.r', 'brow_out_R', 'LOC_Y', -1, 'brow_out_blend.r'),
		('brow_lower_mid.r', 'brow_mid_R', 'LOC_Y', -1, 'brow_m_blend.r'),
		('brow_lower_in.r', 'brow_in_R', 'LOC_Y', -1, 'brow_in_blend.r'),
		('brow_lower_out.l', 'brow_out_L', 'LOC_Y', -1, 'brow_out_blend.l'),
		('brow_lower_mid.l',  'brow_mid_L', 'LOC_Y', -1, 'brow_m_blend.l'), 
		('brow_lower_in.l',  'brow_in_L',  'LOC_Y',  -1,  'brow_in_blend.l'),
		('blink_up_lid',  '',  '',  '',  'head_blend.m'),
		('blink_up_lid.r',  'blink_R',  'LOC_X',  1,  'head_blend.r'),
		('blink_up_lid.l',  'blink_L',  'LOC_X',  1,  'head_blend.l'),
		('blink_low_lid',  '',  '',  '',  'head_blend.m'),
		('blink_low_lid.r',  'blink_R',  'LOC_Y',  1,  'head_blend.r'),
		('blink_low_lid.l',  'blink_L',  'LOC_Y',  1,  'head_blend.l'),
		('goggle_up_lid',  '',  '',  '',  'head_blend.m'),
		('goggle_up_lid.r',  'blink_R',  'LOC_X',  -1,  'head_blend.r'),
		('goggle_up_lid.l',  'blink_L',  'LOC_X',  -1,  'head_blend.l'),
		('goggle_low_lid',  '',  '',  '',  'head_blend.m'),
		('goggle_low_lid.r',  'blink_R',  'LOC_Y',  -1,  'head_blend.r'),
		('goggle_low_lid.l',  'blink_L',  'LOC_Y',  -1,  'head_blend.l'),
		]
		
		self.central_side_shape_keys = {
		'lip_smile':('lip_smile.r', 'lip_smile.l'),
		'lip_frown':('lip_frown.r', 'lip_frown.l'),
		'lip_stretch':('lip_stretch.r', 'lip_stretch.l'),
		'lip_pucker':('lip_pucker.r', 'lip_pucker.l'),
		'lip_upper_raiser':('lip_upper_raiser.r', 'lip_upper_raiser.l'),
		'lip_lower_depressor':('lip_lower_depressor.r', 'lip_lower_depressor.l'),
		'lip_upper_roll':('lip_upper_roll.r', 'lip_upper_roll.l', 'lip_upper_roll.m'),
		'lip_upper_roll_in':('lip_upper_roll_in.r', 'lip_upper_roll_in.l', 'lip_upper_roll_in.m'),
		'lip_lower_roll':('lip_lower_roll.r', 'lip_lower_roll.l', 'lip_lower_roll.m'),
		'lip_lower_roll_in':('lip_lower_roll_in.r', 'lip_lower_roll_in.l', 'lip_lower_roll_in.m'),
		'lip_pinch':('lip_pinch.r', 'lip_pinch.l'),
		'lip_upper_sqz':('lip_upper_sqz.r', 'lip_upper_sqz.l'),
		'lip_lower_sqz':('lip_lower_sqz.r', 'lip_lower_sqz.l'),
		'nose_sneer':('nose_sneer.r', 'nose_sneer.l'),
		'nostril_dilator':('nostril_dilator.r', 'nostril_dilator.l'),
		'nostril_compressor':('nostril_compressor.r', 'nostril_compressor.l'),
		'cheek_puff':('cheek_puff.r', 'cheek_puff.l'),
		'cheek_suck':('cheek_suck.r', 'cheek_suck.l'),
		'cheek_sqz':('cheek_sqz.r', 'cheek_sqz.l'),
		'cheek_raise':('cheek_raise.r', 'cheek_raise.l'),
		'brow_raiser':('brow_raiser_out.r', 'brow_raiser_mid.r', 'brow_raiser_in.r', 'brow_raiser_out.l', 'brow_raiser_mid.l', 'brow_raiser_in.l'),
		'brow_lower':('brow_lower_out.r', 'brow_lower_mid.r', 'brow_lower_in.r', 'brow_lower_out.l', 'brow_lower_mid.l', 'brow_lower_in.l'),
		'autolid_low':('autolid_low.r', 'autolid_low.l'),
		'autolid_up':('autolid_up.r', 'autolid_up.l'),
		'autolid_out':('autolid_out.r', 'autolid_out.l'),
		'autolid_in':('autolid_in.r', 'autolid_in.l'),
		'blink_up_lid':('blink_up_lid.r', 'blink_up_lid.l'),
		'blink_low_lid':('blink_low_lid.r', 'blink_low_lid.l'),
		'goggle_up_lid':('goggle_up_lid.r', 'goggle_up_lid.l'),
		'goggle_low_lid':('goggle_low_lid.r', 'goggle_low_lid.l'),
		}
		
		self.shape_keys_vtx_grp = [
		('autolid_low', 'head_blend.m'),
		('autolid_up', 'head_blend.m'),
		('autolid_out', 'head_blend.m'),
		('autolid_in', 'head_blend.m'),
		('autolid_low.r', 'head_blend.r'),
		('autolid_low.l', 'head_blend.l'),
		('autolid_up.r', 'head_blend.r'),
		('autolid_up.l', 'head_blend.l'),
		('autolid_out.r', 'head_blend.r'),
		('autolid_out.l', 'head_blend.l'),
		('autolid_in.r', 'head_blend.r'),
		('autolid_in.l', 'head_blend.l'),
		]
		
		# -- rig data
		try:
			self.rig_obj = bpy.data.objects[G.rig_name]
			self.rig_arm = self.rig_obj.data
		except:
			print('****** Object \"rig\" Not Found!')
			return
		
		# -- get pose.bones
		try:
			self.eye_bone_r = self.rig_obj.pose.bones['FR_eye_R']
		except:
			print("****** Not Found pose.bones[FR_eye_R]")
			return
		try:
			self.eye_bone_l = self.rig_obj.pose.bones['FR_eye_L']
		except:
			print("****** Not Found pose.bones[FR_eye_L]")
			return
		
		
	def create_shape_keys(self, context):
		# -- pose data
		poses = {
		'jaw_open_C':(0.0, -1.0, 0.0),
		#'jaw_open_C.5':(0.0, -0.5, 0.0),
		'jaw_side_R':(-1.0, 0.0, 0.0),
		'jaw_side_L':(1.0, 0.0, 0.0)
		}
		
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			return(False, mesh_passport[1])
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			return(False, '***** Not key \"body\" in mesh_passport')
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		######  == GET exists Shape Keys
		try:
			keys = ob.data.shape_keys.key_blocks
		except:
			pass
		else:
			for key in poses:
				if key in keys.keys():
					return(False, '****** Shape Keys already exists!')
		
		######
		
		# -- rig
		rig_obj = bpy.data.objects[G.rig_name]
		rig_arm = rig_obj.data

		# -- create vertex_groups
		vtx_groups = self.create_edit_vertes_groups(bpy.context)

		# -- rig to POSE mode
		scene = bpy.context.scene
		scene.objects.active = rig_obj
		bpy.ops.object.mode_set(mode = 'POSE')

		# ********** JAW **************
		######
		'''
		# -- pose data
		poses = {
		'jaw_open_C':(0.0, -1.0, 0.0),
		#'jaw_open_C.5':(0.0, -0.5, 0.0),
		'jaw_side_R':(-1.0, 0.0, 0.0),
		'jaw_side_L':(1.0, 0.0, 0.0)
		}
		'''
		######

		# -- get jaw control
		jaw_cnt = rig_obj.pose.bones['jaw.cnt']

		# JAW ** CREATE SHAPE_KEYS (OPEN, SIDE, SIDEOPEN)
		for key in poses:
			# -- Create shape_key
			# -- -- Basis
			try:
				keys = ob.data.shape_keys.key_blocks
			except:
				ob.shape_key_add(name='Basis', from_mix=True)

			# -- -- new shape_key
			shkey = ob.shape_key_add(name=key, from_mix=True)
			shkey.vertex_group = vtx_groups['head_blend.m'].name

			# -- jaw control to pose
			jaw_cnt.location = poses[key]
			# --- update driver affects
			bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)

			# -- make mesh pose
			me = ob.to_mesh(scene=bpy.context.scene, apply_modifiers=True, settings='PREVIEW')

			# Copy Data
			for vtx in ob.data.vertices:
				shkey.data[vtx.index].co = me.vertices[vtx.index].co

			# remove me
			bpy.data.meshes.remove(me) 

			# -- create JAW.SIDE.OPEN
			if (key == 'jaw_side_R') or (key == 'jaw_side_L'):
				# -- -- new shape_key
				open_key = key.replace('_side','_side_open')
				open_shkey = ob.shape_key_add(name=open_key, from_mix=True)
				open_shkey.vertex_group = vtx_groups['jaw_side'].name
				# -- -- copy shape keys
				for v in ob.data.vertices:
					open_shkey.data[v.index].co = shkey.data[v.index].co
					
		# -- jaw control to start pose
		jaw_cnt.location = (0,0,0)
		# --- update driver affects
		bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)
					
		# JAW ** CREATE SHAPE_KEYS (FWD, BACK)
		poses_ = {'jaw_fwd': 1, 'jaw_back': -1}
		for key in poses_:
			# -- -- new shape_key
			shkey = ob.shape_key_add(name=key, from_mix=True)
			shkey.vertex_group = vtx_groups['head_blend.m'].name

			# -- jaw control to pose
			rig_obj.pose.bones['jaw_back_fwd'].location[1] = poses_[key]
			# --- update driver affects
			bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)

			# -- make mesh pose
			me = ob.to_mesh(scene=bpy.context.scene, apply_modifiers=True, settings='PREVIEW')

			# Copy Data
			for vtx in ob.data.vertices:
				shkey.data[vtx.index].co = me.vertices[vtx.index].co

			# remove me
			bpy.data.meshes.remove(me) 

		# JAW ** remove 'FR_jaw' from armature
		ob.select = True
		scene.objects.active = ob
		bpy.ops.object.mode_set(mode='EDIT')
		# -- remove
		name = 'FR_jaw'
		try:
			vtx_grp = ob.vertex_groups[name]
		except:
			print(('NO  ' + name))
		else:
			index = vtx_grp.index
			ob.vertex_groups.active_index = index
			bpy.ops.object.vertex_group_select()
			ob.vertex_groups.remove(vtx_grp)
			# -- apply vertex to head
			index = bpy.context.object.vertex_groups['DEF-head'].index
			ob.vertex_groups.active_index = index
			bpy.ops.object.vertex_group_assign()

		scene.objects.active = ob
		bpy.ops.object.mode_set(mode='OBJECT')

		# JAW ** set DRIVER to shape_keys
		'''
		# -- JAW.OPEN.0.5.DRIVER
		f_curve = ob.data.shape_keys.key_blocks['jaw_open_C.5'].driver_add('value')
		drv = f_curve.driver
		drv.type = 'AVERAGE'
		drv.show_debug_info = True

		point = f_curve.keyframe_points.insert(0,0)
		point.interpolation = 'LINEAR'
		point = f_curve.keyframe_points.insert(-0.5,1)
		point.interpolation = 'LINEAR'
		point = f_curve.keyframe_points.insert(-1,0)
		point.interpolation = 'LINEAR'

		var = drv.variables.new()
		var.name = 'var'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		fmod = f_curve.modifiers[0]
		f_curve.modifiers.remove(fmod)
		'''
		
		# -- JAW.OPEN.DRIVER
		f_curve = ob.data.shape_keys.key_blocks['jaw_open_C'].driver_add('value')
		drv = f_curve.driver
		drv.type = 'AVERAGE'
		drv.show_debug_info = True

		#point = f_curve.keyframe_points.insert(-0.5,0)
		point = f_curve.keyframe_points.insert(0,0)
		point.interpolation = 'LINEAR'
		point = f_curve.keyframe_points.insert(-1,1)
		point.interpolation = 'LINEAR'

		var = drv.variables.new()
		var.name = 'var'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		fmod = f_curve.modifiers[0]
		f_curve.modifiers.remove(fmod)

		# -- JAW.SIDE.R.DRIVER
		# -- -- jaw_side.r
		f_curve = ob.data.shape_keys.key_blocks['jaw_side_R'].driver_add('value')
		drv = f_curve.driver
		drv.type = 'SCRIPTED'
		drv.show_debug_info = True
		drv.expression = '(0  - var_side) * (1 + var_open)'

		var = drv.variables.new()
		var.name = 'var_side'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_X'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		var = drv.variables.new()
		var.name = 'var_open'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		# -- -- jaw_side_open.r
		f_curve = ob.data.shape_keys.key_blocks['jaw_side_open_R'].driver_add('value')
		drv = f_curve.driver
		drv.type = 'SCRIPTED'
		drv.show_debug_info = True
		drv.expression = '(0 - var_side) * (0 - var_open)'

		var = drv.variables.new()
		var.name = 'var_side'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_X'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		var = drv.variables.new()
		var.name = 'var_open'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		# -- JAW.SIDE.L.DRIVER
		# -- -- jaw_side.l
		f_curve = ob.data.shape_keys.key_blocks['jaw_side_L'].driver_add('value')
		drv = f_curve.driver
		drv.type = 'SCRIPTED'
		drv.show_debug_info = True
		drv.expression = 'var_side * (1 + var_open)'

		var = drv.variables.new()
		var.name = 'var_side'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_X'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		var = drv.variables.new()
		var.name = 'var_open'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		# -- -- jaw_side_open.l
		f_curve = ob.data.shape_keys.key_blocks['jaw_side_open_L'].driver_add('value')
		drv = f_curve.driver
		drv.type = 'SCRIPTED'
		drv.show_debug_info = True
		drv.expression = 'var_side * (0 - var_open)'

		var = drv.variables.new()
		var.name = 'var_side'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_X'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		var = drv.variables.new()
		var.name = 'var_open'
		var.type = 'TRANSFORMS'

		targ = var.targets[0]
		targ.id = rig_obj
		targ.transform_type = 'LOC_Y'
		targ.bone_target = jaw_cnt.name
		targ.transform_space = 'LOCAL_SPACE'

		# ************ CREATE OTHER FACE SHAPE KEYS ****************
		# ***** BODY
		for data in self.face_shape_keys_data_list:
			#('brow_lower_in.l',  'brow_in_L',  'LOC_Y',  -1,  'brow_in_blend.l')
			sh_key_name = data[0]
			cnt = data[1]
			loc = data[2]
			dat = data[3]
			vtx_grp = data[4]
			# create shape_key
			if not sh_key_name in ob.data.shape_keys.key_blocks.keys():
				shkey = ob.shape_key_add(name=sh_key_name, from_mix=True)
				shkey.vertex_group = vtx_grp
			else:
				shkey = ob.data.shape_keys.key_blocks[sh_key_name]
			# create driver
			if cnt == '' or loc == '' or dat == '':
				print(sh_key_name, '  **** not data') 
				continue
				
			# correct driver
			try:
				k_cnt = data[5]
				k_loc = data[6]
				k_dat = data[7]
			
			except:
				# old construction
				f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
				drv = f_curve.driver
				drv.type = 'AVERAGE'
				drv.show_debug_info = True

				point = f_curve.keyframe_points.insert(0,0)
				point.interpolation = 'LINEAR'
				point = f_curve.keyframe_points.insert(dat,1)
				point.interpolation = 'LINEAR'

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig_obj
				targ.transform_type = loc
				targ.bone_target = cnt
				targ.transform_space = 'LOCAL_SPACE'

				fmod = f_curve.modifiers[0]
				f_curve.modifiers.remove(fmod)
				
			else:
				# correct construction
				# old construction
				f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
				drv = f_curve.driver
				drv.type = 'SCRIPTED'
				drv.show_debug_info = True

				point = f_curve.keyframe_points.insert(0,0)
				point.interpolation = 'LINEAR'
				point = f_curve.keyframe_points.insert(dat,1)
				point.interpolation = 'LINEAR'

				# var 1
				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig_obj
				targ.transform_type = loc
				targ.bone_target = cnt
				targ.transform_space = 'LOCAL_SPACE'
				
				# correct var
				var = drv.variables.new()
				var.name = 'correct'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig_obj
				targ.transform_type = k_loc
				targ.bone_target = k_cnt
				targ.transform_space = 'LOCAL_SPACE'
				
				# expression (var * abs(k*2.5) if  abs(k) < 0.4 else var)
				mn = 1/abs(k_dat)
				drv.expression = 'var * abs(correct*' + str(mn) + ') if  abs(correct) < ' + str(abs(k_dat)) + ' else var'

				# remove modifiers
				fmod = f_curve.modifiers[0]
				f_curve.modifiers.remove(fmod)
				
		# ****** ATHER GEO
		for data in self.ather_shape_keys_data_list:
			passp_key = data[0]
			sh_key_name = data[1]
			cnt = data[2]
			loc = data[3]
			dat = data[4]
			vtx_grp = data[5]
			
			# --
			try:
				content = mesh_passport[passp_key]
			except:
				continue
			# --
			for name in content:
				# -- get mesh ob
				try:
					ob = bpy.data.objects[name]
				except:
					return(False,('****** Ather Blends, Ather Geo:', name, 'not Found!'))
					
				if ob.type != 'MESH':
					return(False,('****** Ather Blends, Ather Geo:', name, 'not Mesh!'))
					
				######  == GET exists Shape Keys
				try:
					keys = ob.data.shape_keys.key_blocks
				except:
					basis = ob.shape_key_add(name='Basis', from_mix=True)
				
				# -- create shape_key
				if not sh_key_name in keys.keys():
					shkey = ob.shape_key_add(name=sh_key_name, from_mix=True)
					if vtx_grp:
						shkey.vertex_group = vtx_grp
				else:
					continue
					
				# -- сreate driver
				if cnt == '' or loc == '' or dat == '':
					print(sh_key_name, '  **** not data') 
					continue
					
				# -- -- old construction
				f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
				drv = f_curve.driver
				drv.type = 'AVERAGE'
				drv.show_debug_info = True

				point = f_curve.keyframe_points.insert(0,0)
				point.interpolation = 'LINEAR'
				point = f_curve.keyframe_points.insert(dat,1)
				point.interpolation = 'LINEAR'

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = rig_obj
				targ.transform_type = loc
				targ.bone_target = cnt
				targ.transform_space = 'LOCAL_SPACE'

				fmod = f_curve.modifiers[0]
				f_curve.modifiers.remove(fmod)
								
			
		return(True, 'All Right!')
		
	def create_edit_vertes_groups(self, context):
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			print(mesh_passport[1])	
			return
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			print('****** the name of the \"body\" is not passport')	
			return
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		# -- rig to EDIT mode
		rig_obj = bpy.data.objects[G.rig_name]
		scene = bpy.context.scene
		scene.objects.active = rig_obj
		bpy.ops.object.mode_set(mode = 'EDIT')

		vtx_groups = {}

		# -- get tmp.bone position
		try:
			name = ('FR_' + self.label_tmp_bones[0])
			bone = rig_obj.data.edit_bones[name]
		except:
			print('****** ' + name + ' Not Found!')
			return False

		head = (bone.head[0],bone.head[1],bone.head[2])
		tail = (bone.tail[0], bone.tail[1], bone.tail[2])

		# **************** JAW_SIDE
		try:
			vtx = ob.vertex_groups['jaw_side']
		except:
			vtx = ob.vertex_groups.new('jaw_side')
			for v in ob.data.vertices:
				if v.co[2] >= head[2]:
					vtx.add([v.index], 1.0, 'REPLACE')
				else:
					vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['jaw_side'] = vtx

		# **************** HEAD
		try:
			head_vtx = ob.vertex_groups['head_blend.m']
		except:
			head_vtx = ob.vertex_groups.new('head_blend.m')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				head_vtx.add([v.index], 1.0, 'REPLACE')
			else:
				head_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['head_blend.m'] = head_vtx

		# **************** HEAD R
		try:
			head_r_vtx = ob.vertex_groups['head_blend.r']
		except:
			head_r_vtx = ob.vertex_groups.new('head_blend.r')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				if v.co[0] < 0:
					head_r_vtx.add([v.index], 1.0, 'REPLACE')
				elif v.co[0] == 0:
					head_r_vtx.add([v.index], 0.5, 'REPLACE')
				else:
					head_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				head_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['head_blend.r'] = head_r_vtx

		# ***************** HEAD L
		try:
			head_l_vtx = ob.vertex_groups['head_blend.l']
		except:
			head_l_vtx = ob.vertex_groups.new('head_blend.l')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				if v.co[0] > 0:
					head_l_vtx.add([v.index], 1.0, 'REPLACE')
				elif v.co[0] == 0:
					head_l_vtx.add([v.index], 0.5, 'REPLACE')
				else:
					head_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				head_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['head_blend.l'] = head_l_vtx

		# **************** LIPS *******************************

		# **************** Lip R
		try:
			lip_r_vtx = ob.vertex_groups['lip_blend.r']
		except:
			lip_r_vtx = ob.vertex_groups.new('lip_blend.r')
		#lip_r_vtx = ob.vertex_groups.new('lip_blend.r')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				lip_r_vtx.add([v.index], 1.0, 'REPLACE')
				if (v.co[0] > tail[0]) and (v.co[0] < (0 - tail[0])):
					# calculate weight
					a = tail[0]
					b = (0 - tail[0])
					x = v.co[0]
					'''
					# line interpolation
					weight = (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					lip_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] >= tail[0]:
					lip_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				lip_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['lip_blend.r'] = lip_r_vtx

		# ***************** Lip L
		try:
			lip_l_vtx = ob.vertex_groups['lip_blend.l']
		except:
			lip_l_vtx = ob.vertex_groups.new('lip_blend.l')
		#lip_l_vtx = ob.vertex_groups.new('lip_blend.l')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				lip_l_vtx.add([v.index], 1.0, 'REPLACE')
				if (v.co[0] > tail[0]) and (v.co[0] < (0 - tail[0])):
					# calculate weight
					a = tail[0]
					b = (0 - tail[0])
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))-math.pi) +1)/2

					lip_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] <= tail[0]:
					lip_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				lip_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['lip_blend.l'] = lip_l_vtx

		# *************** Lip Roll R ******************
		try:
			lip_roll_r_vtx = ob.vertex_groups['lip_roll_blend.r']
		except:
			lip_roll_r_vtx = ob.vertex_groups.new('lip_roll_blend.r')

		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				lip_roll_r_vtx.add([v.index], 1.0, 'REPLACE')
				a = tail[0]
				b = 0
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					lip_roll_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] >= b:
					lip_roll_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				lip_roll_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['lip_roll_blend.r'] = lip_roll_r_vtx

		# *************** Lip Roll M ******************
		try:
			lip_roll_m_vtx = ob.vertex_groups['lip_roll_blend.m']
		except:
			lip_roll_m_vtx = ob.vertex_groups.new('lip_roll_blend.m')

		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				lip_roll_m_vtx.add([v.index], 1.0, 'REPLACE')
				# -- Right Part
				a = tail[0]
				b = 0
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))- math.pi) +1)/2

					lip_roll_m_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] <= a:
					lip_roll_m_vtx.add([v.index], 0.0, 'REPLACE')
				# -- Left Part
				a = 0
				b = 0 - tail[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					lip_roll_m_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] >= b:
					lip_roll_m_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				lip_roll_m_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['lip_roll_blend.m'] = lip_roll_m_vtx

		# *************** Lip Roll L ******************
		try:
			lip_roll_l_vtx = ob.vertex_groups['lip_roll_blend.l']
		except:
			lip_roll_l_vtx = ob.vertex_groups.new('lip_roll_blend.l')

		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				lip_roll_l_vtx.add([v.index], 1.0, 'REPLACE')
				a = 0
				b = 0 - tail[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a)) - math.pi) +1)/2

					lip_roll_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] <= a:
					lip_roll_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				lip_roll_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['lip_roll_blend.l'] = lip_roll_l_vtx

		# ************** NOSE *************
		# -- get tmp.bone position
		try:
			name = ('FR_' + self.label_tmp_bones[4])
			bone = rig_obj.data.edit_bones[name]
		except:
			print('****** ' + name + ' Not Found!')
			return False

		head_nose = (bone.head[0],bone.head[1],bone.head[2])
		tail_nose = (bone.tail[0], bone.tail[1], bone.tail[2])

		# ****************** Nose R
		try:
			nose_r_vtx = ob.vertex_groups['nose_blend.r']
		except:
			nose_r_vtx = ob.vertex_groups.new('nose_blend.r')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				nose_r_vtx.add([v.index], 1.0, 'REPLACE')
				if (v.co[0] > tail_nose[0]) and (v.co[0] < (0 - tail_nose[0])):
					# calculate weight
					a = tail_nose[0]
					b = (0 - tail_nose[0])
					x = v.co[0]
					'''
					# line interpolation
					weight = (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					nose_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] >= tail_nose[0]:
					nose_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				nose_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['nose_blend.r'] = nose_r_vtx

		# ****************** Nose L
		try:
			nose_l_vtx = ob.vertex_groups['nose_blend.l']
		except:
			nose_l_vtx = ob.vertex_groups.new('nose_blend.l')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				nose_l_vtx.add([v.index], 1.0, 'REPLACE')
				if (v.co[0] > tail_nose[0]) and (v.co[0] < (0 - tail_nose[0])):
					# calculate weight
					a = tail_nose[0]
					b = (0 - tail_nose[0])
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))-math.pi) +1)/2

					nose_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] <= tail_nose[0]:
					nose_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				nose_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['nose_blend.l'] = nose_l_vtx

		# ***************** BROWS **************************
		# -- get OUT position
		try:
			name = ('FR_' + self.label_tmp_bones[3])
			bone = rig_obj.data.edit_bones[name]
		except:
			print('****** ' + name + ' Not Found!')
			return False
		tail_out = (bone.tail[0], bone.tail[1], bone.tail[2])

		# -- get M position
		try:
			name = ('FR_' + self.label_tmp_bones[1])
			bone = rig_obj.data.edit_bones[name]
		except:
			print('****** ' + name + ' Not Found!')
			return False
		tail_m = (bone.tail[0], bone.tail[1], bone.tail[2])

		# -- get IN position
		try:
			name = ('FR_' + self.label_tmp_bones[2])
			bone = rig_obj.data.edit_bones[name]
		except:
			print('****** ' + name + ' Not Found!')
			return False
		tail_in = (bone.tail[0], bone.tail[1], bone.tail[2])

		# ************* Brow Out R
		try:
			brow_out_r_vtx = ob.vertex_groups['brow_out_blend.r']
		except:
			brow_out_r_vtx = ob.vertex_groups.new('brow_out_blend.r')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				brow_out_r_vtx.add([v.index], 1.0, 'REPLACE')
				a = tail_out[0]
				b = tail_m[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					brow_out_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] > b:
					brow_out_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				brow_out_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['brow_out_blend.r'] = brow_out_r_vtx

		# ************* Brow Out L
		try:
			brow_out_l_vtx = ob.vertex_groups['brow_out_blend.l']
		except:
			brow_out_l_vtx = ob.vertex_groups.new('brow_out_blend.l')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				brow_out_l_vtx.add([v.index], 1.0, 'REPLACE')
				a = 0 - tail_m[0]
				b = 0 - tail_out[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a)) - math.pi) +1)/2

					brow_out_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] < a:
					brow_out_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				brow_out_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['brow_out_blend.l'] = brow_out_l_vtx

		# ************* Brow Middle R
		try:
			brow_m_r_vtx = ob.vertex_groups['brow_m_blend.r']
		except:
			brow_m_r_vtx = ob.vertex_groups.new('brow_m_blend.r')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				brow_m_r_vtx.add([v.index], 1.0, 'REPLACE')
				# Right Part
				a = tail_out[0]
				b = tail_m[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a)) - math.pi) +1)/2

					brow_m_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] < a:
					brow_m_r_vtx.add([v.index], 0.0, 'REPLACE')
				# Left Part
				a = tail_m[0]
				b = tail_in[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					brow_m_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] > b:
					brow_m_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				brow_m_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['brow_m_blend.r'] = brow_m_r_vtx

		# ************* Brow Middle L
		try:
			brow_m_l_vtx = ob.vertex_groups['brow_m_blend.l']
		except:
			brow_m_l_vtx = ob.vertex_groups.new('brow_m_blend.l')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				brow_m_l_vtx.add([v.index], 1.0, 'REPLACE')
				# Right Part
				a = 0 - tail_in[0]
				b = 0 - tail_m[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a)) - math.pi) +1)/2

					brow_m_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] < a:
					brow_m_l_vtx.add([v.index], 0.0, 'REPLACE')
				# Left Part
				a = 0 - tail_m[0]
				b = 0 - tail_out[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					brow_m_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] > b:
					brow_m_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				brow_m_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['brow_m_blend.l'] = brow_m_l_vtx

		# ************* Brow IN R
		try:
			brow_in_r_vtx = ob.vertex_groups['brow_in_blend.r']
		except:
			brow_in_r_vtx = ob.vertex_groups.new('brow_in_blend.r')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				brow_in_r_vtx.add([v.index], 1.0, 'REPLACE')
				# Rigt Part
				a = tail_m[0]
				b = tail_in[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a)) - math.pi) +1)/2

					brow_in_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] < a:
					brow_in_r_vtx.add([v.index], 0.0, 'REPLACE')
				# Left Part
				a = tail_in[0]
				b = 0 - tail_in[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					brow_in_r_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] > b:
					brow_in_r_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				brow_in_r_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['brow_in_blend.r'] = brow_in_r_vtx

		# ************* Brow IN L
		try:
			brow_in_l_vtx = ob.vertex_groups['brow_in_blend.l']
		except:
			brow_in_l_vtx = ob.vertex_groups.new('brow_in_blend.l')
		for v in ob.data.vertices:
			if v.co[2] >= head[2]:
				brow_in_l_vtx.add([v.index], 1.0, 'REPLACE')
				# Rigt Part
				a = tail_in[0]
				b = 0 - tail_in[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a)) - math.pi) +1)/2

					brow_in_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] < a:
					brow_in_l_vtx.add([v.index], 0.0, 'REPLACE')
				# Left Part
				a = 0 - tail_in[0]
				b = 0 - tail_m[0]
				if (v.co[0] > a) and (v.co[0] < b):
					# calculate weight
					x = v.co[0]
					'''
					# line interpolation
					weight = 1 - (x - b)/(a - b)
					'''
					# cos interpolation
					weight = (math.cos(math.pi*((x-a)/(b-a))) +1)/2

					brow_in_l_vtx.add([v.index], weight, 'REPLACE')
				elif v.co[0] > b:
					brow_in_l_vtx.add([v.index], 0.0, 'REPLACE')
			else:
				brow_in_l_vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['brow_in_blend.l'] = brow_in_l_vtx
		
		# **************** STRETCH SQUASH
		try:
			vtx = ob.vertex_groups['str_squash']
		except:
			vtx = ob.vertex_groups.new('str_squash')
			# calculate weight
			for v in ob.data.vertices:
				if v.co[2] >= head[2]:
					vtx.add([v.index], 1.0, 'REPLACE')
				else:
					vtx.add([v.index], 0.0, 'REPLACE')
		vtx_groups['str_squash'] = vtx

		# ******** FIN		
		return vtx_groups
		
	def autolids_base(self, context):
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			return(False, mesh_passport[1])
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			return(False, '***** Not key \"body\" in mesh_passport')
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		#ob = bpy.context.object
		#assert ob.type == 'MESH'
		
		sh_keys = ob.data.shape_keys.key_blocks.keys()
		#print(sh_keys)
		
		# get eye limits # r_eye_limit_rotation l_eye_limit_rotation
		r_cns_name = 'r_eye_limit_rotation'
		l_cns_name = 'l_eye_limit_rotation'
		# R
		try:
			r_cns = self.eye_bone_r.constraints[r_cns_name]
		except:
			return(False, '***** Not eye_r constraints!!!!')
		r_low_lim = r_cns.min_x
		r_up_lim = r_cns.max_x
		r_out_lim = r_cns.min_z
		r_in_lim = r_cns.max_z
		
		# L
		try:
			l_cns = self.eye_bone_l.constraints[l_cns_name]
		except:
			return(False, '***** Not eye_l constraints!!!!')
		l_low_lim = l_cns.min_x
		l_up_lim = l_cns.max_x
		l_out_lim = l_cns.max_z
		l_in_lim = l_cns.min_z
		
		# *********** Shape Keys *************			
		for data in self.shape_keys_vtx_grp:
			sh_key_name = data[0]
			vtx_grp = data[1]
							
			# -- create shape_key
			if not (sh_key_name in sh_keys):
				#print(sh_key_name, vtx_grp)
				shkey = ob.shape_key_add(name=sh_key_name, from_mix=True)
				shkey.vertex_group = vtx_grp
				
				# create drivers				
				if sh_key_name == 'autolid_low.r' or sh_key_name == 'autolid_low.l':
					f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
					drv = f_curve.driver
					drv.type = 'SCRIPTED'
					drv.show_debug_info = True

					point = f_curve.keyframe_points.insert(0,0)
					point.interpolation = 'LINEAR'
					if sh_key_name == 'autolid_low.r':
						point = f_curve.keyframe_points.insert(r_low_lim,1)
					else:
						point = f_curve.keyframe_points.insert(l_low_lim,1)
					point.interpolation = 'LINEAR'
					
					var = drv.variables.new()
					var.name = 'var'
					var.type = 'TRANSFORMS'
					
					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = 'ROT_X'
					if sh_key_name == 'autolid_low.r':
						targ.bone_target = 'FR_eye_R'
					else:
						targ.bone_target = 'FR_eye_L'
					targ.transform_space = 'LOCAL_SPACE'
					
					# correct var
					var = drv.variables.new()
					var.name = 'correct'
					var.type = 'TRANSFORMS'

					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = 'LOC_X'
					if sh_key_name == 'autolid_low.r':
						targ.bone_target = 'blink_R'
					else:
						targ.bone_target = 'blink_L'
					targ.transform_space = 'LOCAL_SPACE'

					# expression (var * abs(k*2.5) if  abs(k) < 0.4 else var)
					drv.expression = 'var * (1 - abs(correct))'

					
					fmod = f_curve.modifiers[0]
					f_curve.modifiers.remove(fmod)
					
				if sh_key_name == 'autolid_up.r' or sh_key_name == 'autolid_up.l':
					f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
					drv = f_curve.driver
					drv.type = 'SCRIPTED'
					drv.show_debug_info = True

					point = f_curve.keyframe_points.insert(0,0)
					point.interpolation = 'LINEAR'
					if sh_key_name == 'autolid_up.r':
						point = f_curve.keyframe_points.insert(r_up_lim,1)
					else:
						point = f_curve.keyframe_points.insert(l_up_lim,1)
					point.interpolation = 'LINEAR'
					
					var = drv.variables.new()
					var.name = 'var'
					var.type = 'TRANSFORMS'
					
					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = 'ROT_X'
					if sh_key_name == 'autolid_up.r':
						targ.bone_target = 'FR_eye_R'
					else:
						targ.bone_target = 'FR_eye_L'
					targ.transform_space = 'LOCAL_SPACE'
					
					# correct var
					var = drv.variables.new()
					var.name = 'correct'
					var.type = 'TRANSFORMS'

					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = 'LOC_X'
					if sh_key_name == 'autolid_up.r':
						targ.bone_target = 'blink_R'
					else:
						targ.bone_target = 'blink_L'
					targ.transform_space = 'LOCAL_SPACE'

					# expression (var * abs(k*2.5) if  abs(k) < 0.4 else var)
					drv.expression = 'var * (1 - abs(correct))'
					
					fmod = f_curve.modifiers[0]
					f_curve.modifiers.remove(fmod)
					
				if sh_key_name == 'autolid_out.r' or sh_key_name == 'autolid_out.l':
					f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
					drv = f_curve.driver
					drv.type = 'AVERAGE'
					drv.show_debug_info = True

					point = f_curve.keyframe_points.insert(0,0)
					point.interpolation = 'LINEAR'
					if sh_key_name == 'autolid_out.r':
						point = f_curve.keyframe_points.insert(r_out_lim,1)
					else:
						point = f_curve.keyframe_points.insert(l_out_lim,1)
					point.interpolation = 'LINEAR'
					
					var = drv.variables.new()
					var.name = 'var'
					var.type = 'TRANSFORMS'
					
					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = 'ROT_Z'
					if sh_key_name == 'autolid_out.r':
						targ.bone_target = 'FR_eye_R'
					else:
						targ.bone_target = 'FR_eye_L'
					targ.transform_space = 'LOCAL_SPACE'
					
					fmod = f_curve.modifiers[0]
					f_curve.modifiers.remove(fmod)
					
				if sh_key_name == 'autolid_in.r' or sh_key_name == 'autolid_in.l':
					f_curve = ob.data.shape_keys.key_blocks[sh_key_name].driver_add('value')
					drv = f_curve.driver
					drv.type = 'AVERAGE'
					drv.show_debug_info = True

					point = f_curve.keyframe_points.insert(0,0)
					point.interpolation = 'LINEAR'
					if sh_key_name == 'autolid_in.r':
						point = f_curve.keyframe_points.insert(r_in_lim,1)
					else:
						point = f_curve.keyframe_points.insert(l_in_lim,1)
					point.interpolation = 'LINEAR'
					
					var = drv.variables.new()
					var.name = 'var'
					var.type = 'TRANSFORMS'
					
					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = 'ROT_Z'
					if sh_key_name == 'autolid_in.r':
						targ.bone_target = 'FR_eye_R'
					else:
						targ.bone_target = 'FR_eye_L'
					targ.transform_space = 'LOCAL_SPACE'
					
					fmod = f_curve.modifiers[0]
					f_curve.modifiers.remove(fmod)
			else:
				return(False, 'Autolid Shape Keys already exists!')
		return(True, 'All Right!')
	
	def insert_in_between(self, context, shape_key, num):
		#passport().string_add_to_passport(bpy.context, 'list_of_inbetweens', shape_key)
		list_of_inbetweens = passport().read_passport(context, 'list_of_inbetweens')
		if list_of_inbetweens[0]:
			if shape_key in list_of_inbetweens[1]:
				return(False, '****** Inbetween Shape Key Already Exists!')
		
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			#print(mesh_passport[1])	
			return(False, '****** Not Mesh Passport!')
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			#print('****** the name of the \"body\" is not passport')	
			return(False, '****** the name of the \"body\" is not passport')
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		#ob = bpy.context.object
		#assert ob.type == 'MESH'
		
		# from  -- central_side_shape_keys
		sh_keys = ob.data.shape_keys.key_blocks.keys()
		if not shape_key in sh_keys:
			return(False, '****** This Shape Key not found!')
		
		# get shape keys data
		central = ob.data.shape_keys.key_blocks[shape_key]
		basis = ob.data.shape_keys.key_blocks['Basis']
		vtx_group = central.vertex_group
		fcurves = ob.data.shape_keys.animation_data.drivers.items()
		
		# new rebild base shape key
		# -- exist fcurve
		fcurve_ex = False
		data_path = 'key_blocks[\"' + shape_key + '\"].value'
		for fc in fcurves:
			if fc[1].data_path == data_path:
				f_curve = fc[1]
				fcurve_ex = True
				break
		
		# -- get max_value
		if fcurve_ex:
			max_value = False
			# -- get max data
			for point in f_curve.keyframe_points:
				if point.co[1] == 1.0:
					max_value = point.co[0]
					break
			# -- get var
			drv = f_curve.driver
			drv_type = drv.type
			expression = False
			if drv_type == 'SCRIPTED':
				expression = drv.expression
			var = drv.variables['var']
			targ = var.targets[0]
			tr_type = targ.transform_type
			bon_target = targ.bone_target
			
			# -- -- get ather vars
			corrects = {}
			for key in drv.variables.keys():
				if key == 'var':
					continue
				c_var = drv.variables[key]
				c_target = c_var.targets[0]
				corrects[key] = (c_target.transform_type, c_target.bone_target)
						
			# -- remove driver
			ob.data.shape_keys.key_blocks[shape_key].driver_remove('value')
			
			# -- create driver
			f_curve = ob.data.shape_keys.key_blocks[shape_key].driver_add('value')
			drv = f_curve.driver
			#drv.type = 'AVERAGE'
			drv.type = drv_type
			if expression:
				drv.expression = expression
			drv.show_debug_info = True

			point = f_curve.keyframe_points.insert(max_value*((num-1)/num),0)
			point.interpolation = 'LINEAR'
			point = f_curve.keyframe_points.insert(max_value,1)
			point.interpolation = 'LINEAR'

			var = drv.variables.new()
			var.name = 'var'
			var.type = 'TRANSFORMS'

			# first var
			targ = var.targets[0]
			targ.id = self.rig_obj
			targ.transform_type = tr_type
			targ.bone_target = bon_target
			targ.transform_space = 'LOCAL_SPACE'
			
			# correct vars
			if corrects:
				for key in corrects:
					c_var = drv.variables.new()
					c_var.name = key
					c_var.type = 'TRANSFORMS'

					targ = c_var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = corrects[key][0]
					targ.bone_target = corrects[key][1]
					targ.transform_space = 'LOCAL_SPACE'

			fmod = f_curve.modifiers[0]
			f_curve.modifiers.remove(fmod)
		
		# ********* CENTRAL
		list_k = []
		for i in range(1, num):
			k = i/num
			list_k.append(k)
						
			# -- create shape key in_between
			new_shape_key_name = shape_key + str(round(k, 2)).replace('0', '')
			if not new_shape_key_name in sh_keys:
				shkey = ob.shape_key_add(name=new_shape_key_name, from_mix=True)
				shkey.vertex_group = vtx_group
				
			# -- make vtx co
			for v in ob.data.vertices:
				basis_v = basis.data[v.index].co
				central_v = central.data[v.index].co
				shkey.data[v.index].co[0] = basis_v[0] + (central_v[0] - basis_v[0])*k
				shkey.data[v.index].co[1] = basis_v[1] + (central_v[1] - basis_v[1])*k
				shkey.data[v.index].co[2] = basis_v[2] + (central_v[2] - basis_v[2])*k
				
			# make driver
			if fcurve_ex:
				f_curve = ob.data.shape_keys.key_blocks[new_shape_key_name].driver_add('value')
				drv = f_curve.driver
				#drv.type = 'AVERAGE'
				drv.type = drv_type
				if expression:
					drv.expression = expression
				drv.show_debug_info = True

				point = f_curve.keyframe_points.insert(max_value*((i-1)/num),0)
				point.interpolation = 'LINEAR'
				point = f_curve.keyframe_points.insert(max_value*k,1)
				point.interpolation = 'LINEAR'
				point = f_curve.keyframe_points.insert(max_value*((i+1)/num),0)
				point.interpolation = 'LINEAR'

				var = drv.variables.new()
				var.name = 'var'
				var.type = 'TRANSFORMS'

				targ = var.targets[0]
				targ.id = self.rig_obj
				targ.transform_type = tr_type
				targ.bone_target = bon_target
				targ.transform_space = 'LOCAL_SPACE'
				
				# correct vars
				if corrects:
					for key in corrects:
						c_var = drv.variables.new()
						c_var.name = key
						c_var.type = 'TRANSFORMS'

						targ = c_var.targets[0]
						targ.id = self.rig_obj
						targ.transform_type = corrects[key][0]
						targ.bone_target = corrects[key][1]
						targ.transform_space = 'LOCAL_SPACE'

				fmod = f_curve.modifiers[0]
				f_curve.modifiers.remove(fmod)
				
		# add shape key in 'list_of_inbetweens'
		#passport().string_add_to_passport(bpy.context, 'list_of_inbetweens', shape_key)
		passport().key_data_add_to_passport(context, 'list_of_inbetweens', shape_key, list_k)
		
		# ********* SIDES
		
		try:
			sides = self.central_side_shape_keys[shape_key]
		except:
			return(True, 'All Right!')
		cent_to_side = {}
		for side in sides:
			# -- vtx group
			full_side_key = ob.data.shape_keys.key_blocks[side]
			vtx_group = full_side_key.vertex_group
			# -- get driver data
			data_path = 'key_blocks[\"' + side + '\"].value'
			max_value = False
			for fc in fcurves:
				if fc[1].data_path == data_path:
					# -- get max data
					for point in fc[1].keyframe_points:
						if point.co[1] == 1.0:
							max_value = point.co[0]
							break
					# -- get var
					drv = fc[1].driver
					drv_type = drv.type
					expression = False
					if drv_type == 'SCRIPTED':
						expression = drv.expression
					var = drv.variables['var']
					targ = var.targets[0]
					tr_type = targ.transform_type
					bon_target = targ.bone_target
										
					# -- -- get ather vars
					corrects = {}
					for key in drv.variables.keys():
						if key == 'var':
							continue
						c_var = drv.variables[key]
						c_target = c_var.targets[0]
						corrects[key] = (c_target.transform_type, c_target.bone_target)
					
					# -- remove driver
					ob.data.shape_keys.key_blocks[side].driver_remove('value')
					
					# -- new driver
					f_curve = ob.data.shape_keys.key_blocks[side].driver_add('value')
					drv = f_curve.driver
					#drv.type = 'AVERAGE'
					drv.type = drv_type
					if expression:
						drv.expression = expression
					drv.show_debug_info = True

					point = f_curve.keyframe_points.insert(max_value*((num-1)/num),0)
					point.interpolation = 'LINEAR'
					point = f_curve.keyframe_points.insert(max_value,1)
					point.interpolation = 'LINEAR'
															
					var = drv.variables.new()
					var.name = 'var'
					var.type = 'TRANSFORMS'
					
					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = tr_type
					targ.bone_target = bon_target
					targ.transform_space = 'LOCAL_SPACE'
					
					# correct vars
					if corrects:
						for key in corrects:
							c_var = drv.variables.new()
							c_var.name = key
							c_var.type = 'TRANSFORMS'

							targ = c_var.targets[0]
							targ.id = self.rig_obj
							targ.transform_type = corrects[key][0]
							targ.bone_target = corrects[key][1]
							targ.transform_space = 'LOCAL_SPACE'
					
					fmod = f_curve.modifiers[0]
					f_curve.modifiers.remove(fmod)
					
					#print('**** ', side, tr_type, bon_target, max_value)
					break
			
			for i in range(1, num):
				k = i/num
				
				# -- create shape key
				ib_side_name = side + str(round(k, 2)).replace('0', '')
				
				# -- 
				try:
					cent_to_side[(shape_key + str(round(k, 2)).replace('0', ''))]
				except:
					cent_to_side[(shape_key + str(round(k, 2)).replace('0', ''))] = []
				cent_to_side[(shape_key + str(round(k, 2)).replace('0', ''))].append(ib_side_name)
				
				# --
				if not ib_side_name in sh_keys:
					ib_side_shkey = ob.shape_key_add(name=ib_side_name, from_mix=True)
					ib_side_shkey.vertex_group = vtx_group
					
					# make driver
					f_curve = ob.data.shape_keys.key_blocks[ib_side_name].driver_add('value')
					drv = f_curve.driver
					#drv.type = 'AVERAGE'
					drv.type = drv_type
					if expression:
						drv.expression = expression
					drv.show_debug_info = True

					point = f_curve.keyframe_points.insert(max_value*((i-1)/num),0)
					point.interpolation = 'LINEAR'
					point = f_curve.keyframe_points.insert(max_value*k,1)
					point.interpolation = 'LINEAR'
					point = f_curve.keyframe_points.insert(max_value*((i+1)/num),0)
					point.interpolation = 'LINEAR'
										
					var = drv.variables.new()
					var.name = 'var'
					var.type = 'TRANSFORMS'
					
					targ = var.targets[0]
					targ.id = self.rig_obj
					targ.transform_type = tr_type
					targ.bone_target = bon_target
					targ.transform_space = 'LOCAL_SPACE'
					
					# correct vars
					if corrects:
						for key in corrects:
							c_var = drv.variables.new()
							c_var.name = key
							c_var.type = 'TRANSFORMS'

							targ = c_var.targets[0]
							targ.id = self.rig_obj
							targ.transform_type = corrects[key][0]
							targ.bone_target = corrects[key][1]
							targ.transform_space = 'LOCAL_SPACE'
					
					fmod = f_curve.modifiers[0]
					f_curve.modifiers.remove(fmod)
				
		# text data block
		try:
			text = bpy.data.texts['rig_meta_data']
		except:
			text = bpy.data.texts.new('rig_meta_data')
			
		string = text.as_string()
		
		if string:
			data = json.loads(string)
			try:
				cent_to_side_blends = data['center_to_side_blends']
			except:
				cent_to_side_blends = {}
				
		else:
			data = {}
			cent_to_side_blends = {}
			
		for key in cent_to_side:
			cent_to_side_blends[key] = cent_to_side[key]

		data['center_to_side_blends'] = cent_to_side_blends
			
		text.clear()
		text.write(json.dumps(data, sort_keys=True, indent=4))
		
		return(True, 'All Right!')
		
	def copy_central_to_side_shape_keys(self, context):
		print('********** central to side *****************')
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			#print('****** the name of the \"body\" is not passport')	
			return(False, '****** the name of the \"body\" is not passport')
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		#ob = bpy.context.object
		#assert ob.type == 'MESH'
		
		try:
			sh_keys = ob.data.shape_keys.key_blocks.keys()
		except:
			return(False, 'Shape Keys Not Found!')
		
		# ****** original
		for key in self.central_side_shape_keys:
			# test exists
			try:
				ob.data.shape_keys.key_blocks[key]
			except:
				continue
			
			for target in self.central_side_shape_keys[key]:
				# -- -- copy shape keys
				for v in ob.data.vertices:
					#open_shkey.data[v.index].co = shkey.data[v.index].co
					ob.data.shape_keys.key_blocks[target].data[v.index].co = ob.data.shape_keys.key_blocks[key].data[v.index].co

		# ****** inbetween
		try:
			text = bpy.data.texts['rig_meta_data']
		except:
			#return(True, '****** Not Inbetween!')
			print('****** Not Inbetween!')
		else:
			string = text.as_string()

			if string:
				data = json.loads(string)
				try:
					cent_to_side_blends = data['center_to_side_blends'] #center_to_side_blends
				except:
					#return(True, '****** Not \"center_to_side_blends\" data!')
					print('****** Not \"center_to_side_blends\" data!')

				else:
					for key in cent_to_side_blends:
						# test exists
						try:
							ob.data.shape_keys.key_blocks[key]
						except:
							#print('***** continue ', key)
							continue
						# original
						for target in cent_to_side_blends[key]:
							# -- -- copy shape keys
							#print('**** key', key, ' to target ', target)
							for vtx in ob.data.vertices:
								#open_shkey.data[v.index].co = shkey.data[v.index].co
								ob.data.shape_keys.key_blocks[target].data[vtx.index].co = ob.data.shape_keys.key_blocks[key].data[vtx.index].co
			else:
				pass
		
		# ----------------- Individual ---------------------
		# ------ jaw_side_R -> jaw_side_open_R
		try:
			target = ob.data.shape_keys.key_blocks['jaw_side_open_R']
			source = ob.data.shape_keys.key_blocks['jaw_side_R']
		except:
			pass
			print('*'*25, 'epte')
		else:
			#print('*'*25, 'yes!')
			for v in ob.data.vertices:
				target.data[v.index].co = source.data[v.index].co
		
		# ----- mirrors
		mirror_shape_keys = [('jaw_side_R', 'jaw_side_L'), ('jaw_side_open_R', 'jaw_side_open_L'), ('lip_side.r','lip_side.l')]
		vertex_group = ob.vertex_groups['head_blend.m']
		vertices = []
		for v in ob.data.vertices:
			if vertex_group.weight(v.index) > 0:
				vertices.append(v)
		
		for keys in mirror_shape_keys:
			try:
				target = ob.data.shape_keys.key_blocks[keys[1]]
				source = ob.data.shape_keys.key_blocks[keys[0]]
			except:
				continue
			
			for v in vertices:
				# get mirror vertex_index
				# -- mirror co
				m_co = (-v.co[0], v.co[1], v.co[2])
				# -- get near mirror vertex
				dist = abs(v.co[0])*2
				m_v = v
				for vtx in vertices:
					d = ((vtx.co[0] - m_co[0])**2 + (vtx.co[1] - m_co[1])**2 + (vtx.co[2] - m_co[2])**2)**0.5
					if d < dist:
						dist = d
						m_v = vtx
					else:
						continue
				#print(v.co, m_v.co)
				
				# set vertex position
				s_co = source.data[m_v.index].co
				delta_x = s_co[0] - m_v.co[0]
				target.data[v.index].co = ((v.co[0] - delta_x), s_co[1], s_co[2])
			#target.data[v.index].co = (source.data[v.index].co)
		
		return(True, 'All Right!')
	
	def edit_shape_keys(self, context, target):
		# ******************** test passoport *****************************
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
		else:
			return(False, mesh_passport[1])
		
		# -- get mesh ob
		try:
			body_name = mesh_passport['body'][0]
		except:
			return(False, '***** Not key \"body\" in mesh_passport')
		else:
			ob = bpy.data.objects[body_name]
		assert ob.type == 'MESH'
		
		#ob = bpy.context.object
		#target = 'jaw_side_L'
		
		#sh_key = ob.data.shape_keys.key_blocks[target]
		index = 0
		try:
			for i,key in enumerate(ob.data.shape_keys.key_blocks.keys()):
				if key == target:
					index = i
					break
		except:
			return(False, '****** object \"body\", does not have the Shape_Keys!')
			
		if index:
			scene = bpy.context.scene
			scene.objects.active = ob
			ob.active_shape_key_index = index
			bpy.ops.object.mode_set(mode = 'EDIT')
		else:
			return(False, '****** This key not found!')
		
		return(True, 'all right!')
		
	def autolids_tuners(self, context):
		pass
	
	def get_data_save_path(self, data_type):
		lineyka = False
		activity_path = None
		if G.user_text_name in bpy.data.texts:
			data_dict = json.loads(bpy.data.texts[G.user_text_name].as_string())
			asset_path = data_dict.get('current_task').get('asset_path')
			activity_name = data_dict.get('activites').get('meta_data')
			if asset_path and activity_name:
				activity_path = os.path.normpath(os.path.join(asset_path, activity_name))
				if os.path.exists(activity_path):
					lineyka = True
		
		if data_type == 'SINGL':
			if lineyka:
				return(os.path.normpath(os.path.join(activity_path, '.singl_vertex_data.json')))
			else:
				#return(os.path.join(os.path.expanduser('~'), '.singl_vertex_data.json').replace('\\','/'))
				return(os.path.normpath(os.path.join(os.path.expanduser('~'), '.singl_vertex_data.json')))
		elif data_type == 'ALL_SHAPE_KEYS':
			if lineyka:
				return(os.path.normpath(os.path.join(activity_path, '.all_shape_keys_vertex_data.json')))
			else:
				#return(os.path.join(os.path.expanduser('~'), '.all_shape_keys_vertex_data.json').replace('\\','/'))
				return(os.path.normpath(os.path.join(os.path.expanduser('~'), '.all_shape_keys_vertex_data.json')))
		elif data_type == 'ALL_VERTEX_GROUPS':
			if lineyka:
				return(os.path.normpath(os.path.join(activity_path, '.all_vertex_groups_data.json')))
			else:
				return(os.path.normpath(os.path.join(os.path.expanduser('~'), '.all_vertex_groups_data.json')))
	
	def export_single_vertex_data(self, context):
		# get select mesh
		ob = bpy.context.object
		if not ob.type == 'MESH':
			return(False, '****** Select object Not Mesh!')
			
		if bpy.context.mode != 'OBJECT':
			return(False, '****** Required "OBJECT" mode!')
		# get save path
		path = self.get_data_save_path('SINGL')
		
		# get vertex data
		vertex_data = {}
		me = ob.to_mesh(scene=bpy.context.scene, apply_modifiers=True, settings='PREVIEW')
		for vtx in ob.data.vertices:
			vertex_data[vtx.index] = me.vertices[vtx.index].co[:]
		bpy.data.meshes.remove(me)
		jsn = json.dumps(vertex_data, sort_keys=True, indent=4)
		data_fale = open(path, 'w')
		data_fale.write(jsn)
		data_fale.close()
		return(True, ('vertex data saved! to: ' + path))
		
	def export_all_shape_key_data(self, context):
		#### get 'body' obj from mesh_passport
		ob = None
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
			try:
				body_name = mesh_passport['body'][0]
			except:
				return(False, '****** Not Body_Key in Mesh_Passport')
			try:
				ob = bpy.data.objects[body_name]
			except:
				return(False, ('****** \"body\" object not found! ' + body_name))
			
			if not ob.type == 'MESH':
				return(False, '****** \"body\" object Not Mesh!')
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		####
		# get save path
		path = self.get_data_save_path('ALL_SHAPE_KEYS')
		
		# get vertex data  ob.data.shape_keys.key_blocks[target]  Basis
		vertex_data = {}
		try:
			list_shape_keys = ob.data.shape_keys.key_blocks.keys()
		except:
			return(False, '***** \"body\" has no Shape_keys')
			
		for name in list_shape_keys:
			if name == 'Basis':
				continue
			vertex_data[name] = {}
			shape_key = ob.data.shape_keys.key_blocks[name]
			for vtx in ob.data.vertices:
				vertex_data[name][vtx.index] = shape_key.data[vtx.index].co[:]
		
		jsn = json.dumps(vertex_data, sort_keys=True, indent=4)
		data_fale = open(path, 'w')
		data_fale.write(jsn)
		data_fale.close()
		return(True, ('vertex data saved to: ' + path))
		
	def export_all_vertex_groups(self, context):
		#### get 'body' obj from mesh_passport
		ob = None
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
			try:
				body_name = mesh_passport['body'][0]
			except:
				return(False, '****** Not Body_Key in Mesh_Passport')
			try:
				ob = bpy.data.objects[body_name]
			except:
				return(False, ('****** \"body\" object not found! ' + body_name))
			
			if not ob.type == 'MESH':
				return(False, '****** \"body\" object Not Mesh!')
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		####
		# get save path
		path = self.get_data_save_path('ALL_VERTEX_GROUPS')
		
		# get vertex data  ob.data.shape_keys.key_blocks[target]  Basis
		weight_data = {}
		try:
			list_vertex_groups = ob.vertex_groups.keys()
		except:
			return(False, '***** \"body\" has no Vertex_Groups')
		for name in list_vertex_groups:
			weight_data[name] = {}
			vertex_group = ob.vertex_groups[name]
			for vtx in ob.data.vertices:
				try:
					weight_data[name][vtx.index] = vertex_group.weight(vtx.index)
				except:
					pass
				
		jsn = json.dumps(weight_data, sort_keys=True, indent=4)
		data_fale = open(path, 'w')
		data_fale.write(jsn)
		data_fale.close()
		return(True, ('weight data saved to: ' + path))
		
	def import_single_vertex_data(self, context, target):
		#### get 'body' obj from mesh_passport
		ob = None
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
			try:
				body_name = mesh_passport['body'][0]
			except:
				return(False, '****** Not Body_Key in Mesh_Passport')
			try:
				ob = bpy.data.objects[body_name]
			except:
				return(False, ('****** \"body\" object not found! ' + body_name))
			
			if not ob.type == 'MESH':
				return(False, '****** \"body\" object Not Mesh!')
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		####
		
		'''
		# get select mesh
		ob = bpy.context.object
		if not ob.type == 'MESH':
			return(False, '****** Select object Not Mesh!')
		'''
		
		# get save path
		path = self.get_data_save_path('SINGL')
		if not os.path.exists(path):
			return(False, '****** data file not found!')
		
		# read vertex data
		data_fale = open(path)
		vertex_data = json.load(data_fale)
		data_fale.close()
		
		# ob to object mode
		context.scene.objects.active = ob
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		# applying data
		shape_key = None
		try:
			shape_key = ob.data.shape_keys.key_blocks[target]
		except:
			return(False, '****** \"body\" has no Shape_Keys')
			
		for v in ob.data.vertices:
			shape_key.data[v.index].co = vertex_data[str(v.index)]
		
		return(True, 'vertex data imported!')
		
	def import_all_shape_key_data(self, context):
		#### get 'body' obj from mesh_passport
		ob = None
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
			try:
				body_name = mesh_passport['body'][0]
			except:
				return(False, '****** Not Body_Key in Mesh_Passport')
			try:
				ob = bpy.data.objects[body_name]
			except:
				return(False, ('****** \"body\" object not found! ' + body_name))
			
			if not ob.type == 'MESH':
				return(False, '****** \"body\" object Not Mesh!')
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		####
		# get save path
		path = self.get_data_save_path('ALL_SHAPE_KEYS')
		if not os.path.exists(path):
			return(False, '****** data file not found!')
			
		# read vertex data
		data_fale = open(path)
		vertex_data = json.load(data_fale)
		data_fale.close()
		
		# ob to object mode
		context.scene.objects.active = ob
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		# applying data
		for name in vertex_data:
			if name == 'Basis':
				continue
			try:
				shape_key = ob.data.shape_keys.key_blocks[name]
			except:
				print('*** not found Shape_Key with name: ', name)
				continue
			for vtx in ob.data.vertices:
				shape_key.data[vtx.index].co = vertex_data[name][str(vtx.index)]
			
		return(True, 'vertex data imported!')
		
	def import_single_sk_from_all(self, context, target):
		#### get 'body' obj from mesh_passport
		ob = None
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
			try:
				body_name = mesh_passport['body'][0]
			except:
				return(False, '****** Not Body_Key in Mesh_Passport')
			try:
				ob = bpy.data.objects[body_name]
			except:
				return(False, ('****** \"body\" object not found! ' + body_name))
			
			if not ob.type == 'MESH':
				return(False, '****** \"body\" object Not Mesh!')
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
			
		####
		# get save path
		path = self.get_data_save_path('ALL_SHAPE_KEYS')
		if not os.path.exists(path):
			return(False, '****** data file not found!')
			
		# read vertex data
		data_fale = open(path)
		vertex_data = json.load(data_fale)
		data_fale.close()
		
		# ob to object mode
		context.scene.objects.active = ob
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		if target in vertex_data.keys():
			if not target in ob.data.shape_keys.key_blocks.keys():
				return(False, ('** not found Shape_Key with name: ', target))
				
			shape_key = ob.data.shape_keys.key_blocks[target]
			
			for vtx in ob.data.vertices:
				shape_key.data[vtx.index].co = vertex_data[target][str(vtx.index)]
		
		return(True, 'single vertex data imported!')
		
	def import_all_vertex_groups(self, context):
		#### get 'body' obj from mesh_passport
		ob = None
		mesh_passport = passport().read_passport(context, 'mesh_passport')
		if mesh_passport[0]:
			mesh_passport = mesh_passport[1]
			try:
				body_name = mesh_passport['body'][0]
			except:
				return(False, '****** Not Body_Key in Mesh_Passport')
			try:
				ob = bpy.data.objects[body_name]
			except:
				return(False, ('****** \"body\" object not found! ' + body_name))
			
			if not ob.type == 'MESH':
				return(False, '****** \"body\" object Not Mesh!')
		else:
			#print(mesh_passport[1])	
			return(False, mesh_passport[1])
		####
		# get save path
		path = self.get_data_save_path('ALL_VERTEX_GROUPS')
		if not os.path.exists(path):
			return(False, '****** data file not found!')
			
		# read weight data
		data_fale = open(path)
		weight_data = json.load(data_fale)
		data_fale.close()
		
		for key in weight_data:
			try:
				vgs = ob.vertex_groups[key]
			except:
				print('****** vertex group \"', key, '\"not Found')
				continue
			for vtx in ob.data.vertices:
				if str(vtx.index) in weight_data[key]:
					vgs.add((vtx.index,), weight_data[key][str(vtx.index)], 'REPLACE')
				else:
					try:
						vgs.remove(vtx.index)
					except:
						pass
		
		return(True, 'all right!')

class eye_limits:
	def __init__(self):
		self.limits = ('LOW','UP','SIDE')
		# poses
		self.start_r = False
		self.start_l = False
		self.low_r = False
		self.low_l = False
		self.up_r = False
		self.up_l = False
		self.right_r = False
		self.right_l = False
		# bones
		# -- rig data
		self.rig_obj = bpy.data.objects[G.rig_name]
		self.rig_arm = self.rig_obj.data
		# -- get pose.bones
		try:
			self.eye_bone_r = self.rig_obj.pose.bones['FR_eye_R']
		except:
			print("****** Not Found pose.bones[FR_eye_R]")
			return
		try:
			self.eye_bone_l = self.rig_obj.pose.bones['FR_eye_L']
		except:
			print("****** Not Found pose.bones[FR_eye_L]")
			return
		# -- get eye-ik-bones
		try:
			self.ik_c = self.rig_obj.pose.bones['eye_ik']
		except:
			print("****** Not Found pose.bones[eye_ik]")
			return
		try:
			self.ik_r = self.rig_obj.pose.bones['eye_R']
		except:
			print("****** Not Found pose.bones[eye_R]")
			return
		try:
			self.ik_l = self.rig_obj.pose.bones['eye_L']
		except:
			print("****** Not Found pose.bones[eye_L]")
			return
		
		# get constraints
		r_cns_name = 'r_eye_limit_rotation'
		l_cns_name = 'l_eye_limit_rotation'
		angle = math.pi/2
		try:
			self.r_cns = self.eye_bone_r.constraints[r_cns_name]
			self.r_cns.use_limit_x = False
			self.r_cns.use_limit_z = False
		except:
			self.r_cns = self.eye_bone_r.constraints.new('LIMIT_ROTATION')
			self.r_cns.name = r_cns_name
			self.r_cns.owner_space = 'LOCAL'
			self.r_cns.use_limit_x = False
			self.r_cns.min_x = -angle
			self.r_cns.max_x = angle
			self.r_cns.use_limit_z = False
			self.r_cns.min_z = -angle
			self.r_cns.max_z = angle
		try:
			self.l_cns = self.eye_bone_l.constraints[l_cns_name]
			self.l_cns.use_limit_x = False
			self.l_cns.use_limit_z = False		
		except:
			self.l_cns = self.eye_bone_l.constraints.new('LIMIT_ROTATION')
			self.l_cns.name = l_cns_name
			self.l_cns.owner_space = 'LOCAL'
			self.l_cns.use_limit_x = False
			self.l_cns.min_x = -angle
			self.l_cns.max_x = angle
			self.l_cns.use_limit_z = False
			self.l_cns.min_z = -angle
			self.l_cns.max_z = angle
			
		#self.get_start_position()
	
		
	def get_start_position(self):
		# --- ik to start
		self.ik_c.location = (0,0,0)
		self.ik_r.location = (0,0,0)
		self.ik_l.location = (0,0,0)
		
		# --- update driver affects
		bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)
		
		self.start_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		self.start_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])
		
		print('okey!')
		
	def get_low_position(self):
		# get low position
		low_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		low_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])
		
		# get start position
		# --- ik to start
		self.ik_c.location = (0,0,0)
		self.ik_r.location = (0,0,0)
		self.ik_l.location = (0,0,0)
		
		# --- update driver affects
		bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)
		
		self.start_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		self.start_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])

		
		# R
		ctt = (((self.start_r[0] - low_r[0])**2 + (self.start_r[1] - low_r[1])**2 + (self.start_r[2] - low_r[2])**2)**0.5)/2
		self.low_r = 2 * (math.asin(ctt/self.eye_bone_r.length))
		
		# L
		ctt_l = (((self.start_l[0] - low_l[0])**2 + (self.start_l[1] - low_l[1])**2 + (self.start_l[2] - low_l[2])**2)**0.5)/2
		self.low_l = 2 * (math.asin(ctt_l/self.eye_bone_l.length))
		
		# apply parametres
		if self.low_r:
			self.r_cns.min_x = -self.low_r
		if self.low_l:
			self.l_cns.min_x = -self.low_l
		
		#print((2 * ctt))
		
	def get_up_position(self):
		# get up position
		up_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		up_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])
		
		# get start position
		# --- ik to start
		self.ik_c.location = (0,0,0)
		self.ik_r.location = (0,0,0)
		self.ik_l.location = (0,0,0)
		
		# --- update driver affects
		bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)
		
		self.start_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		self.start_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])

		
		# R
		ctt = (((self.start_r[0] - up_r[0])**2 + (self.start_r[1] - up_r[1])**2 + (self.start_r[2] - up_r[2])**2)**0.5)/2
		self.up_r = 2 * (math.asin(ctt/self.eye_bone_r.length))
		
		# L
		ctt_l = (((self.start_l[0] - up_l[0])**2 + (self.start_l[1] - up_l[1])**2 + (self.start_l[2] - up_l[2])**2)**0.5)/2
		self.up_l = 2 * (math.asin(ctt_l/self.eye_bone_l.length))
		
		# apply paremetres
		if self.up_r:
			self.r_cns.max_x = self.up_r
		if self.up_l:
			self.l_cns.max_x = self.up_l

	
	def get_right_position(self):
		# get right position
		right_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		right_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])
		
		# get start position
		# --- ik to start
		self.ik_c.location = (0,0,0)
		self.ik_r.location = (0,0,0)
		self.ik_l.location = (0,0,0)
		
		# --- update driver affects
		bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)
		
		self.start_r = (self.eye_bone_r.vector[0], self.eye_bone_r.vector[1], self.eye_bone_r.vector[2])
		self.start_l = (self.eye_bone_l.vector[0], self.eye_bone_l.vector[1], self.eye_bone_l.vector[2])

		
		# R
		ctt = (((self.start_r[0] - right_r[0])**2 + (self.start_r[1] - right_r[1])**2 + (self.start_r[2] - right_r[2])**2)**0.5)/2
		self.right_r = 2 * (math.asin(ctt/self.eye_bone_r.length))
		
		# L
		ctt_l = (((self.start_l[0] - right_l[0])**2 + (self.start_l[1] - right_l[1])**2 + (self.start_l[2] - right_l[2])**2)**0.5)/2
		self.right_l = 2 * (math.asin(ctt_l/self.eye_bone_l.length))
		
		# apply parametres
		if self.right_r:
			self.r_cns.min_z = -self.right_r
			self.l_cns.max_z = self.right_r
		if self.right_l:
			self.l_cns.min_z = -self.right_l
			self.r_cns.max_z = self.right_l

		
	def apply_limits(self):
		'''
		if self.low_r:
			self.r_cns.min_x = -self.low_r
		if self.low_l:
			self.l_cns.min_x = -self.low_l
		if self.up_r:
			self.r_cns.max_x = self.up_r
		if self.up_l:
			self.l_cns.max_x = self.up_l
		if self.right_r:
			self.r_cns.min_z = -self.right_r
			self.l_cns.max_z = self.right_r
		if self.right_l:
			self.l_cns.min_z = -self.right_l
			self.r_cns.max_z = self.right_l
		'''
		self.r_cns.use_limit_x = True
		self.l_cns.use_limit_x = True
		self.r_cns.use_limit_z = True
		self.l_cns.use_limit_z = True
		
		#del(self)
