#include <pybind11/pybind11.h>

#include "FibonnaciMesh.cpp"

  PYBIND11_MODULE(Fibonacci, module) {
      module.doc() = "LGeneralized Lorenz-Mie Theory (GLMT) c++ binding module for light scattering from a spherical scatterer";

        pybind11::class_<FibonacciMesh>(module, "FIBONACCI")
        .def(pybind11::init<int, double, double, double>(),
             pybind11::arg("Sampling"),
             pybind11::arg("MaxAngle"),
             pybind11::arg("PhiOffset"),
             pybind11::arg("GammaOffset") )

        .def_property_readonly("X", &FibonacciMesh::get_x_py)
        .def_property_readonly("Y", &FibonacciMesh::get_y_py)
        .def_property_readonly("Z", &FibonacciMesh::get_z_py)

        .def_property_readonly("R", &FibonacciMesh::get_r_py)
        .def_property_readonly("Phi", &FibonacciMesh::get_phi_py)
        .def_property_readonly("Theta", &FibonacciMesh::get_theta_py)

        .def_readwrite("dOmega", &FibonacciMesh::dOmega)
        .def_readwrite("Omega", &FibonacciMesh::Omega)

        .def("ComputeVectorField", &FibonacciMesh::compute_vector_field)
        .def("ComputeHVProjection", &FibonacciMesh::compute_HV_projection)

        .def_property_readonly("ParaVector", &FibonacciMesh::GetPara)
        .def_property_readonly("PerpVector", &FibonacciMesh::GetPerp)

        .def_property_readonly("HPara", &FibonacciMesh::get_H_Para)
        .def_property_readonly("HPerp", &FibonacciMesh::get_H_Perp)
        .def_property_readonly("VPara", &FibonacciMesh::get_V_Para)
        .def_property_readonly("VPerp", &FibonacciMesh::get_V_Perp)
        ;
  }







// -
