from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
from abc import ABCMeta, abstractmethod

# Main Window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Lung CT Visulization")
        self.resize(603, 553)

        self.layout = QtWidgets.QGridLayout()

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

# Sub windows base class
class SubWindow:
    __metaclass__ = ABCMeta
 
    def __init__(self, parent, row, column):
        # Interface to the main window
        self.vtkWidget = QVTKRenderWindowInteractor()
        parent.layout.addWidget(self.vtkWidget, row, column)
        # Create standard render, render window and interactor
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
    
    @abstractmethod
    def render(self, datapath = None):
        pass

# Volumer Rendering Window
class VolumeRender(SubWindow):

    def render(self, datapath):
        colors = vtk.vtkNamedColors()

        # Create reader for the data
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(datapath)

        # Create transfer mapping scalar value to opacity
        opacityTransferFunction = vtk.vtkPiecewiseFunction()
        opacityTransferFunction.AddPoint(20, 0.0)
        opacityTransferFunction.AddPoint(255, 0.2)

        # Create transfer mapping scalar value to color.
        colorTransferFunction = vtk.vtkColorTransferFunction()
        colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
        colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
        colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
        colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
        colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

        # The property describes how the data will look.
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(colorTransferFunction)
        volumeProperty.SetScalarOpacity(opacityTransferFunction)
        volumeProperty.ShadeOn()
        volumeProperty.SetInterpolationTypeToLinear()

        # The mapper / ray cast function know how to render the data.
        volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        # The volume holds the mapper and the property and
        # can be used to position/orient the volume.
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)

        
        self.ren.AddVolume(volume)
        self.ren.SetBackground(colors.GetColor3d("Wheat"))
        self.ren.GetActiveCamera().Azimuth(45)
        self.ren.GetActiveCamera().Elevation(30)
        self.ren.ResetCameraClippingRange()
        self.ren.ResetCamera()
        
        self.iren.Initialize()
        



if __name__ == '__main__':
    # Create an application
    app = QApplication(sys.argv)
    
    # Create main window
    mainwindow = MainWindow()
    mainwindow.show()

    # Add view to mainwindow
    view1 = VolumeRender(mainwindow, 0, 0)
    view1.render('./1.nii')

    sys.exit(app.exec_())
