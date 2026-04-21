import maya.cmds as cmd

if (cmd.window('My Rigging Interface', exists=True)):
    cmd.deleteUI('My Rigging Interface')

cmd.window('Lol my tools',w=400)
tabs = cmd.tabLayout()
skelTab = cmd.rowColumnLayout(nc=1)
cmd.separator()
cmd.text("Create and Adjust Locators")
cmd.separator()

cmd.text('Spine Count', l = 'Spine Count')
spineCount_field = cmd.intField(minValue = 1, maxValue = 9, value = 4)
cmd.text('Fingers Amount', l = 'Fingers Amount')
fingerCount_field = cmd.intField(minValue = 0, maxValue = 9, value = 4)

cmd.button(l = 'Create Locators', w = 200,h=50, c = 'createLocators()')
cmd.button(l = 'Delete Locators', w = 100,h=25, c = 'deleteLocators()')

cmd.button(l = 'Mirror [L->R]', w = 100, c = 'mirrorLocators(1)')
cmd.button(l = 'Mirror [R->L]', w = 100, c = 'mirrorLocators(-1)')

cmd.separator()
cmd.text("Create and Adjust Joints")
cmd.separator()

cmd.button(l = 'Create Joints', w = 200,h=50, c = 'createJoints()')
cmd.button(l = 'Delete Joints', w = 100,h=25, c = 'deleteJoints()')

editMode = True

cmd.button(l = "Edit Mode", w = 100, c = 'lockLocators(editMode)')
cmd.button(l = "Create IK/FK Joints", w = 100, c = 'createIKFKJoints()')

#cmd.button(l="Rename",w=100,c='renameNamespace()')

cmd.setParent('..')

ctrlTab = cmd.rowColumnLayout(nc = 4,columnWidth=[(1,100),(2,100),(3,100),(4,100)])

cmd.text("CONTROLS")
cmd.separator(height=50,style='doubleDash')
cmd.separator(height=50,style='doubleDash')
cmd.separator(height=50,style='doubleDash')
cmd.textFieldGrp("ctrlName", label="Name of Ctrl:",w=400)
cmd.separator(style='single')
cmd.separator(style='single')
cmd.separator(style='single')

cmd.button(l = "Circle", w = 50, h=50, c = 'createControl("Circle")')
cmd.button(l = "Square", w = 50, h=50, c = 'createControl("Square")')
cmd.button(l = "Arrow", w = 50, h=50, c = 'createControl("Arrow")')
cmd.button(l = "QuadArrow", w = 50, h=50, c = 'createControl("QuadArrow")')
cmd.button(l = "Star", w = 50, h=50, c = 'createControl("Star")')
cmd.button(l = "X", w = 50, h=50, c = 'createControl("X")')
cmd.button(l = "Cog", w = 50, h=50, c = 'createControl("Cog")')
cmd.button(l = "Line", w = 50, h=50, c = 'createControl("Line")')
crvCount_field = cmd.intField(value = 4)
cmd.button(l = "CRV", w = 50, h=50, c = 'createControl("CRV")')

cmd.separator()
cmd.separator()
cmd.separator()
cmd.separator()
cmd.separator()
cmd.separator()

currentCtrlColor = 'Yellow'

cmd.button(l = "Recolor", c = 'recolorCTRLs()')
colorPicker = cmd.optionMenu (l = 'Colors')
cmd.menuItem (l = 'Yellow')
cmd.menuItem (l = 'Blue')
cmd.menuItem (l = 'Red')


cmd.button (l = "Create T-GRP", c = 'createTransformGRP()')
cmd.button(l = "Allign", c = 'allignTransformGRP()')
cmd.setParent('..')


toolTab = cmd.rowColumnLayout(nc = 2, columnWidth=[(1,200),(2,200)])
cmd.text("Tools")
cmd.separator()
cmd.text("Joints on Nurbs")
cmd.separator()

cmd.textFieldGrp('nurbName',label = 'Name of Nurb',w=400)
cmd.separator()

cmd.text('U Value', l = 'U Value')
u_field = cmd.intField(value = 1)
cmd.text('V Value', l = 'V Value')
v_field = cmd.intField(value = 5)
cmd.button(l = 'Create NURBS Surfae', c = 'createNurbsSurface()')
cmd.button(l = 'Delete NURBS Surface', c = 'deleteNurbsSurface()')
cmd.button(l = 'Create Joints on Nurb', c = 'createNurbsJoints()')
cmd.button(l = 'Delete Joints on Nurb', c = 'deleteNurbsJoints()')

cmd.separator()

cmd.separator()


cmd.text('Blend Shape Creator')
cmd.separator()

cmd.text('Joint Count',l = 'Bind Joint Count')
jntBindCount_field = cmd.intField(value=5)
cmd.text('Blend Shapes',l='Amount if Blend Shapes')
blendCount_field = cmd.intField(value=4)
l_tickBox = cmd.checkBox('l_tickBox', l = 'l_side')
r_tickBox = cmd.checkBox('r_tickBox', l='r_side')


cmd.button(l='Create',w=100,c='createBlendJoints()')
cmd.button(l = 'Delete',w=100, c='deleteBlendJoints()')


firstColor = False

cmd.setParent('..')


cmd.tabLayout(tabs, edit = True, tabLabel = ([skelTab, 'Skeleton'], [ctrlTab, 'Controls'],[toolTab, 'Tools']))


cmd.showWindow()

editMode = True



######### FUNCTIONS  #########




def createLocators():
    print ('create locs')
    if(cmd.objExists('master_loc_transform_GRP')):
        print ('master locator group already exists, delete first')
        return()
    else:
        master_grp = cmd.group(em = True, name = 'master_loc_transform_GRP')

    root = cmd.spaceLocator(n = 'ROOT_LOC')
    cmd.scale(0.1,0.1,0.1, root)
    cmd.move(0,1,0,root)
    cmd.parent(root, master_grp)

    createSpine()

    lockLocators(editMode)

def createSpine():
    spineCount = cmd.intField(spineCount_field, query = True, value = True)
    for i in range(0, spineCount):
        spine = cmd.spaceLocator(n = 'spine_' + str(i) + '_LOC')
        cmd.scale(0.1,0.1,0.1, spine)
        if i == 0:
            cmd.parent(spine, 'ROOT_LOC')
        else:
            cmd.parent(spine,'spine_' + str(i-1) + '_LOC')
        cmd.move(0, 1.25 + (0.25 * i),0,spine)
        if i == spineCount-1:
            createHead(spine)
    createArms(1, spineCount)
    createArms(-1, spineCount)
    createLegs(1, spineCount)
    createLegs(-1, spineCount)


def createArms(side, spineCount):
    if side == 1: # left
        if cmd.objExists('l_arm_loc_transform_GRP'):
            print ('Left Arm already exists')
        else:
            arm = cmd.group(em = True, name='l_arm_loc_transform_GRP')
            cmd.parent(arm,'spine_' + str(spineCount-1) + '_LOC')
#shoulder
            shoulder = cmd.spaceLocator( n = 'l_arm_shoulder_LOC')
            cmd.parent(shoulder, arm)
#elbow
            elbow = cmd.spaceLocator( n = 'l_arm_elbow_LOC')
            cmd.parent(elbow,shoulder)
            cmd.move(0.6*side,-3,-0.5,elbow)
#wrist
            wrist = cmd.spaceLocator( n = 'l_arm_wrist_LOC')
            cmd.parent(wrist,elbow)
            cmd.move(0.8*side,-6,0,wrist)
#move and scale
            cmd.move(0.35 * side, 1 + (0.25*spineCount), 0, arm)

            cmd.scale(1,1,1,arm)

            createHand(side,wrist)

    else: #right
        if cmd.objExists('r_arm_loc_transform_GRP'):
            print ('Right Arm already exists')
        else:
            arm = cmd.group(em = True, name='r_arm_loc_transform_GRP')
            cmd.parent(arm,'spine_' + str(spineCount-1) + '_LOC')
#shoulder
            shoulder = cmd.spaceLocator( n = 'r_arm_shoulder_LOC')
            cmd.parent(shoulder, arm)
#elbow
            elbow = cmd.spaceLocator( n = 'r_arm_elbow_LOC')
            cmd.parent(elbow,shoulder)
            cmd.move(0.6*side,-3,-0.5,elbow)
#wrist
            wrist = cmd.spaceLocator( n = 'r_arm_wrist_LOC')
            cmd.parent(wrist,elbow)
            cmd.move(0.8*side,-6,0,wrist)
#move and scale
            cmd.move(0.35 * side, 1 + (0.25*spineCount), 0, arm)

            cmd.scale(1,1,1,arm)

            createHand(side,wrist)

def createLegs(side, spineCount):
    if side == 1: # left
        if cmd.objExists('l_leg_loc_transform_GRP'):
            print ('Left Leg already exists')
        else:
            leg = cmd.group(em = True, name='l_leg_loc_transform_GRP')
            cmd.parent(leg,'spine_' + str(0) + '_LOC')
#hip
            hip = cmd.spaceLocator( n = 'l_leg_hip_LOC')
            cmd.parent(hip, leg)
#knee
            knee = cmd.spaceLocator( n = 'l_leg_knee_LOC')
            cmd.parent(knee, hip)
            cmd.move(0,-4,0.5,knee)
#ankle
            ankle = cmd.spaceLocator( n = 'l_leg_ankle_LOC')
            cmd.parent(ankle, knee)
            cmd.move(0,-8,0,ankle)
#move and scale
            cmd.move(0.35 * side, 2 - (0.25*spineCount), 0, leg)

            cmd.scale(1,1,1,leg)
            createFoot(side,ankle)


    else: #right
        if cmd.objExists('r_leg_loc_transform_GRP'):
            print ('Right Leg already exists')
        else:
            leg = cmd.group(em = True, name='r_leg_loc_transform_GRP')
            cmd.parent(leg,'spine_' + str(0) + '_LOC')
#hip
            hip = cmd.spaceLocator( n = 'r_leg_hip_LOC')
            cmd.parent(hip, leg)
#knee
            knee = cmd.spaceLocator( n = 'r_leg_knee_LOC')
            cmd.parent(knee, hip)
            cmd.move(0,-4,0.5,knee)
#ankle
            ankle = cmd.spaceLocator( n = 'r_leg_ankle_LOC')
            cmd.parent(ankle, knee)
            cmd.move(0,-8,0,ankle)
#move and scale
            cmd.move(0.35 * side, 2 - (0.25*spineCount), 0, leg)

            cmd.scale(1,1,1,leg)
            createFoot(side,ankle)


def createFoot(side, ankle):
    if side == 1:
        if cmd.objExists('l_foot_loc_transform_GRP'):
            print('Left Foot already exists')
        else:
            foot = cmd.group(em = True, name = 'l_foot_loc_transform_GRP')
            cmd.parent(foot, ankle)
        #middle
            middle = cmd.spaceLocator(n = 'l_foot_middle_LOC')
            cmd.parent(middle, foot)
            cmd.move(0,-1,1,middle)
        #toe
            toe = cmd.spaceLocator(n = 'l_foot_toe_LOC')
            cmd.parent(toe, middle)
            cmd.move(0,-1.25,2,toe)
#move and scale
            cmd.matchTransform(foot,ankle)
            cmd.scale(1,1,1,foot)

    else:
        if cmd.objExists('r_foot_loc_transform_GRP'):
            print('Right Foot already exists')
        else:
            foot = cmd.group(em = True, name = 'r_foot_loc_transform_GRP')
            cmd.parent(foot, ankle)

        #middle
            middle = cmd.spaceLocator(n = 'r_foot_middle_LOC')
            cmd.parent(middle, foot)
            cmd.move(0,-1,1,middle)
        #toe
            toe = cmd.spaceLocator(n = 'r_foot_toe_LOC')
            cmd.parent(toe, middle)
            cmd.move(0,-1.25,2,toe)
#move and scale
            cmd.matchTransform(foot,ankle)
            cmd.scale(1,1,1,foot)

def createHand(side, wrist):
    fingerCount = cmd.intField(fingerCount_field, query = True, value = True)

    if side == 1:
        if cmd.objExists('l_hand_loc_transform_GRP'):
            print('Left Hand already exists')
        else:
            hand = cmd.group(em = True, name = 'l_hand_loc_transform_GRP')
            cmd.parent(hand, wrist)
            for i in range(0,fingerCount):


    #metaCarpal
                metaCarpal = cmd.spaceLocator(n = 'l_hand_metaCarpal_AJA_'+str(i)+'_LOC')
                cmd.parent(metaCarpal, hand)
                cmd.move(0,-1,0.25-0.25*i,metaCarpal)
    #phalanxAJA
                phalanxA = cmd.spaceLocator(n = 'l_hand_phalanx_AJA_'+str(i)+'_LOC')
                cmd.parent(phalanxA, metaCarpal)
                cmd.move(0,-1.3,0.25-0.25*i,phalanxA)
    #phalanxAJB
                phalanxB = cmd.spaceLocator(n = 'l_hand_phalanx_AJB_'+str(i)+'_LOC')
                cmd.parent(phalanxB, phalanxA)
                cmd.move(0,-1.6,0.25-0.25*i,phalanxB)

    #phalanxAJC
                phalanxC = cmd.spaceLocator(n = 'l_hand_phalanx_AJC_'+str(i)+'_LOC')
                cmd.parent(phalanxC, phalanxB)
                cmd.move(0,-1.9,0.25-0.25*i,phalanxC)

#thumbAJA
            thumbPhalA = cmd.spaceLocator(n = 'l_hand_thumbPhal_AJA_LOC')
            cmd.parent(thumbPhalA, hand)
            cmd.move(0,-0.25,1,thumbPhalA)
#thumbAJB
            thumbPhalB = cmd.spaceLocator(n = 'l_hand_thumbPhal_AJB_LOC')
            cmd.parent(thumbPhalB, thumbPhalA)
            cmd.move(0,-0.25,1.2,thumbPhalB)
#thumbAJC
            thumbPhalC = cmd.spaceLocator(n = 'l_hand_thumbPhal_AJC_LOC')
            cmd.parent(thumbPhalC, thumbPhalB)
            cmd.move(0,-0.25,1.4,thumbPhalC)
#move and scale
            cmd.matchTransform(hand,wrist)
            cmd.scale(1,1,1,hand)

    else:
        if cmd.objExists('r_hand_loc_transform_GRP'):
            print('Right Hand already exists')
        else:
            hand = cmd.group(em = True, name = 'r_hand_loc_transform_GRP')
            cmd.parent(hand, wrist)
            for i in range(0,fingerCount):


    #metaCarpal
                metaCarpal = cmd.spaceLocator(n = 'r_hand_metaCarpal_AJA_'+str(i)+'_LOC')
                cmd.parent(metaCarpal, hand)
                cmd.move(0,-1,0.25-0.25*i,metaCarpal)
    #phalanxAJA
                phalanxA = cmd.spaceLocator(n = 'r_hand_phalanx_AJA_'+str(i)+'_LOC')
                cmd.parent(phalanxA, metaCarpal)
                cmd.move(0,-1.3,0.25-0.25*i,phalanxA)
    #phalanxAJB
                phalanxB = cmd.spaceLocator(n = 'r_hand_phalanx_AJB_'+str(i)+'_LOC')
                cmd.parent(phalanxB, phalanxA)
                cmd.move(0,-1.6,0.25-0.25*i,phalanxB)

    #phalanxAJC
                phalanxC = cmd.spaceLocator(n = 'r_hand_phalanx_AJC_'+str(i)+'_LOC')
                cmd.parent(phalanxC, phalanxB)
                cmd.move(0,-1.9,0.25-0.25*i,phalanxC)

#thumbAJA
            thumbPhalA = cmd.spaceLocator(n = 'r_hand_thumbPhal_AJA_LOC')
            cmd.parent(thumbPhalA, hand)
            cmd.move(0,-0.25,1,thumbPhalA)
#thumbAJB
            thumbPhalB = cmd.spaceLocator(n = 'r_hand_thumbPhal_AJB_LOC')
            cmd.parent(thumbPhalB, thumbPhalA)
            cmd.move(0,-0.25,1.2,thumbPhalB)
#thumbAJC
            thumbPhalC = cmd.spaceLocator(n = 'r_hand_thumbPhal_AJC_LOC')
            cmd.parent(thumbPhalC, thumbPhalB)
            cmd.move(0,-0.25,1.4,thumbPhalC)
#move and scale
            cmd.matchTransform(hand,wrist)
            cmd.scale(1,1,1,hand)

def createHead(spine):
#head
    if(cmd.objExists('m_head_loc_transform_GRP')):
        print('Head already exists')
    else:
        headGrp = cmd.group(em = True, name = 'm_head_loc_transform_GRP')
        cmd.parent(headGrp, spine)

#neck
        neck = cmd.spaceLocator(n = 'm_head_neck_LOC')
        cmd.parent(neck, headGrp)
        cmd.move(0,1,0,neck)
#head
        head = cmd.spaceLocator(n = 'm_head_head_LOC')
        cmd.parent(head, neck)
        cmd.move(0,4,0,head)
#move and scale
        cmd.matchTransform(headGrp,spine)
        cmd.scale(1,1,1,headGrp)

def mirrorLocators(direction):
    print('Mirror Locators')

    allLeftLocators = cmd.ls("l_*")
    leftLocators = cmd.listRelatives(*allLeftLocators, p = True, f = True)

    allRightLocators = cmd.ls("r_*")
    rightLocators = cmd.listRelatives(*allRightLocators, p = True, f = True)

    if direction == -1:
        for i,l in enumerate(rightLocators):
            pos = cmd.xform(l, q = True, t=True, ws=True)
            cmd.move(-pos[0], pos[1], pos[2], leftLocators[i])

    if direction == 1:
        for i,l in enumerate(leftLocators):
            pos = cmd.xform(l, q = True, t=True, ws=True)
            cmd.move(-pos[0], pos[1], pos[2], rightLocators[i])

def createJoints():

    if cmd.objExists('RIG_GRP'):
        print ('Rig already exists')
        return()
    else:
        jointGrp = cmd.group(em = True, name = 'RIG_GRP')

    #root

    root = cmd.ls("ROOT_LOC")
    rootPos = cmd.xform(root, q = True, t = True, ws = True)
    rootJoint = cmd.joint( radius = 0.15, p = rootPos, name = 'root_JNT')


    # spine

    allSpines = cmd.ls("spine_*", type = 'locator')
    spines = cmd.listRelatives(*allSpines, p = True, f = True)

    for i, s in enumerate(spines):
        pos = cmd.xform(s, q = True, t = True, ws = True)
        j = cmd.joint(radius = 0.1, p = pos, name = 'spine_AJ'+str(i)+'_JNT')
        lastSpineJoint = j

    # head
    m_headNeck = cmd.ls('m_head_neck_LOC')
    m_headNeckPos = cmd.xform(m_headNeck, q = True, t = True, ws = True)
    m_headNeckJoint = cmd.joint(radius = 0.1, p = m_headNeckPos, name = 'm_head_neck_JNT')

    m_headHead = cmd.ls('m_head_head_LOC')
    m_headHeadPos = cmd.xform(m_headHead, q = True, t = True, ws = True)
    m_headHeadJoint = cmd.joint(radius = 0.1, p = m_headHeadPos, name = 'm_head_Head_JNT')

    # arms
    fingerCount = cmd.intField(fingerCount_field, query = True, value = True)

    # l
    l_armShoulder = cmd.ls('l_arm_shoulder_LOC')
    l_armShoulderPos = cmd.xform(l_armShoulder, q = True, t = True, ws = True)
    l_armShoulderJoint = cmd.joint(radius = 0.1, p = l_armShoulderPos, name = 'l_arm_shoulder_JNT')
    cmd.parent(l_armShoulderJoint,lastSpineJoint)

    l_armElbow = cmd.ls('l_arm_elbow_LOC')
    l_armElbowPos = cmd.xform(l_armElbow, q = True, t = True, ws = True)
    l_armElbowJoint = cmd.joint(radius = 0.1, p = l_armElbowPos, name = 'l_arm_elbow_JNT')

    l_armWrist = cmd.ls('l_arm_wrist_LOC')
    l_armWristPos = cmd.xform(l_armWrist, q = True, t = True, ws = True)
    l_armWristJoint = cmd.joint(radius = 0.1, p = l_armWristPos, name = 'l_arm_wrist_JNT')

    # l_hand
    # thumb

    l_handPhalAJA = cmd.ls('l_hand_thumbPhal_AJA_LOC')
    l_handPhalAJAPos = cmd.xform(l_handPhalAJA, q = True, t = True, ws = True)
    l_handPhalAJAJoint = cmd.joint(radius = 0.075, p = l_handPhalAJAPos, name = 'l_hand_thumbPhal_AJA_JNT')

    l_handPhalAJB = cmd.ls('l_hand_thumbPhal_AJB_LOC')
    l_handPhalAJBPos = cmd.xform(l_handPhalAJB, q = True, t = True, ws = True)
    l_handPhalAJBJoint = cmd.joint(radius = 0.075, p = l_handPhalAJBPos, name = 'l_hand_thumbPhal_AJB_JNT')

    l_handPhalAJC = cmd.ls('l_hand_thumbPhal_AJC_LOC')
    l_handPhalAJCPos = cmd.xform(l_handPhalAJC, q = True, t = True, ws = True)
    l_handPhalAJCJoint = cmd.joint(radius = 0.075, p = l_handPhalAJCPos, name = 'l_hand_thumbPhal_AJC_JNT')

    # fingers
    for i in range(0,fingerCount):
        l_handmetaAJA = cmd.ls('l_hand_metaCarpal_AJA_'+str(i)+'_LOC')
        l_handmetaAJAPos = cmd.xform(l_handmetaAJA, q = True, t = True, ws = True)
        l_handmetaAJAJoint = cmd.joint(radius = 0.075, p = l_handmetaAJAPos, name = 'l_hand_metaCarpal_AJA_'+str(i)+'_JNT')
        cmd.parent(l_handmetaAJAJoint,l_armWristJoint)
        l_handFingerPhalAJA = cmd.ls('l_hand_phalanx_AJA_'+str(i)+'_LOC')
        l_handFingerPhalAJAPos = cmd.xform(l_handFingerPhalAJA, q = True, t = True, ws = True)
        l_handFingerPhalAJAJoint = cmd.joint(radius = 0.075, p = l_handFingerPhalAJAPos, name = 'l_hand_phalanx_AJA_'+str(i)+'_JNT')
        l_handFingerPhalAJB = cmd.ls('l_hand_phalanx_AJB_'+str(i)+'_LOC')
        l_handFingerPhalAJBPos = cmd.xform(l_handFingerPhalAJB, q = True, t = True, ws = True)
        l_handFingerPhalAJBJoint = cmd.joint(radius = 0.075, p = l_handFingerPhalAJBPos, name = 'l_hand_phalanx_AJB_'+str(i)+'_JNT')
        l_handFingerPhalAJC = cmd.ls('l_hand_phalanx_AJC_'+str(i)+'_LOC')
        l_handFingerPhalAJCPos = cmd.xform(l_handFingerPhalAJC, q = True, t = True, ws = True)
        l_handFingerPhalAJCJoint = cmd.joint(radius = 0.075, p = l_handFingerPhalAJCPos, name = 'l_hand_phalanx_AJC_'+str(i)+'_JNT')


    #r
    r_armShoulder = cmd.ls('r_arm_shoulder_LOC')
    r_armShoulderPos = cmd.xform(r_armShoulder, q = True, t = True, ws = True)
    r_armShoulderJoint = cmd.joint(radius = 0.1, p = r_armShoulderPos, name = 'r_arm_shoulder_JNT')
    cmd.parent(r_armShoulderJoint,lastSpineJoint)

    r_armElbow = cmd.ls('r_arm_elbow_LOC')
    r_armElbowPos = cmd.xform(r_armElbow, q = True, t = True, ws = True)
    r_armElbowJoint = cmd.joint(radius = 0.1, p = r_armElbowPos, name = 'r_arm_elbow_JNT')

    r_armWrist = cmd.ls('r_arm_wrist_LOC')
    r_armWristPos = cmd.xform(r_armWrist, q = True, t = True, ws = True)
    r_armWristJoint = cmd.joint(radius = 0.1, p = r_armWristPos, name = 'r_arm_wrist_JNT')

    # r_hand
    # thumb

    r_handPhalAJA = cmd.ls('r_hand_thumbPhal_AJA_LOC')
    r_handPhalAJAPos = cmd.xform(r_handPhalAJA, q = True, t = True, ws = True)
    r_handPhalAJAJoint = cmd.joint(radius = 0.075, p = r_handPhalAJAPos, name = 'r_hand_thumbPhal_AJA_JNT')

    r_handPhalAJB = cmd.ls('r_hand_thumbPhal_AJB_LOC')
    r_handPhalAJBPos = cmd.xform(r_handPhalAJB, q = True, t = True, ws = True)
    r_handPhalAJBJoint = cmd.joint(radius = 0.075, p = r_handPhalAJBPos, name = 'r_hand_thumbPhal_AJB_JNT')

    r_handPhalAJC = cmd.ls('r_hand_thumbPhal_AJC_LOC')
    r_handPhalAJCPos = cmd.xform(r_handPhalAJC, q = True, t = True, ws = True)
    r_handPhalAJCJoint = cmd.joint(radius = 0.075, p = r_handPhalAJCPos, name = 'r_hand_thumbPhal_AJC_JNT')

    # fingers
    for i in range(0,fingerCount):
        r_handmetaAJA = cmd.ls('r_hand_metaCarpal_AJA_'+str(i)+'_LOC')
        r_handmetaAJAPos = cmd.xform(r_handmetaAJA, q = True, t = True, ws = True)
        r_handmetaAJAJoint = cmd.joint(radius = 0.075, p = r_handmetaAJAPos, name = 'r_hand_metaCarpal_AJA_'+str(i)+'_JNT')
        cmd.parent(r_handmetaAJAJoint,r_armWristJoint)
        r_handFingerPhalAJA = cmd.ls('r_hand_phalanx_AJA_'+str(i)+'_LOC')
        r_handFingerPhalAJAPos = cmd.xform(r_handFingerPhalAJA, q = True, t = True, ws = True)
        r_handFingerPhalAJAJoint = cmd.joint(radius = 0.075, p = r_handFingerPhalAJAPos, name = 'r_hand_phalanx_AJA_'+str(i)+'_JNT')
        r_handFingerPhalAJB = cmd.ls('r_hand_phalanx_AJB_'+str(i)+'_LOC')
        r_handFingerPhalAJBPos = cmd.xform(r_handFingerPhalAJB, q = True, t = True, ws = True)
        r_handFingerPhalAJBJoint = cmd.joint(radius = 0.075, p = r_handFingerPhalAJBPos, name = 'r_hand_phalanx_AJB_'+str(i)+'_JNT')
        r_handFingerPhalAJC = cmd.ls('r_hand_phalanx_AJC_'+str(i)+'_LOC')
        r_handFingerPhalAJCPos = cmd.xform(r_handFingerPhalAJC, q = True, t = True, ws = True)
        r_handFingerPhalAJCJoint = cmd.joint(radius = 0.075, p = r_handFingerPhalAJCPos, name = 'r_hand_phalanx_AJC_'+str(i)+'_JNT')


    # legs
    # l
    l_legHip = cmd.ls('l_leg_hip_LOC')
    l_legHipPos = cmd.xform(l_legHip, q = True, t = True, ws = True)
    l_legHipJoint = cmd.joint(radius = 0.1, p = l_legHipPos, name = 'l_leg_hip_JNT')
    cmd.parent(l_legHipJoint,rootJoint)

    l_legKnee = cmd.ls('l_leg_knee_LOC')
    l_legKneePos = cmd.xform(l_legKnee, q = True, t = True, ws = True)
    l_legKneeJoint = cmd.joint(radius = 0.1, p = l_legKneePos, name = 'l_leg_knee_JNT')

    l_legAnkle = cmd.ls('l_leg_ankle_LOC')
    l_legAnklePos = cmd.xform(l_legAnkle, q = True, t = True, ws = True)
    l_legAnkleJoint = cmd.joint(radius = 0.1, p = l_legAnklePos, name = 'l_leg_ankle_JNT')

    l_footMiddle = cmd.ls('l_foot_middle_LOC')
    l_footMiddlePos = cmd.xform(l_footMiddle, q = True, t = True, ws = True)
    l_footMiddleJoint = cmd.joint(radius = 0.1, p = l_footMiddlePos, name = 'l_foot_middle_JNT')

    l_footToe = cmd.ls('l_foot_toe_LOC')
    l_footToePos = cmd.xform(l_footToe, q = True, t = True, ws = True)
    l_footToeJoint = cmd.joint(radius = 0.1, p = l_footToePos, name = 'l_foot_toe_JNT')

    # r
    r_legHip = cmd.ls('r_leg_hip_LOC')
    r_legHipPos = cmd.xform(r_legHip, q = True, t = True, ws = True)
    r_legHipJoint = cmd.joint(radius = 0.1, p = r_legHipPos, name = 'r_leg_hip_JNT')
    cmd.parent(r_legHipJoint,rootJoint)

    r_legKnee = cmd.ls('r_leg_knee_LOC')
    r_legKneePos = cmd.xform(r_legKnee, q = True, t = True, ws = True)
    r_legKneeJoint = cmd.joint(radius = 0.1, p = r_legKneePos, name = 'r_leg_knee_JNT')

    r_legAnkle = cmd.ls('r_leg_ankle_LOC')
    r_legAnklePos = cmd.xform(r_legAnkle, q = True, t = True, ws = True)
    r_legAnkleJoint = cmd.joint(radius = 0.1, p = r_legAnklePos, name = 'r_leg_ankle_JNT')

    r_footMiddle = cmd.ls('r_foot_middle_LOC')
    r_footMiddlePos = cmd.xform(r_footMiddle, q = True, t = True, ws = True)
    r_footMiddleJoint = cmd.joint(radius = 0.1, p = r_footMiddlePos, name = 'r_foot_middle_JNT')

    r_footToe = cmd.ls('r_foot_toe_LOC')
    r_footToePos = cmd.xform(r_footToe, q = True, t = True, ws = True)
    r_footToeJoint = cmd.joint(radius = 0.1, p = r_footToePos, name = 'r_foot_toe_JNT')

def createIKFKJoints():
    print ("Creating IK FK Joints")
    if cmd.objExists('root_JNT'):
        rootJnt = cmd.ls('root_JNT')
        FKJnt = cmd.duplicate(rootJnt, rr=True)
        FKJnt += cmd.listRelatives(FKJnt, ad=True,f=True)
        namePath = cmd.ls(FKJnt, l = True)
        namePath.sort()
        for f in namePath[::-1]:
            fkname = f.rpartition("|")[-1]
            cmd.rename(f, 'FK_'+fkname)
        rootJnt = cmd.ls('root_JNT')
        IKJnt = cmd.duplicate(rootJnt, rr=True)
        IKJnt += cmd.listRelatives(IKJnt, ad=True,f=True)
        namePath = cmd.ls(IKJnt, l = True)
        namePath.sort()
        for e in namePath[::-1]:
            ikname = e.rpartition("|")[-1]
            cmd.rename(e, 'IK_'+ikname)

    else:
        print ('There are no base joint to copy yet')


def lockLocators(lock):

    allList = cmd.ls(typ='locator')
    nodes = cmd.listRelatives(allList, parent=True)

    global editMode

    axis = ['x','y','z']
    attr = ['t','r','s']

    for axe in axis:
        for att in attr:
            for node in nodes:
                cmd.setAttr(node+'.'+att+axe, lock = lock)

    if editMode == False:
        editMode = True
    else:
        editMode = False

def deleteLocators():
    print ('delete locs')
    loc_nodes = cmd.ls('*_LOC')
    cmd.delete(loc_nodes)
    loc_grp = cmd.ls('*_loc_transform_GRP')
    cmd.delete(loc_grp)

def deleteJoints():
    print ('delete rig')
    rig_grp = cmd.ls('RIG_GRP')
    cmd.delete(rig_grp)

    jnt_nodes = cmd.ls('*_JNT')
    cmd.delete(jnt_nodes)

def createControl(ctrlAsked):
    ctrlName = cmd.textFieldGrp("ctrlName", q=True, tx=True)
    if ctrlName == "":
        ctrlName = ctrlAsked

    if ctrlAsked == 'Circle':
        print ('making circle')
        ctrl = cmd.circle(n=ctrlName+'_CTRL',nr=(0,1,0))
        cmd.group(ctrl,n = ctrlName + '_ctrl_transform_GRP')
    elif ctrlAsked == 'Square':
        print ('making Square')
        ctrl = cmd.curve(n=ctrlName+'_CTRL',d = 1, p = [(-1,0,-1),(-1,0,1),(1,0,1),(1,0,-1),(-1,0,-1)])
        cmd.group(ctrl,n = ctrlName + '_ctrl_transform_GRP')
    elif ctrlAsked == 'Arrow':
        print ('making Arrow')
        ctrl = cmd.curve(n=ctrlName+'_CTRL', d = 1, p =  [(-1,0,-0.5),(-1,0,0.5),(0,0,0.5),(0,0,1),(1,0,0),(0,0,-1),(0,0,-0.5),(-1,0,-0.5)])
        cmd.group(ctrl, n = ctrlName + '_ctrl_transform_GRP')
    elif ctrlAsked == 'QuadArrow':
        print ('making QuadArrow')
        ctrl = cmd.curve(n = ctrlName+'_CTRL', d = 1, p = [(-0.5, 0, -0.5),(-0.5, 0, -1.5),(-1, 0, -1.5),(0, 0, -2.5),(1, 0, -1.5),(0.5, 0, -1.5),(0.5, 0, -0.5),(1.5, 0, -0.5),(1.5, 0, -1),(2.5, 0, 0),(1.5, 0, 1),(1.5, 0, 0.5),(0.5,0,0.5),(0.5,0,1.5),(1,0,1.5),(0,0,2.5),(-1,0,1.5),(-0.5,0,1.5),(-0.5,0,0.5),(-1.5,0,0.5),(-1.5,0,1),(-2.5,0,0),(-1.5,0,-1),(-1.5,0,-0.5),(-0.5,0,-0.5)])
        cmd.group(ctrl, n = ctrlName + '_ctrl_transform_GRP')
    elif ctrlAsked == 'Star':
        print ('making Star')
        ctrl = cmd.curve(n = ctrlName+'_CTRL', d = 1,p = [(-1,0,0),(-0.25,0,-0.25),(0,0,-1),(0.25,0,-0.25),(1,0,0),(0.25,0,0.25),(0,0,1),(-0.25,0,0.25),(-1,0,0)])
        cmd.group(ctrl, n = ctrlName+'_ctrl_transform_GRP')
    elif ctrlAsked == 'X':
        print ('making X')
        ctrl = cmd.curve(n=ctrlName+'_CTRL', d = 1,p=[(-1,0,-1),(0,0,0),(1,0,-1),(0,0,0),(1,0,1),(0,0,0),(-1,0,1)])
        cmd.group(ctrl,n=ctrlName+'_ctrl_transform_GRP')
    elif ctrlAsked == 'Cog':
        print ('making Cog')
        circ = cmd.circle(n=ctrlName+'_CTRL',nr = (0,1,0),r = 1.035)
        for i in range(0,8):
            ctrl = cmd.curve(n = ctrlName, d=1,p = [(0.25,0,-1),(0.25,0,-1.25),(-0.25,0,-1.25),(-0.25,0,-1)])
            cmd.rotate(0,i*-45,0,ctrl)
            cmd.makeIdentity(apply=True,t=1,r=1,s=1,n=0)
            shp = cmd.listRelatives(ctrl, s = True)[0]
            cmd.parent(shp, circ, r = True, s = True)
            cmd.delete(ctrl)

        cmd.group(circ, n = ctrlName+'_ctrl_transform_GRP')

    elif ctrlAsked =='Line':
        print ('making Line')
        ctrl = cmd.curve(n = ctrlName +'_CTRL', d = 1, p = [(-1,0,0),(1,0,0)])
        cluster1 = cmd.cluster(ctrl+'.cv[0]', n = ctrlName+'_AJA_CLST')
        cluster2 = cmd.cluster(ctrl+'.cv[1]', n = ctrlName+'_AJB_CLST')

        loc1 = cmd.spaceLocator(p = (-1,0,0), n = ctrlName +'AJA_LOC')
        loc2 = cmd.spaceLocator(p = (1,0,0), n = ctrlName + 'AJB_LOC')

        cmd.parent(cmd.listRelatives(cluster1),cmd.listRelatives(loc1))
        cmd.parent(cmd.listRelatives(cluster2),cmd.listRelatives(loc2))

        cmd.group(ctrl,loc1,loc2, n = ctrlName+'_ctrl_transform_GRP')

    elif ctrlAsked =='CRV':
        print ('making CRV')
        crv_count= cmd.intField(crvCount_field, query= True,value=True)
        ctrl = cmd.curve(n=ctrlName + '_CRV', d=1, p=[0, 0, 0])
        for i in range(1,crv_count):
            cmd.curve(ctrlName+'_CRV',a=True,p=[(0,0,i)])

        cmd.group(ctrl,n=ctrlName+'_ctrl_transform_GRP')

    else:
        print ('CTRL asked for is not in the library name: '+ ctrlAsked)

def recolorCTRLs():
    currentCtrlColor = changeCTRLColor()

    print ('recolor now ' + currentCtrlColor)
    selection = cmd.ls(selection=True)
    currentCtrlColor = changeCTRLColor()

    if currentCtrlColor == 'Yellow':
        R = 1.0
        G = 1.0
        B = 0.0

        for sel in selection:
            cmd.setAttr(sel + ".overrideEnabled", 1)
            cmd.setAttr(sel + ".overrideRGBColors", 1)
            cmd.setAttr(sel + ".overrideColorRGB", R, G, B,)

    elif currentCtrlColor == 'Red':
        R = 1.0
        G = 0.0
        B = 0.0

        for sel in selection:
            cmd.setAttr(sel + ".overrideEnabled", 1)
            cmd.setAttr(sel + ".overrideRGBColors", 1)
            cmd.setAttr(sel + ".overrideColorRGB", R, G, B,)
    elif currentCtrlColor == 'Blue':
        R = 0.0
        G = 0.0
        B = 1.0

        for sel in selection:
            cmd.setAttr(sel + ".overrideEnabled", 1)
            cmd.setAttr(sel + ".overrideRGBColors", 1)
            cmd.setAttr(sel + ".overrideColorRGB", R, G, B,)
    else:
        print ('wrong color')

def changeCTRLColor():
    toColor = cmd.optionMenu(colorPicker, q = True, v = True)
    print ('change color to ' + toColor)
    if toColor == 'Yellow':
        currentCtrlColor='Yellow'
    elif toColor == 'Red':
        currentCtrlColor='Red'
    elif toColor == 'Blue':
        currentCtrlColor='Blue'
    else:
        print ('wrong color')

    return currentCtrlColor

def createTransformGRP():
    selObj = cmd.ls(sl=True)

    for obj in selObj:
        grp = cmd.group(em=True)
        rnm_grp = cmd.rename(grp, obj + "_transform_GRP")
        cmd.parent(rnm_grp, obj)
        cmd.setAttr(rnm_grp + ".tx", 0)
        cmd.setAttr(rnm_grp + ".ty", 0)
        cmd.setAttr(rnm_grp + ".tz", 0)
        cmd.setAttr(rnm_grp + ".rx", 0)
        cmd.setAttr(rnm_grp + ".ry", 0)
        cmd.setAttr(rnm_grp + ".rz", 0)

        cmd.delete(cmd.pointConstraint(obj, rnm_grp))

        cmd.parent(rnm_grp, w=True)
        cmd.parent(obj, rnm_grp)

        cmd.makeIdentity(obj, apply=True, t=True, r=True, s=True)

def allignTransformGRP():
    sel = cmd.ls(sl=True)

    cmd.delete(cmd.pointConstraint(sel[1], sel[0]))
    cmd.delete(cmd.orientConstraint(sel[1], sel[0]))

def createNurbsSurface():
    name = cmd.textFieldGrp("nurbName", q=True, tx=True)
    print('Create the nurb with the name ' + name)
    u_value = cmd.intField(u_field,q=True,v=True)
    v_value = cmd.intField(v_field,q=True,v=True)

    theNurb = cmd.nurbsPlane(n = name+'_NURBS',u=u_value,v=v_value)
    theNurbGrp = cmd.group(em=True,name=name+'_nurbs_transform_GRP')
    cmd.parent(theNurb,theNurbGrp)

def deleteNurbsSurface():
    name = cmd.textFieldGrp("nurbName", q=True,tx=True)
    if(cmd.objExists(name+'_nurbs_transform_GRP')):
        cmd.delete(name+'_nurbs_transform_GRP')
    else:
        print('NURBS ARE DRUNK')

def createNurbsJoints():
    pName=cmd.textFieldGrp("nurbName", q=True,tx=True)

    name = pName+'_NURBS'
    if(cmd.objExists(name+'_hair_transform_GRP')):
        print('already existing this wont work you dumdum')
        return()
    else:
        hair_grp = cmd.group(em=True, name=name+'_hairs_transform_GRP')
        move_grp = cmd.group(em=True, name=name+'_move_jnt_transform_GRP')
        cmd.parent(move_grp,hair_grp)

    u_value = cmd.intField(u_field,q=True,v=True)
    v_value = cmd.intField(v_field,q=True,v=True)

    createNurbsFollicle(u_value, v_value, hair_grp, move_grp)

def createNurbsFollicle(u,v,hair_grp,move_grp):
    theNurb = cmd.ls(cmd.textFieldGrp("nurbName", q=True, tx=True)+'_NURBS')[0]

    pName = theNurb+'_Follicle'
    foll_grp = cmd.group(em=True,name=pName+'_GRP')
    cmd.parent(foll_grp, hair_grp)
    nurb = cmd.listRelatives(theNurb, shapes=True)[0]

    if u!=1:
        u=u+1

    for i in range(0,u):
        for x in range(0,v+1):
            foll = cmd.createNode('follicle', name=pName+'_SHP'+str(x+1))
            follParent = cmd.listRelatives(foll,p=True)[0]

            cmd.parent(follParent, foll_grp)
            cmd.setAttr(foll+'.simulationMethod',0)
            cmd.makeIdentity(nurb,apply=True,t=1,r=1,s=1,n=0)

            cmd.connectAttr(foll+'.outRotate',follParent+'.rotate',f=True)
            cmd.connectAttr(foll+'.outTranslate',follParent+'.translate')
            cmd.connectAttr(nurb+'.worldMatrix', foll+'.inputWorldMatrix')
            cmd.connectAttr(nurb+'.local', foll+'.inputSurface')

            divV = float(x)/float(v)
            cmd.setAttr(foll+'.parameterV',divV)
            divU = float(i)/float(u)

            if(u==1):
                cmd.setAttr(foll+'.parameterU',0.5)
            else:
                cmd.setAttr(foll+'.parameterU',divU)

            pos = cmd.xform(follParent, q=True,t=True,ws=True)
            follJoint = cmd.joint(radius=0.1,p=pos,name=pName+'_U'+str(i+1)+'_V'+str(x)+'_bind_JNT')
            moveJoint = cmd.joint(radius=0.2,p=pos,name=pName+'_U'+str(i+1)+'_V'+str(x)+'_move_JNT')

            cmd.parent(moveJoint,move_grp)
            cmd.rename(follParent,pName)

def deleteNurbsJoints():

    print('deleting ')
    name = cmd.textFieldGrp("nurbName", q=True,tx=True)
    if(cmd.objExists(name+'_NURBS_hairs_transform_GRP')):
        cmd.delete(name+'_NURBS_hairs_transform_GRP')
    else:
        print('R U DUNKIN')


def createBlendJoints():
    print ('Creating blend shape joints')
    sel = cmd.ls(selection=True)
    locList = []
    if(len(sel)> 1 or sel[0]==''):
        print ('Too much or too little selected')
        return
    else:
        print(sel)
    name = sel[0].split('_CRV')[0]

    if(cmd.objExists(name+'_bind_transform_GRP')):
        print ('group already exists')
        return()
    else:
        loc_grp = cmd.group(em=True, name=name+'_bind_transform_GRP')
    jntBindCount = cmd.intField(jntBindCount_field, q = True, v = True)

    for i in range(0,jntBindCount):
        lastLoc = cmd.spaceLocator(n = name+'_'+str(i)+'_LOC')
        cmd.parent(lastLoc, loc_grp)
        path = cmd.pathAnimation(sel[0],lastLoc, name= lastLoc[0]+'_motionPath', fm=True,f=True,fa='x',ua='y')
        print(path)
        cmd.cutKey(path,attribute='uValue',option='keys')
        div = float(i)/float(jntBindCount-1)
        print (str(div))
        cmd.setAttr(path+'.uValue', div)
        cmd.setAttr(lastLoc[0]+'Shape.localScaleX',0.1)
        cmd.setAttr(lastLoc[0]+'Shape.localScaleY',0.1)
        cmd.setAttr(lastLoc[0]+'Shape.localScaleZ',0.1)
        locList.append(lastLoc)

    for x in range(0,len(locList)):
        cmd.select(locList[x])
        pos = cmd.xform(locList[x], q = True, t = True, ws=True)
        locJoint = cmd.joint(radius =0.1,p=pos,name=name+'_'+str(x)+'_offset_JNT')
        bindJoint = cmd.joint(radius=0.1, p=pos, name=name+'_'+str(x)+'_bind_JNT')
        sphereMesh = cmd.sphere(radius = 0.2, s=1,nsp=2,hr=1)

        sphereShape = cmd.listRelatives(sphereMesh, s=True)[0]

        cmd.parent(sphereShape,bindJoint,r=True,s=True)
        colorBlendControls(sphereShape)
        cmd.delete(sphereMesh)

    createBlendShapes(sel[0])

def createBlendShapes(crv):
    name = crv.split('_CRV')[0]

    cmd.select(crv)


    if(cmd.objExists(name+'_blend_transform_GRP')):
        print ('already exists delete first')
        return()
    else:
        blend_grp = cmd.group(em=True, name = name+'_blend_transform_GRP')
    cmd.select(crv)
    cmd.blendShape()

    blendCount = cmd.intField(blendCount_field, query = True, value=True)
    for i in range(0,blendCount):
        lastBlend = cmd.duplicate(crv,n=name+'_'+str(i)+'_BLEND')
        cmd.parent(lastBlend, blend_grp)
        cmd.blendShape('blendShape1', e=True, t=(name + '_CRV', i+1, name+'_' + str(i) + '_BLEND', 1.0))

def deleteBlendJoints():
    print('deleting the blends')
    sel = cmd.ls(selection = True)
    if(len(sel)>1 or sel[0]==''):
        print('NOPERS')
        return
    else:
        print(sel)
    name = sel[0].split('_CRV')[0]

    if(cmd.objExists(name+'_bind_transform_GRP')):
        grp = cmd.ls(name+'_bind_transform_GRP')
        cmd.delete(grp)
    if(cmd.objExists(name+'_blend_transform_GRP')):
        grp2 = cmd.ls(name+'_blend_transform_GRP')
        cmd.delete(grp2)

def createBlendColorMaterials():
    print('creating colored materials')

    if cmd.objExists('blendRed'):
        print('returning because mat already exists')
        firstColor=True
        return()
    #yellow

    materialYellow = cmd.shadingNode('lambert',asShader=1,name='blendYellow')
    cmd.setAttr('blendYellow.color',1.0,1.0,0.0, type='double3')
    SGYellow= cmd.sets(renderable = 1,noSurfaceShader=1, empty=1,name='blendYellowSG')
    cmd.connectAttr((materialYellow+'.outColor'),(SGYellow+'.surfaceShader'),f=1)


    #blue

    materialBlue = cmd.shadingNode('lambert',asShader=1,name='blendBlue')
    cmd.setAttr('blendBlue.color',0.0,0.0,1.0, type='double3')
    SGBlue= cmd.sets(renderable = 1,noSurfaceShader=1, empty=1,name='blendBlueSG')
    cmd.connectAttr((materialBlue+'.outColor'),(SGBlue+'.surfaceShader'),f=1)


    #red
    materialRed = cmd.shadingNode('lambert', asShader=1, name='blendRed')
    cmd.setAttr('blendRed.color', 1.0, 0.0, 0.0, type='double3')
    SGRed = cmd.sets(renderable=1, noSurfaceShader=1, empty=1, name='blendRedSG')
    cmd.connectAttr((materialRed + '.outColor'), (SGRed + '.surfaceShader'), f=1)


    firstColor=True

def colorBlendControls(sphere):
    l_check = cmd.checkBox('l_tickBox', q=True, v=True)
    r_check = cmd.checkBox('r_tickBox', q=True, v=True)


    if firstColor==False:
        createBlendColorMaterials()

    if l_check == False and r_check == False:
        b_check = True
    if l_check == True and r_check == True:
        b_check = True

    if b_check == True:
        print('color yellow')
        cmd.sets(sphere,e=1,forceElement='blendYellowSG')
    if l_check == True and r_check == False:
        print('color blue')
        cmd.sets(sphere, e=1, forceElement='blendBlueSG')
    if r_check == True and l_check == False:
        print('color red')
        cmd.sets(sphere, e=1, forceElement='blendRedSG')