# eaf-analysis-SRL

For Yale Social Robotics Lab, Aditi Ramachandran's project.  Code written by Rebecca Nickerson.

Process and compare ground truth smile data (from video coding, processed by eaf_to_text python program not included in this repo). 
Determine relevance and reliability of the test data (from AttentionTool run on video files) compared to the ground truth.
Determine how much smiles overlap between ground truth and test data by comparing the time ranges during which each detected smiles.

Run as:

% python ./processFiles.py   ground_truth_input.txt   ground_truth_output.txt   test_data_input.txt   test_data_output.txt   FINAL.txt

where ground_truth_input.txt contains the data from the eaf_to_text program, and test_data_input contains the exported dump file from AttentionTool

