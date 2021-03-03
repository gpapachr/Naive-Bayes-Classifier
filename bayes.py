import string
from os import listdir
from os.path import isfile, join

def text_cleaning(a):
    clean = [char for char in a if char not in string.punctuation]
    clean = ''.join(clean)
    return [word.lower() for word in clean.split()]

def sort(d):
    sorted_dict = {}
    sorted_keys = sorted(d, reverse=1, key=d.get)

    for w in sorted_keys:
        sorted_dict[w] = d[w]

    return sorted_dict

def total_freq(vocabulary):
    tf = 0
    for freq in vocabulary.values():
        tf += freq
    return tf

def probability_count(input, vocabulary, vl, tf, apriori):   #input: review, vocabulary: negative or positive, vl: vocabulary length, tf: total_freq, apriori: initialized as 0.5
    
    probability = 1
    for word in input:
        if input[word] == 1:
            probability *= (vocabulary[word] + 1) / (tf+vl)
        else:
            probability *= 1 / (tf+vl)
    probability *= apriori
    return probability

def testNegatives(folder, p, negDict, nlength, posDict, plength):  #folder: train, dev or test, p: percentage of data to check 
    
    print("Starting negative test reading")

    files = [f for f in listdir(folder + "/neg") if isfile(join(folder + "/neg", f))]

    target = p/100*len(files)
    total = target
    check = 0

    ctr = 0
    print(total)
    trueNegative = 0
    falsePositive = 0
    tfn = total_freq(negDict)
    tfp = total_freq(posDict)

    for file in files:

        if check >= target:
            break
        file = open(folder + "/neg/" + file, errors = "ignore")
        text = file.read()
        file.close()
        text = text_cleaning(text)
        nreview = {}
        preview = {}
        for word in text:
            if word in negDict.keys():
                nreview[word] = 1
            else:
                nreview[word] = 0
            if word in posDict.keys():
                preview[word] = 1
            else:
                preview[word] = 0
        neg = probability_count(nreview, negDict, nlength, tfn, 0.5)
        pos = probability_count(preview, posDict, plength, tfp, 0.5)

        if neg >= pos:
            trueNegative += 1
        else:
            falsePositive += 1
        ctr += 1
        check += 1
        print("{} out of {} negative reviews".format(ctr, total))

    
    results = [total, trueNegative, falsePositive]

    return results

def testPositives(folder, p, negDict, nlength, posDict, plength): #folder: train, dev or test, p: percentage of data to check 
    
    print("Starting positive test reading")
    
    files = [f for f in listdir(folder  + "/pos") if isfile(join(folder  + "/pos", f))]

    target = p/100*len(files)
    total = target
    check = 0

    ctr = 0
    truePositive = 0
    falseNegative = 0
    tfn = total_freq(negDict)
    tfp = total_freq(posDict)
    
    for file in files:

        if check >= target:
            break
        file = open(folder  + "/pos/" + file, errors = "ignore")
        text = file.read()
        file.close()
        text = text_cleaning(text)
        nreview = {}
        preview = {}
        for word in text:
            if word in negDict.keys():
                nreview[word] = 1
            else:
                nreview[word] = 0
            if word in posDict.keys():
                preview[word] = 1
            else:
                preview[word] = 0
        neg = probability_count(nreview, negDict, nlength, tfn, 0.5)
        pos = probability_count(preview, posDict, plength, tfp, 0.5)

        if neg <= pos:
            truePositive += 1
        else:
            falseNegative +=1
        ctr += 1
        check += 1
        print("{} out of {} positive reviews".format(ctr, total))
    results = [total, truePositive, falseNegative]

    return results

def train(p):

    negDict = {}
    posDict = {}
    nlength = plength = 0

    files = [f for f in listdir("train/neg") if isfile(join("train/neg", f))]
    check = 0
    target = p/100*len(files)

    for file in files:
        if (check >= target):
            break
        file = open("train/neg" + "/" + file, errors="ignore")
        text = file.read()
        file.close()
        review = text_cleaning(text)
        for word in review:
            if word in negDict:
                negDict[word] += 1
            else:
                negDict[word] = 1
                nlength += 1
        check+=1

    sorted_neg = sort(negDict)

    files = [f for f in listdir("train/pos") if isfile(join("train/pos", f))]
    check = 0
    target = p/100*len(files)

    for file in files:
        if (check >= target):
            break
        file = open("train/pos" + "/" + file, errors="ignore")
        text = file.read()
        file.close()
        review = text_cleaning(text)
        for word in review:
            if word in posDict:
                posDict[word] += 1
            else:
                posDict[word] = 1
                plength += 1
        check+=1

    sorted_pos = sort(posDict)

    nr = testNegatives("train", p, sorted_neg, nlength, sorted_pos, plength)
    pr = testPositives("train", p, sorted_neg, nlength, sorted_pos, plength)

    TN = nr[1]                  #true negative
    TP = pr[1]                  #true positive
    totalN = nr[0]              #total negative
    totalP = pr[0]              #total positive
    total = totalN+totalP       #total reviews
    FN = pr[2]                  #false negative
    FP = nr[2]                  #false positive

    train_accuracy = (TN + TP) / total

    results = [sorted_neg, sorted_pos, train_accuracy, FN, FP]

    with open("train_results.txt", "a") as tr:
        tr.write("p% = {}\nFN = {}\nFP = {}\nTrain Accuracy = {}\n------------------\n".format(p, FN, FP, train_accuracy))
    with open("tr.txt", "a") as t:
        t.write("{}\n".format(train_accuracy))
    return results

def dev(p, m, n, negDict, posDict):
    nlength = plength = 0

    newNegDict = {}
    newPosDict = {}
    ctr = 0

    for w in negDict.keys():
        if (ctr < n):
            ctr += 1
            continue
        if(nlength > m):
            break
        nlength +=1
        newNegDict[w] = negDict[w]
    
    ctr = 0

    for w in posDict.keys():
        if (ctr < n):
            ctr += 1
            continue
        if(plength > m):
            break
        plength +=1
        newPosDict[w] = posDict[w]
       
    
    nr = testNegatives("dev", p, newNegDict, nlength, newPosDict, plength)
    pr = testPositives("dev", p, newNegDict, nlength, newPosDict, plength)

    print("dev round {} completed".format(p/10))

    TN = nr[1]
    TP = pr[1]
    totalN = nr[0]
    totalP = pr[0]
    total = totalN+totalP
    FN = pr[2]
    FP = nr[2]

    dev_accuracy = (TN + TP) / total
    
    print("Results counting...")

    with open("dev_results.txt", "a") as results:
        results.write("m = {}\nn = {}\np% = {}\nFN = {}\nFP = {}\nDev Accuracy = {}\n------------------\n".format(m, n, p, FN, FP, dev_accuracy))
    with open("dr_{}_{}.txt".format(m,n), "a") as d:
        d.write("{}\n".format(dev_accuracy))

    return dev_accuracy

def test(p, m, n, negDict, posDict):
    nlength = plength = 0

    newNegDict = {}
    newPosDict = {}
    ctr = 0

    for w in negDict.keys():
        if (ctr < n):
            ctr += 1
            continue
        if(nlength > m):
            break
        nlength +=1
        newNegDict[w] = negDict[w]
    
    ctr = 0

    for w in posDict.keys():
        if (ctr < n):
            ctr += 1
            continue
        if(plength > m):
            break
        plength +=1
        newPosDict[w] = posDict[w]
   
      
    nr = testNegatives("test", p, newNegDict, nlength, newPosDict, plength)
    pr = testPositives("test", p, newNegDict, nlength, newPosDict, plength) 

    print("test round {} completed".format(p/10))

    TN = nr[1]
    TP = pr[1]
    totalN = nr[0]
    totalP = pr[0]
    total = totalN+totalP
    FN = pr[2]
    FP = nr[2]

    test_accuracy = (TN + TP) / total
    precision = TP / (TP + FP)
    recall    = TP / (TP + FN)
    f1 = (2*precision * recall)/(precision + recall)
    
    print("Results counting...")

    with open("test_results.txt", "a") as results:
        results.write("p% = {}\nFN = {}\nFP = {}\nTest Accuracy = {}\nPrecision = {}\nRecall = {}\nF1 = {}\n------------------\n".format
        (p, FN, FP, test_accuracy, precision, recall, f1))

    with open("precision.txt", "a") as f:
        f.write("{}\n".format(precision))

    with open("recall.txt", "a") as f:
        f.write("{}\n".format(recall))

    with open("f1.txt", "a") as f:
        f.write("{}\n".format(f1))

    return test_accuracy

#################################################################################################################
#start main loop

best_m = best_n = best_acc = 0
for p in range(10, 101, 10):
    tr = train(p)

    negDict = tr[0]
    posDict = tr[1]

    print("Train completed for p = {}%".format(p))    

    for m in range(100, 301, 100):
        for n in range(100, 301, 100):
            new_acc = dev(p, m, n, negDict, posDict)
            
            if (new_acc > best_acc):
                best_acc = new_acc
                best_m = m
                best_n = n

with open("best_m_n.txt", "a") as d:
        d.write("{}\n{}\n{}\n".format(best_m, best_n, best_acc))            

for p in range(10, 101, 10):
    tr = train(p)

    negDict = tr[0]
    posDict = tr[1]
    test(p, best_m, best_n, negDict, posDict)

print("Execution Finished")
    