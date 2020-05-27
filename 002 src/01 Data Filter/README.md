这个模块是基于trailing computation的想法构造的，在多因子模型中，常见的三种数值型数据可以分别归类为Factor, Classifier和Filter。其中，一般在构造stock universe的时候都需要使用一定的Filter，可以认为Filter是在已经得到structure data之后的数据预处理的核心，常见的Filter有：在过去180天内不存在st,*st etc. 在过去60天内最低成交量大于10000000之类的。



**Trailing computation**的基本设置

当定义trailing size = n时，实际上假设 trailing 区间为：

pos - n

...

pos - 2

pos - 1

pos < -- 假设观察者在pos-th且没有pos-th的信息。

但是可以在计算中修改这一点，见下文。



目前仍然是dev，没有模组化，下面是一些例子

**从MATLAB的str提取数据**

```Python
from utils import extract_data_from_matlabFile

testDataPath = "..\\data\\projectData.mat"
searchPath = ["projectData.stock.properties.close",
            "projectData.stock.properties.high",
            "projectData.stock.properties.low",
            "projectData.stock.properties.open",
            "projectData.stock.properties.amount",
            "projectData.stock.properties.volume",
            "projectData.stock.properties.PE_TTM",
            "projectData.stock.properties.PE",
            "projectData.stock.totalReturn",
            "projectData.stock.properties.totalMktCap",
           "projectData.stock.properties.floatingShares",
            "projectData.stock.tradeDayTable",
            "projectData.stock.stTable"]
sampleData = extract_data_from_matlabFile(testDataPath, 
                                          searchPath,
                                          isTranspose = True)
```



**内置的一些Filter** - 过去累计的st天数

```Python
from utils import Under_Threshold_CumulativeTradableRule
myTrailing_underThreshold = Under_Threshold_CumulativeTradableRule(
    sampleData["stTable"], startPos = 3,endPos = 7,trailingSize = 3, cumulationThreshold = 7)
myTrailing_underThreshold.run_trailing()
print(myTrailing_underThreshold.get_trailingResult())
```



**内置的一些Filter** - 截面收盘价排序（昨天收盘价位于95%以上区间,quantile排序时忽略nan）

```Python
from utils import Over_Threshold_CrossSectionalQuantile
myTrailing_overQuantile = Over_Threshold_CrossSectionalQuantile(sampleData["close"], startPos = 3, endPos = 7, quantileThreshold = 0.95, trailingSize = 2)
myTrailing_overQuantile.run_trailing()
print(myTrailing_overQuantile.get_trailingResult())
```



假设现在有一种新的trailing computation情况：

pos - (n-1)

...

pos - 2

pos - 1

pos <--假设观察者在pos-th且有pos-th的信息， 那么这时候在定义中trailingSize = n-1而不是之前的n，那么怎么体现可以利用pos-th的信息呢，如下：

```Python
from TimeSeriesTrailingGenerator import TrailingTimeSeries
class cumulativeSum(TrailingTimeSeries):
    def __init__(self, df, startPos, endPos, trailingSize):
        #更推荐使用 super().__init__(df, startPos, endPos, trailingSize) 来取代下面4行
        self.startPos = startPos
        self.endPos = endPos
        self.rawData = df
        self.trailingSize = trailingSize
    
    def compute_trailingSlice(self, trailingSlice):
        """
        imaging have the following dataframe:
            
        index 				   | col1  | col2  | ...|
        pos-(trailingSize)     | value1| value2|
        pos-1   			   | value3| value5|
        pos   			   | value4| value6|
        """
        #return np.sum(trailingSlice.values[:-1,:],axis = 0) #没有使用pos-th的信息
    	return np.sum(trailingSlice.values[:,:],axis = 0) #使用了pos-th的信息
```

