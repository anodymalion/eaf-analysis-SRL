#!/usr/bin/python

#Rebecca Nickerson - last updated 2/25/2015

#run as:
#python processFiles.py ground_truth_input.txt  test_data_input.txt  FINAL.txt

#FINAL will contain relevance and reliability proportions and other data
#test_in_truth = proportion of test data smiles actually present in truth data
#truth_in_test = proportion of truth smiles captured by test data

import sys, re

#changeable
threshold_joy = .5 #necessary joy to count as smile
threshold_au12 = .5 #necessary AU12 activation to count as smile
threshold_au6 = .25 #necessary AU6 activation to count as smile
threshold_size = 25 #minimum number of frames in valid Range
maxgap = 10  #leniency when merging smile ranges 
#(e.g (1,3), (5,6) merged to (1,6) with maxgap > 0)

truth_list = []
test_list_joy = []
test_list_au12 = []
test_list_au6 = []

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
    input_test = str(sys.argv[2])
    final_output = str(sys.argv[3])
    return input_truth, input_test, final_output


#parse out whether smile existed in each frame
def getTruth(input_file):
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
            #output_file.write(val + " ")
            truth_list.append(val)
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


#parse out if joy, AU activation surpassed thresholds in each frame
def getTest(input_file):
    first_line = input_file.readline()
    k = -1 #offset caused by mismatched whitespace in dump file

    while(first_line.find("StudyName") == -1):
        first_line = input_file.readline()

    start_new_joy = True
    rangelist_joy = []

    start_new_au12 = True
    rangelist_au12 = []
    
    start_new_au6 = True
    rangelist_au6 = []

    words = re.split('\t', first_line)

    joy_index = words.index("Joy Evidence")
    au6_index = words.index("AU6 Evidence")
    au12_index = words.index("AU12 Evidence")
    frame_index = words.index("FrameNo")

    for line in input_file:
        words = line.split()
        
        #for joy
        if joy_index < len(words):
            if float(words[joy_index + k]) > threshold_joy:
                val_joy = 1
            else:
                val_joy = 0
        else:
            val_joy = 2

        if start_new_joy and val_joy == 1:
            new_range_joy = Range(int(words[frame_index + k]), int(words[frame_index + k]))
            start_new_joy = False
        elif not start_new_joy and val_joy == 0:
            new_range_joy.end = int(words[frame_index + k]) - 1
            rangelist_joy.append(new_range_joy)
            start_new_joy = True

        #for au 12
        if au12_index < len(words):
            if float(words[au12_index + k]) > threshold_au12:
                val_au12 = 1
            else:
                val_au12 = 0
        else:
            val_au12 = 2 

        if start_new_au12 and val_au12 == 1:
            new_range_au12 = Range(int(words[frame_index + k]), int(words[frame_index + k]))
            start_new_au12 = False
        elif not start_new_au12 and val_au12 == 0:
            new_range_au12.end = int(words[frame_index + k]) - 1
            rangelist_au12.append(new_range_au12)
            start_new_au12 = True

        #for au 6
        if au6_index < len(words):
            if float(words[au6_index + k]) > threshold_au6:
                val_au6 = 1
            else:
                val_au6 = 0
        else:
            val_au6 = 2 

        if start_new_au6 and val_au6 == 1:
            new_range_au6 = Range(int(words[frame_index + k]), int(words[frame_index + k]))
            start_new_au6 = False
        elif not start_new_au6 and val_au6 == 0:
            new_range_au6.end = int(words[frame_index + k]) - 1
            rangelist_au6.append(new_range_au6)
            start_new_au6 = True


        test_list_joy.append(val_joy)
        test_list_au12.append(val_au12)
        test_list_au6.append(val_au6)

    rangelist_joy = mergeRanges(rangelist_joy) 
    rangelist_joy = deleteRanges(rangelist_joy)

    rangelist_au12 = mergeRanges(rangelist_au12) 
    rangelist_au12 = deleteRanges(rangelist_au12)

    rangelist_au6 = mergeRanges(rangelist_au6) 
    rangelist_au6 = deleteRanges(rangelist_au6)

    print "getTest ranges:"
    for rang in rangelist_joy:
        print rang.start, "\t", rang.end
    print "au12 ranges:"
    for rang in rangelist_au12:
        print rang.start, "\t", rang.end
    print "au6 ranges:"
    for rang in rangelist_au6:
        print rang.start, "\t", rang.end
    return rangelist_joy


#merge smiles ranges that are significantly close together
def mergeRanges(rangelist):
 
    new_rangelist = []
    if len(rangelist) > 0:
        prev_rang = rangelist[0]
        for rang in rangelist:
            if rang.start - prev_rang.end <= maxgap + 1:
                prev_rang.end = rang.end
            else:
                new_rangelist.append(prev_rang)
                prev_rang = rang

        new_rangelist.append(prev_rang)
    return new_rangelist

#if range is too small, remove it
def deleteRanges(rangelist):
    new_rangelist = []
    for rang in rangelist:
        if rang.end - rang.start > threshold_size:
            new_rangelist.append(rang)
    return new_rangelist

#create new Ranges based on multiple rangelists
def combineRanges(rlist1, rlist2):
    new_rangelist = []
    #incomplete obviously
    return new_rangelist


#compare on a purely index to index basis (doesn't account for smile ranges)
def compare():
    
    truth_set = truth_list
    test_set = test_list_joy 

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
    print "n_relev:", n_relevance, "\nn_relib:", n_reliable
    print "miscount:", miscount_prop
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
    [input_truth, input_test, final_output] = get_args(argv)
    input_truth_file = open(input_truth, 'r')
    input_test_file = open(input_test, 'r')
    #final_output_file = open(final_output, "w")

    #can change this depending on what the threshold of detecting a smile should be
    truthrange = getTruth(input_truth_file)
    testrange = getTest(input_test_file)
    #[p_rev, p_rel, n_rev, n_rel, mis] = compare()

    input_truth_file.close()
    input_test_file.close()

    '''
    val1 = compareRanges(truthrange, testrange)
    val2 = compareRanges(testrange, truthrange)

    print "proportion of test smiles actually in truth:"
    print val1
    print "proportion of truth smiles captured by test:"
    print val2

    final_output_file.write("parameter: " + "Joy Intensity\n") #change w/ parameter
    final_output_file.write("threshold: " + str(threshold) + "\n")
    final_output_file.write("p_relevance: " + str(p_rev) + "\n")
    final_output_file.write("p_reliability: " + str(p_rel) + "\n")
    final_output_file.write("n_relevance: " + str(n_rev) + "\n")
    final_output_file.write("n_reliability: " + str(n_rel) + "\n")
    final_output_file.write("miscount_proportion: " + str(p_rev) + "\n")
    final_output_file.write("test_in_truth: " + str(val1) + "\n")
    final_output_file.write("truth_in_test: " + str(val2) + "\n")
    final_output_file.close()'''



if __name__ == "__main__":
    main(sys.argv[1:])