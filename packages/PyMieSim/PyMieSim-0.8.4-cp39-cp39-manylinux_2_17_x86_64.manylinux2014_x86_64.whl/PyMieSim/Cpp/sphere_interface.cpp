#include <pybind11/pybind11.h>

#include "Sphere.cpp"

PYBIND11_MODULE(SphereInterface, module)
{
    module.doc() = "Lorenz-Mie Theory (LMT) C++ binding module for PyMieSim Python package.";


      pybind11::class_<SPHERE::State>(module, "CppSphereState");


      pybind11::class_<SPHERE::Scatterer>(module, "SPHERE")
      .def(pybind11::init<double&, double&, double&, complex128&, double&, CVector&>(),
           pybind11::arg("Wavelength"),
           pybind11::arg("Amplitude"),
           pybind11::arg("Diameter"),
           pybind11::arg("Index"),
           pybind11::arg("nMedium"),
           pybind11::arg("Jones")
          )

      .def(pybind11::init<>())

      .def("S1S2",
      &SPHERE::Scatterer::get_s1s2_py,
      pybind11::arg("Phi") )

      .def("Fields",
      &SPHERE::Scatterer::get_unstructured_fields_py,
      pybind11::arg("Phi"),
      pybind11::arg("Theta"),
      pybind11::arg("R") )

      .def("FullFields",
      &SPHERE::Scatterer::get_full_structured_fields_py,
      pybind11::arg("Sampling"),
      pybind11::arg("R") )


      .def("an", pybind11::overload_cast<>(&SPHERE::Scatterer::get_an_py))
      .def("bn", pybind11::overload_cast<>(&SPHERE::Scatterer::get_bn_py))
      .def("cn", pybind11::overload_cast<>(&SPHERE::Scatterer::get_cn_py))
      .def("dn", pybind11::overload_cast<>(&SPHERE::Scatterer::get_dn_py))

      .def_property_readonly("Qsca",  &SPHERE::Scatterer::get_Qsca)
      .def_property_readonly("Qext",  &SPHERE::Scatterer::get_Qext)
      .def_property_readonly("Qabs",  &SPHERE::Scatterer::get_Qabs)
      .def_property_readonly("Qback", &SPHERE::Scatterer::get_Qback)
      .def_property_readonly("Qpr",   &SPHERE::Scatterer::get_Qpr)


      .def_property_readonly("Csca",  &SPHERE::Scatterer::get_Csca)
      .def_property_readonly("Cext",  &SPHERE::Scatterer::get_Cext)
      .def_property_readonly("Cabs",  &SPHERE::Scatterer::get_Cabs)
      .def_property_readonly("Cback", &SPHERE::Scatterer::get_Cback)
      .def_property_readonly("Cpr",   &SPHERE::Scatterer::get_Cpr)

      .def_property_readonly("g", &SPHERE::Scatterer::get_g)


      .def_readwrite("State", &SPHERE::Scatterer::state)
      .def_readwrite("Area", &SPHERE::Scatterer::Area)
      .def_readwrite("SizeParameter", &SPHERE::Scatterer::SizeParameter)
      ;
}







// -
