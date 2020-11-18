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

	def __init__(self, orientation, sliceIndexPercent):
		if (orientation in ['x', 'y', 'z']):
			self.orientation = orientation
		else:
			self.orientation = 'x'

		if (sliceIndexPercent > 1 or sliceIndexPercent < 0):
			self.sliceIndexPercent = 0.5
		else:
			self.sliceIndexPercent = sliceIndexPercent

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

		planeWidget = vtk.vtkImagePlaneWidget()
		planeWidget.SetInteractor(self.iren)
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
		planeWidget.SetInputData(reader.GetOutput())
		planeWidget.SetSliceIndex(self.sliceIndex)
		planeWidget.GetTexturePlaneProperty().SetOpacity(1)
		planeWidget.On()

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
		self.iren.Start()
		self.renWin.Render()




if __name__ == '__main__':
	dirname = os.path.dirname(PySide2.__file__)
	plugin_path = os.path.join(dirname, 'plugins', 'platforms')
	os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

	# Create an application
	app = QApplication(sys.argv)

	# Add view to mainwindow
	view1 = VolumeWidget('z', 0.4)
	view1.render('E:/COVID_CHEST/A034518/4')

	sys.exit(app.exec_())
	
