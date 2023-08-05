#ifndef SPECIAL_H
  #define SPECIAL_H

  #include <vector>
  #include <complex>
  #include <math.h>
  #include <tuple>
  #include "../../../Lib/complex_bessel.cpp"
  #include "Definitions.cpp"

  //---------------------------------AMOS_LIBRARY_WRAPPING--------------------------------------
  template<typename T, typename U>
  inline complex128 F90jn(U order, T x){ return sp_bessel::sph_besselJ(order, x); }
  template<typename T, typename U>
  inline complex128 F90yn(U order, T x){ return sp_bessel::sph_besselY(order, x); }



  template<typename T, typename U>  // https://dlmf.nist.gov/10.51
  inline complex128 F90jn_p(U order, T x)
  {
    return sp_bessel::sph_besselJ(order-1, x) - (order+1.0)/x * sp_bessel::sph_besselJ(order, x);
  }

  template<typename T, typename U>
  inline complex128 F90yn_p(U order, T x)
  {
    return sp_bessel::sph_besselY(order-1, x) - (order+1.0)/x * sp_bessel::sph_besselY(order, x);
   }


  template<typename T, typename U>  // https://dlmf.nist.gov/10.51
  inline complex128 F90h1_p(U order, T x)
  {
   return sp_bessel::sph_hankelH1(order-1, x) - (order+1.0)/x * sp_bessel::sph_hankelH1(order, x);
  }

  template<typename T, typename U>
  inline complex128 F90h2_p(U order, T x)
  {
   return sp_bessel::sph_hankelH2(order-1, x) - (order+1.0)/x * sp_bessel::sph_hankelH2(order, x);
  }


  template<typename T, typename U>
  inline complex128 F90Jn(U order, T x){ return sp_bessel::besselJ(order, x); }
  template<typename T, typename U>
  inline complex128 F90Yn(U order, T x){ return sp_bessel::besselY(order, x); }

  template<typename T>
  inline complex128 F90Jn_p(int order, T x){ return sp_bessel::besselJp(order, x, 1); }
  template<typename T>
  inline complex128 F90Yn_p(int order, T x){ return sp_bessel::besselYp(order, x, 1); }

  template<typename T>
  inline complex128 F90h1(int order, T x){ return sp_bessel::sph_hankelH1(order, x); }
  template<typename T>
  inline complex128 F90h2(int order, T x){ return sp_bessel::sph_hankelH2(order, x); }

  template<typename T>
  inline complex128 F90H1(int order, T x){ return sp_bessel::hankelH1(order, x); }
  template<typename T>
  inline complex128 F90H2(int order, T x){ return sp_bessel::hankelH2(order, x); }

  template<typename T>
  inline complex128 F90H1_p(int order, T x){ return sp_bessel::hankelH1p(order, x); }
  template<typename T>
  inline complex128 F90H2_p(int order, T x){ return sp_bessel::hankelH2p(order, x); }



#endif
// -
