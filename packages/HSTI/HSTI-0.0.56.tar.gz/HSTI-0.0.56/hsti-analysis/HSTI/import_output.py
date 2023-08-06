import numpy as np
import os

def import_output(path):
	temp = []
	with open(path, 'r') as file:
	    lines = file.readlines()
	    df = np.zeros([len(lines),len(lines[-1].split())])*np.nan
	    for i in range(len(lines)):
	        splits = lines[i].split()
	        for j in range(len(splits)):
	            df[i,j] = splits[j]
	    section_last_idx = np.where(np.diff(df[:,0])<0)
	    sections = [df[0:section_last_idx[0][0]+1]]
	    for i in range(len(section_last_idx[0])-1):
	        sections.append(df[section_last_idx[0][i]+1:section_last_idx[0][i+1]+1])
	    sections.append(df[section_last_idx[0][i+1]+1:])
	    return sections
    # return 2+2