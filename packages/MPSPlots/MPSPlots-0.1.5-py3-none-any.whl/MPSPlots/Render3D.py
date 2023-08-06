#   !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyvista
import numpy
import matplotlib


class Scene3D:
    def __init__(self, shape: tuple = (1, 1),
                       unit_size: tuple = (800, 800),
                       window_size: tuple = None, **kwargs):

        if window_size is None:
            window_size = (unit_size[1] * shape[1], unit_size[0] * shape[0])

        self.Figure = pyvista.Plotter(theme=pyvista.themes.DocumentTheme(),
                                      window_size=window_size,
                                      shape=shape, **kwargs)

    def Add_Unstructured(self, Coordinate: numpy.ndarray, Scalar: numpy.ndarray = None, Plot: tuple = (0, 0), **kwargs):
        self.Figure.subplot(*Plot)
        Coordinate = numpy.array(Coordinate).T
        Points = pyvista.wrap(Coordinate)
        self.Figure.add_points(Points, scalars=Scalar, point_size=20, render_points_as_spheres=True, **kwargs)

    def Add_Mesh(self, Coordinate: numpy.ndarray, Plot: tuple = (0, 0), cmap='seismic', **kwargs):
        if isinstance(cmap, str):  # works only for matplotlib 3.6.1
            cmap = matplotlib.colormaps[cmap]

        self.Figure.subplot(*Plot)
        mesh = pyvista.StructuredGrid(*Coordinate)

        self.Figure.add_mesh(mesh=mesh, cmap=cmap, **kwargs)

        return self.Figure

    def Add_theta_vector_field(self, Plot, Radius=1.03 / 2):
        self.Figure.subplot(*Plot)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        Theta_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, Radius, [1], [0], [0])], axis=1)

        Spherical_Vector = pyvista.grid_from_sph_coords(theta, phi, Radius)

        Spherical_Vector.point_data["Theta"] = Theta_vector * 0.1

        self.Figure.add_mesh(Spherical_Vector.glyph(orient="Theta", scale="Theta", tolerance=0.005), color='k')

    def Add_phi_vector_field(self, Plot, Radius=1.03 / 2):
        self.Figure.subplot(*Plot)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        Phi_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, Radius, [0], [1], [0])], axis=1)

        Spherical_Vector = pyvista.grid_from_sph_coords(theta, phi, Radius)

        Spherical_Vector.point_data["Phi"] = Phi_vector * 0.1

        self.Figure.add_mesh(Spherical_Vector.glyph(orient="Phi", scale="Phi", tolerance=0.005), color='k')

    def Add_r_vector_field(self, Plot, R=[1.03 / 2]):
        self.Figure.subplot(*Plot)
        theta = numpy.arange(0, 360, 10)
        phi = numpy.arange(180, 0, -10)

        R_vector = numpy.stack([i.transpose().swapaxes(-2, -1).ravel("C") for i in pyvista.transform_vectors_sph_to_cart(theta, phi, R, *[0, 0, 1])], axis=1)

        Spherical_Vector = pyvista.grid_from_sph_coords(theta, phi, R)

        Spherical_Vector.point_data["R"] = R_vector * 0.1

        self.Figure.add_mesh(Spherical_Vector.glyph(orient="R", scale="R", tolerance=0.005), color='k')

    def __add_unit_sphere__(self, Plot: tuple = (0, 0), **kwargs):
        self.Figure.subplot(*Plot)
        sphere = pyvista.Sphere(radius=1)
        self.Figure.add_mesh(sphere, opacity=0.3)

    def __add_axes__(self, Plot: tuple = (0, 0)):
        self.Figure.subplot(*Plot)
        self.Figure.add_axes_at_origin(labels_off=True)

    def __add__text__(self, Plot: tuple = (0, 0), Text='', **kwargs):
        self.Figure.subplot(*Plot)
        self.Figure.add_text(Text, **kwargs)

    def Show(self, SaveDir: str = None):
        self.Figure.show(screenshot=SaveDir)

        return self

    def Close(self):
        self.Figure.close()
