from PySide6 import QtWidgets, QtCore


class RigRenameWindow(QtWidgets.QWidget):
    def __init__(self):
        super(RigRenameWindow, self).__init__()
        self.setWindowTitle("RigerousRenamer")
        self.resize(300, 150)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.rig_name_label = QtWidgets.QLabel("Rig Name:")
        self.rig_name_field = QtWidgets.QLineEdit()
        self.joint_name_label = QtWidgets.QLabel("Joint Name:")
        self.joint_name_field = QtWidgets.QLineEdit()
        self.left_check = QtWidgets.QCheckBox("Left")
        self.right_check = QtWidgets.QCheckBox("Right")
        self.populate_button = QtWidgets.QPushButton("Populate")
        self.rename_button = QtWidgets.QPushButton("Rename")

        self.populate_button.clicked.connect(self.populate_fields)
        self.rename_button.clicked.connect(self.rename_joints)

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.rig_name_label)
        layout.addWidget(self.rig_name_field)
        layout.addWidget(self.joint_name_label)
        layout.addWidget(self.joint_name_field)
        layout.addWidget(self.left_check)
        layout.addWidget(self.right_check)
        layout.addWidget(self.populate_button)
        layout.addWidget(self.rename_button)
        self.setLayout(layout)

    def populate_fields(self):
        selection = cmds.ls(selection=True, type="joint") or []
        if selection:
            selected_joint = selection[0]
    
            parts = selected_joint.split("_")
            if len(parts) >= 5:
                rig_name = parts[0]
                suffix = parts[1]
                joint_name = parts[2]
    
                self.rig_name_field.setText(rig_name)
                self.joint_name_field.setText(joint_name)
                if suffix == "l":
                    self.left_check.setChecked(True)
                    self.right_check.setChecked(False)
                elif suffix == "r":
                    self.left_check.setChecked(False)
                    self.right_check.setChecked(True)
                else:
                    self.left_check.setChecked(False)
                    self.right_check.setChecked(False)
            else:
                print("Selected joint name does not match expected format")
        else:
            print("No joint selected")


    def rename_joints(self):
        rig_name = self.rig_name_field.text()
        joint_name = self.joint_name_field.text()
    
        suffix = ""
        if self.left_check.isChecked():
            suffix = "l"
        elif self.right_check.isChecked():
            suffix = "r"
        else:
            suffix = "m"
    
        selected_joints = cmds.ls(selection=True, type="joint") or []
        if selected_joints:
            selected_joints.sort(key=lambda x: len(cmds.listRelatives(x, allDescendents=True) or []), reverse=True)
    
            for i, joint in enumerate(selected_joints, start=0): 
                hierarchy_name = self.get_hierarchical_name(i)
                new_name = "{0}_{1}_{2}_AJ{3}_JNT".format(rig_name, suffix, joint_name, hierarchy_name)
                cmds.rename(joint, new_name)
                print("Joint renamed to:", new_name)
        else:
            print("No joints selected")
    
    def get_hierarchical_name(self, index):
        result = ""
        while index >= 0:
            result = chr(65 + index % 26) + result
            index = index // 26 - 1
        return result

    def get_children_hierarchy(self, parent_joint, visited=None):
        if visited is None:
            visited = set()
        children_hierarchy = []
        full_path_parent_joint = cmds.ls(parent_joint, long=True)[0]
        if full_path_parent_joint not in visited:
            children = cmds.listRelatives(full_path_parent_joint, allDescendents=True, type="joint") or []
            for child in children:
                full_path_child = cmds.ls(child, long=True)[0]
                if full_path_child not in visited:
                    children_hierarchy.append(full_path_child)
                    visited.add(full_path_child)
                    children_hierarchy.extend(self.get_children_hierarchy(full_path_child, visited))
        return children_hierarchy





def show_window():
    global rig_rename_window

    try:
        rig_rename_window.close()  
    except:
        pass

    rig_rename_window = RigRenameWindow()
    rig_rename_window.show()


show_window()  