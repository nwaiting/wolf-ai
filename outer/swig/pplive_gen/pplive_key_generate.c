#include <Python.h>
void getKey(char* pkey , time_t t);

#ifdef WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

static PyObject*  generate_old_key(PyObject* self, PyObject* args)
{
  int t, result;
  char key[33]={0};

  if (! PyArg_ParseTuple(args, "i:time", &t))
    return NULL;

  getKey( key , t );

  return Py_BuildValue("s", key);
}


static PyMethodDef moduleMethods[] =
{
  {"generateOldKey", generate_old_key, METH_VARARGS, "generate pplive old key"},
  {NULL, NULL}
};


EXPORT void initpplive_key_generate()
{
  PyObject* m;
  m = Py_InitModule("pplive_key_generate", moduleMethods);
  
}
