#ifndef DETECTOR_H
#define DETECTOR_H

#include "FibonnaciMesh.cpp"

namespace DETECTOR
{

  struct State
  {
    CVector ScalarField;
    double NA, PhiOffset, GammaOffset, Filter;
    bool Coherent, PointCoupling;
    State(){}
    State(CVector &ScalarField,
          double &NA,
          double &PhiOffset,
          double &GammaOffset,
          double &Filter,
          bool   &Coherent,
          bool   &PointCoupling)
          : ScalarField(ScalarField),
          NA(NA),
          PhiOffset(PhiOffset),
          GammaOffset(GammaOffset),
          Filter(Filter),
          Coherent(Coherent),
          PointCoupling(PointCoupling){}
  };

  class Detector
  {
  public:
     FibonacciMesh Mesh;
     State state;
     bool Coherent;

     size_t   GetSampling()      {return state.ScalarField.size();}
     CVector  GetScalarField()   {return state.ScalarField;}
     double   GetNA()            {return state.NA;}
     double   GetPhi()           {return state.PhiOffset;}
     double   GetGamma()         {return state.GammaOffset;}
     bool     GetCoherent()      {return state.Coherent;}
     bool     GetPointCoupling() {return state.PointCoupling;}
     double   GetMaxAngle()      {return Mesh.NA2Angle(GetNA());}

     Detector(){}


     Detector(CVector &ScalarField, double &NA, double& PhiOffset, double &GammaOffset, double &Filter, bool &Coherent, bool &PointCoupling)
     : state(ScalarField, NA, PhiOffset, GammaOffset, Filter, Coherent, PointCoupling)
     {
       this->Mesh = FibonacciMesh( GetSampling(), GetMaxAngle(), GetPhi(), GetGamma());
     }

     Detector(State &state) : state(state)
     {
       this->Mesh = FibonacciMesh( GetSampling(), GetMaxAngle(), GetPhi(), GetGamma());
     }


     template <class T> double Coupling(T &Scatterer)
     {
       if (GetPointCoupling() && GetCoherent())
            return PointCouplingCoherent(Scatterer);

       if (!GetPointCoupling() && GetCoherent())
            return MeanCouplingCoherent(Scatterer);

       if (GetPointCoupling() && !GetCoherent())
            return PointCouplingNoCoherent(Scatterer);

       if (!GetPointCoupling() && !GetCoherent())
            return MeanCouplingNoCoherent(Scatterer);

     }

    template <class T> double PointCouplingNoCoherent(T &Scatterer)
    {
      auto [ETheta, EPhi] = Scatterer.compute_unstructured_fields(Mesh);

      double CouplingTheta = Norm2(ETheta);
      double CouplingPhi   = Norm2(EPhi);


      if (!isnan(state.Filter))
        ApplyFilter(CouplingTheta, CouplingPhi, state.Filter);

      return 0.5 * EPSILON0 * C * (CouplingTheta + CouplingPhi) * Mesh.dOmega;
    }


    template <class T> double MeanCouplingNoCoherent(T &Scatterer)
    {
      return PointCouplingNoCoherent(Scatterer);
    }


    template <class T> double PointCouplingCoherent(T &Scatterer)
    {
      auto [ETheta, EPhi] = Scatterer.compute_unstructured_fields(Mesh);

      auto [EH, EV] = GetProjectedField(ETheta, EPhi);

      ApplyScalarField(EH, EV);

      double CouplingTheta = pow( abs( Norm1( EH ) ), 2 ),
             CouplingPhi   = pow( abs( Norm1( EV ) ), 2 );

      if (!isnan(state.Filter))
        ApplyFilter(CouplingTheta, CouplingPhi, state.Filter);

      return 0.5 * EPSILON0 * C * abs(CouplingTheta + CouplingPhi) * Mesh.dOmega;
    }


    template <class T> double MeanCouplingCoherent(T &Scatterer)
    {
      auto [ETheta, EPhi] = Scatterer.compute_unstructured_fields(Mesh);

      auto [EH, EV] = GetProjectedField(ETheta, EPhi);

      ApplyScalarField(EH, EV);

      complex128 CouplingTheta = Norm2(EH);
      complex128 CouplingPhi   = Norm2(EV);

      if (!isnan(state.Filter))
        ApplyFilter(CouplingTheta, CouplingPhi, state.Filter);

      return 0.5 * EPSILON0 * C * abs( CouplingTheta + CouplingPhi ) * Mesh.dOmega / Mesh.Omega;
    }


    std::tuple<CVector, CVector> GetProjectedField(CVector &ETheta, CVector &EPhi)
    {

      CVector EH(ETheta.size()), EV(ETheta.size());

      for (size_t i=0; i<ETheta.size(); ++i)
      {
        EV[i] = ETheta[i] * Mesh.VPara[i] + EPhi[i] * Mesh.VPerp[i] ;
        EH[i] = ETheta[i] * Mesh.HPara[i] + EPhi[i] * Mesh.HPerp[i] ;
      }

      return std::make_tuple(EH, EV);

    }

    void ApplyScalarField(CVector &Field0, CVector &Field1) //Theta = Para
    {
      for (size_t i=0; i<Field0.size(); i++)
      {
        Field0[i] *= state.ScalarField[i];
        Field1[i] *= state.ScalarField[i];
      }
    }


    template <class T> inline T Norm1(const std::vector<T> &Array)
    {
      T Sum  = 0.0;

      for (auto v : Array)
        Sum += v;

      return Sum;
    }

    template <class T> inline double Norm2(const std::vector<T> &Array)
    {
      T Sum  = 0.0;

      for (auto v : Array)
        Sum += pow( abs(v), 2 );

      return abs(Sum);
    }


    template <class T> inline void Squared(std::vector<T> &Array)
    {
      for (auto v : Array)
         v = pow( abs(v), 2);
    }

    template <class T> inline void ApplyFilter(T &CouplingTheta, T &CouplingPhi, const double &Filter)
    {
      double ThetaFiltering  = pow( sin(Filter), 2 ),
             PhiFiltering    = pow( cos(Filter), 2 );

       CouplingTheta *= ThetaFiltering;
       CouplingPhi   *= PhiFiltering;
    }


  };
}


#endif
