from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication
import vtk
from vtk.util.vtkImageImportFromArray import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
from abc import ABCMeta, abstractmethod
import SimpleITK as sitk
import numpy as np

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
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    
    @abstractmethod
    def render(self, datapath = None):
        pass

# Volumer Rendering Window
class VolumeRender(SubWindow):

    def render(self, datapath, usingMask = False, maskpath = None):

        data = sitk.ReadImage(datapath)
        slices = sitk.GetArrayFromImage(data)
        if usingMask:
            mask = sitk.ReadImage(maskpath)
            mask_slcies = sitk.GetArrayFromImage(mask)
            mask_slcies[mask_slcies >= 1] = 1
            slices = np.multiply(slices, mask_slcies)
        spacing = data.GetSpacing()
        origin = (0,0,0)

        # Create reader for the data
        reader = vtkImageImportFromArray()
        reader.SetArray(slices)
        reader.SetDataSpacing(spacing)
        reader.SetDataOrigin(origin)
        reader.Update()

        # Create transfer mapping scalar value to opacity
        opacityTransferFunction = vtk.vtkPiecewiseFunction()
        #opacityTransferFunction.AddPoint(-400, 0.0)
        #opacityTransferFunction.AddPoint(-380, 0.0)
        #opacityTransferFunction.AddPoint(-370, 0.0)
        opacityTransferFunction.AddPoint(-350, 0.0)
        #opacityTransferFunction.AddPoint(-250, 0.0)
        opacityTransferFunction.AddPoint(-250, 0.2)
        opacityTransferFunction.AddPoint(-200, 0.7)
        opacityTransferFunction.AddPoint(-150, 0.0)
        opacityTransferFunction.AddPoint(-60, 0)
        opacityTransferFunction.AddPoint(-50, 0.9)
        #opacityTransferFunction.AddPoint(-30, 0.0)
        #opacityTransferFunction.AddPoint(-20, 0.9)
        #opacityTransferFunction.AddPoint(-50, 0.0)
        opacityTransferFunction.AddPoint(0, 0.0)

        # Create transfer mapping scalar value to color.
        colorTransferFunction = vtk.vtkColorTransferFunction()
        colorTransferFunction.AddRGBPoint(-300, 0, 0, 0)
        colorTransferFunction.AddRGBPoint(-50, 1, 1, 0.5)
        colorTransferFunction.AddRGBPoint(0, 1, 1, 1)
        #colorTransferFunction.AddRGBPoint(-100, 0, 0, 1)

        # The property describes how the data will look.
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(colorTransferFunction)
        volumeProperty.SetScalarOpacity(opacityTransferFunction)
        volumeProperty.ShadeOn()
        volumeProperty.SetInterpolationTypeToLinear()

        # The mapper / ray cast function know how to render the data.
        self.volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
        self.volumeMapper.SetInputConnection(reader.GetOutputPort())

        # The volume holds the mapper and the property and
        # can be used to position/orient the volume.
        volume = vtk.vtkVolume()
        volume.SetMapper(self.volumeMapper)
        volume.SetProperty(volumeProperty)
        self.ren.AddVolume(volume)
        self.ren.SetBackground(0.7, 0.82, 1)

        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(reader.GetOutputPort())
        outlineMapper = vtk.vtkPolyDataMapper()
        outlineMapper.SetInputConnection(outline.GetOutputPort())
        outlineActor = vtk.vtkActor()
        outlineActor.SetMapper(outlineMapper)
        self.ren.AddActor(outlineActor)

        self.ren.GetActiveCamera().Azimuth(45)
        self.ren.GetActiveCamera().Elevation(30)
        self.ren.ResetCameraClippingRange()
        self.ren.ResetCamera()
        
        self.iren.Initialize()
        self.ren.Render()
        self.iren.Start()

if __name__ == '__main__':
    # Create an application
    app = QApplication(sys.argv)
    
    # Create main window
    mainwindow = MainWindow()
    mainwindow.show()

    # Add view to mainwindow
    view1 = VolumeRender(mainwindow, 0, 0)
    view1.render('./data.nii', usingMask=True, maskpath='./mask.nii')

    view2 = VolumeRender(mainwindow, 0, 1)
    view2.render('./data.nii')

    sys.exit(app.exec_())
