#include <Python.h>
void getExample(char* getexp);

#ifdef WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

static PyObject*  get_pplive_example(PyObject* self, PyObject* args)
{
  int t, result;
  char key[64]={0};
  getExample(key);
  return Py_BuildValue("s", key);
}


static PyMethodDef moduleMethods[] =
{
  {"getPPliveExample", get_pplive_example, METH_VARARGS, "pplive example"},
  {NULL, NULL}
};


EXPORT void initpplive_example()
{
  PyObject* m;
  m = Py_InitModule("pplive_example", moduleMethods);

}
