import sys
import os
import json
import argparse

import numpy as np
from struct import unpack

TRAINSET = 0.9
VALSET = 0.1
TESTSET = 0.0



def check_pair(jsonList):
    binList = []
    for json in jsonList:
        dir, file = os.path.split(json)
        path = dir + '/../lidar/' + file[:-5] + ".bin"
        if os.path.isfile(path):
            binList.append(path)
            continue

        #print("No match found for this file: " + json)
        print("rm" + json)

    return binList

def find_jsonSet(path):
    jsonList=[]
    for dirpath, dirname, filename in os.walk(path, topdown=False):
        aliveSet = ['json']
        jsonList.extend([dirpath+'/'+i for i in filename if i[-4:] in aliveSet])

    return jsonList

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def create_labels(jsonList, abspath):
    for file in jsonList:
        with open(file, 'rt', encoding='UTF-8') as sus:
            datas = json.load(sus)
            basename = os.path.basename(file)
            savePath = abspath + "/labels/" + basename[:-5] + ".txt"
            save_labels(datas, savePath)

    sus.close()

def save_labels(datas, savePath):
    ## format: [x    y    z    dx   dy   dz   heading_angle category_name]
    #           1.50 1.46 0.10 5.12 1.85 4.13 1.56          Vehicle
    #           5.54 0.57 0.41 1.08 0.74 1.95 1.57          Pedestrian
    txtFile = open(savePath, 'w')
    for data in datas:
        #if data['obj_type'] != "Pedestrian":
        #    continue
        xyz = data['psr']['position']
        dxyz = data['psr']['scale']
        theta = data['psr']['rotation']['z']
        category = data['obj_type']

        line = "%f %f %f %f %f %f %f %s\n" %(xyz['x'], xyz['y'], xyz['z'], dxyz['x'], dxyz['y'], dxyz['z'], theta, category)
        txtFile.write(line)

    txtFile.close()    

def create_points(binList, abspath):
    for file in binList:
        x = []
        y = []
        z = []
        intencity = []
        
        try:
            with open(file, 'rb') as sus:
                while True:
                    val1 = unpack('<1f', sus.read(4))
                    val2 = unpack('<1f', sus.read(4))
                    val3 = unpack('<1f', sus.read(4))
                    val4 = unpack('<1f', sus.read(4))
                    x.append(val1[0])
                    y.append(val2[0])
                    z.append(val3[0])
                    intencity.append(val4[0])
        except Exception as e:
            pass
        finally:
            sus.close()

        basename = os.path.basename(file)
        savePath = abspath + "/points/" + basename[:-4] + ".npy"

        datas = [x, y, z, intencity]
        datas = np.reshape(datas, (4, len(x))).T
        save_points(datas, savePath)

def save_points(datas, savePath):
    np.save(savePath, datas)

def create_imageSets(jsonList, abspath):
    baseJsonList = []
    for jsonFile in jsonList:
        baseJson = os.path.basename(jsonFile)
        baseJsonList.append(baseJson[:-5])
    
    baseJsonList.sort()

    savePath = abspath + "/ImageSets/"
    save_imageSets(baseJsonList, savePath)

def save_imageSets(datas, savePath):
    trainTxtFile = open(savePath + "train.txt", 'w')
    valTxtFile = open(savePath + "val.txt", 'w')
    testTxtFile = open(savePath + "test.txt", 'w')

    lenSet = len(datas)


    trainI = int(lenSet * TRAINSET)
    valI = int(lenSet * (TRAINSET+VALSET))

    for i in range(lenSet):
        if i < trainI:
            trainTxtFile.write(datas[i]+"\n")
        elif i < valI:
            valTxtFile.write(datas[i]+"\n")
        else:
            testTxtFile.write(datas[i]+"\n")

    trainTxtFile.close()
    valTxtFile.close()
    testTxtFile.close()

def testnpy():
    loaded_x = np.load('/home/ubuntu/data/pcdet_custom/0001.npy')
 
    print(loaded_x)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='datasetDir', default='/home/ubuntu/src/OpenPCDet/data/custom', help='path to directory')

    args = parser.parse_args()

    #basename = os.path.basename(args.datasetDir)
    abspath = os.path.abspath(args.datasetDir)
    
    
    createFolder(abspath + '/ImageSets')
    createFolder(abspath + '/points')
    createFolder(abspath + '/labels')


    jsonList = find_jsonSet(abspath)
    binList = check_pair(jsonList)

    print("### Lidar data conversion")

    print("#### Create labels")
    create_labels(jsonList, abspath)

    print("#### Create Points")
    create_points(binList, abspath)  

    print("#### Create ImageSets")
    create_imageSets(jsonList, abspath)
    
    print("### Conversion complete")


