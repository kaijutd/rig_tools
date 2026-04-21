import maya.cmds as cmd

if cmd.window("poseWindow", ex=True):
    cmd.deleteUI("poseWindow", window=True)

cmd.window("poseWindow", t="Pose Saver", wh=(500, 500), s=True, menuBar=True)

cmd.menu(l="HowTo")
cmd.menuItem("Select Controls to save according to it's Category (tab specific).", bld=True)
cmd.menu(l="History")
cmd.menuItem("I worked on this lul.", bld=True)

myForm = cmd.formLayout()

myTabs = cmd.tabLayout()

cmd.formLayout(myForm, edit=True,
               attachForm=[(myTabs, "top", 10), (myTabs, "bottom", 10), (myTabs, "left", 10), (myTabs, "right", 10)])

mkPose_layout = cmd.columnLayout()

poseShelf = cmd.shelfLayout(w=455, h=300)

mkPose_b_body = cmd.symbolButton(image="body_img.jpg", w=150, h=150, c="createShelfButton_body(bodyShelf)")
mkPose_b_face = cmd.symbolButton(image="face_img.jpg", w=150, h=150, c="createShelfButton_face(faceShelf)")
mkPose_b_misc = cmd.symbolButton(image="misc_img.jpg", w=150, h=150, c="createShelfButton_misc(miscShelf)")

cmd.setParent("..")
cmd.setParent("..")
bodyCtrl_layout = cmd.columnLayout()
bodyShelf = cmd.shelfLayout(w=500, h=500)

cmd.setParent("..")
cmd.setParent("..")
faceCtrl_layout = cmd.columnLayout()
faceShelf = cmd.shelfLayout(w=500, h=500)

cmd.setParent("..")
cmd.setParent("..")
miscCtrl_layout = cmd.columnLayout()
miscShelf = cmd.shelfLayout(w=500, h=500)

cmd.setParent("..")
cmd.setParent("..")

cmd.tabLayout(myTabs, edit=True,
              tabLabel=[(mkPose_layout, "Pose Types"), (bodyCtrl_layout, "Body Poses"), (faceCtrl_layout, "Face Poses"),
                        (miscCtrl_layout, "Misc Poses")])

cmd.showWindow("poseWindow")


def createShelfButton_body(targetShelf_body):
    storeCmds_body = ""

    selPose = cmd.ls(sl=True)

    if len(selPose) < 1:
        cmd.warning("Nothing Selected! Please select at least one object")
    else:
        for all in selPose:
            keyables = cmd.listAttr(all, k=True, r=True, w=True, c=True, u=True)
            print
            keyables
            for vals in keyables:
                findVal = cmd.getAttr(all + "." + vals)
                print
                findVal
                startCode = "setAttr "
                endCode = ";\n"
                saveToShelf = (startCode + (all + "." + vals) + " %f" + endCode) % findVal
                storeCmds_body += saveToShelf
                print
                storeCmds_body

        pd_body = cmd.promptDialog(t="Body Pose", m="Pose Name:", b="Save")
        if pd_body == "Save":
            pd_body_name = cmd.promptDialog(q=True, text=True)

            cmd.shelfButton(l=pd_body_name, ann=pd_body_name, imageOverlayLabel=pd_body_name, i1="myButtonImage.jpg",
                            command=storeCmds_body, p=targetShelf_body, sourceType="mel")

            usd = cmd.internalVar(usd=True)
            filePathName = (usd + pd_body_name + ".mel")
            svFile = open(filePathName, "w")
            svFile.write(storeCmds_body)
            svFile.close()
            print
            file(filePathName).read()


def createShelfButton_face(targetShelf_face):
    storeCmds_face = ""

    selPose = cmd.ls(sl=True)

    if len(selPose) < 1:
        cmd.warning("Nothing Selected! Please select at least one object")
    else:
        for all in selPose:
            keyables = cmd.listAttr(all, k=True, r=True, w=True, c=True, u=True)
            print(keyables)
            for vals in keyables:
                findVal = cmd.getAttr(all + "." + vals)
                print
                findVal
                startCode = "setAttr "
                endCode = ";\n"
                saveToShelf = (startCode + (all + "." + vals) + " %f" + endCode) % findVal
                storeCmds_face += saveToShelf
                print(storeCmds_face)

        pd_face = cmd.promptDialog(t="Face Pose", m="Pose Name:", b="Save")
        if pd_face == "Save":
            pd_face_name = cmd.promptDialog(q=True, text=True)

            cmd.shelfButton(l=pd_face_name, ann=pd_face_name, imageOverlayLabel=pd_face_name, i1="myButtonImage.jpg",
                            command=storeCmds_face, p=targetShelf_face, sourceType="mel")

            usd = cmd.internalVar(usd=True)
            filePathName = (usd + pd_face_name + ".mel")
            svFile = open(filePathName, "w")
            svFile.write(storeCmds_face)
            svFile.close()
            print(file(filePathName).read())


def createShelfButton_misc(targetShelf_misc):
    storeCmds_misc = ""

    selPose = cmd.ls(sl=True)

    if len(selPose) < 1:
        cmd.warning("Nothing Selected! Please select at least one object")
    else:
        for all in selPose:
            keyables = cmd.listAttr(all, k=True, r=True, w=True, c=True, u=True)
            print
            keyables
            for vals in keyables:
                findVal = cmd.getAttr(all + "." + vals)
                print
                findVal
                startCode = "setAttr "
                endCode = ";\n"
                saveToShelf = (startCode + (all + "." + vals) + " %f" + endCode) % findVal
                storeCmds_misc += saveToShelf
                print(storeCmds_misc)

        pd_misc = cmd.promptDialog(t="Misc Pose", m="Pose Name:", b="Save")
        if pd_misc == "Save":
            pd_misc_name = cmd.promptDialog(q=True, text=True)

            cmd.shelfButton(l=pd_misc_name, ann=pd_misc_name, imageOverlayLabel=pd_misc_name, i1="myButtonImage.jpg",
                            command=storeCmds_misc, p=targetShelf_misc, sourceType="mel")

            usd = cmd.internalVar(usd=True)
            filePathName = (usd + pd_misc_name + ".mel")
            svFile = open(filePathName, "w")
            svFile.write(storeCmds_misc)
            svFile.close()
            file(filePathName).read()