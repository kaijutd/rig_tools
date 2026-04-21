import maya.cmds as cmd

if cmd.window("mkJnt_win", ex=True):
    cmd.deleteUI("mkJnt_win", window=True)
    
cmd.window("mkJnt_win", t="Joint Generator", w=100, s=False)

cmd.columnLayout("c_layout", adj=True)
cmd.separator()
cmd.text("Joint(s) Defintion")
cmd.separator()
cmd.textFieldGrp("jntName", label="Name of Prefix:")
cmd.textFieldGrp("jntAmount", label="Amount of Joints:")
cmd.textFieldGrp("jntSpacing", label="Joint Spacing:")
cmd.separator()
cmd.text("Click Orientation to create")
cmd.separator()
cmd.button("b_xyz", label="XYZ", h=30, c="xyz()",p="c_layout")
cmd.button("b_zxy", label="ZXY", h=30, c="zxy()",p="c_layout")
cmd.button("b_yzx", label="YZX", h=30, c="yzx()",p="c_layout")
cmd.showWindow("mkJnt_win")

def xyz():
    jointName = cmd.textFieldGrp("jntName", q=True, tx=True)
    jointAmount = cmd.textFieldGrp("jntAmount", q=True, tx=True)
    jointSpacing = cmd.textFieldGrp("jntSpacing", q=True, tx=True)
    
    cmd.select(cl=True)
    
    if jointAmount == "1":
        jntSingle = cmd.joint(n=jointName)
        cmd.setAttr(jntSingle + ".jointOrientX", -90)
        cmd.setAttr(jntSingle + ".jointOrientY", 0)
        cmd.setAttr(jntSingle + ".jointOrientZ", 90)
    else:
        for x in range(int(jointAmount)):
            cmd.joint(n=(jointName + "_%i") % x)
            jntPos = (x*float(jointSpacing))
            cmd.move(0, jntPos, 0)
            
        cmd.joint((jointName+"_0"), edit=True, oj="xyz", secondaryAxisOrient="yup",ch=True)
        selLastJnt = cmd.ls(sl=True)
        cmd.setAttr(selLastJnt[0]+".jointOrientX", 0)
        cmd.setAttr(selLastJnt[0]+".jointOrientY", 0)
        cmd.setAttr(selLastJnt[0]+".jointOrientZ", 0)
        
        
def zxy():
    jointName = cmd.textFieldGrp("jntName", q=True, tx=True)
    jointAmount = cmd.textFieldGrp("jntAmount", q=True, tx=True)
    jointSpacing = cmd.textFieldGrp("jntSpacing", q=True, tx=True)
    
    cmd.select(cl=True)
    
    if jointAmount == "1":
        jntSingle = cmd.joint(n=jointName)
        cmd.setAttr(jntSingle + ".jointOrientX", -90)
        cmd.setAttr(jntSingle + ".jointOrientY", 0)
        cmd.setAttr(jntSingle + ".jointOrientZ", 0)
    else:
        for x in range(int(jointAmount)):
            cmd.joint(n=(jointName + "_%i") % x)
            jntPos = (x*float(jointSpacing))
            cmd.move(0, jntPos, 0)
            
        cmd.joint((jointName+"_0"), edit=True, oj="zxy", secondaryAxisOrient="yup",ch=True)
        selLastJnt = cmd.ls(sl=True)
        cmd.setAttr(selLastJnt[0]+".jointOrientX", 0)
        cmd.setAttr(selLastJnt[0]+".jointOrientY", 0)
        cmd.setAttr(selLastJnt[0]+".jointOrientZ", 0)


def yzx():
    jointName = cmd.textFieldGrp("jntName", q=True, tx=True)
    jointAmount = cmd.textFieldGrp("jntAmount", q=True, tx=True)
    jointSpacing = cmd.textFieldGrp("jntSpacing", q=True, tx=True)
    
    cmd.select(cl=True)
    
    if jointAmount == "1":
        jntSingle = cmd.joint(n=jointName)
        cmd.setAttr(jntSingle + ".jointOrientX", 0)
        cmd.setAttr(jntSingle + ".jointOrientY", 0)
        cmd.setAttr(jntSingle + ".jointOrientZ", 0)
    else:
        for x in range(int(jointAmount)):
            cmd.joint(n=(jointName + "_%i") % x)
            jntPos = (x*float(jointSpacing))
            cmd.move(0, jntPos, 0)
            
        cmd.joint((jointName+"_0"), edit=True, oj="yzx", secondaryAxisOrient="yup",ch=True)
        selLastJnt = cmd.ls(sl=True)
        cmd.setAttr(selLastJnt[0]+".jointOrientX", 0)
        cmd.setAttr(selLastJnt[0]+".jointOrientY", 0)
        cmd.setAttr(selLastJnt[0]+".jointOrientZ", 0)


