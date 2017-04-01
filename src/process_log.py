#Python file for all the code for the Insight Data Engineering Coding Challenge
#File name for the log.txt file
data_file="C:/Users/glori/Documents/GitHub/fansite-analytics-challenge/log_input/log_sample.txt"
hosts_file="C:/Users/glori/Documents/GitHub/fansite-analytics-challenge/log_output/hosts.txt"
resources_file="C:/Users/glori/Documents/GitHub/fansite-analytics-challenge/log_output/resources.txt"

#Important packages
import csv
import copy

#Helper function to convert the string of month to a number but as a string
#for easy appending to keep the placeholders
def convert_month(month_str):
	return_value=0
	if month_str=="Jan":
		return_value='01'
	elif month_str=="Feb":
		return_value='02'
	elif month_str=="Mar":
		return_value='03'
	elif month_str=="Apr":
		return_value='04'
	elif month_str=="May":
		return_value='05'
	elif month_str=="Jun":
		return_value='06'
	elif month_str=="Jul":
		return_value='07'
	elif month_str=="Aug":
		return_value='08'
	elif month_str=="Sep":
		return_value='09'
	elif month_str=="Oct":
		return_value='10'
	elif month_str=="Nov":
		return_value='11'
	elif month_str=="Dec":
		return_value='12'
	
	#Print an error if it doesn't match
	if return_value==0:
		print("Error month "+month_str+" does not exist")
	return return_value

#Create a helper function to help convert the date-times to
#time_value is in the form dd/mmm/yyyy:hh:mm::ss -400
def convert_time(time_value):
	#time_list yields the date at index 0, then the hours at index 1
	#then the minutes at index 2 and the seconds at index 3
	time_list=time_value.split(":")
	
	#date_list has the day first, then the month in string form, then 
	#the year
	date_list=time_list[0].split("/")
	
	final_string=date_list[2]+convert_month(date_list[1])+date_list[0]+time_list[1]+time_list[2]+time_list[3]
	
	return final_string
	
#Function to add an hour to the time value; 
#More complicated than just adding 10,000 since there are possibilities
#that it bleeds over into the next day/year
def add_one_hour(time_value):
	
	
	
def main(data_file):
	#Import data from the given text file name
	log_csv=[]
	with open(data_file, encoding='utf-8') as f:
		# reader = csv.reader(f, skipinitialspace=True, quoting=csv.QUOTE_NONE,delimiter=" ")
		# next(reader) #skip header
		# try:
			# for row in reader:
				# #append the row into the list
				# log_csv.append(row)

		# except csv.Error as e:
			# sys.exit('file {}, line {}: {}'.format(data_file, reader.line_num, e))
		#header
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
					#temp_list.append(temp_string)
					#temp_string=""
					#temp_index.append(copy.deepcopy(temp_list))
					#temp_list=[]
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
					#temp_list.append(temp_string)
					#temp_string=""
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
	with open(resources_file, 'w') as output_file:
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
	#xxxxxxxxxxxx
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
	with open(resources_file, 'w') as output_file:
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
	#Super naive way: Make each distinct time a key and then count 
	#the number of access points within an hour of that time
	#We don't assume that the log file is in chronological order, 
	#even though log files usually are and briefly spot checking 
	#some dates seem to show that it is.
	
	#For each time stamp (index 3), if it's not in the dictionary, then add it
	full_time_dictionary=dict()
	for i in range(0,len(log_csv)):
		time_key=convert_time(log_csv[i][3])
		if time_key not in full_time_dictionary.keys():
			full_time_dictionary[time_key]=0
	
	#Go through each log entry and see if it is in the correct range
	for key in full_time_dictionary.keys():
		for i in range(0,len(log_csv)):
			if log_csv[i][3]>=key and log_csv[i][3]<add_one_hour(key):
				full_time_dictionary[key]+=1
	
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
	with open(resources_file, 'w') as output_file:
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
	
	#Version 2: Assume that the times are in chronological order
	

#Feature 4
#Write out Feature 4


#Call the main
if __name__ == '__main__':
	main(data_file)