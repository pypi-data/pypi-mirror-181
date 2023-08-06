#ifndef BASE_SCATTERER_H
#define BASE_SCATTERER_H

  #include "Definitions.cpp"
  #include "utils.cpp"
  #include "Sources.cpp"
  #include "FibonnaciMesh.cpp"


class ScatteringProperties
{
public:
    size_t max_order;
    double size_parameter, area;
    SOURCE::State source;

    virtual std::tuple<CVector, CVector> compute_s1s2(const DVector &Phi){};
    virtual double get_Qsca(){};
    virtual double get_Qext(){};
    virtual double get_Qback(){};
    virtual double get_g(){};

    ScatteringProperties(){}
    ScatteringProperties(double &wavelength, CVector &jones_vector, double &amplitude) : source(wavelength, jones_vector, amplitude){}
    ScatteringProperties(SOURCE::State &source) : source(source){}

    double get_Qforward() {return get_Qsca() - get_Qback();};
    double get_Qpr() {return get_Qext() - get_g() * get_Qsca();};
    double get_Qratio() {return get_Qback() / get_Qsca();};
    double get_Qabs() {return get_Qext() - get_Qsca();};
    double get_Csca() {return get_Qsca() * area;};
    double get_Cext() {return get_Qext() * area;};
    double get_Cabs() {return get_Qabs() * area;};
    double get_Cback() {return get_Qback() * area;};
    double get_Cforward() {return get_Qforward() * area;};
    double get_Cpr() {return get_Qpr() * area;};
    double get_Cratio() {return get_Qratio() * area;};

     DVector get_prefactor()
     {
       DVector Output; Output.reserve(max_order);

       for (size_t m = 0; m < max_order ; ++m)
          Output[m] = (double) ( 2 * (m+1) + 1 ) / ( (m+1) * ( (m+1) + 1 ) );

        return Output;
     }

    complex128 compute_propagator(const double &R)
    {
      return source.amplitude / (source.k * R) * exp(-JJ*source.k*R);
    }

    std::tuple<CVector, CVector> compute_structured_fields(const CVector& S1, const CVector& S2, const DVector& Theta, const double& R)
    {
      CVector EPhi, ETheta;
      size_t Size = Theta.size()*S1.size();

      EPhi.reserve(Size);
      ETheta.reserve(Size);

      complex128 propagator = compute_propagator(R);

      for (uint p=0; p < S1.size(); p++ )
          for (uint t=0; t < Theta.size(); t++ )
          {
            EPhi.push_back(   propagator * S1[p] * ( source.jones_vector[0] * cos(Theta[t]) + source.jones_vector[1] * sin(Theta[t]) ) );

            ETheta.push_back( propagator * S2[p] * ( source.jones_vector[0] * sin(Theta[t]) - source.jones_vector[1] * cos(Theta[t]) ) );
          }

      return std::make_tuple(EPhi, ETheta);
    }

    std::tuple<CVector, CVector> compute_unstructured_fields(const DVector& Phi, const DVector& Theta, const double R=1.0)
    {
      auto [S1, S2] = compute_s1s2(Phi);

      CVector EPhi, ETheta;
      size_t Size = Theta.size();

      EPhi.reserve(Size);
      ETheta.reserve(Size);

      complex128 propagator = compute_propagator(R);

      for (uint idx=0; idx < Size; idx++)
        {
          EPhi.push_back(   propagator * S1[idx] * ( source.jones_vector[0] * cos(Theta[idx]) + source.jones_vector[1] * sin(Theta[idx]) ) );

          ETheta.push_back( propagator * S2[idx] * ( source.jones_vector[0] * sin(Theta[idx]) - source.jones_vector[1] * cos(Theta[idx]) ) );
        }

      return std::make_tuple(EPhi, ETheta);
    }

    std::tuple<CVector, CVector> compute_unstructured_fields(const FibonacciMesh& Mesh, const double R=1.0)
    {
      return compute_unstructured_fields(Mesh.SCoord.Phi, Mesh.SCoord.Theta, R);
    }


    std::tuple<CVector, CVector, DVector, DVector> compute_full_structured_fields(size_t& sampling, double& R)
    {
      FullSteradian FullMesh = FullSteradian(sampling);

      auto [S1, S2] = compute_s1s2(FullMesh.SCoord.Phi);

      auto [EPhi, ETheta] = compute_structured_fields(S1, S2, FullMesh.SCoord.Theta, R);

      return std::make_tuple(EPhi, ETheta, FullMesh.SCoord.Phi, FullMesh.SCoord.Theta);
    }


    std::tuple<CVector, FullSteradian> compute_full_structured_spf(size_t sampling, double R=1.0)
    {
      FullSteradian Mesh = FullSteradian(sampling);

      auto [EPhi, ETheta] = compute_structured_fields(Mesh.SCoord.Phi, Mesh.SCoord.Theta, R);

      Squared(EPhi);
      Squared(ETheta);

      CVector spf = Add(EPhi, ETheta);

      return std::make_tuple(spf, Mesh);
    }

    std::tuple<CVector, CVector> compute_structured_fields(const DVector& Phi, const DVector& Theta, const double R)
    {
      complex128 propagator = compute_propagator(R);

      auto [S1, S2] = compute_s1s2(Phi);

      return compute_structured_fields(S1, S2, Theta, R);
    }

    //--------------------------------------------------------PYTHON-------------------


    std::tuple<Cndarray,Cndarray> get_s1s2_py(const DVector &Phi)
    {
      auto [S1, S2] = compute_s1s2(Phi);

      return std::make_tuple( vector_to_ndarray(std::move(S1)), vector_to_ndarray(std::move(S2)))  ;
    }


    std::tuple<Cndarray, Cndarray, ndarray, ndarray> get_full_structured_fields_py(size_t &sampling, double& R)
    {
      auto [EPhi, ETheta, Theta, Phi] = compute_full_structured_fields(sampling, R);

      Cndarray PyEPhi   = vector_to_ndarray( std::move(EPhi),   {sampling, sampling} );
      Cndarray PyETheta = vector_to_ndarray( std::move(ETheta), {sampling, sampling} );
      ndarray  PyTheta  = vector_to_ndarray( std::move(Theta) );
      ndarray  PyPhi    = vector_to_ndarray( std::move(Phi) );

      PyEPhi   = PyEPhi.attr("transpose")();
      PyETheta = PyETheta.attr("transpose")();

      return std::make_tuple(PyEPhi, PyETheta, PyPhi, PyTheta);
    }

    std::tuple<Cndarray,Cndarray> get_unstructured_fields_py(const DVector& Phi, const DVector& Theta, const double R)
    {
      auto [ETheta, EPhi] = compute_unstructured_fields(Phi, Theta, R);

      return std::make_tuple(vector_to_ndarray(std::move(EPhi)), vector_to_ndarray(std::move(ETheta)))  ;
    }



    double get_g_with_fields(size_t sampling, double R)
    {
        auto [SPF, Mesh]      = compute_full_structured_spf(sampling, R);

        double Norm           = abs( Mesh.Integral(SPF) );
        double ExpectedCos    = abs( Mesh.IntegralCos(SPF) );

        return ExpectedCos/Norm;
    }

};

#endif
