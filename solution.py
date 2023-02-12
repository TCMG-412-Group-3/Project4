import urllib.request
import re
import datetime

urllib.request.urlretrieve('https://s3.amazonaws.com/tcmg476/http_access_log', r"./http_access_log.txt") #downloads txt from http
with open ( './http_access_log.txt', 'r') as data: #opens txt file

  data_list = data.read().splitlines() #converts txt to list, each line is an index (read().splitlines() is used to remove the newline character)
  ttl_rq = len(data_list) #counts total indexes to obtain total number of requests
  
  date_list = []
  data_list.reverse() #sorts from most recent to oldest
  no_date_counter = 0

  empty_dates = []
  for i in range(ttl_rq): #obtain dates from entire list
    try:
      n = str(data_list[i]) #turns list element into a string to split
      n2 = re.split('\[|\]|\:', n) #splits at brackets and colons so there is only date
      date_list.append(n2[1].split(r'/')) #makes each part of date into an element of its own list, added to master list named date_list
    except IndexError: #used to bypass requests without a date
      empty_dates.append(data_list[i]) #adds index of request without a date to list
      no_date_counter += 1 #tallies number of requests without a date
      pass
    
  months_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
  
  comparison = date_list[0] #most recent entry used to compare to previous number of months
  current_date = datetime.date(int(comparison[2]), months_dict[comparison[1]], int(comparison[0])) #turns the most recent date into format useable by datetime module

  counter = 0
  for i in range(len(date_list)): #for loop to compare each entry to the most recent entry
    temp_date = datetime.date(int(date_list[i][2]), months_dict[date_list[i][1]],int(date_list[i][0])) #converts each date entry into a datetime format
    difference = current_date - temp_date #calculates difference of datetimes
    if difference.days <= 180: #conditional to determine if datetime difference is 180 days
      counter += 1 #adds to the number of requests within a 6 month period
    else: #stops the for loop once it reaches 6 months to prevent further parsing
      break
    

# print ('the most recent date is', comparison)
# print(" ")
# print ('The most recent entry is:', data_list[0])
# print(' The oldest entry is:', data_list[-1])

print ('Total number of requests:', ttl_rq)
print('number of requests within the past 6 months:', counter)
print('number of requests without a date:', no_date_counter)