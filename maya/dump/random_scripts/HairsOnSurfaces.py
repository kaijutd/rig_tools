import maya.cmds as cmd

if (cmd.window('HairJointsOnNurbs', exists=True)):
    cmd.deleteUI('HairJointsOnNurbs')

cmd.window('HairJointsOnNurbs')

cmd.rowColumnLayout(nc=2)

cmd.text('U Value', l='U Value')
u_field = cmd.intField(value=1)
cmd.text('V Value', l='V Value')
v_field = cmd.intField(value=5)
# cmd.text('Move Joints', l = 'Move Joints')
# m_field = cmd.intField(value = 3)
cmd.button(l='Create', w=200, c='createJoints()')
cmd.button(l='Delete', w=200, c='deleteJoints()')

cmd.showWindow()


def createJoints():
    print('CREATING')
    sel = cmd.ls(selection=True)

    if (len(sel) > 1 or sel[0] == ""):
        print("PROBLEMOS")
        return
    else:
        print(sel)
    name = sel[0].split('_NURBS')[0]
    if (cmd.objExists(name + '_hairs_transform_GRP')):
        print('hairs already exist, delete first')
        return ()
    else:
        hair_grp = cmd.group(em=True, name=name + '_hairs_transform_GRP')
        move_grp = cmd.group(em=True, name=name + '_move_jnt_transform_GRP')
        cmd.parent(move_grp, hair_grp)

    u_value = cmd.intField(u_field, q=True, v=True)
    v_value = cmd.intField(v_field, q=True, v=True)

    createFollicle(sel[0], u_value, v_value, hair_grp, move_grp)


def createFollicle(sel, u, v, hair_grp, move_grp):
    print(' CREATING FOR ' + sel)
    pName = sel + '_Follicle'
    foll_grp = cmd.group(em=True, name=pName + '_GRP')
    cmd.parent(foll_grp, hair_grp)
    nurb = cmd.listRelatives(sel, shapes=True)[0]

    for i in range(0, u):
        for x in range(0, v + 1):
            foll = cmd.createNode('follicle', name=pName + '_SHP' + str(x + 1))
            follParent = cmd.listRelatives(foll, p=True)[0]

            cmd.parent(follParent, foll_grp)
            cmd.setAttr(foll + '.simulationMethod', 0)
            cmd.makeIdentity(nurb, apply=True, t=1, r=1, s=1, n=0)

            cmd.connectAttr(foll + '.outRotate', follParent + '.rotate', f=True)
            cmd.connectAttr(foll + '.outTranslate', follParent + '.translate')
            cmd.connectAttr(nurb + '.worldMatrix', foll + '.inputWorldMatrix')
            cmd.connectAttr(nurb + '.local', foll + '.inputSurface')

            cmd.setAttr(foll + '.parameterV', x / v)
            if (u == 1):
                cmd.setAttr(foll + '.parameterU', 0.5)
            else:
                cmd.setAttr(foll + '.parameterU', i / u)

            pos = cmd.xform(follParent, q=True, t=True, ws=True)
            follJoint = cmd.joint(radius=0.1, p=pos, name=pName + '_U' + str(i + 1) + '_V' + str(x) + '_bind_JNT')

            moveJoint = cmd.joint(radius=0.2, p=pos, name=pName + '_U' + str(i + 1) + '_V' + str(x) + '_move_JNT')

            cmd.parent(moveJoint, move_grp)
            cmd.rename(follParent, pName)


def deleteJoints():
    print('DELETING')
    sel = cmd.ls(selection=True)
    name = sel[0].split('_NURBS')[0]
    if (cmd.objExists(name + '_hairs_transform_GRP')):
        cmd.delete(name + '_hairs_transform_GRP')

