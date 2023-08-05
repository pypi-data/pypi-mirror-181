#ifndef SETS_H
#define SETS_H

#include "Definitions.cpp"
#include "Sources.cpp"
#include "Sphere.cpp"
#include "Cylinder.cpp"
#include "CoreShell.cpp"
#include "Detectors.cpp"

namespace SPHERE
{
  class Set
  {
    public:
      DVector Diameter;
      CVector Index;
      std::vector<CVector> Material;
      DVector nMedium;
      bool BoundedIndex;
      std::vector<State> States;

      Set(){}
      Set(DVector &Diameter, std::vector<std::vector<complex128>> &Material, DVector &nMedium)
          : Diameter(Diameter), Material(Material), nMedium(nMedium)
          {
            BoundedIndex=true;
          }

      Set(DVector &Diameter, std::vector<complex128> &Index, DVector &nMedium)
          : Diameter(Diameter), Index(Index), nMedium(nMedium)
          {
            BoundedIndex=false;
          }

      State operator[](size_t idx){return this->States[idx];}

   };
}


namespace CYLINDER
{
  class Set
  {
    public:
      DVector Diameter;
      std::vector<complex128> Index;
      std::vector<std::vector<complex128>> Material;
      DVector nMedium;
      bool BoundedIndex;
      std::vector<State> States;

      Set(){}
      Set(DVector &Diameter, std::vector<std::vector<complex128>> &Material, DVector &nMedium)
          : Diameter(Diameter), Material(Material), nMedium(nMedium){BoundedIndex=true;}

      Set(DVector &Diameter, std::vector<complex128> &Index, DVector &nMedium)
          : Diameter(Diameter), Index(Index), nMedium(nMedium){BoundedIndex=false;}

      State operator[](size_t idx){return this->States[idx];}

  };
}


namespace CORESHELL
{
  class Set
  {
    public:
      DVector CoreDiameter, ShellDiameter;
      std::vector<complex128> CoreIndex, ShellIndex;
      std::vector<CVector> CoreMaterial, ShellMaterial;
      DVector nMedium;
      bool BoundedCore, BoundedShell;
      std::vector<State> States;

      Set(){}

      Set(DVector &CoreDiameter, DVector &ShellDiameter, CVector &CoreIndex, CVector &ShellIndex, DVector &nMedium)
      : CoreDiameter(CoreDiameter), ShellDiameter(ShellDiameter), CoreIndex(CoreIndex), ShellIndex(ShellIndex), nMedium(nMedium)
        { BoundedCore=false; BoundedShell=false; }

      Set(DVector &CoreDiameter, DVector &ShellDiameter, CVector &CoreIndex, std::vector<CVector> &ShellMaterial, DVector &nMedium)
      : CoreDiameter(CoreDiameter), ShellDiameter(ShellDiameter), CoreIndex(CoreIndex), ShellMaterial(ShellMaterial), nMedium(nMedium)
        { BoundedCore=false; BoundedShell=true; }

      Set(DVector &CoreDiameter, DVector &ShellDiameter, std::vector<CVector> &CoreMaterial, CVector &ShellIndex, DVector &nMedium)
      : CoreDiameter(CoreDiameter), ShellDiameter(ShellDiameter), CoreMaterial(CoreMaterial), ShellIndex(ShellIndex), nMedium(nMedium)
        {BoundedCore=true; BoundedShell=false;}

      Set(DVector &CoreDiameter, DVector &ShellDiameter, std::vector<CVector> &CoreMaterial, std::vector<CVector> &ShellMaterial, DVector &nMedium)
      : CoreDiameter(CoreDiameter), ShellDiameter(ShellDiameter), CoreMaterial(CoreMaterial), ShellMaterial(ShellMaterial), nMedium(nMedium)
        {BoundedCore=true; BoundedShell=true;}

        State operator[](size_t idx){return this->States[idx];}
  };
}





namespace SOURCE
{
    class Set
    {
      public:
        DVector Wavelength;
        std::vector<CVector> Jones;
        DVector Amplitude;
        std::vector<State> States;

        Set(){}
        Set(DVector &Wavelength, std::vector<CVector> &Jones, DVector &Amplitude)
        : Wavelength(Wavelength), Jones(Jones), Amplitude(Amplitude)
        {}

        State operator[](size_t idx){return this->States[idx];}

    };
}

namespace DETECTOR
{
  class Set
  {
    public:
      std::vector<CVector> ScalarField;
      DVector NA, PhiOffset, GammaOffset, Filter;
      bool Coherent, PointCoupling;
      std::vector<State> States;

      Set(){}
      Set(std::vector<CVector> &ScalarField,
          DVector &NA,
          DVector &PhiOffset,
          DVector &GammaOffset,
          DVector &Filter,
          bool    &Coherent,
          bool    &PointCoupling)
      : ScalarField(ScalarField),
        NA(NA),
        PhiOffset(PhiOffset),
        GammaOffset(GammaOffset),
        Filter(Filter),
        Coherent(Coherent),
        PointCoupling(PointCoupling)
      {}

      State operator[](size_t idx){return this->States[idx];}

  };

}


#endif
