from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys

# Main Window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("My Awesome App")
        self.resize(603, 553)

        self.layout = QtWidgets.QGridLayout()

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

# Create your own vtk rendering view class, a simple template
class SimpleView():
 
    def __init__(self, parent, row, column):
        # Interface to the main window
        self.vtkWidget = QVTKRenderWindowInteractor()
        parent.layout.addWidget(self.vtkWidget, row, column)
        # Create render and interactive render window
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        '''
        Following code can be modified to your own rendering method
        '''
        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)
 
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
 
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
 
        self.ren.AddActor(actor)
 
        self.ren.ResetCamera()
 
        self.iren.Initialize()

if __name__ == '__main__':
    # Create an application
    app = QApplication(sys.argv)
    
    # Create main window
    mainwindow = MainWindow()
    mainwindow.show()

    # Add view to mainwindow
    view1 = SimpleView(mainwindow, 0, 0)
    view2 = SimpleView(mainwindow, 0, 1)
    view3 = SimpleView(mainwindow, 1, 0)
    view4 = SimpleView(mainwindow, 1, 1)

    sys.exit(app.exec_())
