import maya.cmds as cmd

if cmd.window("cnstWin", ex=True):
    cmd.deleteUI("cnstWin", window=True)
    
cmd.window("cnstWin", wh=(300,200), t="Constraining Tool", s=False)
cmd.columnLayout(adj=True)
cmd.textScrollList("conList", h=75, a=["Point Constrain", "Orient Constrain", "Parent Constrain", "Scale Constrain"])
cmd.checkBox("myBx", l="Maintain Offset")
cmd.button(l="Constrain", c="constrain()")
cmd.button(l="Remove",c="remove()")
cmd.showWindow("cnstWin")

def constrain():
    tsl_item = cmd.textScrollList("conList",q=True,si=True)
    
    if cmd.checkBox("myBx", q=True, v=True) == 1:
        if tsl_item[0] == "Parent Constrain":
            cmd.parentConstraint(mo=True)
    else:
        if tsl_item[0] == "Parent Constrain":
            cmd.parentConstraint()
            
    if cmd.checkBox("myBx", q=True, v=True) == 1:
        if tsl_item[0] == "Orient Constrain":
            cmd.orientConstraint(mo=True)
    else:
        if tsl_item[0] == "Orient Constain":
            cmd.orientConstraint()
            
    if cmd.checkBox("myBx", q=True, v=True) == 1:
        if tsl_item[0] == "Parent Constrain":
            cmd.parentConstraint(mo=True)
    else:
        if tsl_item[0] == "Parent Constrain":
            cmd.parentConstraint()
            
    if cmd.checkBox("myBx", q=True, v=True) == 1:
        if tsl_item[0] == "Scale Constain":
            cmd.scaleConstraint(mo=True)
    else:
        if tsl_item[0] == "Scale Constrain":
            cmd.scaleConstraint()
            
    
def remove():
    tsl_item = cmd.textScrollList("conList",q=True,si=True)
    
    if tsl_item[0] == "Parent Constrain":
        selCnsObj = cmd.ls(sl=True)
        getPrtCns = cmd.listRelatives(selCnsObj, type="parentConstraint")
        cmd.delete(getPrtCns)
        
    if tsl_item[0] == "Orient Constrain":
        selCnsObj = cmd.ls(sl=True)
        getOriCns = cmd.listRelatives(selCnsObj, type="orientConstraint")
        cmd.delete(getOriCns)
        
    if tsl_item[0] == "Point Constrain":
        selCnsObj = cmd.ls(sl=True)
        getPntCns = cmd.listRelatives(selCnsObj, type="pointConstraint")
        cmd.delete(getPntCns)
        
    if tsl_item[0] == "Scale Constrain":
        selCnsObj = cmd.ls(sl=True)
        getSclCns = cmd.listRelatives(selCnsObj, type="scaleConstraint")
        cmd.delete(getSclCns)
    