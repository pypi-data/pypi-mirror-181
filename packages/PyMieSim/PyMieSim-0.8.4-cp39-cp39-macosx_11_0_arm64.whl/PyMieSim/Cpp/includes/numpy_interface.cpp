#ifndef NUMPY_INTERFACE_H
#define NUMPY_INTERFACE_H

  #include "Definitions.cpp"


  std::vector<size_t>
  GetStride(std::vector<size_t> Dimension)
  {
    std::reverse(Dimension.begin(), Dimension.end());

    std::vector<size_t> stride;
    stride.push_back( sizeof(double) );

    for (size_t i=0; i<Dimension.size()-1; ++i)
        stride.push_back( stride[i] * Dimension[i] );

    std::reverse(stride.begin(), stride.end());

    return stride;

  }

  template <typename T>
  pybind11::array_t<T> vector_to_ndarray(std::vector<T> &Vector, std::vector<size_t> dimension)
{
    pybind11::array_t<T>  PyVector;

    std::vector<T> * OVectors = new std::vector<T>;
    (*OVectors) = Vector;

    std::vector<size_t> stride = GetStride(dimension);

    pybind11::capsule free_when_done(OVectors->data(), [](void *f) {
       T *foo = reinterpret_cast<T *>(f);
       delete []foo; } );

    PyVector = pybind11::array_t<T>( dimension, stride, OVectors->data(), free_when_done );

     return PyVector;
  }



  template <typename T>
  pybind11::array_t<T> vector_to_ndarray(std::vector<T> &Vector)
{

      pybind11::array_t<T>  PyVector;

      std::vector<T> * Output = new std::vector<T>;
      (*Output) = Vector;

      std::vector<size_t> stride = {sizeof(T)};
      std::vector<size_t> dimension ={Vector.size()};

      pybind11::capsule free_when_done(Output->data(), [](void *f) {
         T *foo = reinterpret_cast<T *>(f);
         delete []foo; } );

      PyVector = pybind11::array_t<T>( dimension, stride, Output->data(), free_when_done );

     return PyVector;
  }













  template<typename T>
  pybind11::array_t<T>
  vector_to_ndarray(std::vector<T> &Vector, std::vector<size_t> dimension, std::vector<size_t> stride){

    pybind11::capsule free_when_done(Vector.data(), [](void *f) { T *foo = reinterpret_cast<T *>(f); } );

    pybind11::array_t<T> PyVector = pybind11::array_t<T>( dimension, stride, Vector.data(), free_when_done );

    return PyVector;
  }

  template<typename T>
  inline pybind11::array_t<T>
  vector_to_ndarray(std::vector<T>&& passthrough)
  {
    auto* ptr = new std::vector<T>(std::move(passthrough));

    const pybind11::capsule freeWhenDone(ptr, [](void *toFree) { delete static_cast<std::vector<T> *>(toFree); });

    auto Numpy = pybind11::array_t<T>({ptr->size()}, {sizeof(T)}, ptr->data(), freeWhenDone);

    return Numpy;
  }




  template<typename T>
  inline pybind11::array_t<T>
  vector_to_ndarray_copy(std::vector<T> passthrough, IVector &Shape)
  {
    auto* ptr = new std::vector<T>(std::move(passthrough));

    const pybind11::capsule freeWhenDone(ptr, [](void *toFree) { delete static_cast<std::vector<T> *>(toFree); });

    auto Numpy = pybind11::array_t<T>({ptr->size()}, {sizeof(T)}, ptr->data(), freeWhenDone);

    Numpy.resize(Shape);

    return Numpy;
  }

  template<typename T>
  inline pybind11::array_t<T>
  vector_to_ndarray_copy(std::vector<T> passthrough)
  {
    auto* ptr = new std::vector<T>(std::move(passthrough));

    const pybind11::capsule freeWhenDone(ptr, [](void *toFree) { delete static_cast<std::vector<T> *>(toFree); });

    auto Numpy = pybind11::array_t<T>({ptr->size()}, {sizeof(T)}, ptr->data(), freeWhenDone);

    return Numpy;
  }

  template<typename T>
  inline pybind11::array_t<T>
  vector_to_ndarray(std::vector<T>&& passthrough, IVector &Shape)
  {
    auto* ptr = new std::vector<T>(std::move(passthrough));

    const pybind11::capsule freeWhenDone(ptr, [](void *toFree) { delete static_cast<std::vector<T> *>(toFree); });

    auto Numpy = pybind11::array_t<T>({ptr->size()}, {sizeof(T)}, ptr->data(), freeWhenDone);

    Numpy.resize(Shape);

    return Numpy;
  }




  template<typename T>
  inline pybind11::array_t<T>
  vector_to_ndarray(std::vector<T>&& passthrough, IVector &&Shape)
  {
    auto* ptr = new std::vector<T>(std::move(passthrough));

    const pybind11::capsule freeWhenDone(ptr, [](void *toFree) { delete static_cast<std::vector<T> *>(toFree); });

    auto Numpy = pybind11::array_t<T>({ptr->size()}, {sizeof(T)}, ptr->data(), freeWhenDone);

    Numpy.resize(Shape);

    return Numpy;
  }

#endif
