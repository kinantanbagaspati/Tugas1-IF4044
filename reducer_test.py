import csv

data_path = "raw_json"

r = open("../" + data_path + ".txt", "r")
lines = r.readlines()
data_dict = {}
lines_scanned = 0
for line in lines:
    line_split = line.strip().split("\t")
    if (line_split[0], line_split[1]) in data_dict:
        data_dict[(line_split[0], line_split[1])][0] += int(line_split[2])
        data_dict[(line_split[0], line_split[1])][1] += int(line_split[3])
    else:
        data_dict[(line_split[0], line_split[1])] = [int(line_split[2]), int(line_split[3])]
    
    lines_scanned += 1
    if lines_scanned % 100 == 0:
        print(str(lines_scanned) + "/" + str(len(lines)) + " lines scanned")

r.close()

w = open(data_path + ".csv", "w", encoding="UTF8", newline="")
writer = csv.writer(w)
writer.writerow(["Social Media", "Date", "Posts", "Comments"])

for key in sorted(list(data_dict.keys())):
    writer.writerow([key[0], key[1], data_dict[key][0], data_dict[key][1]])
w.close
