#coding=utf-8

import tensorflow as tf

"""
一、arthmetic 算术操作（+，-，*，/，Mod）

（1）tensor-tensor操作(element-wise)
#两个tensor 运算
#运算规则：element-wise。即c[i,j,..,k]=a[i,j,..,k] op b[i,j,..,k]
"""
ts1=tf.constant(1.0,shape=[2,2])
ts2=tf.Variable(tf.random_normal([2,2]))
sess.run(tf.global_variables_initializer())
#以ts1和ts2为例：

#（1）加法+
ts_add1=tf.add(ts1,ts2,name=None)
ts_add2=ts1+ts2       #二者等价
#（2）减法-
ts_sub1=tf.subtract(ts1,ts2,name=None)
ts_sub2=ts1-ts2       #二者等价
#（3）乘法*
ts_mul1=tf.multiply(ts1,ts2,name=None)
ts_mul2=ts1*ts2
#（4）除法/
ts_div1=tf.divide(ts1,ts2,name=None)
ts_div2=tf.div(ts1,ts2,name=None)   #div 支持 broadcasting(即shape可不同)
ts_div3=ts1/ts2
#另外还有truediv(x,y) x,y类型必须一致,floor_div等。
#（5）取模Mod(估计基本用不到)

"""
（2）tensor-scalar操作
"""
#scalar-tensor操作。
#对tensor中所有element执行同样的操作(+，-，*，/)
#加法
ts_add=ts1+2
#减法
ts_sub=ts1-2
#乘法
ts_mul=ts1*2
#除法
ts_div=ts1/2

"""
二、基本数学函数

[python] view plain copy
#以下x,y均代表tensor
"""

tf.add_n(inputs, name=None)  #inputs:tensor数组，所有tensor相加
tf.abs(x, name=None)         #绝对值
tf.negative(x, name=None)    #取反
tf.sign(x, name=None)        #取符号(y = sign(x) = -1 if x < 0; 0 if x == 0; 1 if x > 0.)
tf.square(x, name=None)      #y=x*x
tf.round(x, name=None)       #Rounds the values of a tensor to the nearest integer, element-wise.
tf.sqrt(x, name=None)        #sqrt
tf.pow(x, y, name=None)      #x,y均为tensor，element-wise求pow
tf.exp(x, name=None)         #y=e^x
tf.log(x, name=None)         #y=log(x)
tf.ceil(x, name=None)        #ceil
tf.floor(x, name=None)       #floor
tf.maximum(x, y, name=None)  #z=max(x,y)
tf.minimum(x, y, name=None)
tf.cos(x, name=None)         #三角函数,sin,cos,tan,acos,asin,atan
tf.sin(x, name=None)
tf.tan(x, name=None)
tf.acos(x, name=None)
tf.asin(x, name=None)
tf.atan(x, name=None)
#...
#等等一些函数。

"""
三、Matrix矩阵操作

[python] view plain copy
"""

tf.diag(diagonal, name=None)         #得到以diagonal为对角的tensor
tf.diag_part(input, name=None)       #tf.diag 逆操作,得到input的对角矩阵
tf.transpose(a, perm=None,name=None) #转置矩阵,y[i,j]=x[j,i]
#矩阵乘法
tf.matmul(a, b,
  transpose_a=False, transpose_b=False,  #
  adjoint_a=False, adjoint_b=False,      #共轭
  a_is_sparse=False, b_is_sparse=False,  #矩阵是否稀疏
  name=None)

"""
还有一些其他的矩阵操作，见matirx
四、Reduction 归约操作

[python] view plain copy
"""
#（1）tf.reduce_sum
#当keep_dims=False。rank of tensor会降维度。
tf.reduce_sum(input_tensor,
   axis=None,               #要归约的dimention。值为None或一个数字或者数组。如0,1,[0,3,4]
   keep_dims=False,         #if true, retains reduced dimensions with length 1.
   name=None,
   reduction_indices=None)

#（2）tf.reduce_min / tf.reduce_max / tf.reduce_mean
#参数与tf.reduce_sum一致。
#tf.reduce_min : 被归约的数取最小值；
#tf.reduce_max : 被归约的数取最大值；
#tf.reduce_mean: 被归约的数取平均值。

#（3）逻辑操作
# tf.reduce_all：logical and operation
# tf.reduce_any: logical or operation


#（4）自定义操作函数
tf.einsum(equation, *inputs)
#例子：
tf.einsum('ij,jk->ik', ts1,ts2)  #矩阵乘法
tf.einsum('ij->ji',ts1)          #矩阵转置

"""
五、tensor大小 比较

[python] view plain copy
"""

#(1)相等equal (element-wise)
tf.equal(x, y, name=None) #Returns the truth value of (x == y) element-wise.

#(2)不等not_equal
tf.not_equal(x, y, name=None)

#(3)其他比较
tf.less(x, y, name=None)
tf.less_equal(x, y, name=None)
tf.greater(x, y, name=None)
tf.greater_equal(x, y, name=None)

"""
六、恒等映射

[python] view plain copy
"""
#恒等映射
tf.identity(input, name=None) #Return a tensor with the same shape and contents as the input tensor or value.

"""
七、类型转化

[python] view plain copy
"""
tf.cast(x, dtype, name=None)
#Casts a tensor to a new type.

#For example:
# tensor `a` is [1.8, 2.2], dtype=tf.float
#tf.cast(a, tf.int32) ==> [1, 2]  dtype=tf.int32

"""
八、例子

（1）RELU实现
[html] view plain copy
"""
def relu(x):        #要构造一个和x shape一样的Tensor。源码中应该不会用效率这么低的写法。
  y=tf.constant(0.0,shape=x.get_shape())
  return tf.where(tf.greater(x,y),x,y)

sess=tf.Session()
x=tf.Variable(tf.random_normal(shape=[10],stddev=10))
sess.run(tf.global_variables_initializer())
x_relu=relu(x)
data_x,data_x_relu=sess.run((x,x_relu))
for i in range(0,len(data_x)):
  print("%.5f  --relu--> %.5f" %(data_x[i],data_x_relu[i]))
