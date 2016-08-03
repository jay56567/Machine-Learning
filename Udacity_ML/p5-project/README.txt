README file for Investment trending predictor

1. what's in the package:
    report.pdf
    tradePred.py  <- project code
    google.csv    <- dataset
    IBM.csv       <- dataset

2. user instruction:
when running the code, you will be prompted to input the stock name.
So far the tool only supports the two stock names: google  and IBM
the valid input: 
google
IBM

the input is not case sensitive. meaning IBM=iBm for example.

after the stock name is correctly input, you would be asked to input a Predict Period time.
So far the tool only supports three different time, the valid input would be :
7
14
28

7 means 7 days in the future after the last date in the datasets 
14 means 14 days in the future after the last date in the datasets 
28 means 28 days in the future after the last date in the datasets 

After the valid inputs, the code will generate the result accuracy, best sell/buy points, and plot the final in one picture figure
