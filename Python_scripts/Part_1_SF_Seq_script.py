#!/usr/bin/env python



import numpy as np
import argparse



def q_score():
	parser = argparse.ArgumentParser(description='Fastq files generating the quality score at each bp position')
	parser.add_argument("-f", help="FASTQ file", required=True, type=str)
	return parser.parse_args()



# Function for quality score
def convert_phred(letter):                                   
    """Converts a single ASCII character into a quality score, assuming Phred+33"""
    qscore = ord(letter) - 33   # ord takes the ASCII char and turns it into a Phred score 
    return qscore

args = q_score()



for fastq in args.f:
    with open(fastq,"rt") as file:      
        NR = 0
        for line in file:            
            NR += 1
            line = line.strip('\n')               # strip off \n            
            if NR == 4:                           
                sequ_len = len(line)      
                break
    with open(fastq,"rt") as file:       
        NR = 0
       	reads = 0
        all_scores = np.zeros(seq_len)    # running total of means
        score_freq = {}    # dictionary for avg quality score for each read
        
        for line in file:            
            NR += 1
            line = line.strip('\n')                         
            if NR%4==0:                                              
                scores = np.zeros(seq_len)         # quality scores for that read
                i = 0
                reads += 1                         
                
                 # Look at the quality score line and convert it the ascii
                for base_pair in line:
                    all_scores[i] += convert_phred(line[i])   
                    scores[i] += convert_phred(line[i])        
                    i += 1  
                
                # avg quality score for said read
                read_mean = sum(scores)/len(scores)        
                
                # increment a count of avg q_score to dictionary
                if read_mean in score_freq:                
                    score_freq[read_mean] += 1
                else:
                    score_freq[read_mean] = 1
#for the running total, what is the mean at each position?
        for i in range(len(all_scores)):
            all_scores[i] = all_scores[i]/reads



 #avg score at each position 
        with open(fastq+"_mean_score_basepair.txt",'w')	as fh: # write out the metrics to a new file
            fh.write("Mean Q_Score"+"\n")	  #header
            i = 0
            for x in all_scores:
                fh.write(str(all_scores[i])+"\n")
                i += 1
        
        
        # output for dictionary of avg scores of every read
        with open(fastq+"_frequency_total.txt", "w") as fh:
            fh.write("Avg q_score & Frequency"+"\n")
            for key,value in score_freq.items():
                fh.write(str(key)+"\t"+str(value)+"\n")


