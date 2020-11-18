import sys
import os
import PySide2
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication
import vtkmodules.all as vtk
from vtk import vtkActor
from vtk import vtkConeSource
from vtk import vtkPolyDataMapper
from vtk import vtkRenderer
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from abc import ABCMeta, abstractmethod
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class VolumeWidget():

    def __init__(self, sliceXIndexPercent, sliceYIndexPercent, sliceZIndexPercent):

        if (sliceXIndexPercent < 0 or sliceXIndexPercent > 1):
            self.sliceXIndexPercent = 0.5
        else:
            self.sliceXIndexPercent = sliceXIndexPercent

        if (sliceYIndexPercent < 0 or sliceYIndexPercent > 1):
            self.sliceYIndexPercent = 0.5
        else:
            self.sliceYIndexPercent = sliceYIndexPercent

        if (sliceZIndexPercent < 0 or sliceZIndexPercent > 1):
            self.sliceZIndexPercent = 0.5
        else:
            self.sliceZIndexPercent = sliceZIndexPercent
       


        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.iren = vtk.vtkRenderWindowInteractor()
        self.renWin.AddRenderer(self.ren)
        self.iren.SetRenderWindow(self.renWin)

    def render(self, datapath):    
        # Read DICOM images
        datapath = 'E:/COVID_CHEST/A034518/4'
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(datapath)
        reader.Update()

        xMin, xMax, yMin, yMax, zMin, zMax = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0))
        self.sliceXIndex = int((xMax - xMin) * self.sliceXIndexPercent + xMin)
        self.sliceYIndex = int((yMax - yMin) * self.sliceYIndexPercent + yMin)
        self.sliceZIndex = int((zMax - zMin) * self.sliceZIndexPercent + zMin)

        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(reader.GetOutputPort())
        
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(outline.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        self.style = vtk.vtkInteractorStyleTerrain()
        self.iren.SetInteractorStyle(self.style)
        self.iren.SetRenderWindow(self.renWin)

        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.005)

        planeWidgetX = vtk.vtkImagePlaneWidget()
        planeWidgetX.SetInteractor(self.iren)
        planeWidgetX.SetMarginSizeX(0.0)
        planeWidgetX.SetMarginSizeY(0.0)
        planeWidgetX.SetPicker(picker)
        planeWidgetX.RestrictPlaneToVolumeOn()
        planeWidgetX.GetPlaneProperty().SetColor(0.0, 0.0, 1.0)
        planeWidgetX.DisplayTextOn()
        planeWidgetX.UpdatePlacement()
        planeWidgetX.TextureInterpolateOff()
        planeWidgetX.SetResliceInterpolateToLinear()
        planeWidgetX.SetInputData(reader.GetOutput())
        planeWidgetX.SetPlaneOrientationToXAxes()
        planeWidgetX.SetSliceIndex(self.sliceXIndex)
        planeWidgetX.GetTexturePlaneProperty().SetOpacity(1)
        planeWidgetX.On()

        planeWidgetY = vtk.vtkImagePlaneWidget()
        planeWidgetY.SetInteractor(self.iren)
        planeWidgetY.SetMarginSizeX(0.0)
        planeWidgetY.SetMarginSizeY(0.0)
        planeWidgetY.SetPicker(picker)
        planeWidgetY.RestrictPlaneToVolumeOn()
        planeWidgetY.GetPlaneProperty().SetColor(1.0, 0.0, 0.0)
        planeWidgetY.DisplayTextOn()
        planeWidgetY.UpdatePlacement()
        planeWidgetY.TextureInterpolateOff()
        planeWidgetY.SetResliceInterpolateToLinear()
        planeWidgetY.SetInputData(reader.GetOutput())
        planeWidgetY.SetPlaneOrientationToYAxes()
        planeWidgetY.SetSliceIndex(self.sliceYIndex)
        planeWidgetY.GetTexturePlaneProperty().SetOpacity(1)
        planeWidgetY.On()

        planeWidgetZ = vtk.vtkImagePlaneWidget()
        planeWidgetZ.SetInteractor(self.iren)
        planeWidgetZ.SetMarginSizeX(0.0)
        planeWidgetZ.SetMarginSizeY(0.0)
        planeWidgetZ.SetPlaneOrientationToZAxes()
        planeWidgetZ.SetPicker(picker)
        planeWidgetZ.RestrictPlaneToVolumeOn()
        planeWidgetZ.GetPlaneProperty().SetColor(0.0, 1.0, 0.0)
        planeWidgetZ.DisplayTextOn()
        planeWidgetZ.UpdatePlacement()
        planeWidgetZ.TextureInterpolateOff()
        planeWidgetZ.SetResliceInterpolateToLinear()
        planeWidgetZ.SetInputData(reader.GetOutput())
        planeWidgetZ.SetSliceIndex(self.sliceZIndex)
        planeWidgetZ.GetTexturePlaneProperty().SetOpacity(1)
        planeWidgetZ.On()

        self.ren.AddActor(actor)

        ren1 = vtk.vtkRenderer()
        self.renWin.AddRenderer(ren1)
        self.iren.SetRenderWindow(self.renWin)
        

        planeWidgetX1 = vtk.vtkImagePlaneWidget()
        planeWidgetX1.SetInteractor(self.iren)
        planeWidgetX1.SetMarginSizeX(0.0)
        planeWidgetX1.SetMarginSizeY(0.0)
        planeWidgetX1.SetPicker(picker)
        planeWidgetX1.RestrictPlaneToVolumeOn()
        planeWidgetX1.GetPlaneProperty().SetColor(0.0, 0.0, 1.0)
        planeWidgetX1.DisplayTextOff()
        planeWidgetX1.TextureInterpolateOff()
        planeWidgetX1.SetResliceInterpolateToLinear()
        planeWidgetX1.SetInputData(reader.GetOutput())
        planeWidgetX1.SetPlaneOrientationToXAxes()
        planeWidgetX1.SetSliceIndex(self.sliceXIndex)
        planeWidgetX1.GetTexturePlaneProperty().SetOpacity(1)
        planeWidgetX1.On()

        ren1.AddActor(actor)



        ren2 = vtk.vtkRenderer()
        self.renWin.AddRenderer(ren2)
        self.iren.SetRenderWindow(self.renWin)
        
        
        planeWidgetY1 = vtk.vtkImagePlaneWidget()
        planeWidgetY1.SetInteractor(self.iren)
        planeWidgetY1.SetMarginSizeX(0.0)
        planeWidgetY1.SetMarginSizeY(0.0)
        planeWidgetY1.SetPicker(picker)
        planeWidgetY1.RestrictPlaneToVolumeOn()
        planeWidgetY1.GetPlaneProperty().SetColor(1.0, 0.0, 0.0)
        planeWidgetY1.DisplayTextOn()
        planeWidgetY1.TextureInterpolateOff()
        planeWidgetY1.SetResliceInterpolateToLinear()
        planeWidgetY1.SetInputData(reader.GetOutput())
        planeWidgetY1.SetPlaneOrientationToYAxes()
        planeWidgetY1.SetSliceIndex(self.sliceYIndex)
        planeWidgetY1.GetTexturePlaneProperty().SetOpacity(1)
        planeWidgetY1.On()

        ren2.AddActor(actor)


        ren3 = vtk.vtkRenderer()
        self.renWin.AddRenderer(ren3)
        self.iren.SetRenderWindow(self.renWin)
        

        planeWidgetZ1 = vtk.vtkImagePlaneWidget()
        planeWidgetZ1.SetInteractor(self.iren)
        planeWidgetZ1.SetMarginSizeX(0.0)
        planeWidgetZ1.SetMarginSizeY(0.0)
        planeWidgetZ1.SetPlaneOrientationToZAxes()
        planeWidgetZ1.SetPicker(picker)
        planeWidgetZ1.RestrictPlaneToVolumeOn()
        planeWidgetZ1.GetPlaneProperty().SetColor(0.0, 1.0, 0.0)
        planeWidgetZ1.DisplayTextOn()
        planeWidgetZ1.TextureInterpolateOff()
        planeWidgetZ1.SetResliceInterpolateToLinear()
        planeWidgetZ1.SetInputData(reader.GetOutput())
        planeWidgetZ1.SetSliceIndex(self.sliceZIndex)
        planeWidgetZ1.GetTexturePlaneProperty().SetOpacity(1)
        planeWidgetZ1.On()

        ren3.AddActor(actor)


        ren1.SetBackground(1.0, 0.0, 0.0)
        ren2.SetBackground(0.0, 1.0, 0.0)
        ren3.SetBackground(0.0, 0.0, 1.0)
        
        self.renWin.SetSize(600,400)
        self.ren.SetViewport(0, 0.5, 0.5, 1)
        ren1.SetViewport(0.5, 0.5, 1, 1)
        ren2.SetViewport(0, 0, 0.5 , 0.5)
        ren3.SetViewport(0.5, 0 ,1, 0.5)
        

        self.iren.Initialize()
        self.iren.Start()
        self.renWin.Render()




if __name__ == '__main__':
    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

    # Create an application
    app = QApplication(sys.argv)

    # Add view to mainwindow
    view1 = VolumeWidget(0.5, 0.7, 0.2)
    view1.render('E:/COVID_CHEST/A034518/4')

    sys.exit(app.exec_())
    
