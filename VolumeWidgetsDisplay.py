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
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

	def main(self, x, y, z):
		self.x = 0
		self.y = 0
		self.z = 0

		# Read DICOM images
		folder = 'E:/COVID_CHEST/A034518/4'
		reader = vtk.vtkDICOMImageReader()
		reader.SetDirectoryName(folder)
		reader.Update()

		xMin, xMax, yMin, yMax, zMin, zMax = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0))
		if (x < xMax and x >= xMin):
			self.x = x
		if (y < yMax and y >= yMin):
			self.y = y
		if (z < zMax and z >= zMin):
			self.z = z

		spacing = reader.GetOutput().GetSpacing()
		sx, sy, sz = spacing

		origin = reader.GetOutput().GetOrigin()
		ox, oy, oz = origin

		outline = vtk.vtkOutlineFilter()
		outline.SetInputConnection(reader.GetOutputPort())
		
		mapper = vtk.vtkPolyDataMapper()
		mapper.SetInputConnection(outline.GetOutputPort())
		
		actor = vtk.vtkActor()
		actor.SetMapper(mapper)

		renWin = vtk.vtkRenderWindow()
		# ren = vtk.vtkRenderer()
		ren1 = vtk.vtkRenderer()
		ren2 = vtk.vtkRenderer()
		ren3 = vtk.vtkRenderer()
		iren = vtk.vtkRenderWindowInteractor()
		# style = vtk.vtkInteractorStyleImage()
		# iren = vtk.vtkRenderWindowInteractor()
		# iren.SetInteractorStyle(style)
		renWin.AddRenderer(ren1)
		iren.SetRenderWindow(renWin)

		# ren.AddActor(actor)
		

		picker = vtk.vtkCellPicker()
		picker.SetTolerance(0.005)

		planeWidgetX = vtk.vtkImagePlaneWidget()
		planeWidgetX.SetInteractor(iren)
		planeWidgetX.SetMarginSizeX(0.0)
		planeWidgetX.SetMarginSizeY(0.0)
		planeWidgetX.SetKeyPressActivationValue('x')
		planeWidgetX.SetPicker(picker)
		planeWidgetX.RestrictPlaneToVolumeOn()
		planeWidgetX.GetPlaneProperty().SetColor(0.0, 0.0, 1.0)
		planeWidgetX.DisplayTextOn()
		# planeWidgetX.TextureInterpolateOn()
		planeWidgetX.TextureInterpolateOff()
		planeWidgetX.SetResliceInterpolateToLinear()
		planeWidgetX.SetInputData(reader.GetOutput())
		planeWidgetX.SetPlaneOrientationToXAxes()
		planeWidgetX.SetSliceIndex(self.x)
		planeWidgetX.GetTexturePlaneProperty().SetOpacity(1)
		planeWidgetX.On()

		iren.SetRenderWindow(renWin)
		renWin.AddRenderer(ren2)


		planeWidgetY = vtk.vtkImagePlaneWidget()
		planeWidgetY.SetMarginSizeX(0.0)
		planeWidgetY.SetMarginSizeY(0.0)
		planeWidgetY.SetInteractor(iren)
		planeWidgetY.SetKeyPressActivationValue('y')
		planeWidgetY.SetPicker(picker)
		planeWidgetY.RestrictPlaneToVolumeOn()
		planeWidgetY.GetPlaneProperty().SetColor(1.0, 0.0, 0.0)
		planeWidgetY.DisplayTextOn()
		# planeWidgetY.TextureInterpolateOn()
		planeWidgetY.TextureInterpolateOff()
		planeWidgetY.SetResliceInterpolateToLinear()
		planeWidgetY.SetInputData(reader.GetOutput())
		planeWidgetY.SetPlaneOrientationToYAxes()
		planeWidgetY.SetSliceIndex(self.y)
		planeWidgetY.GetTexturePlaneProperty().SetOpacity(1)
		planeWidgetY.On()

		iren.SetRenderWindow(renWin)
		renWin.AddRenderer(ren3)


		planeWidgetZ = vtk.vtkImagePlaneWidget()
		# planeWidgetZ.SetMarginSizeX(0.0)
		# planeWidgetZ.SetMarginSizeY(0.0)
		planeWidgetZ.SetInteractor(iren)
		planeWidgetZ.SetKeyPressActivationValue('z')
		planeWidgetZ.SetPicker(picker)
		planeWidgetZ.RestrictPlaneToVolumeOn()
		planeWidgetZ.GetPlaneProperty().SetColor(0.0, 1.0, 0.0)
		planeWidgetZ.DisplayTextOn()
		# planeWidgetZ.TextureInterpolateOn()
		planeWidgetZ.TextureInterpolateOff()
		planeWidgetZ.SetResliceInterpolateToLinear()
		planeWidgetZ.SetInputData(reader.GetOutput())
		planeWidgetZ.SetPlaneOrientationToZAxes()
		planeWidgetZ.SetSliceIndex(self.z)
		planeWidgetZ.GetTexturePlaneProperty().SetOpacity(1)
		planeWidgetZ.On()

		iren.SetRenderWindow(renWin)
		ren1.AddActor(actor)
		ren2.AddActor(actor)
		ren3.AddActor(actor)




		# cbk = vtkWidgetWindowLevelCallback()
		# cbk.WidgetX = planeWidgetX
		# cbk.WidgetY = planeWidgetY
		# cbk.WidgetZ = planeWidgetZ
		# cbk.actor = actor
		# iren.AddObserver('xx', cbk.execute)
		# cbk.Delete

		

		colorMap1 = vtk.vtkImageMapToColors()
		colorMap1.PassAlphaToOutputOff() # use in RGBA
		colorMap1.SetActiveComponent(0)
		colorMap1.SetOutputFormatToLuminance()
		colorMap1.SetInputData(planeWidgetX.GetResliceOutput())
		colorMap1.SetLookupTable(planeWidgetX.GetLookupTable())
		actor1 = vtk.vtkImageActor()
		actor1.PickableOff()
		actor1.SetInputData(colorMap1.GetOutput())

		colorMap2 = vtk.vtkImageMapToColors()
		colorMap2.PassAlphaToOutputOff() # use in RGBA
		colorMap2.SetActiveComponent(0)
		colorMap2.SetOutputFormatToLuminance()
		colorMap2.SetInputData(planeWidgetY.GetResliceOutput())
		colorMap2.SetLookupTable(planeWidgetY.GetLookupTable())
		actor2 = vtk.vtkImageActor()
		actor2.PickableOff()
		actor2.SetInputData(colorMap2.GetOutput())

		colorMap3 = vtk.vtkImageMapToColors()
		colorMap3.PassAlphaToOutputOff() # use in RGBA
		colorMap3.SetActiveComponent(0)
		colorMap3.SetOutputFormatToLuminance()
		colorMap3.SetInputData(planeWidgetZ.GetResliceOutput())
		colorMap3.SetLookupTable(planeWidgetZ.GetLookupTable())
		actor3 = vtk.vtkImageActor()
		actor3.PickableOff()
		actor3.SetInputData(colorMap3.GetOutput())


		# # ren.AddActor(actor)
		ren1.AddActor(actor1)
		ren2.AddActor(actor2)
		ren3.AddActor(actor3)

		# ren.SetBackground(0.3, 0.3, 0.6)
		ren1.SetBackground(1.0, 0.0, 0.0)
		ren2.SetBackground(0.0, 1.0, 0.0)
		ren3.SetBackground(0.0, 0.0, 1.0)
		renWin.SetSize(600, 400)
		# ren.SetViewport(0, 0.5, 0.5, 1)
		ren1.SetViewport(0.5, 0.5, 1, 1)
		ren2.SetViewport(0, 0, 0.5, 0.5)
		ren3.SetViewport(0.5, 0, 1, 0.5)

		iren.Initialize()
		iren.Start()
		renWin.Render()




if __name__ == '__main__':
	view = VolumeWidget()
	view.main(255, 255, 255)