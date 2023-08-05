#ifndef EXPERIMENT_H
#define EXPERIMENT_H

#include "Definitions.cpp"
#include "numpy_interface.cpp"
#include "Sets.cpp"

class Experiment
  {
  public:
      SPHERE::Set sphereSet;
      CYLINDER::Set cylinderSet;
      CORESHELL::Set coreshellSet;
      DETECTOR::Set detectorSet;
      SOURCE::Set sourceSet;

      Experiment(){}

void set_sphere(SPHERE::Set& ScattererSet){ this->sphereSet = ScattererSet;}

void set_cylinder(CYLINDER::Set& ScattererSet) { this->cylinderSet = ScattererSet; }

void set_coreshell(CORESHELL::Set& ScattererSet) { this->coreshellSet = ScattererSet; }

void set_source(SOURCE::Set &sourceSet){ this->sourceSet = sourceSet; }

void set_detector(DETECTOR::Set &detectorSet){ this->detectorSet = detectorSet; }



//--------------------------------------SPHERE------------------------------------
Cndarray get_sphere_coefficient(CVector (SPHERE::Scatterer::*function)(void), size_t max_order=0)
{
  if (sphereSet.BoundedIndex)
      return get_sphere_coefficient_material(function, max_order);
  else
      return get_sphere_coefficient_index(function, max_order);
}

ndarray get_sphere_data(double (SPHERE::Scatterer::*function)(void), size_t max_order=0)
{
  if (sphereSet.BoundedIndex)
      return get_sphere_data_material(function, max_order);
  else
      return get_sphere_data_index(function, max_order);
}


ndarray get_sphere_Coupling()
{
  if (sphereSet.BoundedIndex)
      return get_sphere_coupling_material();
  else
      return get_sphere_coupling_index();
}




Cndarray get_sphere_coefficient_material(CVector (SPHERE::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace SPHERE;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   sphereSet.Diameter.size(),
                                   sphereSet.Material.size(),
                                   sphereSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  CVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            SPHERE::State   scattererState = SPHERE::State(sphereSet.Diameter[d], sphereSet.Material[i][w], sphereSet.nMedium[n]);

                            SPHERE::Scatterer Scat = SPHERE::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }

  return vector_to_ndarray(Output, FullShape);
}






Cndarray get_sphere_coefficient_index(CVector (SPHERE::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace SPHERE;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               sphereSet.Diameter.size(),
               sphereSet.Index.size(),
               sphereSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  CVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            SPHERE::State   scattererState = SPHERE::State(sphereSet.Diameter[d], sphereSet.Index[i], sphereSet.nMedium[n]);

                            SPHERE::Scatterer Scat = SPHERE::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }

  return vector_to_ndarray(Output, FullShape);
}






ndarray get_sphere_data_material(double (SPHERE::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace SPHERE;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   sphereSet.Diameter.size(),
                                   sphereSet.Material.size(),
                                   sphereSet.nMedium.size()};


  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  DVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            SPHERE::State   scattererState = SPHERE::State(sphereSet.Diameter[d], sphereSet.Material[i][w], sphereSet.nMedium[n]);

                            SPHERE::Scatterer Scat = SPHERE::Scatterer(scattererState, sourceState);

                            Output[idx] = (Scat.*function)();
                          }

  return vector_to_ndarray(Output, FullShape);
}






ndarray get_sphere_data_index(double (SPHERE::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace SPHERE;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               sphereSet.Diameter.size(),
               sphereSet.Index.size(),
               sphereSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            SPHERE::State   scattererState = SPHERE::State(sphereSet.Diameter[d], sphereSet.Index[i], sphereSet.nMedium[n]);

                            SPHERE::Scatterer Scat = SPHERE::Scatterer(scattererState, sourceState, max_order);

                            Output[idx] = (Scat.*function)();

                          }

  return vector_to_ndarray(Output, FullShape);
}






ndarray get_sphere_coupling_material()
{
  using namespace SPHERE;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   sphereSet.Diameter.size(),
                                   sphereSet.Material.size(),
                                   sphereSet.nMedium.size(),
                                   detectorSet.ScalarField.size(),
                                   detectorSet.NA.size(),
                                   detectorSet.PhiOffset.size(),
                                   detectorSet.GammaOffset.size(),
                                   detectorSet.Filter.size()};


  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(11)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          for (size_t s=0; s<FullShape[6]; ++s)
                              for (size_t na=0; na<FullShape[7]; ++na)
                                  for (size_t p=0; p<FullShape[8]; ++p)
                                      for (size_t g=0; g<FullShape[9]; ++g)
                                          for (size_t f=0; f<FullShape[10]; ++f)
                                        {
                                          size_t idx = f  +
                                                       g  * FullShape[10] +
                                                       p  * FullShape[10] * FullShape[9] +
                                                       na * FullShape[10] * FullShape[9] * FullShape[8] +
                                                       s  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                       n  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                       i  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                       d  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                       a  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                       j  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                       w  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                                       ;

                                          SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                          SPHERE::State   scattererState = SPHERE::State(sphereSet.Diameter[d], sphereSet.Material[i][w], sphereSet.nMedium[n]);
                                          DETECTOR::State detectorState  = DETECTOR::State(detectorSet.ScalarField[s], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                          SPHERE::Scatterer Scat = SPHERE::Scatterer(scattererState, sourceState);
                                          DETECTOR::Detector det = DETECTOR::Detector(detectorState);

                                          Output[idx] = abs( det.Coupling(Scat) );
                                        }

  return vector_to_ndarray(Output, FullShape);
}






ndarray get_sphere_coupling_index()
{
  using namespace SPHERE;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               sphereSet.Diameter.size(),
               sphereSet.Index.size(),
               sphereSet.nMedium.size(),
               detectorSet.ScalarField.size(),
               detectorSet.NA.size(),
               detectorSet.PhiOffset.size(),
               detectorSet.GammaOffset.size(),
               detectorSet.Filter.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(11)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          for (size_t s=0; s<FullShape[6]; ++s)
                              for (size_t na=0; na<FullShape[7]; ++na)
                                  for (size_t p=0; p<FullShape[8]; ++p)
                                      for (size_t g=0; g<FullShape[9]; ++g)
                                          for (size_t f=0; f<FullShape[10]; ++f)
                                        {
                                          size_t idx = f  +
                                                       g  * FullShape[10] +
                                                       p  * FullShape[10] * FullShape[9] +
                                                       na * FullShape[10] * FullShape[9] * FullShape[8] +
                                                       s  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                       n  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                       i  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                       d  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                       a  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                       j  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                       w  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1]
                                                       ;



                                          SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                          SPHERE::State   scattererState = SPHERE::State(sphereSet.Diameter[d], sphereSet.Index[i], sphereSet.nMedium[n]);
                                          DETECTOR::State detectorState  = DETECTOR::State(detectorSet.ScalarField[s], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                          SPHERE::Scatterer Scat = SPHERE::Scatterer(scattererState, sourceState);
                                          DETECTOR::Detector det = DETECTOR::Detector(detectorState);

                                          Output[idx] = abs( det.Coupling(Scat) );
                                        }

  return vector_to_ndarray(Output, FullShape);
}


//--------------------------------------CYLINDER------------------------------------
Cndarray get_cylinder_coefficient(CVector (CYLINDER::Scatterer::*function)(void), size_t max_order=0)
{
  if (cylinderSet.BoundedIndex)
      return get_cylinder_coefficient_material(function, max_order);
  else
      return get_cylinder_coefficient_index(function, max_order);
}

ndarray get_cylinder_data(double (CYLINDER::Scatterer::*function)(void), size_t max_order=0)
{
  if (cylinderSet.BoundedIndex)
      return get_cylinder_data_material(function, max_order);
  else
      return get_cylinder_data_index(function, max_order);
}

ndarray get_cylinder_Coupling()
{
  if (cylinderSet.BoundedIndex)
      return get_cylinder_CouplingBound0();
  else
      return get_cylinder_CouplingUnbound();
}



Cndarray get_cylinder_coefficient_material(CVector (CYLINDER::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CYLINDER;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   cylinderSet.Diameter.size(),
                                   cylinderSet.Material.size(),
                                   cylinderSet.nMedium.size()};


  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  CVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CYLINDER::State scattererState = CYLINDER::State(cylinderSet.Diameter[d], cylinderSet.Material[i][w], cylinderSet.nMedium[n]);

                            CYLINDER::Scatterer Scat = CYLINDER::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }

  return vector_to_ndarray(Output, FullShape);
}






Cndarray get_cylinder_coefficient_index(CVector (CYLINDER::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CYLINDER;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               cylinderSet.Diameter.size(),
               cylinderSet.Index.size(),
               cylinderSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  CVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CYLINDER::State scattererState = CYLINDER::State(cylinderSet.Diameter[d], cylinderSet.Index[i], cylinderSet.nMedium[n]);

                            CYLINDER::Scatterer Scat = CYLINDER::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }

  return vector_to_ndarray(Output, FullShape);
}



ndarray get_cylinder_data_material(double (CYLINDER::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CYLINDER;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   cylinderSet.Diameter.size(),
                                   cylinderSet.Material.size(),
                                   cylinderSet.nMedium.size()};


  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  DVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CYLINDER::State scattererState = CYLINDER::State(cylinderSet.Diameter[d], cylinderSet.Material[i][w], cylinderSet.nMedium[n]);

                            CYLINDER::Scatterer Scat = CYLINDER::Scatterer(scattererState, sourceState, max_order);

                            Output[idx] = (Scat.*function)();
                          }

  return vector_to_ndarray(Output, FullShape);
}






ndarray get_cylinder_data_index(double (CYLINDER::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CYLINDER;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               cylinderSet.Diameter.size(),
               cylinderSet.Index.size(),
               cylinderSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          {
                            size_t idx = n  +
                                         i  * FullShape[5] +
                                         d  * FullShape[5] * FullShape[4] +
                                         a  * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CYLINDER::State scattererState = CYLINDER::State(cylinderSet.Diameter[d], cylinderSet.Index[i], cylinderSet.nMedium[n]);

                            CYLINDER::Scatterer Scat = CYLINDER::Scatterer(scattererState, sourceState, max_order);

                            Output[idx] = (Scat.*function)();
                          }

  return vector_to_ndarray(Output, FullShape);
}







ndarray get_cylinder_CouplingBound0()
{
  using namespace CYLINDER;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   cylinderSet.Diameter.size(),
                                   cylinderSet.Material.size(),
                                   cylinderSet.nMedium.size(),
                                   detectorSet.ScalarField.size(),
                                   detectorSet.NA.size(),
                                   detectorSet.PhiOffset.size(),
                                   detectorSet.GammaOffset.size(),
                                   detectorSet.Filter.size()};


  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(11)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          for (size_t s=0; s<FullShape[6]; ++s)
                              for (size_t na=0; na<FullShape[7]; ++na)
                                  for (size_t p=0; p<FullShape[8]; ++p)
                                      for (size_t g=0; g<FullShape[9]; ++g)
                                          for (size_t f=0; f<FullShape[10]; ++f)
                                        {
                                          size_t idx = f  +
                                                       g  * FullShape[10] +
                                                       p  * FullShape[10] * FullShape[9] +
                                                       na * FullShape[10] * FullShape[9] * FullShape[8] +
                                                       s  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                       n  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                       i  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                       d  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                       a  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                       j  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                       w  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                                       ;

                                          SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                          CYLINDER::State scattererState = CYLINDER::State(cylinderSet.Diameter[d], cylinderSet.Material[i][w], cylinderSet.nMedium[n]);
                                          DETECTOR::State detectorState  = DETECTOR::State(detectorSet.ScalarField[s], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                          CYLINDER::Scatterer Scat = CYLINDER::Scatterer(scattererState, sourceState);
                                          DETECTOR::Detector  det = DETECTOR::Detector(detectorState);

                                          Output[idx] = abs( det.Coupling(Scat) );
                                        }

  return vector_to_ndarray(Output, FullShape);
}






ndarray get_cylinder_CouplingUnbound()
{
  using namespace CYLINDER;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               cylinderSet.Diameter.size(),
               cylinderSet.Index.size(),
               cylinderSet.nMedium.size(),
               detectorSet.ScalarField.size(),
               detectorSet.NA.size(),
               detectorSet.PhiOffset.size(),
               detectorSet.GammaOffset.size(),
               detectorSet.Filter.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(11)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t d=0; d<FullShape[3]; ++d)
                  for (size_t i=0; i<FullShape[4]; ++i)
                      for (size_t n=0; n<FullShape[5]; ++n)
                          for (size_t s=0; s<FullShape[6]; ++s)
                              for (size_t na=0; na<FullShape[7]; ++na)
                                  for (size_t p=0; p<FullShape[8]; ++p)
                                      for (size_t g=0; g<FullShape[9]; ++g)
                                          for (size_t f=0; f<FullShape[10]; ++f)
                                        {
                                          size_t idx = f  +
                                                       g  * FullShape[10] +
                                                       p  * FullShape[10] * FullShape[9] +
                                                       na * FullShape[10] * FullShape[9] * FullShape[8] +
                                                       s  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                       n  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                       i  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                       d  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                       a  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                       j  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                       w  * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                                       ;

                                          SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                          CYLINDER::State scattererState = CYLINDER::State(cylinderSet.Diameter[d], cylinderSet.Index[i], cylinderSet.nMedium[n]);
                                          DETECTOR::State detectorState  = DETECTOR::State(detectorSet.ScalarField[s], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                          CYLINDER::Scatterer Scat = CYLINDER::Scatterer(scattererState, sourceState);
                                          DETECTOR::Detector  det = DETECTOR::Detector(detectorState);

                                          Output[idx] = abs( det.Coupling(Scat) );
                                        }

  return vector_to_ndarray(Output, FullShape);
}







//--------------------------------------CORESHELL------------------------------------
//--------------------------------------CORESHELL------------------------------------
Cndarray get_coreshell_coefficient(CVector (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{

  if (coreshellSet.BoundedCore && coreshellSet.BoundedShell)
      return get_coreshell_coefficient_core_material_shell_material(function, max_order);

  if (coreshellSet.BoundedCore && !coreshellSet.BoundedShell)
      return get_coreshell_coefficient_core_material_shell_index(function, max_order);

  if (!coreshellSet.BoundedCore && coreshellSet.BoundedShell)
      return get_coreshell_coefficient_core_index_shell_material(function, max_order);

  if (!coreshellSet.BoundedCore && !coreshellSet.BoundedShell)
      return get_coreshell_coefficient_core_index_shell_index(function, max_order);

}

ndarray get_coreshell_data(double (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  if (coreshellSet.BoundedCore && coreshellSet.BoundedShell)
      return get_coreshell_data_core_material_shell_material(function, max_order);

  if (coreshellSet.BoundedCore && !coreshellSet.BoundedShell)
      return get_coreshell_data_core_material_shell_index(function, max_order);

  if (!coreshellSet.BoundedCore && coreshellSet.BoundedShell)
      return get_coreshell_data_core_index_shell_material(function, max_order);

  if (!coreshellSet.BoundedCore && !coreshellSet.BoundedShell)
      return get_coreshell_data_core_index_shell_index(function, max_order);

}


ndarray get_coreshell_Coupling()
{
  if (coreshellSet.BoundedCore && coreshellSet.BoundedShell)
      return get_coreshell_coupling_core_material_shell_material();

  if (coreshellSet.BoundedCore && !coreshellSet.BoundedShell)
      return get_coreshell_coupling_core_material_shell_index();

  if (!coreshellSet.BoundedCore && coreshellSet.BoundedShell)
      return get_coreshell_coupling_core_index_shell_material();

  if (!coreshellSet.BoundedCore && !coreshellSet.BoundedShell)
  {
    return get_coreshell_coupling_core_index_shell_index();
  }

}


Cndarray get_coreshell_coefficient_core_material_shell_index(CVector (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreMaterial.size(),
                                   coreshellSet.ShellIndex.size(),
                                   coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  CVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                          {
                            size_t idx = n  +
                                         Si * FullShape[7] +
                                         Ci * FullShape[7] * FullShape[6] +
                                         Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                         Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                         a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[2] * FullShape[1]
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreMaterial[Ci][w], coreshellSet.ShellIndex[Si], coreshellSet.nMedium[n]);

                            CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }


  return vector_to_ndarray(Output, FullShape);
}



Cndarray get_coreshell_coefficient_core_index_shell_material(CVector (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreIndex.size(),
                                   coreshellSet.ShellMaterial.size(),
                                   coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  CVector Output(FullSize);

  #pragma omp parallel for collapse(8)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                          {
                            size_t idx = n  +
                                         Si * FullShape[7] +
                                         Ci * FullShape[7] * FullShape[6] +
                                         Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                         Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                         a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[2] * FullShape[1]
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreIndex[Ci], coreshellSet.ShellMaterial[Si][w], coreshellSet.nMedium[n]);

                            CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }


  return vector_to_ndarray(Output, FullShape);
}



Cndarray get_coreshell_coefficient_core_material_shell_material(CVector (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreMaterial.size(),
                                   coreshellSet.ShellMaterial.size(),
                                   coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  CVector Output(FullSize);

  #pragma omp parallel for collapse(8)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                          {
                            size_t idx = n  +
                                         Si * FullShape[7] +
                                         Ci * FullShape[7] * FullShape[6] +
                                         Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                         Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                         a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[2] * FullShape[1]
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                            CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreMaterial[Ci][w], coreshellSet.ShellMaterial[Si][w], coreshellSet.nMedium[n]);

                            CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order+1);

                            Output[idx] = (Scat.*function)()[max_order];
                          }

  return vector_to_ndarray(Output, FullShape);
}




Cndarray get_coreshell_coefficient_core_index_shell_index(CVector (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               coreshellSet.CoreDiameter.size(),
               coreshellSet.ShellDiameter.size(),
               coreshellSet.CoreIndex.size(),
               coreshellSet.ShellIndex.size(),
               coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  CVector Output(FullSize);

  #pragma omp parallel for collapse(8)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                              {
                                size_t idx = n  +
                                             Si * FullShape[7] +
                                             Ci * FullShape[7] * FullShape[6] +
                                             Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                             Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                             a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                             j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                             w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                             ;

                                SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w],
                                                                               sourceSet.Jones[j],
                                                                               sourceSet.Amplitude[a]);

                                CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd],
                                                                                   coreshellSet.ShellDiameter[Sd],
                                                                                   coreshellSet.CoreIndex[Ci],
                                                                                   coreshellSet.ShellIndex[Si],
                                                                                   coreshellSet.nMedium[n]);

                                CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order+1);

                                Output[idx] = (Scat.*function)()[max_order];
                              }

  return vector_to_ndarray(Output, FullShape);
}





ndarray get_coreshell_data_core_material_shell_index(double (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreMaterial.size(),
                                   coreshellSet.ShellIndex.size(),
                                   coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  DVector Output(FullSize);

  #pragma omp parallel for collapse(6)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Cm=0; Cm<FullShape[5]; ++Cm)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                              {
                                size_t idx = n  +
                                             Si * FullShape[7] +
                                             Cm * FullShape[7] * FullShape[6] +
                                             Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                             Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                             a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                             j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                             w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[2] * FullShape[1]
                                             ;

                                SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w],
                                                                               sourceSet.Jones[j],
                                                                               sourceSet.Amplitude[a]);

                                CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd],
                                                                                   coreshellSet.ShellDiameter[Sd],
                                                                                   coreshellSet.CoreMaterial[Cm][w],
                                                                                   coreshellSet.ShellIndex[Si],
                                                                                   coreshellSet.nMedium[n]);

                                CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order);

                                Output[idx] = (Scat.*function)();
                              }


  return vector_to_ndarray(Output, FullShape);
}



ndarray get_coreshell_data_core_index_shell_material(double (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreIndex.size(),
                                   coreshellSet.ShellMaterial.size(),
                                   coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  DVector Output(FullSize);

  #pragma omp parallel for collapse(8)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Sm=0; Sm<FullShape[6]; ++Sm)
                              for (size_t n=0; n<FullShape[7]; ++n)
                          {
                            size_t idx = n  +
                                         Sm * FullShape[7] +
                                         Ci * FullShape[7] * FullShape[6] +
                                         Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                         Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                         a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[2] * FullShape[1]
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w],
                                                                           sourceSet.Jones[j],
                                                                           sourceSet.Amplitude[a]);

                            CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd],
                                                                               coreshellSet.ShellDiameter[Sd],
                                                                               coreshellSet.CoreIndex[Ci],
                                                                               coreshellSet.ShellMaterial[Sm][w],
                                                                               coreshellSet.nMedium[n]);

                            CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order);

                            Output[idx] = (Scat.*function)();
                          }


  return vector_to_ndarray(Output, FullShape);
}



ndarray get_coreshell_data_core_material_shell_material(double (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreMaterial.size(),
                                   coreshellSet.ShellMaterial.size(),
                                   coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  DVector Output(FullSize);

  #pragma omp parallel for collapse(8)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Cm=0; Cm<FullShape[5]; ++Cm)
                          for (size_t Sm=0; Sm<FullShape[6]; ++Sm)
                              for (size_t n=0; n<FullShape[7]; ++n)
                          {
                            size_t idx = n  +
                                         Sm * FullShape[7] +
                                         Cm * FullShape[7] * FullShape[6] +
                                         Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                         Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                         a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                         j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                         w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[2] * FullShape[1]
                                         ;

                            SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w],
                                                                           sourceSet.Jones[j],
                                                                           sourceSet.Amplitude[a]);

                            CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd],
                                                                               coreshellSet.ShellDiameter[Sd],
                                                                               coreshellSet.CoreMaterial[Cm][w],
                                                                               coreshellSet.ShellMaterial[Sm][w],
                                                                               coreshellSet.nMedium[n]);

                            CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order);

                            Output[idx] = (Scat.*function)();
                          }

  return vector_to_ndarray(Output, FullShape);
}




ndarray get_coreshell_data_core_index_shell_index(double (CORESHELL::Scatterer::*function)(void), size_t max_order=0)
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape;

  FullShape = {sourceSet.Wavelength.size(),
               sourceSet.Jones.size(),
               sourceSet.Amplitude.size(),
               coreshellSet.CoreDiameter.size(),
               coreshellSet.ShellDiameter.size(),
               coreshellSet.CoreIndex.size(),
               coreshellSet.ShellIndex.size(),
               coreshellSet.nMedium.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(8)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                              {
                                size_t idx = n  +
                                             Si * FullShape[7] +
                                             Ci * FullShape[7] * FullShape[6] +
                                             Sd * FullShape[7] * FullShape[6] * FullShape[5] +
                                             Cd * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                             a  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                             j  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                             w  * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1];
                                             ;

                                SOURCE::State   sourceState    = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                CORESHELL::State scattererState = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreIndex[Ci], coreshellSet.ShellIndex[Si], coreshellSet.nMedium[n]);

                                CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState, max_order);

                                Output[idx] = (Scat.*function)();
                              }

  return vector_to_ndarray(Output, FullShape);
}











ndarray get_coreshell_coupling_core_index_shell_index()
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreIndex.size(),
                                   coreshellSet.ShellIndex.size(),
                                   coreshellSet.nMedium.size(),
                                   detectorSet.ScalarField.size(),
                                   detectorSet.NA.size(),
                                   detectorSet.PhiOffset.size(),
                                   detectorSet.GammaOffset.size(),
                                   detectorSet.Filter.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);


  #pragma omp parallel for collapse(13)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                                  for (size_t s=0; s<FullShape[8]; ++s)
                                      for (size_t na=0; na<FullShape[9]; ++na)
                                          for (size_t p=0; p<FullShape[10]; ++p)
                                              for (size_t g=0; g<FullShape[11]; ++g)
                                                  for (size_t f=0; f<FullShape[12]; ++f)
                                                  {
                                                    size_t idx = f  +
                                                                 g  * FullShape[12] +
                                                                 p  * FullShape[12] * FullShape[11] +
                                                                 na * FullShape[12] * FullShape[11] * FullShape[10] +
                                                                 s  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] +
                                                                 n  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] +
                                                                 Si * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                                 Ci * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                                 Sd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                                 Cd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                                 a  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                                 j  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                                 w  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1]
                                                                 ;

                                                    SOURCE::State    sourceState     = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                                    CORESHELL::State scattererState  = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreIndex[Ci], coreshellSet.ShellIndex[Si], coreshellSet.nMedium[n]);
                                                    DETECTOR::State  detectorState   = DETECTOR::State(detectorSet.ScalarField[s], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                                    CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState);
                                                    DETECTOR::Detector det = DETECTOR::Detector(detectorState);

                                                    Output[idx] = abs( det.Coupling(Scat) );
                                                  }

  return vector_to_ndarray(Output, FullShape);
}




ndarray get_coreshell_coupling_core_material_shell_index()
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreMaterial.size(),
                                   coreshellSet.ShellIndex.size(),
                                   coreshellSet.nMedium.size(),
                                   detectorSet.ScalarField.size(),
                                   detectorSet.NA.size(),
                                   detectorSet.PhiOffset.size(),
                                   detectorSet.GammaOffset.size(),
                                   detectorSet.Filter.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(13)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                                  for (size_t s=0; s<FullShape[8]; ++s)
                                      for (size_t na=0; na<FullShape[9]; ++na)
                                          for (size_t p=0; p<FullShape[10]; ++p)
                                              for (size_t g=0; g<FullShape[11]; ++g)
                                                  for (size_t f=0; f<FullShape[12]; ++f)
                                                  {
                                                    size_t idx = f  +
                                                                 g  * FullShape[12] +
                                                                 p  * FullShape[12] * FullShape[11] +
                                                                 na * FullShape[12] * FullShape[11] * FullShape[10] +
                                                                 s  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] +
                                                                 n  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] +
                                                                 Si * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                                 Ci * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                                 Sd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                                 Cd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                                 a  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                                 j  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                                 w  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1]
                                                                 ;

                                                    SOURCE::State    sourceState     = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                                    CORESHELL::State scattererState  = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreMaterial[Ci][w], coreshellSet.ShellIndex[Si], coreshellSet.nMedium[n]);
                                                    DETECTOR::State  detectorState   = DETECTOR::State(detectorSet.ScalarField[0], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                                    CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState);
                                                    DETECTOR::Detector det = DETECTOR::Detector(detectorState);

                                                    Output[idx] = abs( det.Coupling(Scat) );
                                                  }

  return vector_to_ndarray(Output, FullShape);
}









ndarray get_coreshell_coupling_core_index_shell_material()
{
  using namespace CORESHELL;

  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreIndex.size(),
                                   coreshellSet.ShellMaterial.size(),
                                   coreshellSet.nMedium.size(),
                                   detectorSet.ScalarField.size(),
                                   detectorSet.NA.size(),
                                   detectorSet.PhiOffset.size(),
                                   detectorSet.GammaOffset.size(),
                                   detectorSet.Filter.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;


  DVector Output(FullSize);

  #pragma omp parallel for collapse(13)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                                  for (size_t s=0; s<FullShape[8]; ++s)
                                      for (size_t na=0; na<FullShape[9]; ++na)
                                          for (size_t p=0; p<FullShape[10]; ++p)
                                              for (size_t g=0; g<FullShape[11]; ++g)
                                                  for (size_t f=0; f<FullShape[12]; ++f)
                                                  {
                                                    size_t idx = f  +
                                                                 g  * FullShape[12] +
                                                                 p  * FullShape[12] * FullShape[11] +
                                                                 na * FullShape[12] * FullShape[11] * FullShape[10] +
                                                                 s  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] +
                                                                 n  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] +
                                                                 Si * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                                 Ci * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                                 Sd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                                 Cd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                                 a  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                                 j  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                                 w  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1]
                                                                 ;

                                                    SOURCE::State    sourceState     = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                                    CORESHELL::State scattererState  = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreIndex[Ci], coreshellSet.ShellMaterial[Si][w], coreshellSet.nMedium[n]);
                                                    DETECTOR::State  detectorState   = DETECTOR::State(detectorSet.ScalarField[0], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                                    CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState);
                                                    DETECTOR::Detector det = DETECTOR::Detector(detectorState);

                                                    Output[idx] = abs( det.Coupling(Scat) );
                                                  }

  return vector_to_ndarray(Output, FullShape);
}





ndarray get_coreshell_coupling_core_material_shell_material()
{
  using namespace CORESHELL;
  std::vector<size_t> FullShape = {sourceSet.Wavelength.size(),
                                   sourceSet.Jones.size(),
                                   sourceSet.Amplitude.size(),
                                   coreshellSet.CoreDiameter.size(),
                                   coreshellSet.ShellDiameter.size(),
                                   coreshellSet.CoreIndex.size(),
                                   coreshellSet.ShellMaterial.size(),
                                   coreshellSet.nMedium.size(),
                                   detectorSet.ScalarField.size(),
                                   detectorSet.NA.size(),
                                   detectorSet.PhiOffset.size(),
                                   detectorSet.GammaOffset.size(),
                                   detectorSet.Filter.size()};

  size_t FullSize = 1;
  for (auto e: FullShape)
      FullSize *= e;

  DVector Output(FullSize);

  #pragma omp parallel for collapse(13)
  for (size_t w=0; w<FullShape[0]; ++w)
      for (size_t j=0; j<FullShape[1]; ++j)
          for (size_t a=0; a<FullShape[2]; ++a)
              for (size_t Cd=0; Cd<FullShape[3]; ++Cd)
                  for (size_t Sd=0; Sd<FullShape[4]; ++Sd)
                      for (size_t Ci=0; Ci<FullShape[5]; ++Ci)
                          for (size_t Si=0; Si<FullShape[6]; ++Si)
                              for (size_t n=0; n<FullShape[7]; ++n)
                                  for (size_t s=0; s<FullShape[8]; ++s)
                                      for (size_t na=0; na<FullShape[9]; ++na)
                                          for (size_t p=0; p<FullShape[10]; ++p)
                                              for (size_t g=0; g<FullShape[11]; ++g)
                                                  for (size_t f=0; f<FullShape[12]; ++f)
                                                  {
                                                    size_t idx = f  +
                                                                 g  * FullShape[12] +
                                                                 p  * FullShape[12] * FullShape[11] +
                                                                 na * FullShape[12] * FullShape[11] * FullShape[10] +
                                                                 s  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] +
                                                                 n  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] +
                                                                 Si * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] +
                                                                 Ci * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] +
                                                                 Sd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] +
                                                                 Cd * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] +
                                                                 a  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] +
                                                                 j  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] +
                                                                 w  * FullShape[12] * FullShape[11] * FullShape[10] * FullShape[9] * FullShape[8] * FullShape[7] * FullShape[6] * FullShape[5] * FullShape[4] * FullShape[3] * FullShape[2] * FullShape[1]
                                                                 ;

                                                    SOURCE::State    sourceState     = SOURCE::State(sourceSet.Wavelength[w], sourceSet.Jones[j], sourceSet.Amplitude[a]);
                                                    CORESHELL::State scattererState  = CORESHELL::State(coreshellSet.CoreDiameter[Cd], coreshellSet.ShellDiameter[Sd], coreshellSet.CoreMaterial[Ci][w], coreshellSet.ShellMaterial[Si][w], coreshellSet.nMedium[n]);
                                                    DETECTOR::State  detectorState   = DETECTOR::State(detectorSet.ScalarField[0], detectorSet.NA[na], detectorSet.PhiOffset[p], detectorSet.GammaOffset[g], detectorSet.Filter[f], detectorSet.Coherent, detectorSet.PointCoupling);

                                                    CORESHELL::Scatterer Scat = CORESHELL::Scatterer(scattererState, sourceState);
                                                    DETECTOR::Detector det = DETECTOR::Detector(detectorState);

                                                    Output[idx] = abs( det.Coupling(Scat) );
                                                  }

  return vector_to_ndarray(Output, FullShape);
}

ndarray get_sphere_Qsca()    { return get_sphere_data( &SPHERE::Scatterer::get_Qsca ) ; }
ndarray get_sphere_Qext()    { return get_sphere_data( &SPHERE::Scatterer::get_Qext ) ; }
ndarray get_sphere_Qabs()    { return get_sphere_data( &SPHERE::Scatterer::get_Qabs ) ; }
ndarray get_sphere_Qpr()     { return get_sphere_data( &SPHERE::Scatterer::get_Qpr ) ; }
ndarray get_sphere_Qback()   { return get_sphere_data( &SPHERE::Scatterer::get_Qback ) ; }
ndarray get_sphere_Qforward(){ return get_sphere_data( &SPHERE::Scatterer::get_Qforward ) ; }
ndarray get_sphere_Csca()    { return get_sphere_data( &SPHERE::Scatterer::get_Csca ) ; }
ndarray get_sphere_Cext()    { return get_sphere_data( &SPHERE::Scatterer::get_Cext ) ; }
ndarray get_sphere_Cabs()    { return get_sphere_data( &SPHERE::Scatterer::get_Cabs ) ; }
ndarray get_sphere_Cpr()     { return get_sphere_data( &SPHERE::Scatterer::get_Cpr ) ; }
ndarray get_sphere_Cback()   { return get_sphere_data( &SPHERE::Scatterer::get_Cback ) ; }
ndarray get_sphere_Cforward(){ return get_sphere_data( &SPHERE::Scatterer::get_Cforward ) ; }
ndarray get_sphere_g()       { return get_sphere_data( &SPHERE::Scatterer::get_g ) ; }

Cndarray get_sphere_an(size_t max_order){ return get_sphere_coefficient( &SPHERE::Scatterer::get_an, max_order ) ; }
Cndarray get_sphere_bn(size_t max_order){ return get_sphere_coefficient( &SPHERE::Scatterer::get_bn, max_order ) ; }
Cndarray get_sphere_a1()                { return get_sphere_coefficient( &SPHERE::Scatterer::get_an, 1 ) ; }
Cndarray get_sphere_b1()                { return get_sphere_coefficient( &SPHERE::Scatterer::get_bn, 1 ) ; }
Cndarray get_sphere_a2()                { return get_sphere_coefficient( &SPHERE::Scatterer::get_an, 2 ) ; }
Cndarray get_sphere_b2()                { return get_sphere_coefficient( &SPHERE::Scatterer::get_bn, 2 ) ; }
Cndarray get_sphere_a3()                { return get_sphere_coefficient( &SPHERE::Scatterer::get_an, 3 ) ; }
Cndarray get_sphere_b3()                { return get_sphere_coefficient( &SPHERE::Scatterer::get_bn, 3 ) ; }

ndarray get_cylinder_Qsca()    { return get_cylinder_data( &CYLINDER::Scatterer::get_Qsca ) ; }
ndarray get_cylinder_Qext()    { return get_cylinder_data( &CYLINDER::Scatterer::get_Qext ) ; }
ndarray get_cylinder_Qabs()    { return get_cylinder_data( &CYLINDER::Scatterer::get_Qabs ) ; }
ndarray get_cylinder_Qpr()     { return get_cylinder_data( &CYLINDER::Scatterer::get_Qpr ) ; }
ndarray get_cylinder_Qback()   { return get_cylinder_data( &CYLINDER::Scatterer::get_Qback ) ; }
ndarray get_cylinder_Qforward(){ return get_cylinder_data( &CYLINDER::Scatterer::get_Qforward ) ; }
ndarray get_cylinder_Csca()    { return get_cylinder_data( &CYLINDER::Scatterer::get_Csca ) ; }
ndarray get_cylinder_Cext()    { return get_cylinder_data( &CYLINDER::Scatterer::get_Cext ) ; }
ndarray get_cylinder_Cabs()    { return get_cylinder_data( &CYLINDER::Scatterer::get_Cabs ) ; }
ndarray get_cylinder_Cpr()     { return get_cylinder_data( &CYLINDER::Scatterer::get_Cpr ) ; }
ndarray get_cylinder_Cback()   { return get_cylinder_data( &CYLINDER::Scatterer::get_Cback ) ; }
ndarray get_cylinder_Cforward(){ return get_cylinder_data( &CYLINDER::Scatterer::get_Cforward ) ; }
ndarray get_cylinder_g()       { return get_cylinder_data( &CYLINDER::Scatterer::get_g ) ; }

Cndarray get_cylinder_a1n(size_t max_order){ return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a1n, max_order ) ; }
Cndarray get_cylinder_b1n(size_t max_order){ return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b1n, max_order ) ; }
Cndarray get_cylinder_a2n(size_t max_order){ return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a2n, max_order ) ; }
Cndarray get_cylinder_b2n(size_t max_order){ return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b2n, max_order ) ; }
Cndarray get_cylinder_a11()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a1n, 1 ) ; }
Cndarray get_cylinder_b11()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b1n, 1 ) ; }
Cndarray get_cylinder_a21()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a2n, 1 ) ; }
Cndarray get_cylinder_b21()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b2n, 1 ) ; }
Cndarray get_cylinder_a12()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a1n, 2 ) ; }
Cndarray get_cylinder_b12()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b1n, 2 ) ; }
Cndarray get_cylinder_a22()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a2n, 2 ) ; }
Cndarray get_cylinder_b22()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b2n, 2 ) ; }
Cndarray get_cylinder_a13()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a1n, 3 ) ; }
Cndarray get_cylinder_b13()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b1n, 3 ) ; }
Cndarray get_cylinder_a23()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_a2n, 3 ) ; }
Cndarray get_cylinder_b23()                { return get_cylinder_coefficient( &CYLINDER::Scatterer::get_b2n, 3 ) ; }

ndarray get_coreshell_Qsca()    { return get_coreshell_data( &CORESHELL::Scatterer::get_Qsca ) ; }
ndarray get_coreshell_Qext()    { return get_coreshell_data( &CORESHELL::Scatterer::get_Qext ) ; }
ndarray get_coreshell_Qabs()    { return get_coreshell_data( &CORESHELL::Scatterer::get_Qabs ) ; }
ndarray get_coreshell_Qpr()     { return get_coreshell_data( &CORESHELL::Scatterer::get_Qpr ) ; }
ndarray get_coreshell_Qback()   { return get_coreshell_data( &CORESHELL::Scatterer::get_Qback ) ; }
ndarray get_coreshell_Qforward(){ return get_coreshell_data( &CORESHELL::Scatterer::get_Qforward ) ; }
ndarray get_coreshell_Csca()    { return get_coreshell_data( &CORESHELL::Scatterer::get_Csca ) ; }
ndarray get_coreshell_Cext()    { return get_coreshell_data( &CORESHELL::Scatterer::get_Cext ) ; }
ndarray get_coreshell_Cabs()    { return get_coreshell_data( &CORESHELL::Scatterer::get_Cabs ) ; }
ndarray get_coreshell_Cpr()     { return get_coreshell_data( &CORESHELL::Scatterer::get_Cpr ) ; }
ndarray get_coreshell_Cback()   { return get_coreshell_data( &CORESHELL::Scatterer::get_Cback ) ; }
ndarray get_coreshell_Cforward(){ return get_coreshell_data( &CORESHELL::Scatterer::get_Cforward ) ; }
ndarray get_coreshell_g()       { return get_coreshell_data( &CORESHELL::Scatterer::get_g ) ; }

Cndarray get_coreshell_an(size_t max_order){ return get_coreshell_coefficient( &CORESHELL::Scatterer::get_an, max_order ) ; }
Cndarray get_coreshell_bn(size_t max_order){ return get_coreshell_coefficient( &CORESHELL::Scatterer::get_bn, max_order ) ; }
Cndarray get_coreshell_a1()                { return get_coreshell_coefficient( &CORESHELL::Scatterer::get_an, 1 ) ; }
Cndarray get_coreshell_b1()                { return get_coreshell_coefficient( &CORESHELL::Scatterer::get_bn, 1 ) ; }
Cndarray get_coreshell_a2()                { return get_coreshell_coefficient( &CORESHELL::Scatterer::get_an, 2 ) ; }
Cndarray get_coreshell_b2()                { return get_coreshell_coefficient( &CORESHELL::Scatterer::get_bn, 2 ) ; }
Cndarray get_coreshell_a3()                { return get_coreshell_coefficient( &CORESHELL::Scatterer::get_an, 3 ) ; }
Cndarray get_coreshell_b3()                { return get_coreshell_coefficient( &CORESHELL::Scatterer::get_bn, 3 ) ; }
};



#endif

