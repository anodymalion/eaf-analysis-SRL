#Explanation of FINAL.txt
**number of true smiles:** the number of distinct smiles that actually occur in the truth data (how many times the subject smiled)
**threshold_joy**: the threshold of evidence needed for the Joy marker to decide that a smile occurred in that frame
**threshold_au12**: the threshold of AU12 evidence of activation needed to decide that a smile occurred in that frame

using discrete smile ranges:
**proportion of joy ranges actually in truth**: what proportion of the discrete smiles detected using the Joy measurement alone were also smiles in the truth data
**proportion of truth smiles captured by Joy**: what proportion of smiles in the truth data were detected as discrete smiles by the Joy markers
**proportion of AU12 ranges actually in truth**: what proportion of the discrete smiles detected using the AU12 measurement alone were also smiles in the truth data
**proportion of truth smiles captured by AU12**: what proportion of smiles in the truth data were detected as smiles by the AU12 markers
**proportion of combined joy/au12 smiles in truth**: what proportion of the smiles determined by combining the Joy/AU12 markers were also smiles in the truth data
**proportion of truth smiles captured by Joy/AU12**: what proportion of smiles in the truth data were detected as smiles using combined Joy/AU12 markers

on a purely frame-by-frame basis:
**parameters**: parameter1 vs parameter2
**p_relevance**: when parameter1 = 1, how often did parameter2 = 1?
**p_reliability**: when parameter2 = 1, how often did parameter1 = 1?
**n_relevance**: when parameter1 = 0, how often did parameter2 = 0?
**n_relability**: when parameter2 = 0, how often did parameter1 = 0?
**miscount_proportion**: proportion of frames that did not have enough data to determine whether or not a smile was present