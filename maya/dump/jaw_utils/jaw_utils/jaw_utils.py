import maya.cmds as cmd

# name constants
GROUP = 'GRP'
JOINT = 'JNT'
GUIDE = 'GUIDE'
JAW = 'jaw'

#  side constans
LEFT = 'L'
RIGHT = 'R'
CENTER = 'C'

def build():
    """
    ACHTUNG HIER WIRD GEBAUT
    :return:
    """
    createHierarchy()
    createMinorJoints()
    createBroadJoints()
    createBaseJoints()
    constraintBroadJoints()
    createSeal('up')
    createSeal('low')
    createJawAttrs()
    createJawConstraints()
    defineJawValues('up')
    defineJawValues('low')
    createJawOffset()
    createSealAttrs()
    connectSeal('up')
    connectSeal('low')
    createCornerPin()

    print('Das ding ist erfolgreich gebaut')
    print('BUILT SUCCESFULLY')



def addOffset(destination, suffix='OFFSET'):
    """
    kopiert von arm_utils
    :return:
    """

    grp_offset = cmd.createNode('transform',name='{}_{}'.format(destination,suffix))
    dest_mat = cmd.xform(destination,q=True,m=True,ws=True)
    cmd.xform(grp_offset,m=dest_mat,ws=True)

    dest_parent = cmd.listRelatives(destination,parent=True)
    if dest_parent:
        cmd.parent(grp_offset, dest_parent)
    cmd.parent(destination,grp_offset)

    return grp_offset


def createGuides(number=3):
    """
    locator und gruppe erstellen evtl gruppen funktion
    :param number:
    :return:
    """
    jaw_guide_grp = cmd.createNode('transform',name='{}_{}_{}_{}'.format(CENTER,JAW,GUIDE,GROUP))
    loc_grp = cmd.createNode('transform',name='{}_{}_lip_{}_{}'.format(CENTER,JAW,GUIDE,GROUP), parent=jaw_guide_grp)
    lip_loc_grp = cmd.createNode('transform',name='{}_{}_lipMinor_{}_{}'.format(CENTER,JAW,GUIDE,GROUP), parent=loc_grp)

    for part in ['Up', 'Low']:

        part_mult = 1 if part == 'Up' else -1
        mid_data = (0,part_mult,0)

        mid_loc = cmd.spaceLocator(name='{}_{}{}_lip_{}'.format(CENTER,JAW,part,GUIDE))[0]
        cmd.parent(mid_loc,lip_loc_grp)

        for side in [LEFT,RIGHT]:
            for x in range(number):
                offsetMult = x+1 if side == LEFT else -(x+1)
                loc_data = (offsetMult, part_mult, 0)
                loc = cmd.spaceLocator(name='{}_{}{}_lip_{:02d}_{}'.format(side,JAW,part,x+1,GUIDE))[0]
                cmd.parent(loc, lip_loc_grp)
                #set loc data
                cmd.setAttr('{}.t'.format(loc), *loc_data)
        # set center data
        cmd.setAttr('{}.t'.format(mid_loc), *mid_data )

    # corners

    left_corner_loc = cmd.spaceLocator(name='{}_{}Corner_lip_{}'.format(LEFT,JAW,GUIDE))[0]
    right_corner_loc = cmd.spaceLocator(name='{}_{}Corner_lip_{}'.format(RIGHT,JAW,GUIDE))[0]
    cmd.parent(left_corner_loc, lip_loc_grp)
    cmd.parent(right_corner_loc, lip_loc_grp)

    cmd.setAttr('{}.t'.format(left_corner_loc),*(number+1,0,0))
    cmd.setAttr('{}.t'.format(right_corner_loc),*(-(number+1),0,0))

    cmd.select(cl=True)

    # base

    jaw_base_guide_grp = cmd.createNode('transform', name='{}_{}_base_{}_{}'.format(CENTER,JAW,GUIDE,GROUP), parent = jaw_guide_grp)
    jaw_guide = cmd.spaceLocator(name = '{}_{}_{}'.format(CENTER,JAW,GUIDE))[0]
    jaw_inverse_guide = cmd.spaceLocator(name = '{}_{}_inverse_{}'.format(CENTER,JAW,GUIDE))[0]

    cmd.setAttr('{}.t'.format(jaw_guide),*(0,-1,-number))
    cmd.setAttr('{}.t'.format(jaw_inverse_guide), *(0, 1, -number))

    cmd.parent(jaw_guide,jaw_base_guide_grp)
    cmd.parent(jaw_inverse_guide,jaw_base_guide_grp)

    cmd.select(cl=True)


def lip_guides():
    """
    lol
    :return:
    """
    grp = '{}_{}_lipMinor_{}_{}'.format(CENTER,JAW,GUIDE,GROUP)
    return [loc for loc in cmd.listRelatives(grp) if cmd.objExists(grp)]

def jaw_guides():
    """
    lol
    :return:
    """
    grp = '{}_{}_base_{}_{}'.format(CENTER,JAW,GUIDE,GROUP)
    return [loc for loc in cmd.listRelatives(grp) if cmd.objExists(grp)]



def createHierarchy():
    """
    grupperiung
    :return:
    """
    main_grp = cmd.createNode('transform', name='{}_{}_rig_{}'.format(CENTER,JAW,GROUP))
    lip_grp = cmd.createNode('transform', name='{}_{}_lip_{}'.format(CENTER,JAW,GROUP), parent=main_grp)
    base_grp = cmd.createNode('transform', name='{}_{}_base_{}'.format(CENTER,JAW,GROUP),parent=main_grp)

    lip_minor_grp = cmd.createNode('transform', name='{}_{}_lip_minor_{}'.format(CENTER,JAW,GROUP), parent=lip_grp)
    lip_broad_grp = cmd.createNode('transform', name='{}_{}_lip_broad_{}'.format(CENTER, JAW, GROUP), parent=lip_grp)

    cmd.select(cl=True)

def createMinorJoints():
    """
    joints erstellen
    :return:
    """

    minor_joints = list()

    for guide in lip_guides():
        mat = cmd.xform(guide,q=True,m=True,ws=True)
        jnt = cmd.joint(name=guide.replace(GUIDE,JOINT))
        cmd.setAttr('{}.radius'.format(jnt),0.5)
        cmd.xform(jnt, m=mat,ws=True)

        cmd.parent(jnt,'{}_{}_lip_minor_{}'.format(CENTER,JAW,GROUP))

        minor_joints.append(jnt)

    return minor_joints


def createBroadJoints():
    """
    controls in form von joints
    :return:
    """
    upper_joint = cmd.joint(name='{}_{}_broad_up_{}'.format(CENTER,JAW,JOINT))
    cmd.select(cl=True)
    lower_joint = cmd.joint(name='{}_{}_broad_low_{}'.format(CENTER,JAW,JOINT))
    cmd.select(cl=True)
    left_joint = cmd.joint(name='{}_{}_broad_corner_{}'.format(LEFT,JAW,JOINT))
    cmd.select(cl=True)
    right_joint = cmd.joint(name='{}_{}_broad_corner_{}'.format(RIGHT,JAW,JOINT))
    cmd.select(cl=True)

    cmd.parent([upper_joint,lower_joint,left_joint,right_joint],'{}_{}_lip_broad_{}'.format(CENTER, JAW, GROUP))

    upper_pos = cmd.xform('{}_{}Up_lip_{}'.format(CENTER,JAW,GUIDE),q=True,m=True,ws=True)
    lower_pos = cmd.xform('{}_{}Low_lip_{}'.format(CENTER,JAW,GUIDE),q=True,m=True,ws=True)
    left_pos = cmd.xform('{}_{}Corner_lip_{}'.format(LEFT,JAW,GUIDE),q=True,m=True,ws=True)
    right_pos = cmd.xform('{}_{}Corner_lip_{}'.format(RIGHT,JAW,GUIDE),q=True,m=True,ws=True)

    cmd.xform(upper_joint,m=upper_pos)
    cmd.xform(lower_joint,m=lower_pos)
    cmd.xform(left_joint,m=left_pos)
    cmd.xform(right_joint,m=right_pos)

    cmd.select(cl=True)


def createBaseJoints():
    """
    kiefer erstellen
    :return:
    """
    jaw_jnt = cmd.joint(name='{}_{}_{}'.format(CENTER,JAW,JOINT))
    jaw_inverse_jnt = cmd.joint(name='{}_inverse_{}_{}'.format(CENTER,JAW,JOINT))

    jaw_mat = cmd.xform(jaw_guides()[0],q=True,m=True,ws=True)
    jaw_inverse_mat = cmd.xform(jaw_guides()[1],q=True,m=True,ws=True)

    cmd.xform(jaw_jnt,m=jaw_mat,ws=True)
    cmd.xform(jaw_inverse_jnt,m=jaw_inverse_mat,ws=True)

    cmd.parent([jaw_jnt,jaw_inverse_jnt],'{}_{}_base_{}'.format(CENTER,JAW,GROUP))

    cmd.select(cl=True)

    addOffset(jaw_jnt,suffix='OFFSET')
    addOffset(jaw_inverse_jnt,suffix='OFFSET')

    addOffset(jaw_jnt,suffix='AUTO')
    addOffset(jaw_inverse_jnt,suffix='AUTO')

    cmd.select(cl=True)

def constraintBroadJoints():
    """
    constraints
    :return:
    """

    jaw_joint = '{}_{}_{}'.format(CENTER,JAW,JOINT)
    jaw_inverse_joint = '{}_inverse_{}_{}'.format(CENTER,JAW,JOINT)

    broad_upper = '{}_{}_broad_up_{}'.format(CENTER,JAW,JOINT)
    broad_lower = '{}_{}_broad_low_{}'.format(CENTER, JAW, JOINT)
    broad_left = '{}_{}_broad_corner_{}'.format(LEFT, JAW, JOINT)
    broad_right = '{}_{}_broad_corner_{}'.format(RIGHT, JAW, JOINT)

    upper_off = addOffset(broad_upper)
    lower_off = addOffset(broad_lower)
    left_off = addOffset(broad_left)
    right_off = addOffset(broad_right)

    cmd.parentConstraint(jaw_joint, lower_off,mo=True)
    cmd.parentConstraint(jaw_inverse_joint,upper_off,mo=True)

    cmd.parentConstraint(upper_off,lower_off,left_off,mo=True)
    cmd.parentConstraint(upper_off,lower_off, right_off,mo=True)

    cmd.select(cl=True)

def getPartsDict():
    """
    du bist ein genie
    :return:
    """
    upper_token = 'jawUp'
    lower_token = 'jawLow'
    corner_token = 'jawCorner'

    broad_upper = '{}_{}_broad_up_{}'.format(CENTER, JAW, JOINT)
    broad_lower = '{}_{}_broad_low_{}'.format(CENTER, JAW, JOINT)
    broad_left = '{}_{}_broad_corner_{}'.format(LEFT, JAW, JOINT)
    broad_right = '{}_{}_broad_corner_{}'.format(RIGHT, JAW, JOINT)

    lip_jnts = cmd.listRelatives('{}_{}_lip_{}'.format(CENTER,JAW,GROUP),allDescendents=True)

    lookup = {'C_up': {},'C_low': {},
              'L_up': {}, 'L_low': {},
              'R_up': {}, 'R_low': {},
              'L_corner': {}, 'R_corner': {}}

    for joint in lip_jnts:

        if cmd.objectType(joint) !='joint':
            continue

        if joint.startswith('C') and upper_token in joint:
            lookup['C_up'][joint] = [broad_upper]
        if joint.startswith('C') and lower_token in joint:
            lookup['C_low'][joint] = [broad_lower]

        if joint.startswith('L') and upper_token in joint:
            lookup['L_up'][joint] = [broad_upper,broad_left]
        if joint.startswith('L') and lower_token in joint:
            lookup['L_low'][joint] = [broad_lower, broad_left]

        if joint.startswith('R') and upper_token in joint:
            lookup['R_up'][joint] = [broad_upper,broad_right]
        if joint.startswith('R') and lower_token in joint:
            lookup['R_low'][joint] = [broad_lower, broad_right]

        if joint.startswith('L') and corner_token in joint:
            lookup['L_corner'][joint] = [broad_left]
        if joint.startswith('R') and corner_token in joint:
            lookup['R_corner'][joint] = [broad_right]

    return lookup

def getJointInOrder(part):
    """
    first try BITCH
    :param part: up, low , corner
    :return:
    """
    lip_parts = [reversed(sorted(getPartsDict()['L_{}'.format(part)].keys())),
                 getPartsDict()['C_{}'.format(part)].keys(),
                 sorted(getPartsDict()['R_{}'.format(part)].keys())]

    return [joint for joint in lip_parts for joint in joint]


def createSeal(part):
    """
    gruppen fuer den zip effekt
    :param part: up, low
    :return:
    """
    seal_name = '{}_seal_{}'.format(CENTER,GROUP)
    seal_parent = seal_name if cmd.objExists(seal_name) else cmd.createNode('transform',name=seal_name,parent='{}_{}_rig_{}'.format(CENTER,JAW,GROUP))

    part_grp = cmd.createNode('transform',name=seal_name.replace('seal','seal_{}'.format(part)),parent=seal_parent)

    l_corner = '{}_{}_broad_corner_{}'.format(LEFT,JAW,JOINT)
    r_corner = '{}_{}_broad_corner_{}'.format(RIGHT,JAW,JOINT)

    value = len(getJointInOrder(part))

    for index, joint in enumerate(getJointInOrder(part)):
        node = cmd.createNode('transform', name=joint.replace('JNT','{}_seal'.format(part)),parent = part_grp)
        jnt_mat = cmd.xform(joint, q=True, m=True,ws=True)
        cmd.xform(node,m=jnt_mat,ws=True)

        #parent oder anders?
        parConstraint = cmd.parentConstraint(l_corner,r_corner,node,mo=True)[0]
        cmd.setAttr('{}.interpType'.format(parConstraint),2)

        r_corner_value = float(index) / float(value - 1)
        l_corner_value = 1 - r_corner_value

        l_corner_attr = '{}.{}W0'.format(parConstraint,l_corner)
        r_corner_attr = '{}.{}W1'.format(parConstraint,r_corner)

        cmd.setAttr(l_corner_attr,l_corner_value)
        cmd.setAttr(r_corner_attr,r_corner_value)

    cmd.select(cl=True)



def createJawAttrs():
    """
    attribute auslagern fuer evtl editor sculpt spaeter

    :return:
    """

    node = cmd.createNode('transform', name='jaw_attributes', parent='{}_{}_rig_{}'.format(CENTER, JAW, GROUP))
    cmd.addAttr(node, ln=sorted(getPartsDict()['C_up'].keys())[0], min=0, max=1, dv=0)
    cmd.setAttr('{}.{}'.format(node, sorted(getPartsDict()['C_up'].keys())[0]), lock=1)

    for up in sorted(getPartsDict()['L_up'].keys()):
        cmd.addAttr(node, ln=up, min=0, max=1, dv=0)

    cmd.addAttr(node, ln=sorted(getPartsDict()['L_corner'].keys())[0], min=0, max=1, dv=1)
    cmd.setAttr('{}.{}'.format(node, sorted(getPartsDict()['L_corner'].keys())[0]), lock=1)

    for low in sorted(getPartsDict()['L_low'].keys()):
        cmd.addAttr(node, ln=low, min=0, max=1, dv=0)

    cmd.addAttr(node, ln=sorted(getPartsDict()['C_low'].keys())[0], min=0, max=1, dv=0)
    cmd.setAttr('{}.{}'.format(node, sorted(getPartsDict()['C_low'].keys())[0]), lock=1)

    for up in sorted(getPartsDict()['R_up'].keys()):
        cmd.addAttr(node, ln=up, min=0, max=1, dv=0)

    cmd.addAttr(node, ln=sorted(getPartsDict()['R_corner'].keys())[0], min=0, max=1, dv=1)
    cmd.setAttr('{}.{}'.format(node, sorted(getPartsDict()['R_corner'].keys())[0]), lock=1)

    for low in sorted(getPartsDict()['R_low'].keys()):
        cmd.addAttr(node, ln=low, min=0, max=1, dv=0)




def createJawConstraints():
    """
    constraints mit werten aus jawAttrs
    :return:
    """

    for value in getPartsDict().values():
        for lip_jnt, broad_jnt in value.items():
            seal_token = 'up_seal' if 'Up' in lip_jnt else 'low_seal'
            print(seal_token)
            lip_seal = lip_jnt.replace(JOINT, seal_token)

            if cmd.objExists(lip_seal):
                const = cmd.parentConstraint(broad_jnt,lip_seal,lip_jnt,mo=True)[0]
                cmd.setAttr('{}.interpType'.format(const,2))

                if len(broad_jnt)==1:
                    seal_attr = '{}_parentConstraint1.{}W1'.format(lip_jnt, lip_seal)
                    rev = cmd.createNode('reverse', name = lip_jnt.replace(JOINT, 'REV'))
                    cmd.connectAttr(seal_attr,'{}.inputX'.format(rev))
                    cmd.connectAttr('{}.outputX'.format(rev),'{}_parentConstraint1.{}W0'.format(lip_jnt,broad_jnt[0]))
                    cmd.setAttr(seal_attr,0)
                if len(broad_jnt)==2:
                    if lip_jnt.startswith('L'):
                        seal_attr = '{}_parentConstraint1.{}W2'.format(lip_jnt, lip_seal)
                        cmd.setAttr(seal_attr, 0)

                        seal_rev = cmd.createNode('reverse',name=lip_jnt.replace('JNT', 'seal_REV'))
                        jaw_attr_rev = cmd.createNode('reverse',name=lip_jnt.replace('JNT', 'jaw_attr_REV'))
                        seal_mult = cmd.createNode('multiplyDivide',name=lip_jnt.replace('JNT', 'seal_MULT'))

                        cmd.connectAttr(seal_attr,'{}.inputX'.format(seal_rev))
                        cmd.connectAttr('{}.outputX'.format(seal_rev),'{}.input2X'.format(seal_mult))
                        cmd.connectAttr('{}.outputX'.format(seal_rev),'{}.input2Y'.format(seal_mult))

                        cmd.connectAttr('jaw_attributes.{}'.format(lip_jnt.replace(lip_jnt[0],'L')),'{}.input1Y'.format(seal_mult))
                        cmd.connectAttr('jaw_attributes.{}'.format(lip_jnt.replace(lip_jnt[0],'L')),'{}.inputX'.format(jaw_attr_rev))
                        cmd.connectAttr('{}.outputX'.format(jaw_attr_rev),'{}.input1X'.format(seal_mult))

                        cmd.connectAttr('{}.outputX'.format(seal_mult),'{}_parentConstraint1.{}W0'.format(lip_jnt,broad_jnt[0]))
                        cmd.connectAttr('{}.outputY'.format(seal_mult),'{}_parentConstraint1.{}W1'.format(lip_jnt,broad_jnt[1]))
                    elif lip_jnt.startswith('R'):
                        seal_attr = '{}_parentConstraint1.{}W2'.format(lip_jnt, lip_seal)
                        cmd.setAttr(seal_attr, 0)

                        seal_rev = cmd.createNode('reverse', name=lip_jnt.replace('JNT', 'seal_REV'))
                        jaw_attr_rev = cmd.createNode('reverse', name=lip_jnt.replace('JNT', 'jaw_attr_REV'))
                        seal_mult = cmd.createNode('multiplyDivide', name=lip_jnt.replace('JNT', 'seal_MULT'))

                        cmd.connectAttr(seal_attr, '{}.inputX'.format(seal_rev))
                        cmd.connectAttr('{}.outputX'.format(seal_rev), '{}.input2X'.format(seal_mult))
                        cmd.connectAttr('{}.outputX'.format(seal_rev), '{}.input2Y'.format(seal_mult))

                        cmd.connectAttr('jaw_attributes.{}'.format(lip_jnt.replace(lip_jnt[0], 'R')),
                                        '{}.input1Y'.format(seal_mult))
                        cmd.connectAttr('jaw_attributes.{}'.format(lip_jnt.replace(lip_jnt[0], 'R')),
                                        '{}.inputX'.format(jaw_attr_rev))
                        cmd.connectAttr('{}.outputX'.format(jaw_attr_rev), '{}.input1X'.format(seal_mult))

                        cmd.connectAttr('{}.outputX'.format(seal_mult),
                                        '{}_parentConstraint1.{}W0'.format(lip_jnt, broad_jnt[0]))
                        cmd.connectAttr('{}.outputY'.format(seal_mult),
                                        '{}_parentConstraint1.{}W1'.format(lip_jnt, broad_jnt[1]))


            else:
                const = cmd.parentConstraint(broad_jnt, lip_jnt, mo=True)[0]
                cmd.setAttr('{}.interpType'.format(const, 2))

def defineJawValues(part, deg=1.3):
    """
    paar values einspeisen L und R gespiegelt
    :return:
    """
    jaw_attr = [att for att in getJointInOrder(part) if not att.startswith('C') and not att.startswith('R')]
    value = len(jaw_attr)

    for index, attr_name in enumerate(jaw_attr[::-1]):
        attrL = 'jaw_attributes.{}'.format(attr_name)
        attrR = 'jaw_attributes.{}'.format(attr_name).replace('L','R',1)
        linear_value = float (index)/ float(value-1)
        div_value = linear_value/deg
        final_value = div_value*linear_value
        cmd.setAttr(attrL,final_value)
        cmd.setAttr(attrR,final_value)

def createJawOffset():
    """
    offset und connection fuer unterkiefer bewegung
    :return:
    """
    jaw_attr = 'jaw_attributes'
    jaw_joint = '{}_{}_{}'.format(CENTER,JAW,JOINT)
    jaw_auto = '{}_{}_{}_AUTO'.format(CENTER,JAW,JOINT)


    cmd.addAttr(jaw_attr, ln='follow_ty',min=-10, max=10,dv=0)
    cmd.addAttr(jaw_attr, ln='follow_tz',min=-10, max=10,dv=0)

    unit = cmd.createNode('unitConversion',name='{}_{}_f_UNIT'.format(CENTER,JAW))

    remap_y = cmd.createNode('remapValue', name='{}_{}_Y_REMAP'.format(CENTER,JAW))
    cmd.setAttr('{}.inputMax'.format(remap_y),1)

    remap_z = cmd.createNode('remapValue', name='{}_{}_Z_REMAP'.format(CENTER, JAW))
    cmd.setAttr('{}.inputMax'.format(remap_z), 1)

    mult_y = cmd.createNode('multDoubleLinear',name='{}_{}_Y_MULT'.format(CENTER,JAW))
    cmd.setAttr('{}.input2'.format(mult_y), -1)

    cmd.connectAttr('{}.rx'.format(jaw_joint), '{}.input'.format(unit))
    cmd.connectAttr('{}.output'.format(unit),'{}.inputValue'.format(remap_y))
    cmd.connectAttr('{}.output'.format(unit),'{}.inputValue'.format(remap_z))

    cmd.connectAttr('{}.follow_ty'.format(jaw_attr),'{}.input1'.format(mult_y))
    cmd.connectAttr('{}.follow_tz'.format(jaw_attr),'{}.outputMax'.format(remap_z))
    cmd.connectAttr('{}.output'.format(mult_y),'{}.outputMax'.format(remap_y))

    cmd.connectAttr('{}.outValue'.format(remap_y),'{}.ty'.format(jaw_auto))
    cmd.connectAttr('{}.outValue'.format(remap_z),'{}.tz'.format(jaw_auto))

def createSealAttrs():
    """
    jaja
    :return:
    """
    seal_attr = 'jaw_attributes'

    cmd.addAttr(seal_attr,at='double', ln='L_seal',min=0,max=10,dv=0)
    cmd.addAttr(seal_attr,at='double', ln='R_seal',min=0,max=10,dv=0)

    cmd.addAttr(seal_attr,at='double', ln='L_seal_delay',min=0,max=10,dv=0)
    cmd.addAttr(seal_attr,at='double', ln='R_seal_delay',min=0,max=10,dv=0)


def connectSeal(part):
    """
    kb mehr einfach aus szene uebersetzen
    :param part:
    :return:
    """
    seal_token = 'seal_{}'.format(part)
    jaw_attrs = 'jaw_attributes'
    lip_jnts = getJointInOrder(part)
    value = len(lip_jnts)

    seal_driver = cmd.createNode('lightInfo',name='{}_{}_DRV'.format(CENTER,seal_token))
    triggers = {'L': list(), 'R': list()}

    for side in 'LR':
        delay_sub_name = '{}_{}_delay_SUB'.format(side,seal_token)
        delay_sub = cmd.createNode('plusMinusAverage',name=delay_sub_name)

        cmd.setAttr('{}.operation'.format(delay_sub),2)
        cmd.setAttr('{}.input1D[0]'.format(delay_sub),10)
        cmd.connectAttr('{}.{}_seal_delay'.format(jaw_attrs,side), '{}.input1D[1]'.format(delay_sub))

        lerp = 1/float(value-1)

        delay_div_name = '{}_{}_delay_DIV'.format(side,seal_token)
        delay_div = cmd.createNode('multDoubleLinear', name=delay_div_name)
        cmd.setAttr('{}.input2'.format(delay_div),lerp)
        cmd.connectAttr('{}.output1D'.format(delay_sub),'{}.input1'.format(delay_div))

        mult_triggers = list()
        sub_triggers = list()
        triggers[side].append(mult_triggers)
        triggers[side].append(sub_triggers)

        for index in range(value):
            print(index)
            index_name = 'jaw_{:02d}'.format(index)

            delay_mult_name = '{}_{}_{}_delay_MULT'.format(index_name,side,seal_token)
            delay_mult = cmd.createNode('multDoubleLinear', name=delay_mult_name)
            cmd.setAttr('{}.input1'.format(delay_mult),index)
            cmd.connectAttr('{}.output'.format(delay_div),'{}.input2'.format(delay_mult))

            mult_triggers.append(delay_mult)


            delay_sub_name = '{}_{}_{}_delay_SUB'.format(index_name, side,seal_token)
            delay_sub = cmd.createNode('plusMinusAverage', name = delay_sub_name)
            cmd.connectAttr('{}.output'.format(delay_mult), '{}.input1D[0]'.format(delay_sub))
            cmd.connectAttr('{}.{}_seal_delay'.format(jaw_attrs,side),'{}.input1D[1]'.format(delay_sub))

            sub_triggers.append(delay_sub)

    const_targets = list()

    for jnt in lip_jnts:
        attrs = cmd.listAttr('{}_parentConstraint1'.format(jnt),ud=True)

        for attr in attrs:
            print(attr)
            if 'seal' in attr:
                const_targets.append('{}_parentConstraint1.{}'.format(jnt,attr))


    for left_index, const_target in enumerate(const_targets):
        print('boink')
        right_index = value - left_index  - 1
        index_name = '{}_{}'.format(seal_token,left_index)

        l_mult_trigger, l_sub_trigger = triggers['L'][0][left_index], triggers['L'][1][left_index]
        r_mult_trigger, r_sub_trigger = triggers['R'][0][right_index], triggers['R'][1][right_index]

        l_remap_name = 'L_{}_{}_REMAP'.format(seal_token, index_name)
        l_remap = cmd.createNode('remapValue', name = l_remap_name)
        cmd.setAttr('{}.outputMax'.format(l_remap),1)
        cmd.setAttr('{}.value[0].value_Interp'.format(l_remap),2)
        cmd.connectAttr('{}.output'.format(l_mult_trigger), '{}.inputMin'.format(l_remap))
        cmd.connectAttr('{}.output1D'.format(l_sub_trigger),'{}.inputMax'.format(l_remap))

        cmd.connectAttr('{}.L_seal'.format(jaw_attrs),'{}.inputValue'.format(l_remap))

        r_sub_name = 'R_{}_offset_{}_SUB'.format(seal_token,index_name)
        r_sub = cmd.createNode('plusMinusAverage', name=r_sub_name)
        cmd.setAttr('{}.input1D[0]'.format(r_sub),1)
        cmd.setAttr('{}.operation'.format(r_sub),2)

        cmd.connectAttr('{}.outValue'.format(l_remap),'{}.input1D[1]'.format(r_sub))

        r_remap_name = 'R_{}_{}_REMAP'.format(seal_token, index_name)
        r_remap = cmd.createNode('remapValue', name = r_remap_name)
        cmd.setAttr('{}.outputMax'.format(r_remap),1)
        cmd.setAttr('{}.value[0].value_Interp'.format(r_remap),2)

        cmd.connectAttr('{}.output'.format(r_mult_trigger), '{}.inputMin'.format(r_remap))
        cmd.connectAttr('{}.output1D'.format(r_sub_trigger),'{}.inputMax'.format(r_remap))

        cmd.connectAttr('{}.R_seal'.format(jaw_attrs),'{}.inputValue'.format(r_remap))

        cmd.connectAttr('{}.output1D'.format(r_sub),'{}.outputMax'.format(r_remap))

        plus_name = '{}_SUM'.format(index_name)
        plus = cmd.createNode('plusMinusAverage', name=plus_name)

        cmd.connectAttr('{}.outValue'.format(l_remap),'{}.input1D[0]'.format(plus))
        cmd.connectAttr('{}.outValue'.format(r_remap),'{}.input1D[1]'.format(plus))

        clamp_name = '{}_CLAMP'.format(index_name)
        clamp = cmd.createNode('remapValue', name=clamp_name)
        cmd.connectAttr('{}.output1D'.format(plus),'{}.inputValue'.format(clamp))

        cmd.addAttr(seal_driver, at='double',ln=index_name,min=0,max=1,dv=0)
        cmd.connectAttr('{}.outValue'.format(clamp), '{}.{}'.format(seal_driver,index_name))

        cmd.connectAttr('{}.{}'.format(seal_driver,index_name),const_target)

def createCornerPin():
    """
    nach dem feedback mund ecken
    :return:
    """

    pin_driver = cmd.createNode('lightInfo',name='{}_pin_DRV'.format(CENTER))
    jaw_attr ='jaw_attributes'

    for side in 'LR':
        cmd.addAttr(jaw_attr,at='bool',ln='{}_auto_corner_pin'.format(side))
        cmd.addAttr(jaw_attr, at='double', ln='{}_corner_pin'.format(side),min=-10,max=10,dv=0)
        cmd.addAttr(jaw_attr, at='double', ln='{}_input_ty'.format(side),min=-10,max=10,dv=0)

        clamp = cmd.createNode('clamp',name='{}_corner_pin_auto_CLAMP'.format(side))
        cmd.setAttr('{}.minR'.format(clamp),-10)
        cmd.setAttr('{}.maxR'.format(clamp),10)

        cmd.connectAttr('{}.{}_input_ty'.format(jaw_attr,side),'{}.inputR'.format(clamp))
        cond = cmd.createNode('condition',name='{}_corner_pin_auto_COND'.format(side))
        cmd.setAttr('{}.operation'.format(cond),0)
        cmd.setAttr('{}.secondTerm'.format(cond),1)

        cmd.connectAttr('{}.{}_auto_corner_pin'.format(jaw_attr,side),'{}.firstTerm'.format(cond))
        cmd.connectAttr('{}.outputR'.format(clamp),'{}.colorIfTrueR'.format(cond))
        cmd.connectAttr('{}.{}_corner_pin'.format(jaw_attr,side),'{}.colorIfFalseR'.format(cond))

        plus = cmd.createNode('plusMinusAverage',name='{}_corner_pin_PLUS'.format(side))
        cmd.setAttr('{}.input1D[1]'.format(plus),10)
        cmd.connectAttr('{}.outColorR'.format(cond),'{}.input1D[0]'.format(plus))

        div = cmd.createNode('multDoubleLinear',name = '{}_corner_pin_DIV'.format(side))
        cmd.setAttr('{}.input2'.format(div),0.05)
        cmd.connectAttr('{}.output1D'.format(plus), '{}.input1'.format(div))

        cmd.addAttr(pin_driver,at='double', ln='{}_pin'.format(side),min=0,max=1,dv=0)
        cmd.connectAttr('{}.output'.format(div),'{}.{}_pin'.format(pin_driver,side))

        const_pin_up = '{}_jaw_broad_corner_JNT_OFFSET_parentConstraint1.C_jaw_broad_up_JNT_OFFSETW0'.format(side)
        const_pin_down = '{}_jaw_broad_corner_JNT_OFFSET_parentConstraint1.C_jaw_broad_low_JNT_OFFSETW1'.format(side)

        cmd.connectAttr('{}.{}_pin'.format(pin_driver,side),const_pin_up)
        rev = cmd.createNode('reverse', name='{}_corner_pin_REV'.format(side))
        cmd.connectAttr('{}.{}_pin'.format(pin_driver,side),'{}.inputX'.format(rev))
        cmd.connectAttr('{}.outputX'.format(rev),const_pin_down)



