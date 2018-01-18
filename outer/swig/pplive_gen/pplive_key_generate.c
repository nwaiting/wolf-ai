#include <Python.h>
void getKey(char* pkey , time_t t);

#ifdef WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

/*
    写程序编译成dll文件
    这个libspam.dll就是我们需要的动态库，将它改名为spam.pyd(python中的pyd其实就是dll)，复制到你的python路径/libs目录下
*/

static PyObject*  generate_old_key(PyObject* self, PyObject* args)
{
  int t, result;
  char key[33]={0};

  if (! PyArg_ParseTuple(args, "i:time", &t))
    return NULL;

  getKey( key , t );

  /*
    s = char *
    i = int
    l = long int
    h = short int
    c = char
    f = float
    d = double
    O = PyObject *
    (items) = A tuple
    |items = Optional arguments
    Py_BuildValue和PyArg_ParseTuple功能相反，它会将C的值转换成Python的值
  */
  return Py_BuildValue("s", key);
}

/*
    PyMethodDef moduleMethods数组定义了需要导出到Python中的名字，函数指针，参数类型，描述信息。注意第三个参数，标志了函数的参数类型
    METH_VARARGS代表的就是我们写Python时的*args,而METH_KEYWORDS就是Python中的**kwargs,所谓的字典字典变量。描述信息就在Python中就是DocString了
*/
static PyMethodDef moduleMethods[] =
{
  {"generateOldKey", generate_old_key, METH_VARARGS, "generate pplive old key"},
  {NULL, NULL}
};


/*
模块名：
    最后就需要初始化该模块了，注意名字必须是initXXX，其中XXX就是我们所说的模块名。也就是说我们重命名的pyd文件名，initXXX和Py_InitModule(XXX)三者必须一致
*/
EXPORT void initpplive_key_generate()
{
  PyObject* m;
  m = Py_InitModule("pplive_key_generate", moduleMethods);
}
