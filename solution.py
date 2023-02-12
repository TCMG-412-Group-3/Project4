import urllib.request
import re
import datetime
import decimal

urllib.request.urlretrieve('https://s3.amazonaws.com/tcmg476/http_access_log', r"./http_access_log.txt") #downloads txt from http
with open ( './http_access_log.txt', 'r') as data: #opens txt file

  data_list = data.read().splitlines() #converts txt to list, each line is an index (read().splitlines() is used to remove the newline character)
  ttl_rq = len(data_list) #counts total indexes to obtain total number of requests
  
  date_list = []
  empty_dates = []

  status_3xx_counter = 0
  status_4xx_counter = 0

  file_dict = {}  

  data_list.reverse() #sorts from most recent to oldest
  no_date_counter = 0

  for i in range(ttl_rq): #obtain dates from entire list
    try:
      n = str(data_list[i]) #turns list element into a string to split
      n2 = re.split('\[|\]|\:', n) #splits at brackets and colons so there is only date
      date_list.append(n2[1].split(r'/')) #makes each part of date into an element of its own list, added to master list named date_list

      n3 = re.split('\"', n2[5]) 
      status_temp_str = str(n3[2]).strip() # obtains only status code from regex split. strips to get rid of whitespace
      if status_temp_str.startswith('3'): # looks for status code to start with 3
        status_3xx_counter += 1 # tallies 3 codes
      elif status_temp_str.startswith('4'): # looks for status code to start with 4
        status_4xx_counter += 1 # tallies 4 codes
      else:
        pass

      n4 = re.split('"GET | HTTP', n2[5]) #file name counter
      n4_2 = n4[1].split() #gets rid of extra stuff after the file extension
      if n4_2[0] in file_dict:
        file_dict[n4_2[0]] += 1
      else:
        file_dict[n4_2[0]] = 1

    except IndexError: #used to bypass requests without a date
      empty_dates.append(data_list[i]) #adds index of request without a date to list
      no_date_counter += 1 #tallies number of requests without a date
      pass
    
  months_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
  
  comparison = date_list[0] #most recent entry used to compare to previous number of months
  current_date = datetime.date(int(comparison[2]), months_dict[comparison[1]], int(comparison[0])) #turns the most recent date into format useable by datetime module

  past_6months_counter = 0
  for i in range(len(date_list)): #for loop to compare each entry to the most recent entry
    temp_date = datetime.date(int(date_list[i][2]), months_dict[date_list[i][1]],int(date_list[i][0])) #converts each date entry into a datetime format
    difference = current_date - temp_date #calculates difference of datetimes
    if difference.days <= 180: #conditional to determine if datetime difference is 180 days
      past_6months_counter += 1 #adds to the number of requests within a 6 month period
    else: #stops the for loop once it reaches 6 months to prevent further parsing
      break
    
status_3xx_percent = (decimal.Decimal((status_3xx_counter/ttl_rq)*100)).quantize(decimal.Decimal('.01')) # calculates % and rounds to 2 decimal places
status_4xx_percent = (decimal.Decimal((status_4xx_counter/ttl_rq)*100)).quantize(decimal.Decimal('.01'))

file_max_count = 0
file_min_list = []

for i in file_dict:
  if file_max_count < file_dict[i]: #compares the max count to current count, if more then replaced
    file_max_count = file_dict[i]
  elif file_dict[i] == 1: #checks if current count is = 1 to be added to least requested file list
    file_min_list.append(i)
  else:
    pass

file_max_name = list(file_dict.keys())[list(file_dict.values()).index(file_max_count)] #looks up key given value of dictionary
with open('file_min_document.txt', 'w') as file_min_doc: #adds every 'least' requested file to a txt to prevent cluttering when ran
  file_min_doc.write('\n'.join(file_min_list))

print ('Total number of requests:', ttl_rq)
print('number of requests within the past 6 months:', past_6months_counter)
print('number of requests without a date:', no_date_counter)
print('The number of 3xx status is:', status_3xx_counter, 'which is: %', status_3xx_percent) 
print('The number of 4xx status is:', status_4xx_counter, 'which is: %', status_4xx_percent)
print('The most requested file is', file_max_name, 'with', file_max_count, 'requests')
print('The least requested files were output into file_min_document.txt with each request having 1 count')
