#include <pybind11/pybind11.h>

#include "Sets.cpp"


PYBIND11_MODULE(Sets, module)
{
      pybind11::class_<SPHERE::Set>(module, "CppSphereSet")
      .def(pybind11::init<DVector&, std::vector<complex128>&, DVector&>(),
           pybind11::arg("Diameter"),
           pybind11::arg("Index"),
           pybind11::arg("nMedium") )

      .def(pybind11::init<DVector&, std::vector<std::vector<complex128>>&, DVector&>(),
           pybind11::arg("Diameter"),
           pybind11::arg("Material"),
           pybind11::arg("nMedium") )
           ;

      pybind11::class_<CYLINDER::Set>(module, "CppCylinderSet")
      .def(pybind11::init<DVector&, CVector&, DVector&>(),
           pybind11::arg("Diameter"),
           pybind11::arg("Index"),
           pybind11::arg("nMedium")
           )

      .def(pybind11::init<DVector&, std::vector<std::vector<complex128>>&, DVector&>(),
           pybind11::arg("Diameter"),
           pybind11::arg("Material"),
           pybind11::arg("nMedium")
           );


    pybind11::class_<CORESHELL::Set>(module, "CppCoreShellSet")
    .def(pybind11::init<DVector&, DVector&, CVector&, CVector&, DVector&>(),
         pybind11::arg("CoreDiameter"),
         pybind11::arg("ShellDiameter"),
         pybind11::arg("CoreIndex"),
         pybind11::arg("ShellIndex"),
         pybind11::arg("nMedium") )

    .def(pybind11::init<DVector&, DVector&, CVector&, std::vector<CVector>&, DVector&>(),
         pybind11::arg("CoreDiameter"),
         pybind11::arg("ShellDiameter"),
         pybind11::arg("CoreIndex"),
         pybind11::arg("ShellMaterial"),
         pybind11::arg("nMedium"))

    .def(pybind11::init<DVector&, DVector&, std::vector<CVector>&, CVector&, DVector&>(),
         pybind11::arg("CoreDiameter"),
         pybind11::arg("ShellDiameter"),
         pybind11::arg("CoreMaterial"),
         pybind11::arg("ShellIndex"),
         pybind11::arg("nMedium") )

    .def(pybind11::init<DVector&, DVector&, std::vector<CVector>&, std::vector<CVector>&, DVector&>(),
         pybind11::arg("CoreDiameter"),
         pybind11::arg("ShellDiameter"),
         pybind11::arg("CoreMaterial"),
         pybind11::arg("ShellMaterial"),
         pybind11::arg("nMedium") )
         ;

      pybind11::class_<SOURCE::Set>(module, "CppSourceSet")
      .def(pybind11::init<DVector&, std::vector<CVector>&, DVector&>(),
           pybind11::arg("Wavelength"),
           pybind11::arg("Jones"),
           pybind11::arg("Amplitude") );


     pybind11::class_<DETECTOR::Set>(module, "CppDetectorSet")
     .def(pybind11::init<std::vector<CVector>&, DVector&, DVector&, DVector&, DVector&, bool&, bool&>(),
          pybind11::arg("ScalarField"),
          pybind11::arg("NA"),
          pybind11::arg("PhiOffset"),
          pybind11::arg("GammaOffset"),
          pybind11::arg("Filter"),
          pybind11::arg("Coherent"),
          pybind11::arg("PointCoupling")
          );

}






// -
