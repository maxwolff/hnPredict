import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def openSentiments(): 
    comments = parse('comments.txt') #0
    score = parse('score.txt')       #1 
    anger = parse('anger.txt')       #2
    disgust = parse('disgust.txt')   #3
    fear = parse('fear.txt')         #4
    joy = parse('joy.txt')           #5
    sadness = parse('sadness.txt')   #6

    print len(sadness)
    return np.array([comments,score, anger,disgust,fear,joy,sadness])

def parse(file):
    arr = []
    with open(file, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            arr.append(float(row[0]))
    return arr


sentiments = openSentiments()

x = sentiments[0]
y = sentiments[6]


gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print r_value, p_value, std_err
plt.scatter(x,y)
plt.plot(x, (gradient*x + intercept))
plt.show()


