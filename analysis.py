#!/usr/bin/env python2.7
'''
analysis.py
Ronald Sadlier
7-18-2014
'''
from os import listdir
from os.path import isfile, join
import struct
import numpy

# We can use this to debug
verbose = False

def convert_files(inputDir, outputDir, expectedNumFileItems):
  fileList = [f for f in listdir(inputDir) if isfile(join(inputDir,f))]

  if verbose:
    print("Converting binary files in \""+inputDir+"\" and saving to \""+outputDir+"\"")
    print("Found "+str(len(fileList))+" file(s)")

  fileList.sort(key=float)
  
  overallList = []
  issueList = []

  for inputfile in fileList:
    if verbose:
      print("Read in: "+inputfile)

    dataValues = []

    with open(inputDir+"/"+inputfile, "rb") as f:
      integerBytes = f.read(4)
      while integerBytes:
        dataValues.append(struct.unpack('<f', integerBytes))
        integerBytes = f.read(4)

      dataValues = [i for i, in dataValues]

      if len(dataValues) != 0:
        if len(dataValues) != expectedNumFileItems:
          issueList.append(str(inputfile))

        sum = 0.0
        for value in dataValues:
          sum += value
        average = sum / float(len(dataValues))
        variance = numpy.var(dataValues)

        overallList.append([inputfile, average, variance])

        with open(outputDir+"/"+inputfile+".dat", "w") as f:
          f.write("# File Count: "+str(len(dataValues))+"\n")
          f.write("# File Average: "+str(average)+"\n")
          f.write("# file Variance: "+str(variance)+"\n")
          for value in dataValues:
            f.write(str(value)+"\n")
          if verbose is True:
            print("Unpacked and wrote "+str(len(dataValues))+" float(s)")
      else:
        issueList.append(inputfile)
  with open(outputDir+"/_overall.dat", "w") as f:
    f.write("# [key]\t[average]\t[variance]\n")
    for item in overallList:
      f.write(str(item[0]) +"\t"+str(item[1])+"\t"+str(item[2])+"\n")

  if verbose:
    print("Wrote overall statistics file")

  if len(issueList) != 0:
    print("We had problems with analyzing "+str(len(issueList))+" files:")
    for issue in issueList:
      print(str(issue))

if __name__ == '__main__':
  inputDir = input("Please enter input dir:")
  outputDir = input("Please enter output dir:")
  expectedNumFileItems = input("Please enter expected number of items in each file:")
