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
##
      n3 = re.split('\"', n2[5]) 
      status_temp_str = str(n3[2]).strip() # obtains only status code from regex split. strips to get rid of whitespace
      if status_temp_str.startswith('3'): # looks for status code to start with 3
        status_3xx_counter += 1 # tallies 3 codes
      elif status_temp_str.startswith('4'): # looks for status code to start with 4
        status_4xx_counter += 1 # tallies 4 codes
      else:
        pass
##
      n4 = re.split('"GET | HTTP', n2[5]) #file name counter
      n4_2 = n4[1].split() #gets rid of extra stuff after the file extension
      if n4_2[0] in file_dict:
        file_dict[n4_2[0]] += 1
      else:
        file_dict[n4_2[0]] = 1
##
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

##    
status_3xx_percent = (decimal.Decimal((status_3xx_counter/ttl_rq)*100)).quantize(decimal.Decimal('.01')) # calculates % and rounds to 2 decimal places
status_4xx_percent = (decimal.Decimal((status_4xx_counter/ttl_rq)*100)).quantize(decimal.Decimal('.01'))
##

##
file_max_count = 0
file_min_list = []

for i in file_dict:
  if file_max_count < file_dict[i]: #compares the max count to current count, if more then replaced
    file_max_count = file_dict[i]
  elif file_dict[i] == 1: #checks if current count is = 1 to be added to least requested file list
    file_min_list.append(i)
  else:
    pass
##

file_max_name = list(file_dict.keys())[list(file_dict.values()).index(file_max_count)] #looks up key given value of dictionary
with open('file_min_document.txt', 'w') as file_min_doc: #adds every 'least' requested file to a txt to prevent cluttering when ran
  file_min_doc.write('\n'.join(file_min_list))

##
for i in range(ttl_rq): #creates a [month]_log.txt file for requests each month
  index_content = data_list[i] #finds the request content
  if any(z in index_content for z in months_dict.keys()): #checks if request cotent has month, else it makes IndexError
    month_checker = re.split("\/", index_content) #retrieves month from request
    with open(month_checker[1]+'_log.txt', 'a') as month_file: #appends request to the respective file
        month_file.write(index_content+'\n')
  else: #request does not have a month in it
    previous_request_index = i 
    while True:
      previous_request_index -= 1 #search continuously through previous requests
      previous_req = data_list[previous_request_index] # ^
      month_checker = re.split("\/", previous_req) 
      if any(z in previous_req for z in months_dict.keys()): #finds most related request with a month
        with open(month_checker[1]+'_log.txt', 'a') as month_file: #places the current request into month file of that closest request with proper date
          month_file.write(index_content+'\n')
          break
      else: continue #restarts loop to continue finding previous request
##

#Find requests made on each day
#store dictionary of dates and number of requests
date_list.reverse()
day_dict = {}
current_date = datetime.date(int(date_list[0][2]), months_dict[date_list[0][1]],int(date_list[0][0]))
day_dict[str(current_date)] = 1
date_to_collect = current_date

#iterate through each date in the list
for i in range(len(date_list)):
  current_date = datetime.date(int(date_list[i][2]), months_dict[date_list[i][1]],int(date_list[i][0]))
  #if we get to a new date, set the current_date to the new date
  if (current_date != date_to_collect):
    date_to_collect = current_date
    #add date to dictionary
    if str(date_to_collect) not in day_dict:
      day_dict[str(date_to_collect)] = 1
    continue
  else:
    day_dict[str(date_to_collect)] += 1



#find how many requests were made per week

week_count = 0 
week_dict = {}
current_date = datetime.date(int(date_list[0][2]), months_dict[date_list[0][1]],int(date_list[0][0]))
date_to_collect = current_date
week_dict[week_count] = 1
for i in range(len(date_list)):
  current_date = datetime.date(int(date_list[i][2]), months_dict[date_list[i][1]],int(date_list[i][0]))
  #if we hit a week (7) days, increment the week count
  if ((current_date - datetime.timedelta(days=7)) == date_to_collect):
    week_count += 1
    date_to_collect = current_date
    #add date to dictionary
    if week_count not in week_dict:
      week_dict[week_count] = 1
    continue
  else:
    week_dict[week_count] += 1



#find requests made per month

month_year_dict = {}
current_month_year = date_list[0][1] + ' ' + date_list[0][2]
month_date_to_collect = current_month_year
month_year_dict[current_month_year] = 1
for i in range(len(date_list)):
  current_month_year = date_list[i][1] + ' ' + date_list[i][2]
  #if we hit a new month, set the current_month_year to the new month, and craete a new entry in the dictionary if it doesn't exist
  if (current_month_year != month_date_to_collect):
    month_date_to_collect = current_month_year
    #add date to dictionary
    if month_date_to_collect not in month_year_dict:
      month_year_dict[month_date_to_collect] = 1
    continue
  else:
    month_year_dict[month_date_to_collect] += 1

print('-'*50)
print ('Total number of requests:', ttl_rq)
print('number of requests within the past 6 months:', past_6months_counter)
print('number of requests without a date:', no_date_counter)
print('-'*50)
print('number of requests made on each day:')
for i in day_dict:
  print('Date:', i, 'Number of requests:', day_dict[i])
print('-'*50)
print('number of requests made per week:')
for i in week_dict:
  print('Week:', i+1, 'Number of requests:', week_dict[i])
print('-'*50)
print('number of requests made per month:')
for i in month_year_dict:
  print('Month:', i, 'Number of requests:', month_year_dict[i])
print('-'*50)
print('The number of 3xx status is:', status_3xx_counter, 'which is: %', status_3xx_percent) 
print('The number of 4xx status is:', status_4xx_counter, 'which is: %', status_4xx_percent)
print('The most requested file is', file_max_name, 'with', file_max_count, 'requests')
print('The least requested files were output into file_min_document.txt with each request having 1 count')
