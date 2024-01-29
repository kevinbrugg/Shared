from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds

_POLYGON_MESH_LIMIT = 10
_VERTEX_LIMIT = 10
# TODO swap out global selected variable for the local ones in definitions at the end.
_SELECTED = cmds.ls(selection=True)
_MESH = cmds.ls(type="mesh")
_TRANSFORM = cmds.listRelatives(_MESH, type='transform', parent=True)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Pipe Checker")
        # button creation
        button_pipecheck = QtWidgets.QPushButton("Check Pipeline")
        button_cancel = QtWidgets.QPushButton("Cancel")
        button_pipecheck.clicked.connect(self.CheckAll)
        # main layout
        layout = QtWidgets.QVBoxLayout()

        # layout for buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(button_cancel)
        button_layout.addWidget(button_pipecheck)

        # layout for pipecheck report
        pipecheck_layout = QtWidgets.QVBoxLayout()
        # the attributes of each check are stored within each check class
        history_check = HistoryCheck()
        mesh_density_check = MeshCheck()
        vertex_density_check = VertexCheck()
        instance_check = InstanceCheck()

        pipecheck_layout.addWidget(history_check)
        pipecheck_layout.addWidget(mesh_density_check)
        pipecheck_layout.addWidget(vertex_density_check)
        pipecheck_layout.addWidget(instance_check)

        # adding nested layout to layout
        layout.addLayout(pipecheck_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        # end of code
        self.show()

    def CheckAll(self):

        history_check = HistoryCheck()
        mesh_density_check = MeshCheck()
        vertex_density_check = VertexCheck()
        instance_check = InstanceCheck()
        # TODO find out why running the checks this way never enables the fix button.
        history_check.run_check()
        mesh_density_check.run_check()
        vertex_density_check.run_check()
        instance_check.run_check()



class CheckWidget(QtWidgets.QWidget):
    """blank widget class to cold custom widget for pipe checkers"""

    def __init__(self, name, button, parent=None):
        super(CheckWidget, self).__init__(parent=parent)
        self.name = name
        self.button = button
        self._setupUi()

    def _setupUi(self):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self.name)
        self.check_button = QtWidgets.QPushButton(self.button)
        self.check_button.clicked.connect(self.run_check)
        self.fix_button = QtWidgets.QPushButton("Fix it!")
        self.fix_button.clicked.connect(self.fix)
        self.fix_button.setDisabled(True)
        self.status_label = QtWidgets.QLabel()
        self.status_label.setText("NA")

        # self.status_message = ......


        layout.addWidget(label)
        layout.addWidget(self.check_button)
        layout.addWidget(self.fix_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def run_check(self):
        # Pass through function to be implemented as a child
        pass

    def fix(self):
        pass

    def select(self):
        pass


# This will inherit all parts of the CheckWidget, you can implement the fix method and run_check method here
class HistoryCheck(CheckWidget):

    def __init__(self):
        # populating button names here
        super(HistoryCheck, self).__init__("Check History", "Run Check")


    def run_check(self):
        self.issue_list = []
        for self.mesh in _MESH:
            history = cmds.listConnections(self.mesh + ".inMesh", skipConversionNodes=True, source=True)
            if history:
                cmds.warning('{} has history... click Fix it! To delete history'.format(cmds.listRelatives(self.mesh, type='transform', parent=True)))
                self.issue_list.append(self.mesh)
                self.fix_button.setEnabled(True)
                self.status_label.setText("Failed, some asset(s) in your scene has history")

            if history == False:
                self.status_label.setText("Passed!")

    def fix(self):
        cmds.delete(self.issue_list, constructionHistory=True)
        self.status_label.setText("Passed! History deleted")
        print("History for {} deleted".format(self.issue_list))
        self.issue_list = []

# NOTE: In the rest of these classes, implement similar to the history check, keep things
# very generic except in the actual checks, that way things are super reusable


class MeshCheck(CheckWidget):

    def __init__(self):
        super(MeshCheck, self).__init__("Check Mesh Density", "Run Check")

    def run_check(self):
        self.issue_list = []
        for mesh in _MESH:
            polyCount = [cmds.polyEvaluate(mesh, f=True)]
            polyTotal = sum(polyCount)
            if polyTotal > _POLYGON_MESH_LIMIT:
                self.issue_list.append(mesh)


        if polyTotal > _POLYGON_MESH_LIMIT:
            cmds.warning("Polygon count is too high for {} Click Fix it! To select problematic meshes".format(cmds.listRelatives(mesh, type='transform', parent=True)))
            self.status_label.setText("Polygon density is too high! Click fix button to highlight problematic meshes")
            self.fix_button.setEnabled(True)
            return
        else:
            self.status_label.setText("Passed!")

    def fix(self):

        transforms = cmds.listRelatives(self.issue_list, type='transform', parent=True)
        cmds.select(transforms)
        self.issue_list = []


class VertexCheck(CheckWidget):
    def __init__(self):
        super(VertexCheck, self).__init__("Check Vertex Density", "Run Check")

    def run_check(self):
        self.issue_list = []
        for mesh in _MESH:
            vertex_count = [cmds.polyEvaluate(mesh, v=True)]
            vertex_total = sum(vertex_count)
            if vertex_total > _VERTEX_LIMIT:
                self.issue_list.append(mesh)
                cmds.warning("Vertex count is too high for {} Click Fix it! To select problematic meshes".format(cmds.listRelatives(mesh, type='transform', parent=True)))

        if vertex_total > _VERTEX_LIMIT:
            self.status_label.setText("Vertex density is too high! Click fix button to highlight problematic meshes")
            self.fix_button.setEnabled(True)
            return
        else:
            self.status_label.setText("Passed!")

    def fix(self):
        transforms = cmds.listRelatives(self.issue_list, type='transform', parent=True)
        cmds.select(transforms)
        self.issue_list = []


class InstanceCheck(CheckWidget):
    def __init__(self):
        super(InstanceCheck, self).__init__("Check For Instanced Meshes", "Run Check")

    def run_check(self):
        self.issue_list = []
        geo = cmds.ls(type="mesh", ap=True)
        if _MESH != geo:
            difference = list(set(geo) - set(_MESH))
            self.transforms = cmds.listRelatives(difference, type='transform', parent=True)
            self.issue_list.append(self.transforms)
            cmds.warning(' {} are instanced mesh, click Fix it! To highlight instanced meshes'.format(self.issue_list))
            self.status_label.setText("Instanced meshes exist!")
            self.fix_button.setEnabled(True)

        else:
            self.status_label.setText("Passed!")

    def fix(self):
        cmds.select(self.transforms)
        self.issue_list = []


if __name__ == '__main__':
    w = MainWindow()
