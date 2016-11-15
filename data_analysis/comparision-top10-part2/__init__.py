from __future__ import division
# print(__doc__)
import time
import numpy as np
# from sklearn import preprocessing
# from sklearn.datasets.samples_generator import make_blobs
from collections import defaultdict
import math
import random
import multiprocessing
from numpy import genfromtxt
from numpy import loadtxt
import linecache
import heapq
from scipy.spatial.distance import euclidean
import csv
import os
import pickle

INF = 999999


def NormalizeOneDem(oneDemdata):
    maxnum = -1000
    minnum = 100000
    for i in range(len(oneDemdata)):
        if float(oneDemdata[i]) >= maxnum:
            maxnum = float(oneDemdata[i])
        if float(oneDemdata[i]) <= minnum:
            minnum = float(oneDemdata[i])
    for i in range(len(oneDemdata)):
        if maxnum == minnum:
            oneDemdata[i] = 0
        else:
            oneDemdata[i] = (float(oneDemdata[i]) - minnum) / (maxnum - minnum)
    return oneDemdata


def getHitAboveT(query, hitTable, hitparaIndex, IndexPara):
    q_hit_above_T = dict()
    for q in query:  # query is the #8 point
        q_hit_above_T[q] = []
        for j in range(len(hitTable[hitparaIndex[q]])):  # array start with 0 while point index start with 1
            if hitTable[hitparaIndex[q]][j] >= T:
                q_hit_above_T[q].append(IndexPara[j])
    return q_hit_above_T


def getHitAboveTWithFilter(query, hitTable, dataset, paraIndex, IndexPara, hitparaIndex):
    q_hit_above_T = dict()
    for q in query:  # query is the #8 point
        q_hit_above_T[q] = []
        for j in range(len(hitTable[hitparaIndex[q]])):  # array start with 0 while point index start with 1
            if hitTable[hitparaIndex[q]][j] >= T and euclidean(dataset[paraIndex[q]], dataset[int(j)]) <= R:
                q_hit_above_T[q].append(IndexPara[j])
    return q_hit_above_T


def convertPointToDoc(point):
    return para_to_doc_dict[point]


def convertQdicttoDocdict(query, Qdict):
    queryWithSelectedDoc = dict()
    for q in query:
        selectedDoc = list()
        for para in Qdict[q]:
            selectedDoc.append(convertPointToDoc(para))
        queryWithSelectedDoc[q] = list(set(selectedDoc))
    return queryWithSelectedDoc


def getAllDoc(query, Qdict):
    result = Qdict[query[0]]
    for q in query:
        result = list(set(result).union(set(Qdict[q])))
    return result


def getSHDPrunedDoc(query, Qdict):
    result = Qdict[query[0]]
    for q in query:
        result = list(set(result).intersection(set(Qdict[q])))
    return result


def getLSHMHD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, precent):
    docMins = []
    for query_point in query:
        minium = getMHDbyqLSH(query_point, doc, hitTable, dataset, paraIndex, hitparaIndex)
        docMins.append(minium)
    docMins.sort(reverse=True)
    topN = math.ceil(len(docMins) * (1 - precent))
    if precent == 1:
        topN = 1
    MHDTotal = 0
    for i in range(int(topN)):
        MHDTotal += docMins[i]
    return MHDTotal / topN


def getLSHM2HD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, begin, end):
    docMins = []
    for query_point in query:
        minium = getMHDbyqLSH(query_point, doc, hitTable, dataset, paraIndex, hitparaIndex)
        docMins.append(minium)
    docMins.sort(reverse=True)
    start = math.ceil(len(docMins) * begin)
    stop = math.ceil(len(docMins) * end)
    num = stop - start
    MHDTotal = 0
    for i in range(int(num)):
        MHDTotal += docMins[int(i + start)]
    return MHDTotal / num


def getBFMHD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, precent):
    docMins = []
    for query_point in query:
        minium = getMHDbyqBF(query_point, doc, dataset, paraIndex)
        docMins.append(minium)
    docMins.sort(reverse=True)
    topN = math.ceil(len(docMins) * (1 - precent))
    MHDTotal = 0
    for i in range(int(topN)):
        MHDTotal += docMins[i]
    return MHDTotal / topN


def getBFM2HD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, begin, end):
    docMins = []
    for query_point in query:
        minium = getMHDbyqBF(query_point, doc, dataset, paraIndex)
        docMins.append(minium)
    docMins.sort(reverse=True)
    start = math.ceil(len(docMins) * begin)
    stop = math.ceil(len(docMins) * end)
    num = stop - start
    MHDTotal = 0
    for i in range(int(num)):
        MHDTotal += docMins[int(i + start)]
    return MHDTotal / num


def getMHDbyqLSH(q, doc, hitTable, dataset, paraIndex, hitparaIndex):  # compute the MHD bound matrix
    hitValueofDoc = []
    for p in doc_to_para_dict[doc]:
        if paraIndex[p] >= NP:
            continue
        hitValueofDoc.append((p, hitTable[hitparaIndex[q]][paraIndex[p]]))
    hitValueofDoc.sort(key=lambda tup: tup[1], reverse=True)
    top5hits = [x[0] for x in hitValueofDoc][:5]  # here set as 5
    minium = INF
    # the top value can be changed, set top5 first
    for point in top5hits:
        dis = euclidean(dataset[paraIndex[q]], dataset[paraIndex[point]])
        if dis < minium:
            minium = dis
    return minium


def getMHDbyqBF(q, doc, dataset, paraIndex):
    minium = INF
    for p in doc_to_para_dict[doc]:
        if paraIndex[p] >= NP:
            continue
        temp = euclidean(dataset[paraIndex[q]], dataset[paraIndex[p]])
        if temp < minium:
            minium = temp
    return minium


# queryDic: the ininal dic generate before Prun
def MHDPrunList(query, docList, hitTable, dataset, paraIndex, R, hitparaIndex, queryDic, method, precent):
    disList = []
    for doc in docList:
        dist = []
        for q in query:
            if doc in queryDic[q]:
                if method == "lsh":
                    dist.append(getMHDbyqLSH(q, doc, hitTable, dataset, paraIndex, hitparaIndex))
                else:
                    dist.append(getMHDbyqBF(q, doc, dataset, paraIndex))
            else:
                dist.append(R)
        dist.sort(reverse=True)  # sort MHD bound matrix from large to small

        topN = math.ceil(len(dist) * (1 - precent))
        if precent == 1:
            topN = 1
        totalDis = sum(dist[:int(topN)])
        distFin = totalDis / topN
        disList.append((doc, distFin))
    disList.sort(key=lambda tup: tup[1])
    sortedDocList = [x[0] for x in disList]
    # print sortedDocList, len(sortedDocList)
    return sortedDocList


# queryDic: the ininal dic generate before Prun (M2HD)
def M2HDPrunList(query, docList, hitTable, dataset, paraIndex, R, hitparaIndex, queryDic, method, begin, end):
    disList = []
    for doc in docList:
        dist = []
        for q in query:
            if doc in queryDic[q]:
                if method == "lsh":
                    dist.append(getMHDbyqLSH(q, doc, hitTable, dataset, paraIndex, hitparaIndex))
                else:
                    dist.append(getMHDbyqBF(q, doc, dataset, paraIndex))
            else:
                dist.append(R)
        dist.sort(reverse=True)  # sort MHD bound matrix from large to small
        start = math.ceil(len(dist) * begin)
        stop = math.ceil(len(dist) * end)
        num = stop - start
        totalDis = sum(dist[int(start): int(stop)])
        distFin = totalDis / num
        disList.append((doc, distFin))
    disList.sort(key=lambda tup: tup[1])
    sortedDocList = [x[0] for x in disList]
    # print sortedDocList, len(sortedDocList)
    return sortedDocList


def geneMHDPrun(docList, query, hitTable, topN, flagNum, dataset, paraIndex, hitparaIndex, precent, method):
    resultList = []
    stopFlag = 0
    count = 0
    for doc in docList:
        if stopFlag >= flagNum:
            break
        if method == "lsh":
            MHDDis = getLSHMHD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, precent)
        elif method == "bf":
            MHDDis = getBFMHD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, precent)
        count += 1
        if len(resultList) < topN:
            resultList.append((MHDDis, doc))
        else:
            resultList.sort(key=lambda tup: tup[0], reverse=True)
            topDis = resultList[0][0]
            if topDis > MHDDis:
                resultList[0] = (MHDDis, doc)
                stopFlag = 0
            else:
                stopFlag += 1
    resultList.sort(key=lambda tup: tup[0])
    result = [x[1] for x in resultList]
    return (count, result), resultList


def geneM2HDPrun(docList, query, hitTable, topN, flagNum, dataset, paraIndex, hitparaIndex, method, begin, end):
    resultList = []
    stopFlag = 0
    count = 0
    for doc in docList:
        if stopFlag >= flagNum:
            break
        if method == "lsh":
            MHDDis = getLSHM2HD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, begin, end)
        elif method == "bf":
            MHDDis = getBFM2HD(query, doc, hitTable, dataset, paraIndex, hitparaIndex, begin, end)
        count += 1
        if len(resultList) < topN:
            resultList.append((MHDDis, doc))
        else:
            resultList.sort(key=lambda tup: tup[0], reverse=True)
            topDis = resultList[0][0]
            if topDis > MHDDis:
                resultList[0] = (MHDDis, doc)
                stopFlag = 0
            else:
                stopFlag += 1
    resultList.sort(key=lambda tup: tup[0])

    result = [x[1] for x in resultList]
    return (count, result), resultList


def getLSHSHD(query, doc, doc_to_para_dict, hitTable, dataset, paraIndex, hitparaIndex):
    docMins = []
    for query_point in query:
        hitValueofDoc = []
        for p in doc_to_para_dict[doc]:
            if paraIndex[p] >= NP:
                continue
            hitValueofDoc.append((p, hitTable[hitparaIndex[query_point]][paraIndex[p]]))
        hitValueofDoc.sort(key=lambda tup: tup[1], reverse=True)
        top5hits = [x[0] for x in hitValueofDoc][:5]  # here set as 5
        minium = INF
        for p in top5hits:
            dis = euclidean(dataset[paraIndex[query_point]], dataset[paraIndex[p]])
            if dis < minium:
                minium = dis
        docMins.append(minium)
    maxium = 0
    for minDist in docMins:
        if minDist > maxium:
            maxium = minDist
    return maxium


def getBFSHD(query, doc, doc_to_para_dict, hitTable, dataset, paraIndex, hitparaIndex):
    docMins = []
    for query_point in query:
        minium = INF
        for p in doc_to_para_dict[doc]:
            if paraIndex[p] >= NP:
                continue
            dis = euclidean(dataset[paraIndex[query_point]], dataset[paraIndex[p]])
            if dis < minium:
                minium = dis
        docMins.append(minium)
    maxium = 0
    for minDist in docMins:
        if minDist > maxium:
            maxium = minDist
    return maxium


def getSHDTop5Doc(listOfdoc, query, doc_to_para_dict, shdTopN, hitTable, dataset, paraIndex, hitparaIndex, method):
    shdValues = []
    for d in listOfdoc:
        if method == "lsh":
            shdValues.append((d, getLSHSHD(query, d, doc_to_para_dict, hitTable, dataset, paraIndex, hitparaIndex)))
        else:
            shdValues.append((d, getBFSHD(query, d, doc_to_para_dict, hitTable, dataset, paraIndex, hitparaIndex)))
    shdValues.sort(key=lambda tup: tup[1])
    top5Doc = [x[0] for x in shdValues][:shdTopN]
    return top5Doc, shdValues


def PKNN(query, candiList, disFunc, weiFunc, k, beta, hitTable, topN, dataset, paraIndex):
    distList = []
    for c in candiList:
        if disFunc == "BF_SHD":
            dist = getBFSHD(query, c, doc_to_para_dict, hitTable, dataset, paraIndex, hitparaIndex)
        elif disFunc == "BF_MHD":
            dist = getBFMHD(query, c, hitTable, dataset, paraIndex, hitparaIndex, MHDRatio)
        elif disFunc == "BF_M2HD":
            dist = getBFM2HD(query, c, hitTable, dataset, paraIndex, hitparaIndex, startp, endp)
        elif disFunc == "LSH_SHD":
            dist = getLSHSHD(query, c, doc_to_para_dict, hitTable, dataset, paraIndex, hitparaIndex)
        elif disFunc == "LSH_MHD":
            dist = getLSHMHD(query, c, hitTable, dataset, paraIndex, hitparaIndex, MHDRatio)
        elif disFunc == "LSH_M2HD":
            dist = getLSHM2HD(query, c, hitTable, dataset, paraIndex, hitparaIndex, startp, endp)
        distList.append((c, dist))
    distList.sort(key=lambda tup: tup[1])
    topKList = distList[:k]
    distReverList = []
    for x in topKList:
        if x[1] == 0:
            continue
        distReverList.append((x[0], topKList[1][1] / pow(x[1], 5)))  # HERE modify better distribution function
    probList = dict()
    sumofrDis = sum([x[1] for x in distReverList])
    for x in topKList:
        probList[doc_to_au_dict[x[0]]] = 0
    for tup in distReverList:
        au = doc_to_au_dict[tup[0]]
        prob = tup[1] / sumofrDis
        probList[au] = probList[au] + prob
    probList = sorted(probList.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    return probList


def multiprocessNorm(dataset):
    if __name__ == "__main__":
        pool_size = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(pool_size)
        results = pool.map(NormalizeOneDem, dataset.T, )
        pool.close()
        pool.join()
    #       normData = combinedata(results)
    return np.asarray(results).T


# print "reading file"
# start = time.time()
# #my_data = []
# #with open("../../dataset.csv") as f:
# #   for line in f:
# #       sliceline = line.replace("\n", "").replace("\r", "").split(",")
#  #          my_data.append(sliceline)
# #my_data = genfromtxt('../../dataset.csv', delimiter=',')
# my_data = loadtxt('./demo_dataset_new.csv', delimiter=',')
# #my_data = np.asarray(multiprocessLoad("../../splitedFiles1000000"))
# print time.time()-start, "used to read file"
# parameters
D = 40  # dimensions
L = 200  # the number of group hash
K = 3  # the number of hash functions in each group hash
# N=30000 # the size of dataset
# N=4259934 # the size of dataset
N = 4511
NP = 4511
# N=879713 # the size of dataset
# NP = 879713 #the size of data used for QP
# NP = 4259934 #the size of data used for QP
# NP = 30000 #the size of data used for QP
NDocQ = 5
R = 0.12 * math.sqrt(D)  # query range
W = 1.2  # the width of bucket
T = 20  # collision threshold

MHDRatio = 0.5  # the MHD precentage
# M2LSHrange: from large to small based on mindist
startp = 0.25
endp = 0.5

topknn = 11  # MHD TopN list length
shdTopN = 11  # SHD TopN list length
flagNum = 3  # MHD TopN flag for pruning method(after flag times, stop..)


# start_pick=time.time()
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "loading pickle file ......"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# combinedhitQP = pickle.load( open( "combinedhitQP.p", "rb" ) )
# print "pickle has been loaded successfully"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "Time taken to laod pickle file is :", time.time()-start_pick
#
# # doc=[]
# # line=linecache.getlines("query_set_for_demoPaper.csv")
# # for i in range(len(line)):
# #         sliceline = line[i].replace("\n", "").replace("\r", "").split(",")
# #         doc.append(sliceline)
# # querySet=[]
# # for i in range(len(doc)):
# #     for j in range(len(doc[i])):
# #         doc[i][j]= int(doc[i][j])
# #         querySet.append(doc[i][j])
# querySet=[17141]
# print "This is the list of the query documents: ", querySet
#
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
# print "////////////////////////////////////"
#
# print "Candidate generation of each query document is started"
# start = time.time()
# #extract labels
# doc_id = my_data[:,0]
# author_id = my_data[:,1]
# para_id = my_data[:,2]
#
# dataset = my_data[:,[3, 4, 5, 6, 7, 9, 12, 14, 15, 16, 17, 19, 20, 21, 24, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 38, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 57]]
#
# #generate Indexes
# para_to_doc_dict = dict(zip(para_id,doc_id))
# doc_to_au_dict = dict(zip(doc_id,author_id))
# para_to_au_dict = dict(zip(para_id,author_id))
# paraIndex = dict()
# IndexPara = dict()
# for i in range(len(para_id)):
#     paraIndex[para_id[i]] = i
#
# for i in range(len(para_id)):
#     IndexPara[i] = para_id[i]
#
# doc_to_para_dict = defaultdict(list)
# for key, value in sorted(para_to_doc_dict.iteritems()):
#     doc_to_para_dict[value].append(key)
# doc_to_para_dict = dict(doc_to_para_dict)
#
# au_to_para_dict = defaultdict(list)
# for key, value in sorted(para_to_au_dict.iteritems()):
#     au_to_para_dict[value].append(key)
# au_to_para_dict = dict(au_to_para_dict)
#
# au_to_doc_dict = defaultdict(list)
# for key, value in sorted(doc_to_au_dict.iteritems()):
#     au_to_doc_dict[value].append(key)
# au_to_doc_dict = dict(au_to_doc_dict)
# print time.time()-start, "seconds used to index"
#
# #normalize data
# start = time.time()
# #datasetm= NormalizeDataset(dataset)
# datasetm= multiprocessNorm(dataset)
# datasetQ = []
# datasetP = []
# datasetN = []
# print time.time()-start, "seconds used to normalize"
# for i in range(N):
#         datasetN.append(datasetm[i])
#
# for i in range(NP):
#         datasetP.append(datasetm[i])
#
# hitparaIndex = dict()
# hitIndexPara = dict()
#
# for doc in querySet:
#     try:
#         paraList = doc_to_para_dict[doc]
#         for para in paraList:
#             datasetQ.append(datasetm[paraIndex[para]])
#             hitparaIndex[para]=(len(datasetQ)-1)
#             hitIndexPara[(len(datasetQ)-1)]=para
#     except KeyError:
#         continue


def load_pickle_file():
    print "////////////////////////////////////"
    print "////////////////////////////////////"
    print "////////////////////////////////////"
    print "loading pickle file ......"
    print "////////////////////////////////////"
    print "////////////////////////////////////"
    print "////////////////////////////////////"
    return pickle.load(open("combinedhitQP.p", "rb"))


def load_data_set():
    return loadtxt('./demo_dataset_new.csv', delimiter=',')


def calculate_index():
    my_data = load_data_set()

    print "Candidate generation of each query document is started"
    start = time.time()
    # extract labels
    doc_id = my_data[:, 0]
    author_id = my_data[:, 1]
    para_id = my_data[:, 2]

    # generate Indexes
    global para_to_doc_dict
    global doc_to_au_dict
    global para_to_au_dict
    global doc_to_para_dict
    global au_to_para_dict
    global au_to_doc_dict
    para_to_doc_dict = dict(zip(para_id, doc_id))
    doc_to_au_dict = dict(zip(doc_id, author_id))
    para_to_au_dict = dict(zip(para_id, author_id))
    paraIndex = dict()
    IndexPara = dict()
    for i in range(len(para_id)):
        paraIndex[para_id[i]] = i

    for i in range(len(para_id)):
        IndexPara[i] = para_id[i]

    doc_to_para_dict = defaultdict(list)
    for key, value in sorted(para_to_doc_dict.iteritems()):
        doc_to_para_dict[value].append(key)
    doc_to_para_dict = dict(doc_to_para_dict)

    au_to_para_dict = defaultdict(list)
    for key, value in sorted(para_to_au_dict.iteritems()):
        au_to_para_dict[value].append(key)
    au_to_para_dict = dict(au_to_para_dict)

    au_to_doc_dict = defaultdict(list)
    for key, value in sorted(doc_to_au_dict.iteritems()):
        au_to_doc_dict[value].append(key)
    au_to_doc_dict = dict(au_to_doc_dict)
    print time.time() - start, "seconds used to index"

    return my_data, para_to_doc_dict, doc_to_au_dict, para_to_au_dict, paraIndex, IndexPara, doc_to_para_dict, au_to_para_dict, au_to_doc_dict


def queryExp(q):
    combinedhitQP = load_pickle_file()
    my_data, para_to_doc_dict, doc_to_au_dict, para_to_au_dict, paraIndex, IndexPara, doc_to_para_dict, au_to_para_dict, au_to_doc_dict = calculate_index()

    # Calculate the dataset
    dataset = my_data[:,
              [3, 4, 5, 6, 7, 9, 12, 14, 15, 16, 17, 19, 20, 21, 24, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 38, 41, 43,
               44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 57]]
    # normalize data
    start = time.time()
    # datasetm= NormalizeDataset(dataset)
    datasetm = multiprocessNorm(dataset)
    datasetQ = []
    datasetP = []
    datasetN = []
    global hitparaIndex
    global hitIndexPara

    print time.time() - start, "seconds used to normalize"
    for i in range(N):
        datasetN.append(datasetm[i])

    for i in range(NP):
        datasetP.append(datasetm[i])

    hitparaIndex = dict()
    hitIndexPara = dict()

    try:
        paraList = doc_to_para_dict[q]
        for para in paraList:
            datasetQ.append(datasetm[paraIndex[para]])
            hitparaIndex[para] = (len(datasetQ) - 1)
            hitIndexPara[(len(datasetQ) - 1)] = para
    except KeyError:
        return
    # End of modification

    try:
        queryParaList = doc_to_para_dict[q]
    except KeyError:
        return
    data = ""
    queryParaList = doc_to_para_dict[q]
    print ""
    print "DocID", q
    data += (str(q) + "\n")

    try:
        # LSH Pruning SHD
        start = time.time()
        q_hit_above_T = getHitAboveT(queryParaList, combinedhitQP, hitparaIndex, IndexPara)
        doc_hit_above_T_dict = convertQdicttoDocdict(queryParaList, q_hit_above_T)
        LSHLongListTime = time.time() - start
        print "Time to generate long doc_list (LSH+SHD) ", LSHLongListTime
        data += (str(LSHLongListTime) + "\n")
        start = time.time()
        ListLSH_SHDPrun = getSHDPrunedDoc(queryParaList, doc_hit_above_T_dict)
        LSHSHDPrunListTime = time.time() - start
        print "Pruning Time (LSH+SHD): ", LSHSHDPrunListTime
        data += (str(LSHSHDPrunListTime) + "\n")
        start = time.time()
        LSH_SHD_list, LSH_SHD_values = getSHDTop5Doc(ListLSH_SHDPrun, queryParaList, doc_to_para_dict, shdTopN,
                                                     combinedhitQP, datasetP, paraIndex, hitparaIndex, "lsh")
        LSH_SHDTop5ListTime = time.time() - start

        print "Time to return topk doclist (LSH+SHD):", LSH_SHDTop5ListTime
        data += (str(LSH_SHDTop5ListTime) + "\n")

        # LSH Pruning MHD
        start = time.time()
        q_hit_above_T = getHitAboveT(queryParaList, combinedhitQP, hitparaIndex, IndexPara)
        doc_hit_above_T_dict = convertQdicttoDocdict(queryParaList, q_hit_above_T)
        ListLSH_ALL = getAllDoc(queryParaList, doc_hit_above_T_dict)
        LSHMHDLongListTime = time.time() - start
        print "Time to generate long doc_list (LSH+MHD) ", LSHMHDLongListTime
        data += (str(LSHMHDLongListTime) + "\n")
        start = time.time()
        sortedListLSH = MHDPrunList(queryParaList, ListLSH_ALL, combinedhitQP, datasetm, paraIndex, R, hitparaIndex,
                                    doc_hit_above_T_dict, "lsh", MHDRatio)
        LSH_MHD_Result, LSH_MHD_values = geneMHDPrun(sortedListLSH, queryParaList, combinedhitQP, topknn, flagNum,
                                                     datasetm, paraIndex, hitparaIndex, MHDRatio, "lsh")

        LSH_MHD_len = LSH_MHD_Result[0]
        LSH_MHD_list = LSH_MHD_Result[1]
        LSHMHDgenTop5ListTime = time.time() - start
        print "Time to return topk doclist (LSH+MHD):", LSHMHDgenTop5ListTime
        data += (str(LSHMHDgenTop5ListTime) + "\n")

        # LSH Pruning M2HD
        start = time.time()
        q_hit_above_T = getHitAboveT(queryParaList, combinedhitQP, hitparaIndex, IndexPara)
        doc_hit_above_T_dict = convertQdicttoDocdict(queryParaList, q_hit_above_T)
        ListLSH_ALL = getAllDoc(queryParaList, doc_hit_above_T_dict)
        LSHMHDLongListTime = time.time() - start
        print "Time to generate long doc_list (LSH+M2HD) ", LSHMHDLongListTime
        data += (str(LSHMHDLongListTime) + "\n")
        start = time.time()
        sortedListLSH = M2HDPrunList(queryParaList, ListLSH_ALL, combinedhitQP, datasetm, paraIndex, R, hitparaIndex,
                                     doc_hit_above_T_dict, "lsh", startp, endp)
        LSH_M2HD_Result, LSH_M2HD_values = geneM2HDPrun(sortedListLSH, queryParaList, combinedhitQP, topknn, flagNum,
                                                        datasetm, paraIndex, hitparaIndex, "lsh", startp, endp)
        LSH_M2HD_len = LSH_M2HD_Result[0]
        LSH_M2HD_list = LSH_M2HD_Result[1]

        LSHM2HDgenTop5ListTime = time.time() - start
        print "Time to return topk doclist (LSH+M2HD):", LSHM2HDgenTop5ListTime
        data += (str(LSHM2HDgenTop5ListTime) + "\n")

        print "docList Length LSH: ", len(ListLSH_ALL)
        data += (str(len(ListLSH_ALL)) + "\n")
        print "docList Length LSH_SHD: ", len(ListLSH_SHDPrun)
        data += (str(ListLSH_SHDPrun) + "\n")
        data += (str(LSH_MHD_len) + "\n")
        print "docList Length LSH_MHD: ", LSH_MHD_len
        data += (str(LSH_M2HD_len) + "\n")
        print "docList Length LSH_M2HD: ", LSH_M2HD_len

        data += (str(len(ListLSH_ALL) / len(ListLSH_SHDPrun)) + "\n")
        print "prunRatio LSH_SHD: ", len(ListLSH_ALL) / len(ListLSH_SHDPrun)
        data += (str(len(ListLSH_ALL) / LSH_MHD_len) + "\n")
        print "prunRatio LSH_MHD: ", len(ListLSH_ALL) / LSH_MHD_len

        data += (str(len(ListLSH_ALL) / LSH_M2HD_len) + "\n")
        print "prunRatio LSH_M2HD: ", len(ListLSH_ALL) / LSH_M2HD_len

        def print_authorid(final_list):
            if len(final_list) == 1:
                print "there is only one doc"
            else:
                print doc_to_au_dict[final_list[1]]

        print "///////////////////////////////////////////"
        print "use the top2 closet document to determine author_id:"
        print "Origin author: ", doc_to_au_dict[q]
        data += (str(doc_to_au_dict[q]) + "\n")

        LSH_SHD_PKNN = PKNN(queryParaList, LSH_SHD_list, "LSH_SHD", "", 20, 0, combinedhitQP, 5, datasetP, paraIndex)
        print "LSH_SHD PKNN: ", LSH_SHD_PKNN
        data += (str(LSH_SHD_PKNN) + "\n")

        LSH_MHD_PKNN = PKNN(queryParaList, LSH_MHD_list, "LSH_MHD", "", 20, 0, combinedhitQP, 5, datasetP, paraIndex)
        print "LSH_MHD PKNN: ", LSH_MHD_PKNN
        data += (str(LSH_MHD_PKNN) + "\n")

        LSH_M2HD_PKNN = PKNN(queryParaList, LSH_MHD_list, "LSH_M2HD", "", 20, 0, combinedhitQP, 5, datasetP, paraIndex)
        print "LSH_M2HD PKNN: ", LSH_M2HD_PKNN
        data += (str(LSH_M2HD_PKNN) + "\n")

        def changeDocTODocAuTuple(docList):
            result = []
            for doc in docList:
                result.append((doc, doc_to_au_dict[doc]))
            return result

        fileNameString = "./expResult10K_one/" + str(q)
        f = open(fileNameString, 'wb')
        f.write(data)
        f.close()
        return
    except Exception as e:
        print e.message
        return


if __name__ == '__main__':
    querySet = [17141]
    queryExp(17141)
    # start_time = time.time()
    # pool_size=multiprocessing.cpu_count()
    # processNum = 5
    # pool = multiprocessing.Pool(processes=processNum,)
    # temp= pool.map(queryExp,querySet,)
    # pool.close()
    # pool.join()
    # endtime = time.time() - start_time
