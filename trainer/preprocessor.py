import pandas as pd
import numpy as np


# pre-process the input files
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Fill the missing age values by using the mean both on train and test data sets
train = pd.read_csv('../data/train.csv')
test = pd.read_csv('../data/test.csv')
full = pd.concat([train, test])

print(train["Age"].isnull().sum())
print(test["Age"].isnull().sum())
print(full["Age"].isnull().sum())
print(full["Age"].mean())


file = open('../data/train.data.csv')
writer = open('../data/train.data.processed.csv', 'w')

line = file.readline()

while line:
    cols = line.split(',')
    title = cols[4].strip().split(' ')[0]
    print(title)
    cabin_class = cols[11][:1]
    cabin_nos = cols[11][1:]
    cabin_no = cabin_nos.split(' ')[0]
    cabin_no = cabin_no if is_int(cabin_no) else 0
    # print(cabin_class)
    # print(cabin_no)
    writer.write('{},{},{},{}\n'.format(line.rstrip(), cabin_class, cabin_no, title))
    line = file.readline()

file.close()
writer.close()