bl_info = {
    "name": "LiveLink",
    "author": "Viga Entertainment Technology",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > LiveLink",
    "description": "Live link setup between Blender and Unreal",
    "warning": "",
    "doc_url": "",
    "category": "LiveLink",
}

import bpy
import math
from socket import *

# Common functions

def MessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
#Static Mesh Panel
sub=[]
sub_names=[]
names=[]
def Sub_update(self,context):
        list=bpy.context.selected_objects
        global sub_names
        for obj in list:
                if obj.type== 'MESH':
                    sub.append((obj.name,obj.name,""))
                    sub_names.append(obj.name)
                   
                else:
                    return{'CANCELLED'}
          
def returnSub(self,context):
    res=[]
    global names
    for i in sub:
      if i not in res:
         res.append(i)
         
    for j in sub_names:
      if j not in names:
         names.append(j)
         
    return res

def removeSub(self,context):
    mytool = context.scene.my_tool2
    temp=mytool.my_string
    if(mytool.my_string!=""):
       a=(mytool.my_string,mytool.my_string,"")
       sub.remove(a)
       sub_names.remove(temp)
       names.remove(temp)
        
class AddSubjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.subjects_register"
    bl_label = "Add Subjects"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        Sub_update(self,context)
        return{'FINISHED'}
    
class RemoveSubjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.subjects_removal"
    bl_label = "Remove Subjects"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        removeSub(self,context)
        return{'FINISHED'}
    
class StaticProperties(bpy.types.PropertyGroup): 
    
    my_enum  : bpy.props.StringProperty(name="Mesh Type",default="O")
        
    my_enum2 : bpy.props.EnumProperty(
        name = "Control",
        description = "enum desc",
        items = [("SM","Single Mesh","")]
    )
    
    my_string : bpy.props.EnumProperty(
        name = "Subjects",
        description = "enum desc",
        items=returnSub,
        default=None
    )   

GetIconStatic="RADIOBUT_OFF"    
class LiveLinkStatic(bpy.types.Panel):
    #bl_parent_id = "BlenderUE LiveLink"
    bl_label = "Static Mesh"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"    
    bl_category  = "LiveLink"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        global GetIconStatic
        layout = self.layout
        scene = context.scene
        mytool  = scene.my_tool2
        col = layout.column(align=True)
        row = col.row(align=True)
        row=layout.row()
        row.label(text="IP Address : 127.0.0.1")
        row=layout.row()
        row.label(text="Port : 2000")

        layout.prop(mytool,"my_enum2")
        layout.prop(mytool,"my_string")
        row=layout.row()
        box=row.box()
        box.operator(AddSubjects.bl_idname, text="Add subjects",icon='ADD')
        #row=layout.row()
        box1=row.box()
        box1.operator(RemoveSubjects.bl_idname, text="Remove subject",icon='REMOVE')      
        row=layout.row()
        box2=row.box()
        box2.operator("wm.modal_timer_operator", text="Start Live Link",icon=GetIconStatic)
        row=layout.row()
        box3=row.box()
        box3.operator(StopLiveLink.bl_idname, text="Stop Live Link",icon='X')
        # row=layout.row()
        # row.prop(context.scene, prop_name)


cancelstatic=False

class StopLiveLink(bpy.types.Operator):
    bl_idname = "object.stop_livelink"
    bl_label = "Stop LiveLink"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        global cancelstatic
        cancelstatic=True
        return{'FINISHED'}
    
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    bl_options = {"UNDO"}
    host = "127.0.0.1" # set to IP address of target computer
    port = 2000
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM) 
    _timer = None      
    
    def modal(self, context, event):
        mytool = context.scene.my_tool2
        global GetIconStatic
        global cancelstatic
        if cancelstatic and mytool.my_string!="":
            GetIconStatic="RADIOBUT_OFF"
            self.cancel(context)
            cancelstatic=False
            return {'CANCELLED'}
        
        if event.type == 'TIMER':
            #bpy.data.objects["Cube"]
            if(mytool.my_string!=""):                    
                r=bpy.data.objects[mytool.my_string].rotation_euler
                rotx=math.degrees(r.x)
                roty=math.degrees(r.y)
                rotz=math.degrees(r.z)
                message = mytool.my_enum + "_"+mytool.my_string+"="
                message+="(" + str(-(bpy.data.objects[mytool.my_string].location.x*100)) + "," + str(bpy.data.objects[mytool.my_string].location.y*100) +  "," + str(bpy.data.objects[mytool.my_string].location.z*100) +  "," + str(-rotx) +  "," + str(roty)+  "," + str(-rotz) + "," +str(bpy.data.objects[mytool.my_string].scale.x)+ "," +str(bpy.data.objects[mytool.my_string].scale.y)+ "," +str(bpy.data.objects[mytool.my_string].scale.z)+ ")" + "||"
                GetIconStatic="RADIOBUT_ON"
                
            elif(mytool.my_enum=="O" and mytool.my_string==""):
                MessageBox("No static mesh selected","Subjects")
                GetIconStatic="RADIOBUT_OFF"
                self.cancel(context)
                return {'CANCELLED'}
            
            print(message)          
            self.UDPSock.sendto(message.encode(), self.addr)
            
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


#----------------------------------------------------------------------------------------------#
# For Skeletal Meshes

sub_Arm=[]
sub_names_Arm=[]
names_Arm=[]

#Add armature names to array
def Sub_update_Arm(self,context):
        list=bpy.context.selected_objects
        global sub_names_Arm
        for obj in list:
                if obj.type=='ARMATURE':
                    sub_Arm.append((obj.name,obj.name,""))
                    sub_names_Arm.append(obj.name)
                   
                else:
                    return{'CANCELLED'}
          
def returnSubArm(self,context):
    res=[]
    global names_Arm
    for i in sub_Arm:
      if i not in res:
         res.append(i)
         
    for j in sub_names_Arm:
      if j not in names_Arm:
         names_Arm.append(j)
    
    return res

def removeSubArm(self,context):
    mytool = context.scene.my_tool
    temp=mytool.my_string
    if(mytool.my_string!=""):
       a=(mytool.my_string,mytool.my_string,"")
       sub_Arm.remove(a)
       sub_names_Arm.remove(temp)
       names_Arm.remove(temp)

# Add subjects to UI
class AddSubjects_Skeletal(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.subjects_register_skeletal"
    bl_label = "Add Subjects"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(context.scene.my_tool.my_enum)
        Sub_update_Arm(self,context)
        return{'FINISHED'}
    
class RemoveSubjects_Skeletal(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.subjects_removal_skeletal"
    bl_label = "Remove Subjects"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        removeSubArm(self,context)
        return{'FINISHED'}

class SkeletalProperties(bpy.types.PropertyGroup): 
    
    my_enum  : bpy.props.StringProperty(name="Mesh Type",default="A")
    
    my_enum1 : bpy.props.EnumProperty(
        name = "Bone Type",
        description = "enum desc",
        items = [("||","Armature","")]
    )
    
    my_enum2 : bpy.props.EnumProperty(
        name = "Control",
        description = "enum desc",
        items = [("BC","Bone Control (Individual Animation)",""),
        ("AN","Simultaneous Animation","")]
    )
    
    my_string : bpy.props.EnumProperty(
        name = "Subjects",
        description = "enum desc",
        items=returnSubArm,
        default=None
    ) 

GetIcon="RADIOBUT_OFF"
class LiveLinkSkeletal(bpy.types.Panel):
    #bl_parent_id = "BlenderUE LiveLink"
    bl_label = "Skeletal Mesh"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"    
    bl_category  = "LiveLink"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        global GetIcon
        layout = self.layout
        scene = context.scene
        mytool  = scene.my_tool
        col = layout.column(align=True)
        row = col.row(align=True)
        row=layout.row()
        row.label(text="IP Address : 127.0.0.1")
        row=layout.row()
        row.label(text="Port : 2000")
        
        layout.prop(mytool,"my_enum1")
        layout.prop(mytool,"my_enum2")
        layout.prop(mytool,"my_string")
        row=layout.row()
        box=row.box()
        box.operator(AddSubjects_Skeletal.bl_idname, text="Add subjects",icon='ADD')
        #row=layout.row()
        box1=row.box()
        box1.operator(RemoveSubjects_Skeletal.bl_idname, text="Remove subject",icon='REMOVE')      
        row=layout.row()
        box2=row.box()
        box2.operator("wm.modal_timer_operator_skeletal", text="Start Live Link",icon=GetIcon)
        row=layout.row()
        box3=row.box()
        box3.operator(StopLiveLinkSkeletal.bl_idname, text="Stop Live Link",icon='X')
        # row=layout.row()
        # row.prop(context.scene, prop_name)
        
message1=""
class SkeletalMeshModalTimer(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator_skeletal"
    bl_label = "Modal Timer Operator Skeletal"
    bl_options = {"UNDO"}
    host = "127.0.0.1" # set to IP address of target computer
    port = 2000
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM) 
    _timer = None      
    
    def modal(self, context, event):
        mytool = context.scene.my_tool
        global GetIcon
        global cancel
        if cancel and mytool.my_string!="":
            GetIcon="RADIOBUT_OFF"
            self.cancel(context)
            cancel=False
            return {'CANCELLED'}
        
        if event.type == 'TIMER':
            #bpy.data.objects["Cube"]
            global message1
            if(mytool.my_enum2=="BC" and mytool.my_string!=""):                        
                count = 0
                GetIcon="RADIOBUT_ON"
                message1 = mytool.my_enum + "_"+mytool.my_string+"="
                for i in bpy.data.objects[mytool.my_string].pose.bones:
                    #if(count < 3):
                    #    count = count + 1
                    #else:
                    #    break
                    #boneEdit = bpy.data.armatures['root'].bones[i.name].matrix_local.to_quaternion()
                    obj = i.id_data
                    matrix_final = obj.matrix_world @ i.matrix
                    locationWS = i.location
                    quaternionWS =i.rotation_quaternion# matrix_final.to_quaternion()
                    #quaternionWS = i.rotation_quaternion * boneEdit
                    #print(quaternionWS)
                    #mixamo bone name conversion
                    bone_name=i.name
                    split_name=bone_name.split(":")[-1]
                    message1+=split_name + ":(" + "{:.9f}".format(locationWS.x)+ "," + "{:.9f}".format(-locationWS.y) +  "," + "{:.9f}".format(-locationWS.z) +  "," + "{:.9f}".format(-quaternionWS.x) +  "," + "{:.9f}".format(quaternionWS.y)+  "," + "{:.9f}".format(-quaternionWS.z)+ "," + "{:.9f}".format(quaternionWS.w)+ ")" + "|"
                message1 = message1 + "|"
            
            elif(mytool.my_enum2=="BC" and mytool.my_string==""):
                MessageBox("No subject selected","Subjects")
                GetIcon="RADIOBUT_OFF"
                self.cancel(context)
                return {'CANCELLED'}
            
            elif(mytool.my_enum2=="AN" and mytool.my_string!=""):
               GetIcon="RADIOBUT_ON"
               for j in names_Arm:
                  message1+=mytool.my_enum + "_"+j+"="
                  for i in bpy.data.objects[j].pose.bones:
                      obj = i.id_data
                      matrix_final = obj.matrix_world @ i.matrix
                      locationWS = i.location
                      quaternionWS =i.rotation_quaternion
                      #mixamo bone name conversion
                      bone_name=i.name
                      split_name=bone_name.split(":")[-1]
                      message1+=split_name + ":(" + "{:.9f}".format(locationWS.x)+ "," + "{:.9f}".format(-locationWS.y) +  "," + "{:.9f}".format(-locationWS.z) +  "," + "{:.9f}".format(-quaternionWS.x) +  "," + "{:.9f}".format(quaternionWS.y)+  "," + "{:.9f}".format(-quaternionWS.z)+ "," + "{:.9f}".format(quaternionWS.w)+ ")" + "|"
                  message1 = message1 + "|"
                  
            elif(mytool.my_enum2=="AN" and mytool.my_string==""):
                MessageBox("No skeletal mesh selected","Subjects")
                GetIcon="RADIOBUT_OFF"
                self.cancel(context)
                return {'CANCELLED'}
                      
            message=message1
            print(message)
            self.UDPSock.sendto(message.encode(), self.addr)
            message1=""
            
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

cancel=False
class StopLiveLinkSkeletal(bpy.types.Operator):
    bl_idname = "object.stop_livelink_skeletal"
    bl_label = "Stop LiveLink"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        global cancel
        cancel=True
        return{'FINISHED'}

classes = [AddSubjects,AddSubjects_Skeletal,RemoveSubjects,RemoveSubjects_Skeletal,SkeletalProperties,StaticProperties,LiveLinkStatic,LiveLinkSkeletal,ModalTimerOperator,SkeletalMeshModalTimer,StopLiveLink,StopLiveLinkSkeletal]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.my_tool2 = bpy.props.PointerProperty(type = StaticProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type = SkeletalProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.my_tool2


if __name__ == "__main__":
    register()

    # test call