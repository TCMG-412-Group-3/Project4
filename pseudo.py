
#
# for this week's project, we must answer the following
# 1. How many requests were made on each day? 
# 2. How many requests were made on a week-by-week basis? Per month?
# 3. What percentage of the requests were not successful (any 4xx status code)?
# 4. What percentage of the requests were redirected elsewhere (any 3xx codes)?
# 5. What was the most-requested file?
# 6. What was the least-requested file

# uncertain solution to 1 and 2
# parse each line and compare dates to store the same dates in counter variables
# compare dates by value of month and if they are the same, += of another counter variable
# for the week by week would we have to check of the day is 1-7, 8-14, ... ?? there should be a simpler way to divide the weeks of each month

# for 3 and 4 we iterate through the log file after initiating two count variables
# one counter "failed" and one "redirect" == 0 before the loop
# if request was not successful (check if first value of status code == 4), int failed +=1
# if request was redirected (check if first value of status code == 3), int redirect +=1
# we have the total requests saved as ttl_rq so to get the percentages, 
# print (failed/ttl_rq) * 100 "% of requests were not successful" and print (redirect/ttl_rq) * 100 "% of requests were redirected elsewhere"

# for 5 and 6 we must compare each element of the log file to each other to get the most and least requested file
# initiate variables for most and least requested files "most" and "least" == 0
# outside loop will iterate through each request and store the number of times one request appears 
# to compare, inner loop will compare the stored number of times it appears to a different request
# if # request > prev, set most the request, if # request < prev, set request as least, iterate through whole list
