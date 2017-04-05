#Python file for all the code for the Insight Data Engineering Coding Challenge

#Important packages
import csv
import copy
import math
import datetime
import argparse
import collections

def main():
	parser = argparse.ArgumentParser(description='Script for Insight Data Challenge')
	parser.add_argument('data_file', help='path to data_file')
	parser.add_argument('hosts_file', help='path to hosts')
	parser.add_argument('hours_file', help='path to hours_file')
	parser.add_argument('resources_file', help='path to resources_file')
	parser.add_argument('blocked_file', help='path to blocked_file')
	args = parser.parse_args()
	#Import data from the given text file name
	log_csv=[]
	with open(args.data_file, encoding='iso-8859-1') as f:
		#header line
		#reader=f.readline()

		#first line
		reader=f.readline()
		while reader!="":
			iterator=0
			temp_string=""
			check_quote=0
			temp_index=[]
			#temp_list=[]
			while iterator<len(reader):
				#Assume that quotes and [] don't occur in the same index
				if (reader[iterator]=='"' or reader[iterator]=="[") and check_quote==0:
					check_quote=1
					#Don't append the quote
					iterator=iterator+1
				elif (reader[iterator]=='"' or reader[iterator]=="]") and check_quote==1:
					check_quote=0
					#Don't append the quotes
					#the string is complete so append it to the index
					temp_index.append(temp_string)
					temp_string=""
					#Need to skip the space after the end quote as well
					iterator=iterator+1
				elif reader[iterator]==" " and check_quote==0:
					#Add the string to the index if it's not empty
					if temp_string!="":
						temp_index.append(temp_string)
					temp_string=""
					iterator=iterator+1
				elif reader[iterator]==" " and check_quote==1:
					#Append the space to the string
					#Don't clear temp_string yet
					temp_string=temp_string+reader[iterator]
					iterator=iterator+1
				#If we're at the end of the line
				elif reader[iterator]=='\n' and temp_string!='':
					temp_index.append(temp_string)
					iterator=iterator+1
				else: #Regular letter
					temp_string=temp_string+reader[iterator]
					iterator=iterator+1
			log_csv.append(temp_index)
			#Read the next line
			reader=f.readline()

	#Feature 1
	#List the top 10 most active host/IP addresses that have accessed the site.
	#Write out Feature 1
	#First, reformat all the data into a dictionary and for each host/IP address,
	#count up all the occurrences for each of them
	host_count_dictionary=dict()
	for i in range(0,len(log_csv)):
		#If we have seen the host key before, then increase the count by one
		if log_csv[i][0] in host_count_dictionary.keys():
			host_count_dictionary[log_csv[i][0]]=host_count_dictionary[log_csv[i][0]]+1
		#If we haven't seen the host key before then we add it to the dictonary keys
		#and then assign it to have a count of 1
		else:
			host_count_dictionary[log_csv[i][0]]=1

	#Delete the empty key
	if '' in host_count_dictionary.keys():
		del host_count_dictionary['']

	#Now we have to determine which of the hosts have the highest count
	max_10_list=[]
	max_10_dictionary=dict()
	#Delete the empty key in max_10_dictionary
	if '' in max_10_dictionary.keys():
		del max_10_dictionary['']
	#Have to go through each host/IP address and see if it's the top 10 rank
	for key in host_count_dictionary.keys():
		#If there aren't 10, then just add the value into the list
		#and add the key-value into the dictionary
		if len(max_10_list)<10:
			max_10_list.append(host_count_dictionary[key])
			max_10_dictionary[host_count_dictionary[key]]=key
		else:
			#Save the min
			min_value=min(max_10_list)
			#check if the value is larger than the minimum value in the current 10
			if key>min_value:
				#first sort the values in the 10_list to get the min which is the index 0
				max_10_list.sort()
				#Rewrite the list without the smallest value
				max_10_list=copy.deepcopy(max_10_list[1:10])
				#remove the key corresponding to the smallest value
				del max_10_dictionary[min]
				#Now add the new (higher) value to the value list and the dictionary
				max_10_list.append(host_count_dictionary[key])
				max_10_dictionary[key]=host_count_dictionary[key]

	#Write the results to a file, but in descending order
	#First sort the value list in descending order
	max_10_list.sort(reverse=True)
	with open(args.hosts_file, 'w') as output_file:
		for i in range(0,len(max_10_list)):
			output_file.write(str(max_10_dictionary[max_10_list[i]]))
			output_file.write(",")
			output_file.write(str(max_10_list[i]))
			output_file.write("\n")

	#Feature 2: Identify the 10 resources that consume the most bandwidth on the site
	#Create the dictionary to sum up the activity
	#bytes is the last index in the row; can be "-" which means 0
	#resource is the third from last index in the row
	#Need to split it by spaces and pick index 1

	#Create the dictionary for each resource
	resource_dictionary=dict()
	#calculating this for now so that the code can be written; sub later
	last_index=len(log_csv[0])-1
	third_last_index=len(log_csv[0])-3
	for i in range(0,len(log_csv)):
		#Scrape the resource
		resource=log_csv[i][third_last_index].split(" ")[1]
		bytes=log_csv[i][last_index]
		#Case if bytes is 0
		if bytes=="-":
			bytes=0
		#check if the resource is already a key
		if resource in resource_dictionary.keys():
			#then increment the number of bytes
			resource_dictionary[resource]+=int(bytes)
		else:
			resource_dictionary[resource]=int(bytes)

	#Remove the empty key if it exists
	if '' in resource_dictionary.keys():
		del resource_dictionary['']

	#Now we have to determine which of the resources use the most bandwidth
	max_10_list=[]
	max_10_dictionary=dict()
	if '' in max_10_dictionary.keys():
		del max_10_dictionary['']
	#Have to go through each resource and see if it's the top 10 rank
	for key in resource_dictionary.keys():
		#If there aren't 10, then just add the value into the list
		#and add the key-value into the dictionary
		if len(max_10_list)<10:
			max_10_list.append(resource_dictionary[key])
			max_10_dictionary[resource_dictionary[key]]=key
		else:
			#Save the min
			min_value=min(max_10_list)
			#check if the value is larger than the minimum value in the current 10
			if key>min_value:
				#first sort the values in the 10_list to get the min which is the index 0
				max_10_list.sort()
				#Rewrite the list without the smallest value
				max_10_list=copy.deepcopy(max_10_list[1:10])
				#remove the key corresponding to the smallest value
				del max_10_dictionary[min]
				#Now add the new (higher) value to the value list and the dictionary
				max_10_list.append(resource_dictionary[key])
				max_10_dictionary[key]=resource_dictionary[key]

	#Write the results to a file, but in descending order
	#First sort the value list in descending order
	max_10_list.sort(reverse=True)
	with open(args.resources_file, 'w') as output_file:
		for i in range(0,len(max_10_list)):
			output_file.write(str(max_10_dictionary[max_10_list[i]]))
			output_file.write("\n")
			#then delete the key so we search through less
			del max_10_dictionary[max_10_list[i]]


	#Feature 3
	#Assume that log files are in chronological order
	#so for each time value we want to know how many requests are made

	#For each time stamp (index 3), if it's not in the dictionary, then add it
	full_time_dictionary=dict()
	#This commented version only looks at hourly periods that have a request right at
	#the beginning of the period to decrease the overall number of logs we would have to write
	#and go through for the max
	#for i in range(0,len(log_csv)):
#		time_key=datetime.datetime.strptime(log_csv[i][3],"%d/%b/%Y:%H:%M:%S %z")
		#if time_key not in full_time_dictionary.keys():
		#	full_time_dictionary[time_key]=0
			#count the number of access points from this point onward
			#including the time_key
		#	j=i
		#	while j<len(log_csv) and datetime.datetime.strptime(log_csv[j][3],"%d/%b/%Y:%H:%M:%S %z")<=time_key+datetime.timedelta(hours=1):
		#		full_time_dictionary[time_key]=full_time_dictionary[time_key]+1
				#need to increment the secondary iterator
		#		j=j+1
	min_time=datetime.datetime.strptime(log_csv[0][3],"%d/%b/%Y:%H:%M:%S %z")
	max_time=datetime.datetime.strptime(log_csv[len(log_csv)-1][3],"%d/%b/%Y:%H:%M:%S %z")
	time_counter=copy.deepcopy(min_time)
	iterator=0
	time_counter_counter=0
	while time_counter<=max_time:
		#add the key, guaranteed to not have a duplicate key
		full_time_dictionary[time_counter]=0
		iterator=time_counter_counter
		#Count the number of occurrences
		while iterator<len(log_csv) and datetime.datetime.strptime(log_csv[iterator][3],"%d/%b/%Y:%H:%M:%S %z")<=time_counter+datetime.timedelta(hours=1):
			full_time_dictionary[time_counter]+=1
			iterator+=1
		#only increase the index counter if the next time in the list is larger than the time_counter
		#print(log_csv[time_counter_counter][3])
		#print(time_counter)
		if time_counter_counter<len(log_csv)-1 and time_counter+datetime.timedelta(seconds=1)>datetime.datetime.strptime(log_csv[time_counter_counter][3],"%d/%b/%Y:%H:%M:%S %z"):
			#print("TRUE")
			time_counter_counter=time_counter_counter+1
		#Increment by one second
		time_counter=time_counter+datetime.timedelta(seconds=1)

	#Delete the empty key from full_time_dictionary
	if '' in full_time_dictionary.keys():
		del full_time_dictionary['']

	#Now we have to determine which hours had the most frequent visits
	max_10_list=[]
	max_10_dictionary=dict()
	if '' in max_10_dictionary.keys():
		del max_10_dictionary['']
	#Have to go through each resource and see if it's the top 10 rank
	for key in full_time_dictionary.keys():
		#If there aren't 10, then just add the value into the list
		#and add the key-value into the dictionary
		if len(max_10_list)<10:
			max_10_list.append(full_time_dictionary[key])
			max_10_dictionary[key]=full_time_dictionary[key]
		else:
			#Save the min
			min_value=min(max_10_list)
			#check if the value is larger than the minimum value in the current 10
			if full_time_dictionary[key]>min_value:
				#first sort the values in the 10_list to get the min which is the index 0
				max_10_list.sort()
				#Rewrite the list without the smallest value
				max_10_list=copy.deepcopy(max_10_list[1:10])

				for k in max_10_dictionary.keys():
					#If the key had the min value then get rid of it
					#remove the key corresponding to the smallest value
					if max_10_dictionary[k]==min_value:
						del max_10_dictionary[k]
						break
				#Now add the new (higher) value to the value list and the dictionary
				max_10_list.append(full_time_dictionary[key])
				max_10_dictionary[key]=full_time_dictionary[key]

	#Write the results to a file, but in descending order
	#First sort the value list in descending order
	#If there are ties we need to print them in increasing time order
	#The counter function makes a dictionary of the occurrences of each item
	max_10_check=list(set(max_10_list))
	full_list=dict()
	for k in max_10_check:
		temp_list=[]
		for i in max_10_dictionary.keys():
			if k==max_10_dictionary[i]:
				temp_list.append(i)
		#Sort the list
		temp_list.sort()
		full_list[k]=copy.deepcopy(temp_list)
	if '' in full_list.keys():
		del full_list['']

	mini_list=list(set(max_10_list))
	mini_list.sort(reverse=True)
	with open(args.hours_file, 'w') as output_file:
		for i in range(0,len(mini_list)):
			for key in full_list[mini_list[i]]:
				output_file.write(datetime.datetime.strftime(key,"%d/%b/%Y:%H:%M:%S %z"))
				output_file.write(",")
				output_file.write(str(mini_list[i]))
				output_file.write("\n")
					#Have to delete that one in case there are duplicates
				#	del max_10_dictionary[key]
				#	break
			#then delete the key so we search through less
		output_file.write("\n")

	#Feature 4
	#for each log item, if it's a bad login (error code 401)
	#index for the error code is second from the last
	#Add the indices to a dictionary whose key is a list of the host and the site
	#the value is a list of the subsequent indices
	index_list=[]
	error_code_index=len(log_csv[1])-2
	for i in range(0,len(log_csv)):
		current_time=datetime.datetime.strptime(log_csv[i][3],"%d/%b/%Y:%H:%M:%S %z")
		#Hold on to the host and the site
		check_host=log_csv[i][0]
		check_site=log_csv[i][4]
		if i in index_list:
			continue
		#Check if it's already in the error dictionary
		failed_counter=0
		if log_csv[i][error_code_index]=='401':
			#Start searching from here
			j=i
			check_time=datetime.datetime.strptime(log_csv[j][3],"%d/%b/%Y:%H:%M:%S %z")
			while check_time<=current_time+datetime.timedelta(seconds=20) and j<(len(log_csv)-1):
				check_time=datetime.datetime.strptime(log_csv[j][3],"%d/%b/%Y:%H:%M:%S %z")
				#Count the number of failures if it's the same host
				if log_csv[j][0]==check_host and log_csv[j][4]==check_site and log_csv[j][error_code_index]=='401':
						failed_counter+=1
						#If we hit 3 in 20 seconds, then record all following the third value
						k=j+1
						k_time=datetime.datetime.strptime(log_csv[k][3],"%d/%b/%Y:%H:%M:%S %z")
						if failed_counter==3:
							#Keep going from now until 5 minutes
							#Need to keep track of this iterator
							while k_time<=check_time+datetime.timedelta(minutes=5) and k<len(log_csv):
								k_time=datetime.datetime.strptime(log_csv[k][3],"%d/%b/%Y:%H:%M:%S %z")
								if log_csv[k][0]==check_host and log_csv[k][4]==check_site and k not in index_list:
									index_list.append(k)
								k=k+1

				#break if it's the same host and site and there is a successful login
				elif log_csv[i][0]==check_host and log_csv[i][4]==check_site and log_csv[i][error_code_index]!='401':
					break
				j=j+1
	#Write all the error codes to the file
	with open(args.blocked_file, 'w') as output_file:
		for k in index_list:
			#Write item by item to file
			#write host
			output_file.write(log_csv[k][0])
			#Write two dashes
			output_file.write(" ")
			output_file.write(log_csv[k][1])
			output_file.write(" ")
			output_file.write(log_csv[k][2])
			output_file.write(" ")
			#Write the date
			#output_file.write(datetime.datetime.strftime(log_csv[k][3],"%d/%b/%Y:%H:%M:%S %z"))
			output_file.write("[")
			output_file.write(log_csv[k][3])
			output_file.write("]")
			output_file.write(" ")
			output_file.write('"')
			output_file.write(log_csv[k][4])
			output_file.write('"')
			output_file.write(" ")
			output_file.write(log_csv[k][5])
			output_file.write(" ")
			output_file.write(log_csv[k][6])
			output_file.write("\n")

#Call the main function
if __name__ == '__main__':
	main()
