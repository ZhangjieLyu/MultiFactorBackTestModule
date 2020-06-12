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


