#include <pybind11/pybind11.h>

#include "CoreShell.cpp"

PYBIND11_MODULE(CoreShellInterface, module)
{
    module.doc() = "Lorenz-Mie Theory (LMT) C++ binding module for PyMieSim Python package.";


     pybind11::class_<CORESHELL::State>(module, "CppCoreShellState");


     pybind11::class_<CORESHELL::Scatterer>(module, "CORESHELL")
      .def(pybind11::init<double &, double &, double &, double &, complex128 &, complex128 &, double &, CVector &>(),
           pybind11::arg("Wavelength"),
           pybind11::arg("Amplitude"),
           pybind11::arg("CoreDiameter"),
           pybind11::arg("ShellDiameter"),
           pybind11::arg("CoreIndex"),
           pybind11::arg("ShellIndex"),
           pybind11::arg("nMedium"),
           pybind11::arg("Jones")
          )

       .def("S1S2",
            &CORESHELL::Scatterer::get_s1s2_py,
            pybind11::arg("Phi") )

      .def("Fields",
           &CORESHELL::Scatterer::get_unstructured_fields_py,
           pybind11::arg("Phi"),
           pybind11::arg("Theta"),
           pybind11::arg("R") )

      .def("FullFields",
           &CORESHELL::Scatterer::get_full_structured_fields_py,
           pybind11::arg("Sampling"),
           pybind11::arg("R") )

      .def("an", pybind11::overload_cast<>(&CORESHELL::Scatterer::get_an_py))
      .def("bn", pybind11::overload_cast<>(&CORESHELL::Scatterer::get_bn_py))

      .def_property_readonly("Qsca",  &CORESHELL::Scatterer::get_Qsca)
      .def_property_readonly("Qext",  &CORESHELL::Scatterer::get_Qext)
      .def_property_readonly("Qabs",  &CORESHELL::Scatterer::get_Qabs)
      .def_property_readonly("Qback", &CORESHELL::Scatterer::get_Qback)
      .def_property_readonly("Qpr",   &CORESHELL::Scatterer::get_Qpr)

      .def_property_readonly("Csca",  &CORESHELL::Scatterer::get_Csca)
      .def_property_readonly("Cext",  &CORESHELL::Scatterer::get_Cext)
      .def_property_readonly("Cabs",  &CORESHELL::Scatterer::get_Cabs)
      .def_property_readonly("Cback", &CORESHELL::Scatterer::get_Cback)
      .def_property_readonly("Cpr",   &CORESHELL::Scatterer::get_Cpr)

      .def_property_readonly("g",     &CORESHELL::Scatterer::get_g)

      .def_readwrite("State", &CORESHELL::Scatterer::state)
      .def_readwrite("Area", &CORESHELL::Scatterer::Area)
      .def_readwrite("SizeParameter", &CORESHELL::Scatterer::SizeParameter)
      ;
}







// -
