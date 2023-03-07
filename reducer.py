#!/home/bigdata/anaconda3/bin/python

import sys

is_first = True
current_key = ("", "")
current_sum = [0, 0]

for line in sys.stdin:
	words = line.strip().split("\t")
	if(is_first):
		is_first = False
		current_key = (words[0], words[1])
	if(current_key == (words[0], words[1])):
		current_sum[0] += int(words[2])
		current_sum[1] += int(words[3])
	else:
		print(current_key[0] + "\t" + current_key[1] + "\t" + str(current_sum[0]) + "\t" + str(current_sum[1]))
		current_key = (words[0], words[1])
		current_sum[0] = 0
		current_sum[1] = 0

print(current_key[0] + "\t" + current_key[1] + "\t" + str(current_sum[0]) + "\t" + str(current_sum[1]))