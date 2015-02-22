#!/usr/bin/python

#Rebecca Nickerson - last updated 2/20/2015

#run as:
#python processFiles.py ground_truth_input.txt  ground_truth_output.txt  test_data_input.txt  test_data_output.txt correlation_output.txt

#correlation_output will contain relevance and reliability proportions
#doesn't actually output anything to that file yet

import sys, re

class Range:
    '''information of each range of smile data'''
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.contained = 0

def get_args(argv):
    args = str(sys.argv)
    input_truth = str(sys.argv[1])
    output_truth = str(sys.argv[2])
    input_test = str(sys.argv[3])
    output_test = str(sys.argv[4])
    return input_truth, output_truth, input_test, output_test

#parse out whether smile existed in each frame
def getTruth(input_file, output_file):
    first_line = input_file.readline()
    words = re.split(',|\r|\n|, ', first_line)
    smile_index = words.index("SMILE")
    frame_index = words.index("FRAME")
    frame_current = -1
    start_new = True
    rangelist = []

    for line in input_file:
        words = line.split()
        if(int(words[frame_index]) > frame_current):
            frame_current = int(words[frame_index])
            val = words[smile_index]
            output_file.write(val + " ")
            if start_new and int(val) == 1:
                new_range = Range(int(words[frame_index]), int(words[frame_index]))
                start_new = False
            elif not start_new and int(val) == 0:
                new_range.end = int(words[frame_index]) - 1
                rangelist.append(new_range)
                start_new = True

    if not start_new:
        new_range.end = frame_current
        rangelist.append(new_range)
    
    print "getTruth ranges:"   
    for rang in rangelist:
        print rang.start, " \t", rang.end
    return rangelist


#parse out if joy surpassed a set level in each frame
def getTest(input_file, output_file):
    first_line = input_file.readline()
    k = 2 #offset caused by weird whitespace :( - may have to edit depending on the input file
    
    while(first_line.find("StudyName") == -1):
        first_line = input_file.readline()

    start_new = True
    rangelist = []
    words = re.split('\t', first_line)

    joy_index = words.index("Joy Evidence")
    frame_index = words.index("FrameNo")
    print "INDEX:", frame_index, joy_index
    for line in input_file:
        words = line.split()
        if joy_index < len(words):
            if float(words[joy_index + k]) > .5:
                output_file.write("1 ")
                print "evidence:", words[frame_index + k]
                val = 1
            else:
                output_file.write("0 ")
                val = 0
        else:
            output_file.write("2 ")
            val = 2
        if start_new and val == 1:
            new_range = Range(int(words[frame_index + k]), int(words[frame_index + k]))
            start_new = False
        elif not start_new and val == 0:
            new_range.end = int(words[frame_index + k]) - 1
            rangelist.append(new_range)
            start_new = True

    print "getTest ranges:"
    for rang in rangelist:
        print rang.start, "\t", rang.end
    return rangelist


def compare(truth_file, test_file):
    
    truth_set = truth_file.readline().split()
    test_set = test_file.readline().split()

    p_relevance = -1.0
    p_reliable = -1.0
    n_relevance = -1.0
    n_reliable = -1.0

    p_relevanceCount = 0.0
    p_reliableCount = 0.0
    n_relevanceCount = 0.0
    n_reliableCount = 0.0

    p_countv = 0.0
    p_countb = 0.0
    n_countv = 0.0
    n_countb = 0.0
    
    total = 0.0
    miscount = 0.0
    miscount_prop = -1.0

    if(len(truth_set) < len(test_set)):
        size = len(truth_set)
    else:
        size = len(test_set)

    for i in range(size):
        print int(test_set[i]), int(truth_set[i])
        total += 1
        if int(test_set[i]) == 2:
            miscount += 1
            continue
        if int(test_set[i]) == 1:
            if int(truth_set[i]) == 1:
                p_relevanceCount += 1
            p_countv += 1
        else:
            if int(truth_set[i]) == 0:
                n_relevanceCount += 1
            n_countv += 1
        if int(truth_set[i]) == 1:
            if int(test_set[i]) == 1:
                p_reliableCount += 1
            p_countb += 1
        else:
            if int(test_set[i]) == 0:
                n_reliableCount += 1
            n_countb += 1
        
    if p_countv > 0:
        p_relevance = p_relevanceCount / p_countv
    if p_countb > 0:
        p_reliable = p_reliableCount / p_countb
    if n_countv > 0:
        n_relevance = n_relevanceCount / n_countv
    if n_countb > 0:
        n_reliable = n_reliableCount / n_countb
    if total > 0:
        miscount_prop = miscount / total

    print "p_relev:", p_relevance, "\np_relib:", p_reliable, "\nn_relev:", n_relevance, "\nn_relib:", n_reliable, "\nmiscount:", miscount_prop


def compareRanges(truth_ranges, test_ranges):

    for testrange in test_ranges:
        a = int(testrange.start)
        b = int(testrange.end)
        for truthrange in truth_ranges:
            c = int(truthrange.start)
            d = int(truthrange.end)
            #print "testing:",a,b,";",c,d
            if b < c:
                #print "n1"
                continue
            elif a > d:
                #print "n2"
                continue
            elif c <= a:
                #print "n3"
                if b >= d:
                    #print "d-a+1 =", d-a+1
                    testrange.contained += (d - a + 1)
                else:
                    #print "b-a+1 =", b-a+1
                    testrange.contained += (b - a + 1)
            else: #a < c, b > c
                #print "n4"
                if b > d:
                    #print "(d-c+1) =", d - c + 1
                    testrange.contained += (d - c + 1)
                else:
                    #print "(b-c+1) =", b - c + 1
                    testrange.contained += (b - c + 1)
                
        print "testrange total for", a, b, ":", testrange.contained 


def main(argv):
    [input_truth, output_truth, input_test, output_test] = get_args(argv)
    '''input_truth_file = open(input_truth, 'r')
    input_test_file = open(input_test, 'r')
    output_truth_file = open(output_truth, "w")
    output_test_file = open(output_test, "w")

    truthrange = getTruth(input_truth_file, output_truth_file)
    testrange = getTest(input_test_file, output_test_file)

    output_truth_file.close()
    output_test_file.close()

    test_in = open(output_test, 'r')
    truth_in = open(output_truth, 'r')
    compare(truth_in, test_in)
    test_in.close()
    truth_in.close()

    input_truth_file.close()
    input_test_file.close()'''

    #compareRanges(truthrange, testrange)


if __name__ == "__main__":
    main(sys.argv[1:])