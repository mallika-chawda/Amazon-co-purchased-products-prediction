import numpy as np
import pandas as pd
import re
import csv
from datetime import datetime, timedelta

filepath= 'amazon-meta.txt'

csv_path= 'amazon-meta.csv'

review_csv_path= 'amazon-meta-review.csv'

class AmazonObject:
    Id=0
    ASIN=0
    title=''
    group=''
    sales_rank=''
    similar_count=0
    similar=''
    categories=''
    total_reviews=0
    total_downloads=0
    average_rating=0
    total_review_rating=0.0
    total_review_count=0
    date=''
    individual_categories=[]
    
class Review:
    date=''
    rating_sum=0
    votes_=0
    helpful_votes=0

id_pattern= '''^Id:\s*(?P<ID_number>\d+)$'''

ASIN_pattern = '''^ASIN:\s*(?P<ASIN_number>\d+)$'''

title_pattern = '''^\s*title:\s*(?P<title_text>.*)$'''

group_pattern = '''^group:\s*(?P<group_text>.*)$'''

similar_pattern = '''^similar:\s*(?P<similar_count>\d+)(?P<similar_book_ids>[\s*\d+]*)$'''

sales_rank_pattern = '''^salesrank:\s*(?P<sales_rank>\d+)$'''

reviews_pattern = '''^reviews:\s*total:\s*(?P<total_count>\d+)\s*downloaded:\s*(?P<download_count>\d+)\s*avg\s*rating:\s*(?P<average_rating>\d*[.,]?\d*)$'''

categories_pattern = '''^(\|(?P<pattern_category>\w*)\[\d*\])*$'''

individual_review_pattern = '''^\s*(?P<date>[0-9|\-]*)\s*cutomer:\s*(?P<customer_id>[A-Z|a-z|0-9]*)\s*
rating:\s*(?P<rating>[0-9]*)\s*votes:\s*(?P<votes>[0-9]*)\s*
helpful:\s*(?P<helpful_votes>[0-9]*)\s*$'''

id_pattern_matcher = re.compile(id_pattern, re.VERBOSE)
ASIN_pattern_matcher = re.compile(ASIN_pattern, re.VERBOSE)
title_pattern_matcher = re.compile(title_pattern, re.VERBOSE)
group_pattern_matcher = re.compile(group_pattern, re.VERBOSE)
similar_pattern_matcher = re.compile(similar_pattern, re.VERBOSE)
sales_rank_pattern_matcher = re.compile(sales_rank_pattern, re.VERBOSE)
reviews_pattern_matcher = re.compile(reviews_pattern, re.VERBOSE)
individual_review_pattern_matcher = re.compile(individual_review_pattern, re.VERBOSE)
#categories_pattern_matcher = re.compile(categories_pattern, re.VERBOSE)
#individual_category_pattern = "(\|)([\W|\w|\s]*)(\[)([0-9]*)(\])"
individual_category_pattern = "(\[)([0-9]*)(\])"

#print(re.findall(individual_category_pattern, "|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]"))
#input()

'''
print(re.match(individual_review_pattern_matcher, "2002-5-13 cutomer: A2IGOA66Y6O8TQ rating: 5 votes: 3 helpful: 2").group("date"))
print(re.match(individual_review_pattern_matcher, "2002-5-13 cutomer: A2IGOA66Y6O8TQ rating: 5 votes: 3 helpful: 2").group("customer_id"))
print(re.match(individual_review_pattern_matcher, "2002-5-13 cutomer: A2IGOA66Y6O8TQ rating: 5 votes: 3 helpful: 2").group("rating"))
print(re.match(individual_review_pattern_matcher, "2002-5-13 cutomer: A2IGOA66Y6O8TQ rating: 5 votes: 3 helpful: 2").group("votes"))
print(re.match(individual_review_pattern_matcher, "2002-5-13 cutomer: A2IGOA66Y6O8TQ rating: 5 votes: 3 helpful: 2").group("helpful_votes"))

#tests for matching id line
print(re.match(id_pattern_matcher, "Id:   2").group("ID_number"))
#print(re.match(id_pattern_matcher, "PId:   2").group("ID_number"))

#tests for matching ASIN line
print(re.match(ASIN_pattern_matcher, "ASIN: 0738700797").group("ASIN_number"))

#tests for matching title
print(re.match(title_pattern_matcher, "title: Candlemas: Feast of Flames").group("title_text"))

#tests for matching group line
print(re.match(group_pattern_matcher, "group: Book").group("group_text"))

#tests for matching similar movies
print(re.match(similar_pattern_matcher, "similar: 5  0738700827  1567184960  1567182836  0738700525  0738700940").group("similar_book_ids"))

#tests for matching reviews
print(re.match(reviews_pattern_matcher, "reviews: total: 12  downloaded: 12  avg rating: 4.5").group("total_count"))
print(re.match(reviews_pattern_matcher, "reviews: total: 12  downloaded: 12  avg rating: 4.5").group("download_count"))
print(re.match(reviews_pattern_matcher, "reviews: total: 12  downloaded: 12  avg rating: 4.5").group("average_rating"))

#tests for categories matching
#print(re.match(categories_pattern_matcher, "|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[1236]").group("pattern_category"))

#obj_list = []
'''

FileWriter = csv.writer(open(csv_path, 'w',  newline=''))
FileWriter.writerow(["Id", "ASIN", "Title", "Sales rank", "Group", "Similar", "Similar count", "Total reviews", "Total downloads", "Average rating", "Calculated Average", "Date", "All categories"])

with open(filepath,  encoding="utf8") as fp:

    count=0
    obj= None
    
    for line in fp.readlines():       
        
        try:
    
            count+=1
            if(count%100000==0):
                print(count)
            line= line.strip()
            id_match = re.match(id_pattern_matcher, line)
            if(id_match):
                if(obj):
                   if(obj.total_review_count==0):
                        obj.total_review_count=1
                   FileWriter.writerow([str(obj.Id), str(obj.ASIN), str(obj.title), str(obj.sales_rank), str(obj.group), str(obj.similar), str(obj.similar_count), str(obj.total_reviews), str(obj.total_downloads), str(obj.average_rating), str(float(obj.total_review_rating)/obj.total_review_count),str(obj.date), str('-'.join(list(set(obj.individual_categories))))])
                obj = AmazonObject()
                obj.individual_categories=[]
                obj.Id= id_match.group("ID_number")
                continue
            
            ASIN_match = re.match(ASIN_pattern_matcher, line)
            if(ASIN_match):
                obj.ASIN = ASIN_match.group("ASIN_number")
                continue
                
            title_match = re.match(title_pattern_matcher, line)
            if(title_match):
                obj.title = title_match.group("title_text")
                continue
                
            group_match = re.match(group_pattern_matcher, line)
            if(group_match):
                obj.group = group_match.group("group_text")
                continue
                
            sales_rank_match = re.match(sales_rank_pattern_matcher, line)
            if(sales_rank_match):
                obj.sales_rank = sales_rank_match.group("sales_rank")
                continue
                
            similar_match = re.match(similar_pattern_matcher, line)
            if(similar_match):
                obj.similar_count = int(similar_match.group("similar_count"))
                obj.similar = similar_match.group("similar_book_ids")
                continue
                
            reviews_match = re.match(reviews_pattern_matcher, line)
            if(reviews_match):
                obj.total_reviews = reviews_match.group("total_count")
                obj.total_downloads = reviews_match.group("download_count")
                obj.average_rating = reviews_match.group("average_rating")
                continue
                
            individual_reviews_match = re.match(individual_review_pattern_matcher, line)
            if(individual_reviews_match):
                obj.total_review_rating += int(individual_reviews_match.group("rating"))
                obj.total_review_count+=1
                new_date = individual_reviews_match.group("date")
                if(obj.date):
                    if(new_date > obj.date):
                        obj.date= new_date
                else:
                    obj.date= new_date
                        
                continue
            
            categories_match= re.findall(individual_category_pattern, line)
            if(categories_match):
                for match in categories_match:
                    obj.individual_categories.append(match[1])
                continue
           
        except Exception as e:
            print("Exception caught")
            print(e)
            continue
            
    FileWriter.writerow([str(obj.Id), str(obj.ASIN), str(obj.title), str(obj.sales_rank), str(obj.group), str(obj.similar), str(obj.similar_count), str(obj.total_reviews), str(obj.total_downloads), str(obj.average_rating), str(float(obj.total_review_rating)/obj.total_review_count),str(obj.date), str('-'.join(list(set(obj.individual_categories))))])
                

'''          
for obj in obj_list:
    print(obj.Id)
    print(obj.ASIN)
    print(obj.group)
    print(obj.title)            
'''     
            
            