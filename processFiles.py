#!/usr/bin/python

#Rebecca Nickerson - last updated 2/23/2015

#run as:
#python processFiles.py ground_truth_input.txt  ground_truth_output.txt  test_data_input.txt  test_data_output.txt correlation_output.txt

#correlation_output will contain relevance and reliability proportions
#test_in_truth = proportion of test data smiles actually present in truth data
#truth_in_test = proportion of truth smiles captured by test data

import sys, re

class Range:
    '''information of each range of smile data'''
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.contained = 0
        self.prop = 0.0

def get_args(argv):
    args = str(sys.argv)
    input_truth = str(sys.argv[1])
    output_truth = str(sys.argv[2])
    input_test = str(sys.argv[3])
    output_test = str(sys.argv[4])
    final_output = str(sys.argv[5])
    return input_truth, output_truth, input_test, output_test, final_output

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
def getTest(input_file, output_file, threshold):
    first_line = input_file.readline()
    k = -1 #offset caused by weird whitespace :( - may have to change it depending on the input_file

    while(first_line.find("StudyName") == -1):
        first_line = input_file.readline()

    start_new = True
    rangelist = []
    words = re.split('\t', first_line)

    joy_index = words.index("Joy Evidence")
    frame_index = words.index("FrameNo")
    #print "INDEX:", frame_index, joy_index
    for line in input_file:
        words = line.split()
        if joy_index < len(words):
            if float(words[joy_index + k]) > threshold:
                output_file.write("1 ")
                #print "evidence:", words[frame_index + k], ":", words[joy_index + k]
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

    print "p_relev:", p_relevance, "\np_relib:", p_reliable 
    print "n_relev:", n_relevance, "\nn_relib:", n_reliable, "\nmiscount:", miscount_prop
    return p_relevance, p_reliable, n_relevance, n_reliable, miscount_prop


#compare the truth and test ranges to see what proportion of the truth is captured by the test
def compareRanges(truth_ranges, test_ranges):
    total_contained = 0.0
    total_number = 0.0

    for testrange in test_ranges:
        a = int(testrange.start)
        b = int(testrange.end)
        for truthrange in truth_ranges:
            c = int(truthrange.start)
            d = int(truthrange.end)
            if b < c:
                continue
            elif a > d:
                continue
            elif c <= a:
                if b >= d:
                    testrange.contained += (d - a + 1)
                else:
                    testrange.contained += (b - a + 1)
            else: #a < c, b > c
                if b > d:
                    testrange.contained += (d - c + 1)
                else:
                    testrange.contained += (b - c + 1)
        total_contained += testrange.contained
        total_number += testrange.end - testrange.start + 1
        prop = float(testrange.contained) / float((testrange.end - testrange.start + 1))
        testrange.prop = prop
    if total_number > 0:
        total_prop = total_contained / total_number
    else:
        total_prop = -1
    return total_prop


def main(argv):
    [input_truth, output_truth, input_test, output_test, final_output] = get_args(argv)
    input_truth_file = open(input_truth, 'r')
    input_test_file = open(input_test, 'r')
    output_truth_file = open(output_truth, "w")
    output_test_file = open(output_test, "w")
    final_output_file = open(final_output, "w")

    #can change this depending on what the threshold of detecting a smile should be
    threshold = .5

    truthrange = getTruth(input_truth_file, output_truth_file)
    testrange = getTest(input_test_file, output_test_file, threshold)

    output_truth_file.close()
    output_test_file.close()

    test_in = open(output_test, 'r')
    truth_in = open(output_truth, 'r')
    [p_rev, p_rel, n_rev, n_rel, mis] = compare(truth_in, test_in)
    test_in.close()
    truth_in.close()

    input_truth_file.close()
    input_test_file.close()

    val1 = compareRanges(truthrange, testrange)
    val2 = compareRanges(testrange, truthrange)

    print "proportion of test smiles actually in truth:"
    print val1
    print "proportion of truth smiles captured by test:"
    print val2

    final_output_file.write("parameter: " + "Joy Intensity\n") #change w/ parameter
    final_output_file.write("threshold" + str(threshold) + "\n")
    final_output_file.write("p_relevance: " + str(p_rev) + "\n")
    final_output_file.write("p_reliability: " + str(p_rel) + "\n")
    final_output_file.write("n_relevance: " + str(n_rev) + "\n")
    final_output_file.write("n_reliability: " + str(n_rel) + "\n")
    final_output_file.write("miscount_proportion: " + str(p_rev) + "\n")
    final_output_file.write("test_in_truth: " + str(val1) + "\n")
    final_output_file.write("truth_in_test: " + str(val2) + "\n")
    final_output_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])