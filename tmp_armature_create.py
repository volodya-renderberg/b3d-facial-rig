# create template of face rig
# 
# bones list
#
import bpy

class TMP_create:
	'''
	self.bones_list = [(name, head, tail, parent), ...] - deform bones
	self.bones_list = [(name, head, tail, parent), ...] - face panel bones
	self.bones_list = [(name, head, tail, parent), ...] - side panel bones
	
	self.create_bones(bpy.context) - create template bones of face rig, from self.bones_list
	
	'''
	
	def __init__(self):
		self.y = -0.7		
		
		self.bones_list = [
		('FRTMP_root', (0.0000, 0.0552, 1.0099), (0.0000, 0.0380, 1.1837), ''),
		('FRTMP_jaw', (0.0000, 0.0000, 1.1837), (0.0000, -0.1500, 1.0690), 'FRTMP_root'),
		('FRTMP_jaw_control', (0.5000, self.y, 1.017), (0.5000, self.y, 1.10), 'FRTMP_root'),
		#('FRTMP_vtx_grp_set', (0.0000, -0.1000, 1.00), (-0.0800, -0.1000, 1.10), 'FRTMP_root'),
		('FRTMP_eye_L', (0.0800, -0.0700, 1.3), (0.0800, -0.1500, 1.3), 'FRTMP_root'),
		('FRTMP_eye_R', (-0.0800, -0.0700, 1.3), (-0.0800, -0.1500, 1.3), 'FRTMP_root'),
		('FRTMP_tongue_base', (0.0000, -0.0300, 1.1837), (0.0000, -0.0700, 1.19), 'FRTMP_root'),
		('FRTMP_tongue_middle', (0.0000, -0.0700, 1.19), (0.0000, -0.1100, 1.19), 'FRTMP_tongue_base'),
		('FRTMP_tongue_end', (0.0000, -0.1100, 1.19), (0.0000, -0.1500, 1.1837), 'FRTMP_tongue_middle'),
		('FRTMP_ear_L', (0.1500, 0.038, 1.23), (0.1500, 0.038, 1.3), 'FRTMP_root'),
		('FRTMP_ear_R', (-0.1500, 0.038, 1.23), (-0.1500, 0.038, 1.3), 'FRTMP_root'),
		('FRTMP_upper_jaw', (0.00, -0.05, 1.21), (0.00, -0.15, 1.21), 'FRTMP_root'),
		('FRTMP_lower_jaw', (0.00, -0.05, 1.17), (0.00, -0.13, 1.12), 'FRTMP_root'),
		# vtx tmp bones
		('FRTMP_vtx_lip_grp_set', (0.0000, self.y/2, 1.00), (-0.0800, self.y/2, 1.10), 'FRTMP_root'),
		('FRTMP_vtx_brow_m_set', (-0.057, self.y/2, 1.283), (-0.075, self.y/2, 1.359), 'FRTMP_root'),
		('FRTMP_vtx_brow_in_set', (-0.057, self.y/2, 1.283), (-0.04, self.y/2, 1.356), 'FRTMP_root'),
		('FRTMP_vtx_brow_out_set', (-0.057, self.y/2, 1.283), (-0.109, self.y/2, 1.342), 'FRTMP_root'),
		('FRTMP_vtx_nose_set', (0.0, self.y/2, 1.145), (-0.043, self.y/2, 1.191), 'FRTMP_root'),
		]
		
		self.fp_bones_list = [
		('FRTMP_lip_M', (0.00, self.y, 1.14), (0.00, self.y, 1.174), 'FRTMP_root'),	
		('FRTMP_lip_R', (-0.080, self.y, 1.14), (-0.080, self.y, 1.174), 'FRTMP_root'),	
		('FRTMP_lip_L', (0.080, self.y, 1.14), (0.080, self.y, 1.174), 'FRTMP_root'),
		('FRTMP_lip_up_raise_R', (-0.050, self.y, 1.17), (-0.060, self.y, 1.20), 'FRTMP_root'),	
		('FRTMP_lip_up_raise_L', (0.050, self.y, 1.17), (0.060, self.y, 1.20), 'FRTMP_root'),
		('FRTMP_lip_low_depress_R', (-0.050, self.y, 1.13), (-0.060, self.y, 1.10), 'FRTMP_root'),
		('FRTMP_lip_low_depress_L', (0.050, self.y, 1.13), (0.060, self.y, 1.10), 'FRTMP_root'),
		('FRTMP_lip_up_roll_R', (-0.160, self.y, 1.15), (-0.160, self.y, 1.17), 'FRTMP_root'),
		('FRTMP_lip_up_roll_M', (-0.145, self.y, 1.15), (-0.145, self.y, 1.17), 'FRTMP_root'),
		('FRTMP_lip_up_roll_L', (-0.130, self.y, 1.15), (-0.130, self.y, 1.17), 'FRTMP_root'),
		('FRTMP_lip_low_roll_R', (-0.160, self.y, 1.12), (-0.160, self.y, 1.14), 'FRTMP_root'),
		('FRTMP_lip_low_roll_M', (-0.145, self.y, 1.12), (-0.145, self.y, 1.14), 'FRTMP_root'),
		('FRTMP_lip_low_roll_L', (-0.130, self.y, 1.12), (-0.130, self.y, 1.14), 'FRTMP_root'),
		('FRTMP_lips_pinch_R', (0.120, self.y, 1.130), (0.120, self.y, 1.150), 'FRTMP_root'),
		('FRTMP_lips_pinch_L', (0.135, self.y, 1.130), (0.135, self.y, 1.150), 'FRTMP_root'),
		#('FRTMP_lip_up_sqz_R', (-0.039, self.y, 1.2), (-0.033, self.y, 1.179), 'FRTMP_root'),
		#('FRTMP_lip_up_sqz_L', (0.039, self.y, 1.2), (0.033, self.y, 1.179), 'FRTMP_root'),
		#('FRTMP_lip_low_sqz_R', (-0.039, self.y, 1.102), (-0.033, self.y, 1.123), 'FRTMP_root'),
		#('FRTMP_lip_low_sqz_L', (0.039, self.y, 1.102), (0.033, self.y, 1.123), 'FRTMP_root'),
		('FRTMP_nose_R', (-0.033, self.y, 1.215), (-0.022, self.y, 1.250), 'FRTMP_root'),
		('FRTMP_nose_L', (0.033, self.y, 1.215), (0.022, self.y, 1.250), 'FRTMP_root'),
		('FRTMP_cheek_R', (-0.092, self.y, 1.222), (-0.082, self.y, 1.264), 'FRTMP_root'),
		('FRTMP_cheek_L', (0.092, self.y, 1.222), (0.082, self.y, 1.264), 'FRTMP_root'),
		('FRTMP_brow_out_R', (-0.078, self.y, 1.324), (-0.078, self.y, 1.344), 'FRTMP_root'),
		('FRTMP_brow_mid_R', (-0.063, self.y, 1.324), (-0.063, self.y, 1.344), 'FRTMP_root'),
		('FRTMP_brow_in_R', (-0.048, self.y, 1.324), (-0.048, self.y, 1.344), 'FRTMP_root'),
		('FRTMP_brow_out_L', (0.078, self.y, 1.324), (0.078, self.y, 1.344), 'FRTMP_root'),
		('FRTMP_brow_mid_L', (0.063, self.y, 1.324), (0.063, self.y, 1.344), 'FRTMP_root'),
		('FRTMP_brow_in_L', (0.048, self.y, 1.324), (0.048, self.y, 1.344), 'FRTMP_root'),
		('FRTMP_brow_gather_R', (-0.069, self.y, 1.357), (-0.048, self.y, 1.357), 'FRTMP_root'),
		('FRTMP_brow_gather_L', (0.069, self.y, 1.357), (0.048, self.y, 1.357), 'FRTMP_root'),
		('FRTMP_blink_R', (-0.161, self.y, 1.26), (-0.161, self.y, 1.305), 'FRTMP_root'),
		('FRTMP_blink_L', (0.161, self.y, 1.26), (0.161, self.y, 1.305), 'FRTMP_root'),
		('FRTMP_pupil_R', (0.21, self.y, 1.271), (0.21, self.y, 1.291), 'FRTMP_root'),
		('FRTMP_pupil_L', (0.225, self.y, 1.271), (0.225, self.y, 1.291), 'FRTMP_root'),
		('FRTMP_eye_global_R', (-0.08, self.y, 1.284), (-0.08, self.y, 1.315), 'FRTMP_root'),
		('FRTMP_eye_global_L', (0.08, self.y, 1.284), (0.08, self.y, 1.315), 'FRTMP_root'),
		]
		
		self.sp_bones_list = [
		('FRTMP_lips', (0.499, self.y, 1.12), (0.499, self.y, 1.194), 'FRTMP_root'),
		('FRTMP_cheeks', (0.367, self.y, 1.12), (0.367, self.y, 1.194), 'FRTMP_root'),
		('FRTMP_jaw_back_fwd', (0.389, self.y, 1.025), (0.389, self.y, 1.099), 'FRTMP_root'),
		('FRTMP_funnel', (0.325, self.y, 1.025), (0.325, self.y, 1.099), 'FRTMP_root'),
		('FRTMP_lip_up_raise', (0.707, self.y, 1.12), (0.707, self.y, 1.194), 'FRTMP_root'),
		('FRTMP_lip_low_depress', (0.747, self.y, 1.194), (0.747, self.y, 1.12), 'FRTMP_root'),
		('FRTMP_nose', (0.635, self.y, 1.12), (0.635, self.y, 1.194), 'FRTMP_root'),
		#('FRTMP_lip_up_sqz', (0.72, self.y, 1.194), (0.72, self.y, 1.158), 'FRTMP_root'),
		#('FRTMP_lip_low_sqz', (0.72, self.y, 1.111), (0.72, self.y, 1.144), 'FRTMP_root'),
		('FRTMP_lips_pinch', (0.707, self.y, 1.023), (0.707, self.y, 1.085), 'FRTMP_root'),
		('FRTMP_lips_close', (0.747, self.y, 1.023), (0.747, self.y, 1.085), 'FRTMP_root'),
		('FRTMP_lip_up_roll', (0.592, self.y, 1.075), (0.676, self.y, 1.075), 'FRTMP_root'),
		('FRTMP_lip_low_roll', (0.592, self.y, 1.031), (0.676, self.y, 1.031), 'FRTMP_root'),
		]
		
		self.all_bones = [
		self.bones_list,
		self.fp_bones_list,
		self.sp_bones_list
		]
		
		self.armature_name = 'face_rig_tmp'
		
	def test_exists(self, context):
		scene = bpy.context.scene
		try:
			obj = bpy.data.objects[self.armature_name]
		except:
			return(False)
		else:
			return(True)
		
	def create_bones(self, context):
		pass
		# --------- Create Armature --------------
		scene = bpy.context.scene
		try:
			obj = bpy.data.objects[self.armature_name]
		except:
			arm = bpy.data.armatures.new(self.armature_name)
			obj = bpy.data.objects.new(self.armature_name, arm)
			#obj.draw_type = 'WIRE'
			scene.objects.link(obj)
		else:
			# to edit mode
			scene.objects.active = obj
			bpy.ops.object.mode_set(mode='EDIT')
			
			# get position data
			arm = bpy.data.armatures[self.armature_name]
			new_all_bones = []
			for bones_list in self.all_bones:
				new_bones_list = []
				for key in bones_list:
					if not key[0] in arm.edit_bones:
						new_bones_list.append(key)
						continue
					bone = arm.edit_bones[key[0]]
					new_key = (key[0], tuple(bone.head), tuple(bone.tail), key[3])
					new_bones_list.append(new_key)
				new_all_bones.append(new_bones_list)
			self.all_bones = new_all_bones
			
			#remove bones
			for bone in arm.edit_bones:
				arm.edit_bones.remove(bone)
			
			'''
			# remove armature
			scene.objects.active = obj
			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.data.objects.remove(obj, do_unlink=True)
			bpy.data.armatures.remove(arm, do_unlink=True)

			# create armature
			arm = bpy.data.armatures.new(self.armature_name)
			obj = bpy.data.objects.new(self.armature_name, arm)
			#obj.draw_type = 'WIRE'
			scene.objects.link(obj)
			'''
		
		scene.objects.active = obj
		bpy.ops.object.mode_set(mode='EDIT')
		
		# ----------- Create joints ----------------
		for bones_list in self.all_bones:
			for key in bones_list:
				bone = arm.edit_bones.new(key[0])
				bone.head = key[1]
				bone.tail = key[2]
				bone.roll = 0.0000
				if key[0] == 'FRTMP_tongue_middle' or key[0] == 'FRTMP_tongue_end':
					bone.use_connect = True
				else:
					bone.use_connect = False
				if key[3] != '':
					bone.parent = arm.edit_bones[key[3]]
		
		# ------- fin ----------
		return True, ('****** face rig tmp created')
			
def register():
    pass
	
def unregister():
    pass