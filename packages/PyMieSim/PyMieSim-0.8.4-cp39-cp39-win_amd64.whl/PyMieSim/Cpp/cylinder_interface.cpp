#include <pybind11/pybind11.h>

#include "Cylinder.cpp"

PYBIND11_MODULE(CylinderInterface, module)
{
    module.doc() = "Lorenz-Mie Theory (LMT) C++ binding module for PyMieSim Python package.";


     pybind11::class_<CYLINDER::State>(module, "CppCylinderState");


      pybind11::class_<CYLINDER::Scatterer>(module, "CYLINDER")
      .def(pybind11::init<double&, double&, double&, complex128&, double&, CVector&>(),
           pybind11::arg("Wavelength"),
           pybind11::arg("Amplitude"),
           pybind11::arg("Diameter"),
           pybind11::arg("Index"),
           pybind11::arg("nMedium"),
           pybind11::arg("Jones")
          )

       .def("S1S2",
            &CYLINDER::Scatterer::get_s1s2_py,
            pybind11::arg("Phi") )

      .def("Fields",
           &CYLINDER::Scatterer::get_unstructured_fields_py,
           pybind11::arg("Phi"),
           pybind11::arg("Theta"),
           pybind11::arg("R") )

      .def("FullFields",
           &CYLINDER::Scatterer::get_full_structured_fields_py,
           pybind11::arg("Sampling"),
           pybind11::arg("R") )

      .def("a1n", pybind11::overload_cast<>(&CYLINDER::Scatterer::get_a1n_py))
      .def("b1n", pybind11::overload_cast<>(&CYLINDER::Scatterer::get_b1n_py))
      .def("a2n", pybind11::overload_cast<>(&CYLINDER::Scatterer::get_a2n_py))
      .def("b2n", pybind11::overload_cast<>(&CYLINDER::Scatterer::get_b2n_py))

      .def_property_readonly("Qsca",  &CYLINDER::Scatterer::get_Qsca)
      .def_property_readonly("Qext",  &CYLINDER::Scatterer::get_Qext)
      .def_property_readonly("Qabs",  &CYLINDER::Scatterer::get_Qabs)
      .def_property_readonly("Qback", &CYLINDER::Scatterer::get_Qback)
      .def_property_readonly("Qpr",   &CYLINDER::Scatterer::get_Qpr)

      .def_property_readonly("Csca",  &CYLINDER::Scatterer::get_Csca)
      .def_property_readonly("Cext",  &CYLINDER::Scatterer::get_Cext)
      .def_property_readonly("Cabs",  &CYLINDER::Scatterer::get_Cabs)
      .def_property_readonly("Cback", &CYLINDER::Scatterer::get_Cback)
      .def_property_readonly("Cpr",   &CYLINDER::Scatterer::get_Cpr)

      .def_property_readonly("g",     &CYLINDER::Scatterer::get_g)

      .def_readwrite("State",         &CYLINDER::Scatterer::state)
      .def_readwrite("Area",          &CYLINDER::Scatterer::Area)
      .def_readwrite("SizeParameter", &CYLINDER::Scatterer::SizeParameter)
      ;
}







// -
