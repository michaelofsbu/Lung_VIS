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



class Display2DDicomSlices():
	def render(self, folder):
		# Read DICOM images
		# folder = 'E:/COVID_CHEST/A034518/4'
		reader = vtk.vtkDICOMImageReader()
		reader.SetDirectoryName(folder)
		reader.Update()

		#Create Sagittal Slice Matrix
		sagittal = vtk.vtkMatrix4x4()
		# sagittal.DeepCopy((0, 0, -1, 1,
		# 				   1, 0, 0, 1,
		# 				   0, -1, 0, 1,
		# 				   0, 0, 0, 1))

		# Reslice image
		# widget = QVTKRenderWindowInteractor()
		slice = vtk.vtkImageReslice()
		slice.SetInputConnection(reader.GetOutputPort())
		slice.SetOutputDimensionality(2)
		slice.SetResliceAxes(sagittal)
		slice.SetInterpolationModeToLinear()

		# Display the image
		actor = vtk.vtkImageActor()
		actor.GetMapper().SetInputConnection(slice.GetOutputPort())

		renderer = vtk.vtkRenderer()
				
		
		# Remove Renderer And Reset
		renderer.RemoveAllViewProps()
		renderer.ResetCamera()
		renderer.AddActor(actor)
		renderer.SetBackground(1,1,1) # Background color white

		renderWindow = vtk.vtkRenderWindow()
		#renderWindow.SetWindowName("Test")
		renderWindow.AddRenderer(renderer)

		# Set up the interaction
		slice_interactorStyle = vtk.vtkInteractorStyleImage()
		slice_interactor = vtk.vtkRenderWindowInteractor()
		slice_interactor.SetInteractorStyle(slice_interactorStyle)
		slice_interactor.SetRenderWindow(renderWindow)
		
		
		renderWindow.Render()

		# Start interaction
		slice_interactor.Start()

if __name__ == '__main__':
	dirname = os.path.dirname(PySide2.__file__)
	plugin_path = os.path.join(dirname, 'plugins', 'platforms')
	os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

	# Create an application
	app = QApplication(sys.argv)

	# Add view to mainwindow
	view1 = Display2DDicomSlices()
	view1.render('E:/COVID_CHEST/A034518/4')

	sys.exit(app.exec_())