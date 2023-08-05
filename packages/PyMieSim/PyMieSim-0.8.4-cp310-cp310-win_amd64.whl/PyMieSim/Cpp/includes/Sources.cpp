#pragma once

namespace SOURCE
{

  struct State
  {
    double Wavelength;
    CVector Jones;
    double Amplitude;
    size_t WavelengthIdx;
    double k;
    bool Polarized = true;


    State(){}
    State(double  &Wavelength, CVector &Jones, double &Amplitude):
    Wavelength(Wavelength), Jones(Jones), Amplitude(Amplitude)
    {
      if (std::isnan( real( Jones[0] ))) Polarized = false;

      this->k = 2.0 * PI / this->Wavelength;
    }
  };

  class Source
  {
  public:
    double Wavelength, Polarization, E0, k;

    Source(const double &Wavelength,
           const double &Polarization,
           const double E0)
             :  Wavelength(Wavelength),
                Polarization(Polarization),
                E0(E0)
    { k = 2 * PI / Wavelength; }


    Source(){}
    ~Source(){}

    void SetWavelength(double value) { Wavelength = value; k = 2.0 * PI / value; }

    void SetPolarization(double value) { Polarization = value; }

    void SetE0(double value) { E0 = value; }
  };
}