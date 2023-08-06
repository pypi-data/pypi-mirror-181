#ifndef SPHERE_H
#define SPHERE_H

  #include "BaseScatterer.cpp"
  #include "numpy_interface.cpp"
  #include "VSH.cpp"
  #include <optional>

  namespace SPHERE
  {
    struct State
    {
      double diameter;
      complex128 index;
      double n_medium;
      State(){}
      State(double &diameter, complex128 &index, double &n_medium)
                  : diameter(diameter), index(index), n_medium(n_medium){}

      State(double &diameter, complex128 &&index, double &n_medium)
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
            std::optional<CVector> _An, _Bn, _Cn, _Dn;

            State     state;

            Cndarray get_an_py() { return vector_to_ndarray(_An.value(), {max_order}); }
            Cndarray get_bn_py() { return vector_to_ndarray(_Bn.value(), {max_order}); }
            Cndarray get_cn_py() { return vector_to_ndarray(_Cn.value(), {max_order}); }
            Cndarray get_dn_py() { return vector_to_ndarray(_Dn.value(), {max_order}); }

            CVector get_an() { if (_An) return _An.value(); else{ compute_an_bn(); return _An.value(); } };
            CVector get_bn() { if (_Bn) return _Bn.value(); else{ compute_an_bn(); return _Bn.value(); } };
            CVector get_cn() { if (_An) return _Cn.value(); else{ ComputeCnDn(); return _Cn.value(); } };
            CVector get_dn() { if (_Bn) return _Dn.value(); else{ ComputeCnDn(); return _Dn.value(); } };

            Scatterer(){}
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
              state.apply_medium();
              this->size_parameter = PI * state.diameter / source.wavelength;
              if (max_order == 0)
                  this->max_order = (size_t) (2 + this->size_parameter + 4 * pow(this->size_parameter, 1./3.)) + 16;
              this->area = PI * pow(state.diameter/2.0, 2);
              compute_an_bn();

            }


        void compute_an_bn()
        {
          _An = CVector(max_order);
          _Bn = CVector(max_order);

          complex128 x   = size_parameter,
                     m   = state.index,
                     mx  = m * x,
                     _da, _db, _gsx, _gs1x, _px, _chx, _p1x, _ch1x, _p2x, _ch2x;

          size_t     nmx = std::max( max_order, (size_t) std::abs(mx) ) + 16;
          CVector    Dn  = VSH::SPHERICAL::compute_dn(nmx, mx);

          double     n;

          _p1x  = sin(x);
          _ch1x = cos(x);

          for (size_t i = 1; i < max_order+1; ++i)
            {
                n          = (double) i;
                _px        =  x * F90jn(n, x);
                _chx       = -x * F90yn(n, x);

                _p2x       = _px;
                _ch2x      = _chx;

                _gsx       =  _px  - 1.*JJ * _chx;
                _gs1x      =  _p1x - 1.*JJ * _ch1x;

                _da        = Dn[i]/m + n/x ;
                _db        = Dn[i]*m + n/x ;

                _An.value()[i-1] = (_da * _px - _p1x) / (_da * _gsx - _gs1x) ;
                _Bn.value()[i-1] = (_db * _px - _p1x) / (_db * _gsx - _gs1x) ;

                _p1x  = _p2x;
                _ch1x = _ch2x;
            }
        }


      void ComputeCnDn(size_t max_order = 0)
      {

        if (max_order == 0) max_order = this->max_order;

        _Cn = CVector(max_order);
        _Dn = CVector(max_order);

        complex128 x   = size_parameter,
                   m   = state.index,
                   z  = m * x;

        size_t nmx = std::max( max_order, (size_t) std::abs(z) ) + 16;

        CVector Cnx = CVector(nmx),
                Cnn, jnx, jnmx, yx, hx, b1x, y1x, hn1x, ax, ahx, numerator,
                c_denominator, d_denominator;

        b1x.push_back( +sin(x) / x );
        y1x.push_back( -cos(x) / x );

        for (double i = nmx; i > 1; i--)
        {
          Cnx[i-2] = i - z*z/(Cnx[i-1] + i);
        }

        for (size_t i = 0; i < max_order; i++)
        {
          double n = (double) i;
          Cnn.push_back( Cnx[i] );
          jnx.push_back(  F90jn( n+1, x ) );

          jnmx.push_back( 1. / ( F90jn(n+1, z ) ) );
          yx.push_back( F90yn(n+1, x ) );
          hx.push_back( jnx[i] + JJ * yx[i] );

          b1x.push_back( jnx[i] );
          y1x.push_back( yx[i] );
          hn1x.push_back( b1x[i] + JJ * y1x[i] );

          ax.push_back(  x * b1x[i]  - ( n+1 ) * jnx[i] );
          ahx.push_back( x * hn1x[i] - ( n+1 ) * hx[i]  );

          numerator.push_back( jnx[i] * ahx[i] - hx[i] * ax[i] );
          c_denominator.push_back( ahx[i] - hx[i] * Cnn[i] );
          d_denominator.push_back( m * m * ahx[i] - hx[i] * Cnn[i] );
          _Cn.value()[i] = jnmx[i] * numerator[i] / c_denominator[i] ;
          _Dn.value()[i] = jnmx[i] * m * numerator[i] / d_denominator[i] ;
        }
      }


      double get_g()
      {
          double temp = 0;

          CVector an = get_an(), bn = get_bn();

          for(size_t it = 0; it < max_order-1; ++it)
          {
              double n = (double) it + 1;
              temp += ( n * (n + 2.) / (n + 1.) ) * std::real(an[it] * std::conj(an[it+1]) + bn[it] * std::conj(bn[it+1]) );
              temp += ( (2. * n + 1. ) / ( n * (n + 1.) ) )  * std::real( an[it] * std::conj(bn[it]) );
          }

          return temp * 4. / ( get_Qsca() * pow(size_parameter, 2) );
      }



    std::tuple<CVector, CVector> compute_s1s2(const DVector &Phi)
    {
      CVector an = get_an(), bn = get_bn();

      CVector S1(Phi.size(), 0.0), S2(Phi.size(), 0.0);

      DVector Prefactor = get_prefactor();

      DVector Mu; Mu.reserve(Phi.size());

      for (double phi : Phi)
          Mu.push_back( cos( phi-PI/2.0 ) );


      for (uint i = 0; i < Phi.size(); i++)
      {
          auto [pin, taun] = VSH::SPHERICAL::MiePiTau( Mu[i], max_order);

          for (uint m = 0; m < max_order ; m++){
              S1[i]    += Prefactor[m] * ( an[m] * pin[m] +  bn[m] * taun[m] );
              S2[i]    += Prefactor[m] * ( an[m] * taun[m] + bn[m] * pin[m]  );
            }
      }

      return std::make_tuple(S1, S2)  ;
    }



    double get_Qsca()
    {
        CVector an = get_an(), bn = get_bn();

        double temp = 0;
        for(size_t it = 0; it < max_order; ++it)
        {
             double n = (double) it + 1;
             temp += (2.* n + 1.) * ( pow( std::abs(an[it]), 2) + pow( std::abs(bn[it]), 2)  );

        }
        return temp * 2. / pow( size_parameter, 2.);
    }


    double get_Qext()
    {
      CVector an = get_an(), bn = get_bn();

      double temp = 0;
      for(size_t it = 0; it < max_order; ++it)
      {
           double n = (double) it + 1;
           temp += (2.* n + 1.) * std::real( an[it] + bn[it] );

      }
      return temp * 2. / pow( size_parameter, 2.);
    }


    double get_Qback()
    {
        CVector an = get_an(), bn = get_bn();

        complex128 temp = 0;
        for(size_t it = 0; it < max_order-1; ++it)
        {
          double n = (double) it + 1;
          temp += (2. * n + 1) * pow(-1., n) * ( an[it] - bn[it] ) ;
        }

        temp *= pow( std::abs(temp), 2. ) / pow( size_parameter, 2. );
        return std::abs(temp);
    }



  };

}


#endif
// -
