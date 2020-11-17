from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication
import vtk
from vtk.util.vtkImageImportFromArray import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
from abc import ABCMeta, abstractmethod
import SimpleITK as sitk
import numpy as np
import os

# Main Window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.volumeReader = vtk.vtkNIFTIImageReader()
        self.maskReader = vtk.vtkNIFTIImageReader()
        self.volumeloaded = False
        self.maskloaded = False
        self.init_ui()
    
    def init_ui(self):
        mainLayout = QtWidgets.QVBoxLayout()
        menu = self.menuBar()
        self.renderLayout = QtWidgets.QGridLayout()

        fileMenu = menu.addMenu('File')
        loadMenu = QtWidgets.QMenu('Load',self)
        loadVolumeAct = QtWidgets.QAction('New File', self)
        loadVolumeAct.triggered.connect(self.loadVolume)
        loadMenu.addAction(loadVolumeAct)
        loadMaskAct = QtWidgets.QAction('New Mask', self)
        loadMaskAct.triggered.connect(self.loadMask)
        loadMenu.addAction(loadMaskAct)
        fileMenu.addMenu(loadMenu)

        mainLayout.addWidget(menu)
        mainLayout.addLayout(self.renderLayout)
        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.setWindowTitle("Lung CT Visulization")
        self.resize(800, 700)

    def loadVolume(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        #print(filename)
        self.volumeReader.SetFileName(filename[0])
        self.volumeloaded = True

    def loadMask(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        #print(filename)
        self.maskReader.SetFileName(filename[0])
        self.maskloaded = True


# Sub windows base class
class SubWindow:
    __metaclass__ = ABCMeta
 
    def __init__(self, parent, row, column):
        # Interface to the main window
        self.vtkWidget = QVTKRenderWindowInteractor()
        parent.renderLayout.addWidget(self.vtkWidget, row, column)
        # Create standard render, render window and interactor
        self.ren = vtk.vtkRenderer()
        self.renWin = self.vtkWidget.GetRenderWindow()
        self.renWin.AddRenderer(self.ren)
        self.iren = self.renWin.GetInteractor()
        self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.parent = parent
    
    @abstractmethod
    def render(self, datapath = None):
        pass

# Volumer Rendering Window
class VolumeRender(SubWindow):

    def render(self, datapath, usingMask = False, maskpath = None):

        #data = sitk.ReadImage(datapath)
        #slices = sitk.GetArrayFromImage(data)
        #spacing = data.GetSpacing()
        #spacing = self.parent.volumeReader.GetDataSpacing()
        #origin = (0,0,0)
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(datapath)
        spacing = reader.GetDataSpacing()
        origin = reader.GetDataOrigin()
        if usingMask:
            maskreader = vtk.vtkNIFTIImageReader()
            maskreader.SetFileName(maskpath)
            maskreader.SetDataSpacing(spacing)
            maskreader.SetDataOrigin(origin)
            maskreader.Update()

        # Create reader for the data
        #reader = vtkImageImportFromArray()
        #reader = self.parent.volumeReader
        #reader.SetArray(slices)
        #reader.SetDataSpacing(spacing)
        #reader.SetDataOrigin(origin)
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
        volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
        volumeMapper.SetInputConnection(reader.GetOutputPort())
        if usingMask:
            volumeMapper.SetMaskTypeToBinary()
            volumeMapper.SetMaskInput(maskreader.GetOutput())
            

        # The volume holds the mapper and the property and
        # can be used to position/orient the volume.
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
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

# Class for 2d slice rendering
class SliceRender(SubWindow):
    def __init__(self, parent, row, column, orientation, sliceIndexPercent):
        super().__init__(parent, row, column)
        if (orientation in ['x', 'y', 'z']):
            self.orientation = orientation
        else:
            self.orientation = 'x'

        if (sliceIndexPercent > 1 or sliceIndexPercent < 0):
            self.sliceIndexPercent = 0.5
        else:
            self.sliceIndexPercent = sliceIndexPercent

    def render(self, datapath):    
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(datapath)
        reader.Update()

        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(reader.GetOutputPort())
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(outline.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        style = vtk.vtkInteractorStyleTerrain()
        self.iren.SetInteractorStyle(style)
        self.iren.SetRenderWindow(self.renWin)

        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.005)

        planeWidget = vtk.vtkImagePlaneWidget()
        planeWidget.SetInteractor(self.iren)
        planeWidget.SetInputData(reader.GetOutput())
        planeWidget.SetMarginSizeX(0.0)
        planeWidget.SetMarginSizeY(0.0)
            
        xMin, xMax, yMin, yMax, zMin, zMax = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0))
        if (self.orientation == 'x'):
            self.sliceIndex = int(self.sliceIndexPercent * (xMax - xMin) + xMin)
            planeWidget.SetPlaneOrientationToXAxes()
        elif (self.orientation == 'y'):
            self.sliceIndex = int(self.sliceIndexPercent * (yMax - yMin) + yMin)
            planeWidget.SetPlaneOrientationToYAxes()
        elif (self.orientation == 'z'):
            self.sliceIndex = int(self.sliceIndexPercent * (zMax - zMin) + zMin)
            planeWidget.SetPlaneOrientationToZAxes()
        else:
            pass
        print("You are looking slice {} on {}-axis".format(self.sliceIndex, self.orientation))

        
        # planeWidget.SetKeyPressActivationValue(self.orientation)
        planeWidget.SetPicker(picker)
        planeWidget.RestrictPlaneToVolumeOn()
        planeWidget.GetPlaneProperty().SetColor(0.0, 0.0, 1.0)
        planeWidget.DisplayTextOn()
        planeWidget.UpdatePlacement()
        planeWidget.TextureInterpolateOff()
        planeWidget.SetResliceInterpolateToLinear()
        planeWidget.SetSliceIndex(self.sliceIndex)
        planeWidget.GetTexturePlaneProperty().SetOpacity(1)
        planeWidget.On()
        planeWidget.InteractionOn()

        self.ren.AddActor(actor)
        

        colorMap = vtk.vtkImageMapToColors()
        colorMap.PassAlphaToOutputOff() # use in RGBA
        colorMap.SetActiveComponent(0)
        colorMap.SetOutputFormatToLuminance()
        colorMap.SetInputData(planeWidget.GetResliceOutput())
        colorMap.SetLookupTable(planeWidget.GetLookupTable())
        actor1 = vtk.vtkImageActor()
        actor1.PickableOff()
        actor1.SetInputData(colorMap.GetOutput())
        self.ren.AddActor(actor1)

        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()
        

if __name__ == '__main__':
    # Create an application
    app = QApplication(sys.argv)
    
    # Create main window
    mainwindow = MainWindow()
    mainwindow.show()

    # Add view to mainwindow
    view1 = VolumeRender(mainwindow, 0, 1)
    view1.render('./data.nii', usingMask=True, maskpath='./mask.nii')

    view2 = SliceRender(mainwindow, 0, 0, 'z', 0.4)
    view2.render('./data.nii')

    view3 = SliceRender(mainwindow, 1, 0, 'x', 0.4)
    view3.render('./data.nii')

    view4 = SliceRender(mainwindow, 1, 1, 'y', 0.4)
    view4.render('./data.nii')

    sys.exit(app.exec_())
