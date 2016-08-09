import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation 
from sklearn.linear_model import LinearRegression,RidgeCV
import datetime,time 
from matplotlib import pyplot as plt
from matplotlib import style,dates
import ModelLearning as ML
from scipy import stats

#
# capstone project
# build a investment trending predictor tool
#

# user input validations
data = pd.DataFrame()
input = False
while (input != True):
    dataName = raw_input('please input stock name(only Google, IBM are suuported for now): ')
    if dataName.upper() == 'GOOGLE':
        data = pd.read_csv('googl.csv').set_index('Date')
        input = True
    elif dataName.upper() == 'IBM':
        data = pd.read_csv('IBM.csv').set_index('Date')
        input = True
    else: print 'wrong input, try again or use Ctrl-C to terminate. '

input = False
while (input != True):
    # test if the input for time period matches the expect
    predPeriod = raw_input('please input the predict period: you can do 7, 14, 28: ')
    if not predPeriod.isdigit() or \
       predPeriod != '7' and \
       predPeriod != '14' and \
       predPeriod != '28':
        print 'wrong input, try again or use Ctrl-C to terminate. '
    else: input = True

#good input, we need to prepare data first
predPeriod = int(predPeriod)
data = data.sort_index()
     
# calculate high low value change %
data['highLowChg%'] = (data['High'] - data['Low']) *100 / data['Adj Close']

# calculate open close value change %
data['openCloseChg%'] = (data['Adj Close'] - data['Open']) * 100 / data['Open']

# make up the new feature for dataset
dataset = pd.DataFrame(data[['Volume', 'highLowChg%', 'openCloseChg%', 'Adj Close']])

#print data #[debug]

label_y = 'Adj Close' # create label 

# fill all the naN fields instead of just get rid of them
dataset.fillna(value=-9999999, inplace=True)

# create predict label for future and make a new column that put
# current label value and value needs to be predicted together
dataset['label'] = dataset[label_y].shift(-predPeriod) 

#print data

# create feature table
X = np.array(dataset.drop(['label'], axis = 1))

# feature scaling
X = preprocessing.scale(X)

# create features for predict
X_pred = X[-predPeriod:]

X = X[:-predPeriod] #re-sizing the features for training
dataset.dropna(inplace=True) # get rid of naN for 'label' column

# create label 
y = np.array(dataset['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2, random_state=1)

# use linearRegression as algrithm
#clf = LinearRegression()
clf = RidgeCV (alphas =[0.1, 0.5, 1, 10])
clf.fit(X_train, y_train)
#start_time = time.time()
y_pred = clf.predict(X_pred)
#print time.time() - start_time
accuracy = clf.score(X_test, y_test)
# visualize Learning Curves
#ML.ModelLearning(X, y)
#ML.ModelComplexity(X_train, y_train)

#Linear slope calculation
#print clf.alpha_
#print clf
#print clf.coef_
#print clf.intercept_
print 'predict accuracy is: {:0.2f}'.format(accuracy)


# build a column in data for predict result
data['predict/Adj Close'] = data['Adj Close'] # add column for predict value/Adj Close

# build up the date for predict period
lastDateInSec = time.mktime(datetime.datetime.strptime(data.iloc[-1].name, "%Y-%m-%d").timetuple())
dayInSec = 86400 # one day has 60 * 60 * 24 seconds

for y in y_pred:
    nextDate = datetime.datetime.fromtimestamp(lastDateInSec + dayInSec).strftime("%Y-%m-%d")
    tmp =  nextDate.split('-')
    if datetime.date(int(tmp[0]),int(tmp[1]),int(tmp[2])).weekday() >= 4:
        lastDateInSec += dayInSec * 3 
    else:
        lastDateInSec += dayInSec
    data.loc[nextDate] =[np.nan for _ in range(len(data.columns) - 1)] + [y]

#enhansement suggest buy/sell points
sellPoint = y_pred.max()
sellDate  = data[data['predict/Adj Close'] == sellPoint].index.tolist()[0]
print 'best sell point is: {:0.2f} at {}'.format(sellPoint,sellDate) 

buyPoint = y_pred.min()
buyDate  = data[data['predict/Adj Close'] == buyPoint].index.tolist()[0]
print 'best buy point is: {:0.2f} at {}'.format(buyPoint,buyDate) 

data['bestSellBuy'] = np.nan # create a new coloumn for best sell and best buy, for later plot
idx = data[data['predict/Adj Close'] == sellPoint].index
data.set_value(idx[0],'bestSellBuy', sellPoint)

idx = data[data['predict/Adj Close'] == buyPoint].index
data.set_value(idx[0],'bestSellBuy', buyPoint)

# now let's visualize the data
style.use('ggplot')
data['predict/Adj Close'].plot(label='predict')
data['Adj Close'].plot(label='Adj Close')
data['Open'].plot(label='Open')
data['bestSellBuy'].plot(x=data.index, y='bestSellBuy', style='bx')

plt.legend(loc= 'lower left')
plt.xlabel('Date')
plt.ylabel('price')
plt.title('Stock Price Prediction for : ' + dataName.upper())
plt.show()
