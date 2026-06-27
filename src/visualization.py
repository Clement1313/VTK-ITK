import vtk


def display(filename):

    reader = vtk.vtkNrrdReader()
    reader.SetFileName(filename)
    reader.Update()

    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)

    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0, 0, 0, 0)
    color.AddRGBPoint(1000, 1, 1, 1)

    opacity = vtk.vtkPiecewiseFunction()
    opacity.AddPoint(0, 0)
    opacity.AddPoint(1000, 0.8)

    prop = vtk.vtkVolumeProperty()
    prop.SetColor(color)
    prop.SetScalarOpacity(opacity)
    prop.ShadeOff()

    volume.SetProperty(prop)

    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.ResetCamera()

    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    window.Render()
    interactor.Start()


if __name__ == "__main__":
    # display("Data/case6_gre1.nrrd")
    display("results/registered_translation.nrrd")
