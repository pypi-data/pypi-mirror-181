#ifndef CYLINDER_H
#define CYLINDER_H


  #include "BaseScatterer.cpp"
  #include <optional>

namespace CYLINDER
{

  struct State
  {
    double diameter;
    complex128 index;
    double n_medium;
    State(){}
    State(double &diameter, complex128 &index, double &n_medium)
                : diameter(diameter), index(index), n_medium(n_medium){}

    void apply_medium()
    {
      this->index    /= this->n_medium;
      this->diameter *= this->n_medium;
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



          Scatterer(double     &wavelength,
                    double     &amplitude,
                    double     &diameter,
                    complex128 &index,
                    double     &n_medium,
                    CVector    &jones_vector,
                    size_t     max_order = 0 )
                     : state(diameter, index, n_medium), ScatteringProperties(wavelength, jones_vector, amplitude)
                    {
                      this->max_order = max_order;
                      initialize();
                    }

          Scatterer(State &state, SOURCE::State &source, size_t max_order = 0)
                    : state(state), ScatteringProperties(source)
                    {
                      this->max_order = max_order;
                      initialize();
                    }

          void initialize()
          {
            // state.apply_medium();
            this->size_parameter = PI * state.diameter / source.wavelength;
            if (max_order == 0)
                this->max_order  = (size_t) (2 + this->size_parameter + 4 * pow(this->size_parameter, 1./3.)) + 16;
            this->area = state.diameter;
            compute_an_bn();

          }


          double     get_diameter()      {return state.diameter;}
          complex128 get_index()         {return state.index;}
          double     get_wavelength()    {return source.wavelength;}
          double     get_k()             {return source.k;}
          CVector    get_jones_vector()  {return source.jones_vector;}




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

          Qsca1 =  2. / size_parameter * ( 2.0 * Qsca1 + pow( abs(b1n[0]), 2 ) );
          Qsca2 =  2. / size_parameter * ( 2.0 * Qsca2 + pow( abs(a2n[0]), 2 ) );

          return process_polarization(Qsca1, Qsca2);
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

        Qext1 = 2. / size_parameter * std::real( b1n[0] + 2.0 * Qext1 );
        Qext2 = 2. / size_parameter * std::real( a1n[0] + 2.0 * Qext2 );

        return process_polarization(Qext1, Qext2);
      }

      double process_polarization(complex128 &Value0, complex128& value1)
      {
        if (source.Polarized == false)
            return 0.5 * ( abs( value1 ) + abs( Value0 ) );
        else
            return abs( value1 ) * pow(abs(source.jones_vector[0]), 2) + abs( Value0 ) * pow(abs(source.jones_vector[1]), 2);
      }

      void compute_an_bn()
      {
        _A1n = CVector(max_order);
        _B1n = CVector(max_order);

        _A2n = CVector(max_order);
        _B2n = CVector(max_order);

        double     x = size_parameter;
        complex128 m = state.index / state.n_medium;
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
