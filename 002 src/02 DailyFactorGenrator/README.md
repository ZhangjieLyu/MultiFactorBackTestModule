# How to install matlab.engine for python 
---
in our project we'll need to install matlab for python to run the matlab base code.
if you only use python code you can skip this part 

The matlab.engine is not a package you can find in conda. Instead we need to install through a setup.py given by matlab

My envirment 
1. python 3.6 (using anaconda)
2. matlab 2018a
3. conda (forgot version, I don't think is important)

if you don't use conda you can follow this guide given by matlab
[安装用于 Python 的 MATLAB 引擎 API](https://ww2.mathworks.cn/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)

For anaconda env I used following steps ref to [this link](https://ww2.mathworks.cn/matlabcentral/answers/346068-how-do-i-properly-install-matlab-engine-using-the-anaconda-package-manager-for-python):

1. open CMD 
2. activate the env. Mine is env_mlf, type in your env name![](https://i.imgur.com/KJqkOTI.png)
3. find the root path of your matlab![](https://i.imgur.com/FLfTHpQ.png)
4. cd to .\extern\engines\python
5. python setup.py install
![](https://i.imgur.com/kNXsjUL.png)



# How to use PythonFactorGenerator.py

1. import 

```Python
from PythonFactorGenerator import PythonFactorGenerator
```

2. init

```python
factorRequirement_dict={'testFactor1':
                        {'functionName': 'testSum',
                         'datasetNames':['close','high'],
                         'parameters':{"p":23}},
                        'testFactor2':
                        {'functionName': 'testMinus',
                         'datasetNames':['close', 'high'],
                         'parameters':{"p":3}}
                        }
generationType_str = 'Python'
startPos = 3
endPos = 5

testGenerator = PythonFactorGenerator(generationType_str, factorRequirement_dict,
                                      startPos = startPos, endPos = endPos)
```

3. get factor from your folder
注意，在自己定义的 module.class中，最终计算函数需要和class name相同，都是factorProfile.functionName，这样的设计设计是为了使得可以定义的计算function更加复杂，可以接入各类机器学习学习方法，只要最后使用带有module.functionName.functionName() signature的method返回计算结果就可以了。

```Python
testGenerator.set_factor_expression_search_path("..\\03 FactorFunctions\\python",
                                                ['testFactors'])
aResult = testGenerator.get_factor('testFactor1')
groupOfResults = testGenerator.get_all_factors(verbose = 1)
```

results:

```
set factor expression path: C:\Users\91592\Dropbox\WorkingSpace\NaiveBackTestPy_ForLoop\02 src\03 FactorFunctions\python
testFactor1 generated successfully via testFactors.testSum
testFactor1 generated successfully via testFactors.testSum
testFactor2 generated successfully via testFactors.testMinus
```

