#ifndef CYLINDER_H
#define CYLINDER_H


  #include "BaseScatterer.cpp"
  #include <optional>

namespace CYLINDER
{

  struct State
  {
    double Diameter;
    complex128 Index;
    double nMedium;
    State(){}
    State(double &Diameter, complex128 &Index, double &nMedium)
                : Diameter(Diameter), Index(Index), nMedium(nMedium){}

    void ApplyMedium()
    {
      this->Index    /= this->nMedium;
      this->Diameter *= this->nMedium;
    }
  };


  class Scatterer: public ScatteringProperties
  {
      public:

          std::optional<CVector> _A1n, _B1n, _A2n, _B2n;

          State   state;

          Cndarray get_a1n_py() { return vector_to_ndarray(_A1n.value(), {max_order}); }
          Cndarray get_b1n_py() { return vector_to_ndarray(_B1n.value(), {max_order}); }
          Cndarray get_a2n_py() { return vector_to_ndarray(_A2n.value(), {max_order}); }
          Cndarray get_b2n_py() { return vector_to_ndarray(_B2n.value(), {max_order}); }

          CVector get_a1n() { if (_A1n) return _A1n.value(); else{ compute_an_bn(); return _A1n.value(); } };
          CVector get_b1n() { if (_B1n) return _B1n.value(); else{ compute_an_bn(); return _B1n.value(); } };
          CVector get_a2n() { if (_A2n) return _A2n.value(); else{ compute_an_bn(); return _A2n.value(); } };
          CVector get_b2n() { if (_B2n) return _B2n.value(); else{ compute_an_bn(); return _B2n.value(); } };



          Scatterer(double     &Wavelength,
                    double     &Amplitude,
                    double     &Diameter,
                    complex128 &Index,
                    double     &nMedium,
                    CVector    &Jones,
                    size_t      max_order = 0 )
                     : state(Diameter, Index, nMedium), ScatteringProperties(Wavelength, Jones, Amplitude)
                    {
                      this->max_order = max_order;
                      Init();
                    }

          Scatterer(State &state, SOURCE::State &source, size_t max_order = 0)
                    : state(state), ScatteringProperties(source)
                    {
                      this->max_order = max_order;
                      Init();
                    }

          void Init()
          {
            // state.ApplyMedium();
            this->SizeParameter = PI * state.Diameter / source.Wavelength;
            if (max_order == 0 )
                this->max_order  = (size_t) (2 + this->SizeParameter + 4 * pow(this->SizeParameter, 1./3.)) + 16;
            this->Area = state.Diameter;
            compute_an_bn();

          }


          double     get_Diameter()      {return state.Diameter;}
          complex128 get_Index()         {return state.Index;}
          double     get_Wavelength()    {return source.Wavelength;}
          double     get_k()             {return source.k;}
          CVector    get_Jones()         {return source.Jones;}




      double get_g()
      {
          return get_g_with_fields(1000, 1.0);
      }


      double get_Qsca()
      {
          CVector a1n = get_a1n(),
                  b1n = get_b1n(),
                  a2n = get_a2n(),
                  b2n = get_b2n();

          complex128 Qsca1=0, Qsca2=0;

          for(size_t it = 1; it < max_order; it++)
          {
            Qsca1 +=  pow( std::abs(a1n[it]), 2) + pow( std::abs(b1n[it]), 2) ;
            Qsca2 +=  pow( std::abs(a2n[it]), 2) + pow( std::abs(b2n[it]), 2) ;
          }

          Qsca1 =  2. / SizeParameter * ( 2.0 * Qsca1 + pow( abs(b1n[0]), 2 ) );
          Qsca2 =  2. / SizeParameter * ( 2.0 * Qsca2 + pow( abs(a2n[0]), 2 ) );

          return PolarizationEffet(Qsca1, Qsca2);
      }


      double get_Qext()
      {
        CVector a1n = get_a1n(),
                b1n = get_b1n(),
                a2n = get_a2n(),
                b2n = get_b2n();

        complex128 Qext1=0, Qext2=0;

        for(size_t it = 1; it < max_order; ++it)
        {
          Qext1 += b1n[it];
          Qext2 += a2n[it];
        }

        Qext1 = 2. / SizeParameter * std::real( b1n[0] + 2.0 * Qext1 );
        Qext2 = 2. / SizeParameter * std::real( a1n[0] + 2.0 * Qext2 );

        return PolarizationEffet(Qext1, Qext2);
      }

      double PolarizationEffet(complex128 &Value0, complex128& value1)
      {
        if (source.Polarized == false)
            return 0.5 * ( abs( value1 ) + abs( Value0 ) );
        else
            return abs( value1 ) * pow(abs(source.Jones[0]), 2) + abs( Value0 ) * pow(abs(source.Jones[1]), 2);
      }

      void compute_an_bn()
      {
        _A1n = CVector(max_order);
        _B1n = CVector(max_order);

        _A2n = CVector(max_order);
        _B2n = CVector(max_order);

        double     x = SizeParameter;
        complex128 m = state.Index / state.nMedium;
        complex128 z = m*x;

        complex128 numerator, denominator;

        CVector JVectorZ(max_order+1),
                JVectorZp(max_order+1),
                JVectorX(max_order+1),
                JVectorXp(max_order+1),
                HVectorX(max_order+1),
                HVectorXp(max_order+1);

        for (size_t n = 0; n < max_order+1; ++n)
        {
          double nd    = (double) n ;
          JVectorZ[n]  = F90Jn(nd, z);
          JVectorZp[n] = F90Jn_p(nd, z);
          JVectorX[n]  = F90Jn(nd, x);
          JVectorXp[n] = F90Jn_p(nd, x);
          HVectorX[n]  = F90H1(nd, x);
          HVectorXp[n]  = F90H1_p(nd, x);
        }


        for (size_t n = 0; n < (size_t) max_order; n++)
        {
          numerator      = m * JVectorZ[n] * JVectorXp[n] -  JVectorZp[n] * JVectorX[n];
          denominator    = m * JVectorZ[n] * HVectorXp[n] -  JVectorZp[n] * HVectorX[n];
          _A1n.value()[n] = 0.0 ;
          _A2n.value()[n] = numerator/denominator ;

          numerator      =   JVectorZ[n] * JVectorXp[n] - m * JVectorZp[n] * JVectorX[n];
          denominator    =   JVectorZ[n] * HVectorXp[n] - m * JVectorZp[n] * HVectorX[n];
          _B1n.value()[n] = numerator/denominator ;
          _B2n.value()[n] = 0.0 ;
        }
      }


      std::tuple<CVector, CVector> compute_s1s2(const DVector &Phi)
      {
        CVector T1(Phi.size()), T2(Phi.size());

        for (uint i = 0; i < Phi.size(); i++){
            T1[i] = _B1n.value()[0];
            T2[i] = _A2n.value()[0];
            for (size_t order = 1; order < max_order ; order++){
                T1[i]    += 2.0*_B1n.value()[order] * cos(order * (PI - (Phi[i]+PI/2.0) ) );
                T2[i]    += 2.0*_A2n.value()[order] * cos(order * (PI - (Phi[i]+PI/2.0) ) );
              }
        }

        return std::make_tuple( T1, T2 )  ;
      }

  };

}

#endif
