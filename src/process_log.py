#Python file for all the code for the Insight Data Engineering Coding Challenge

#Important packages
import csv
import copy
import math
import datetime
import argparse

def main():
	parser = argparse.ArgumentParser(description='Script for Insight Data Challenge')
	parser.add_argument('data_file', help='path to data_file')
	parser.add_argument('hosts_file', help='path to hosts')
	parser.add_argument('resources_file', help='path to resources_file')
	parser.add_argument('hours_file', help='path to hours_file')
	parser.add_argument('blocked_file', help='path to blocked_file')
	args = parser.parse_args()
	#Import data from the given text file name
	log_csv=[]
	with open(args.data_file, encoding='iso-8859-1') as f:
		#header line
		reader=f.readline()

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
			host_count_dictionary[log_csv[i][0]]+=1
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
			max_10_dictionary[key]=host_count_dictionary[key]
		else:
			#Save the min
			min_value=min(max_10_list)
			#check if the value is larger than the minimum value in the current 10
			if host_count_dictionary[key]>min_value:
				#first sort the values in the 10_list to get the min which is the index 0
				max_10_list.sort()
				#Rewrite the list without the smallest value
				max_10_list=copy.deepcopy(max_10_list[1:9])
				#remove the key corresponding to the smallest value
				for check_key in max_10_dictionary.keys():
					if max_10_dictionary[check_key]==min_value:
						del max_10_dictionary[check_key]
						break
				#Now add the new (higher) value to the value list and the dictionary
				max_10_list.append(host_count_dictionary[key])
				max_10_dictionary[key]=host_count_dictionary[key]



	#Write the results to a file, but in descending order
	#First sort the value list in descending order
	max_10_list.sort(reverse=True)
	with open(args.hosts_file, 'w') as output_file:
		for i in range(0,len(max_10_list)):
			for key in max_10_dictionary.keys():
				if max_10_dictionary[key]==max_10_list[i]:
					output_file.write(key)
					output_file.write(" ")
					output_file.write(str(max_10_dictionary[key]))
					output_file.write("\n")
					#then delete the key so we search through less
					del max_10_dictionary[key]
					#Also, stop searching
					break

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
			max_10_dictionary[key]=resource_dictionary[key]
		else:
			#Save the min
			min_value=min(max_10_list)
			#check if the value is larger than the minimum value in the current 10
			if resource_dictionary[key]>min_value:
				#first sort the values in the 10_list to get the min which is the index 0
				max_10_list.sort()
				#Rewrite the list without the smallest value
				max_10_list=copy.deepcopy(max_10_list[1:9])
				#remove the key corresponding to the smallest value
				for check_key in max_10_dictionary.keys():
					if max_10_dictionary[check_key]==min_value:
						del max_10_dictionary[check_key]
						break
				#Now add the new (higher) value to the value list and the dictionary
				max_10_list.append(resource_dictionary[key])
				max_10_dictionary[key]=resource_dictionary[key]

	#Write the results to a file, but in descending order
	#First sort the value list in descending order
	max_10_list.sort(reverse=True)
	with open(args.resources_file, 'w') as output_file:
		for i in range(0,len(max_10_list)):
			for key in max_10_dictionary.keys():
				if max_10_dictionary[key]==max_10_list[i]:
					output_file.write(key)
					output_file.write(" ")
					output_file.write(str(max_10_dictionary[key]))
					output_file.write("\n")
					#then delete the key so we search through less
					del max_10_dictionary[key]
					#Also, stop searching
					break

	#Feature 3
	#Assume that log files are in chronological order
	#so for each time value we want to know how many requests are made

	#For each time stamp (index 3), if it's not in the dictionary, then add it
	full_time_dictionary=dict()
	#iterator is the overall iterator for each row
	iterator=0
	while iterator<len(log_csv):
		time_key=datetime.datetime.strptime(log_csv[i][3],"%d/%b/%Y:%H:%M:%S %z")
		if time_key not in full_time_dictionary.keys():
			full_time_dictionary[time_key]=0
			#count the number of access points from this point onward
			#including the time_key
			j=iterator
			while j<len(log_csv) and datetime.datetime.strptime(log_csv[j][3],"%d/%b/%Y:%H:%M:%S %z")<=time_key+datetime.timedelta(hours=1):
				full_time_dictionary[time_key]+=1
				#need to increment the secondary iterator
				j=j+1
		iterator=iterator+1

	#Find the top 10
	#Now we have to determine which time period has the most access points
	max_10_list=[]
	max_10_dictionary=dict()
	#Delete the empty key in max_10_dictionary
	if '' in max_10_dictionary.keys():
		del max_10_dictionary['']
	#Have to go through each time and see if it's the top 10 rank
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
				max_10_list=copy.deepcopy(max_10_list[1:9])
				#remove the key corresponding to the smallest value
				for check_key in max_10_dictionary.keys():
					if max_10_dictionary[check_key]==min_value:
						del max_10_dictionary[check_key]
						break
				#Now add the new (higher) value to the value list and the dictionary
				max_10_list.append(full_time_dictionary[key])
				max_10_dictionary[key]=full_time_dictionary[key]

	#Write the results to a file, but in descending order
	#First sort the value list in descending order
	max_10_list.sort(reverse=True)
	with open(args.hours_file, 'w') as output_file:
		for i in range(0,len(max_10_list)):
			for key in max_10_dictionary.keys():
				if max_10_dictionary[key]==max_10_list[i]:
					output_file.write(datetime.datetime.strftime(key,"%d/%b/%Y:%H:%M:%S %z"))
					output_file.write(" ")
					output_file.write(str(max_10_dictionary[key]))
					output_file.write("\n")
					#then delete the key so we search through less
					del max_10_dictionary[key]
					#Also, stop searching
					break
		output_file.write("\n")

	#Feature 4
	#for each log item, if it's a bad login (error code 401)
	#index for the error code is second from the last
	with open(args.blocked_file, 'w') as output_file:
		error_code_index=len(log_csv[1])-2
		for i in range(0,len(log_csv)):
			current_time=datetime.datetime.strptime(log_csv[i][3],"%d/%b/%Y:%H:%M:%S %z")
			failed_counter=0
			if log_csv[i][error_code_index]=='401':
				#Hold on to the host and the site
				check_host=log_csv[i][0]
				check_site=log_csv[i][4]
				#Start searching from here
				j=i
				check_time=datetime.datetime.strptime(log_csv[j][3],"%d/%b/%Y:%H:%M:%S %z")
				while check_time<=current_time+datetime.timedelta(seconds=20) and j<(len(log_csv)-2):
					#Count the number of failures if it's the same host
					if log_csv[j][0]==check_host and log_csv[j][4]==check_site and log_csv[j][error_code_index]=='401':
						failed_counter+=1
						#If we hit 3 in 20 seconds, then record all following the third value
						k=j+1
						k_time=datetime.datetime.strptime(log_csv[k][3],"%d/%b/%Y:%H:%M:%S %z")
						if failed_counter==3:
							#Keep going from now until 5 minutes
							#Need to keep track of this iterator
							while k_time<=check_time+datetime.timedelta(minutes=5):
								#Write item by item to file
								for it in range(0,len(log_csv[k])):
									output_file.write(log_csv[k][it])
								output_file.write("\n")
								k=k+1
								k_time=datetime.datetime.strptime(log_csv[k][3],"%d/%b/%Y:%H:%M:%S %z")
					#break if it's the same host and site and there is a successful login
					elif log_csv[i][0]==check_host and log_csv[i][4]==check_site and log_csv[i][error_code_index]!='401':
						break
					j=j+1
					check_time=datetime.datetime.strptime(log_csv[j][3],"%d/%b/%Y:%H:%M:%S %z")


#Call the main function
if __name__ == '__main__':
	main()
