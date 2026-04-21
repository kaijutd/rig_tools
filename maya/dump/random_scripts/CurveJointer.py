import maya.cmds as cmd

if (cmd.window('CurveJointer', exists=True)):
    cmd.deleteUI('CurveJointer')

cmd.window('CurveJointer')

cmd.rowColumnLayout(nc=2)

cmd.text('Joint Count', l='Bind Joint Count')
jntBindCount_field = cmd.intField(value=10)
cmd.text('Blend Shapes', l='Blend Shapes')
blendCount_field = cmd.intField(value=4)

l_tickBox = cmd.checkBox('l_tickBox', l='l side')
r_tickBox = cmd.checkBox('r_tickBox', l='r side')

cmd.button(l='Create', w=200, c='createJoints()')
cmd.button(l='Delete', w=200, c='deleteJoints()')
cmd.button(l='Color Controls', w=200, c='colorControls()')

cmd.showWindow()


######### FUNCTIONS  #########

def createJoints():
    print('create locs')
    sel = cmd.ls(selection=True)
    locList = []
    if (len(sel) > 1 or sel[0] == ""):
        print("PROBLEMOS")
        return
    else:
        print(sel)
    name = sel[0].split('_CRV')[0]

    ### bind joints

    if (cmd.objExists(name + '_bind_transform_GRP')):
        print('bind group already exists, delete first')
        return ()
    else:
        loc_grp = cmd.group(em=True, name=name + '_bind_transform_GRP')
    jntBindCount = cmd.intField(jntBindCount_field, query=True, value=True)

    for i in range(0, jntBindCount):
        lastLoc = cmd.spaceLocator(n=name + "_" + str(i) + '_LOC')
        cmd.parent(lastLoc, loc_grp)
        path = cmd.pathAnimation(sel[0], lastLoc, name=lastLoc[0] + "_motionPath", fm=True, f=True, fa='x', ua='y')
        # pathAnimation -fractionMode true -follow true -followAxis x -upAxis y -worldUpType "scene" -inverseUp false -inverseFront false -bank false -startTimeU `playbackOptions -query -minTime` -endTimeU  `playbackOptions -query -maxTime`;
        print(path)
        cmd.cutKey(path, attribute='uValue', option='keys')
        cmd.setAttr(path + '.uValue', i / (jntBindCount - 1))
        cmd.setAttr(lastLoc[0] + 'Shape.localScaleX', 0.1)
        cmd.setAttr(lastLoc[0] + 'Shape.localScaleY', 0.1)
        cmd.setAttr(lastLoc[0] + 'Shape.localScaleZ', 0.1)
        locList.append(lastLoc)

    print(locList)

    for i in range(0, len(locList)):
        cmd.select(locList[i])
        pos = cmd.xform(locList[i], q=True, t=True, ws=True)
        locJoint = cmd.joint(radius=0.1, p=pos, name=name + '_' + str(i) + '_offset_bind_JNT')
        bindJoint = cmd.joint(radius=0.1, p=pos, name=name + '_' + str(i) + '_bind_JNT')
        sphereMesh = cmd.sphere(radius=0.2, s=1, nsp=2, hr=1)

        sphereShape = cmd.listRelatives(sphereMesh, s=True)[0]

        cmd.parent(sphereShape, bindJoint, r=True, s=True)
        cmd.delete(sphereMesh)

    createBlendShapes(sel[0])


def createBlendShapes(crv):
    name = crv.split('_CRV')[0]

    if (cmd.objExists(name + '_blend_transform_GRP')):
        print('blend group already exists, delete first')
        return ()
    else:
        blend_grp = cmd.group(em=True, name=name + '_blend_transform_GRP')

    blendCount = cmd.intField(blendCount_field, query=True, value=True)

    for i in range(0, blendCount):
        lastBlend = cmd.duplicate(crv, n=name + '_' + str(i) + '_BLEND')
        cmd.parent(lastBlend, blend_grp)


def deleteJoints():
    print('delete locs')
    sel = cmd.ls(selection=True)

    if (len(sel) > 1 or sel[0] == ""):
        print("PROBLEMOS")
        return
    else:
        print(sel)
    name = sel[0].split('_CRV')[0]

    if (cmd.objExists(name + '_bind_transform_GRP')):
        grp = cmd.ls(name + '_bind_transform_GRP')
        cmd.delete(grp)
    if (cmd.objExists(name + '_blend_transform_GRP')):
        grp2 = cmd.ls(name + '_blend_transform_GRP')
        cmd.delete(grp2)


def colorControls():
    l_check = cmd.checkBox('l_tickBox', q=True, v=True)
    r_check = cmd.checkBox('r_tickBox', q=True, v=True)

    if l_check == False and r_check == False:
        b_check = False
        print('not both')
    if l_check == True and r_check == True:
        b_check = True
        print('both')
    if l_check == True and r_check == False:
        print('l check')
    if r_check == True and l_check == False:
        print('r check')

