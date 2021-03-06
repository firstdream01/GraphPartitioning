#!/usr/bin/python
# -*- coding: utf-8 -*-

# SWR方案测试代码--不考虑邻居节点的情况

import random
import math
import time

def SWRPartitioning(edgelist, numOfParts, wins):
    f = open(edgelist, "r")

    # [[(src, dst), (src, dst),...],[()],[()]....]          每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                          存储每个分区对应的点
    vertexDic = {}
    # { vertex:set(part1, part2,...),... }                  存储每个点对应的分区
    ver2partDic = {}
    # { vertex:degree,... }                                 存储每个点对应的度信息
    ver2degreeDic = {}
    # { part:numofneigbors,... }                            存储每个分区对应该轮顶点的邻居数量
    part2neighbor = {}
    # 存储总边数
    edgeNum = 0

    for i in range(numOfParts):
        vertexDic[i] = set()

    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])

        window = wins
        maxwindowsize = 10000000000
    
            
        # 对边进行分配
        edgeNum = edgeNum + 1
        if ver2partDic.has_key(src):
            srcMachines = ver2partDic[src]
        else:
            ver2partDic[src] = set()
            srcMachines = ver2partDic[src]
        if ver2partDic.has_key(tar):
            tarMachines = ver2partDic[tar]
        else:
            ver2partDic[tar] = set()
            tarMachines = ver2partDic[tar]
        if ver2degreeDic.has_key(src):
            srcDegree = ver2degreeDic[src]
        else:
            ver2degreeDic[src] = 0
            srcDegree = 0
        if ver2degreeDic.has_key(tar):
            tarDegree = ver2degreeDic[tar]
        else:
            ver2degreeDic[tar] = 0
            tarDegree = 0
        

        if (len(srcMachines) == 0) and (len(tarMachines) == 0):
            part = -1
            for i in range(numOfParts):
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) > 0) and (len(tarMachines) == 0):
            part = -1
            for i in srcMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) == 0) and (len(tarMachines) > 0):
            part = -1
            for i in tarMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        else:
            Intersection = srcMachines & tarMachines
            Convergence = srcMachines | tarMachines
            part = -1
            if len(Intersection) == 0:
                if srcDegree > tarDegree:
                    for i in tarMachines:
                        if part == -1:
                            part = i
                            continue
                        if len(Partitions[i]) < len(Partitions[part]):
                            part = i
                else:
                    for i in srcMachines:
                        if part == -1:
                            part = i
                            continue
                        if len(Partitions[i]) < len(Partitions[part]):
                            part = i  
            else:
                for i in Intersection:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i

        # 更新各种集合数据
        Partitions[part].append((src, tar))
        vertexDic[part].add(src)
        vertexDic[part].add(tar)
        ver2partDic[src].add(part)
        ver2partDic[tar].add(part)
        ver2degreeDic[src] = ver2degreeDic[src] + 1
        ver2degreeDic[tar] = ver2degreeDic[tar] + 1

    # 获取所有子图的顶点个数    
    allVertex = 0L
    maxVertices = 0L
    for i in range(numOfParts):
        allVertex = allVertex + len(vertexDic[i])
        if maxVertices < len(vertexDic[i]):
            maxVertices = len(vertexDic[i])
    # 获取整个图的顶点个数
    vertexAll = vertexDic[0]
    for i in range(1, numOfParts):
        vertexAll.update(vertexDic[i])
    # 获取顶点的LSD和LRSD
    temp = 0L
    AveVerSize = len(vertexAll)/float(numOfParts)
    for i in range(0, numOfParts):
        temp = temp + (len(vertexDic[i]) - AveVerSize) * (len(vertexDic[i]) - AveVerSize)
    temp = temp/numOfParts
    temp = math.sqrt(temp)

    VLSD = temp
    VLRSD = VLSD/AveVerSize

    VRF = allVertex/float(len(vertexAll))
    
    # 获取边的相关信息
    maxEdges = 0L
    AveSize = edgeNum/float(numOfParts)
    temp = 0L
    for i in range(numOfParts):
        temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
        if maxEdges < len(Partitions[i]):
            maxEdges = len(Partitions[i])
        print len(Partitions[i])
    temp = temp/numOfParts
    temp = math.sqrt(temp)

    LSD = temp
    LRSD = LSD/AveSize

    # 依次是 VRF  LSD  LRSD  VLSD  VLRSD  子图点最大值  子图点平均值  子图边最大值  子图边平均值
    print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts


time_start = time.time()

SWRPartitioning("/home/w/data/web-BerkStan.txt", 64, 7600795)

time_end = time.time()
time_used = time_end - time_start

print time_used
