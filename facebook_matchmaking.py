'''
Created on Feb 10, 2016
@author: hanhanwu
Get my friends Facebook data using Facebook Graph API
Covert the generated training data into numerical data and use libsvm to do friends prediction
'''

import facebook
import requests
from geopy.geocoders import Nominatim
from geopy.distance import vincenty 
import sys
  
        
def get_friends_ids(profile, graph):
    friends = graph.get_connections(profile['id'], 'friends')
    friends_dict = {}
    # Wrap this block in a while loop so we can keep paginating requests until finished.
    while True:
        try:
            for friend in friends['data']:
                fid = friend['id']
                friends_dict[fid] = {}
                friends_dict[fid]['name'] = friend['name']
            # Attempt to make a request to the next page of data, if it exists.
            friends = requests.get(friends['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the loop and end the script.
            break
    return friends_dict


def compare_str(str1, str2):
    if str1 == str2: return 1
    return 0


def get_distance(location1, location2):
    geolocator = Nominatim()
    l1 = geolocator.geocode(location1)
    l2 = geolocator.geocode(location2)
    al1 = (l1.latitude, l1.longitude)
    al2 = (l2.latitude, l2.longitude)
    distce = vincenty(al1, al2).miles
    return distce
    
    
# get gender,work,hometown,likes,location,education,birthday
def get_user_info(user_id, graph):
    user_info = {}
    user_profile = graph.get_object(user_id)
    gender = user_profile['gender']
    hometown, location, education, work = None, None, None, None
    if 'hometown' in user_profile.keys():
        hometown = user_profile['hometown']['id']
    if 'location' in user_profile.keys():
        location = user_profile['location']['name']
    if 'education' in user_profile.keys():
        education = user_profile['education']
    if 'work' in user_profile.keys():
        work = user_profile['work']
    likes = []
    likes_data = graph.get_connections(user_profile['id'], 'likes')
    while True:
        try:
            likes.extend(likes_data['data'])
            # Attempt to make a request to the next page of data, if it exists.
            likes_data = requests.get(likes_data['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the loop and end the script.
            break
     
    user_info['gender'] = gender
    user_info['hometown'] = hometown
    user_info['location'] = location
    if education != None:
        education = simplify_edu(education)
    user_info['education'] = education
    if work != None:
        work = simplify_work(work)
    user_info['work'] = work
    if likes != None:
        likes = simplify_likes(likes)
    user_info['likes'] = likes
    return user_info
    
    
def simplify_likes(likes):
    simplified_likes = {}
    for dct in likes:
        category_id = dct['id']
        simplified_likes[category_id] = []
        if 'category_list' in dct.keys():
            for itm in dct['category_list']:
                item_id = itm['id']
                simplified_likes[category_id].append(item_id)
    return simplified_likes


def simplify_work(work):
    simplified_work = {}
    simplified_work.setdefault('employer', [])
    simplified_work.setdefault('position', [])
    simplified_work.setdefault('location', [])
    for dct in work:
        simplified_work['employer'].append(dct['employer']['id'])
        if 'position' in dct.keys():
            simplified_work['position'].append(dct['position']['id'])
        if 'location' in dct.keys():
            simplified_work['location'].append(dct['location']['id'])
    return simplified_work
    
    
def simplify_edu(edu):
    education = {}
    education.setdefault('school', [])
    education.setdefault('major', [])
    for dct in edu:
        education['school'].append(dct['school']['id'])
        if 'concentration' in dct.keys():
            for item in dct['concentration']:
                education['major'].append(item['id'])                
    return education


# if they share same category, add 1, and if in the same category, they share same likes, add more 1s
def compare_likes(likes1, likes2):
    likes_score = 0
    for k,v1 in likes1.items():
        if k in likes2.keys():
            likes_score += 1
            v2 = likes2[k]
            common_items = [t for t in v1 if t in v2]
            likes_score += len(common_items)
    return likes_score


def compare_work(work1, work2):
    work_score = 0
    e1 = work1['employer']
    e2 = work2['employer']
    common_e = [e for e in e1 if e in e2]
    work_score += len(common_e)
    
    p1 = work1['position']
    p2 = work2['position']
    common_p = [p for p in p1 if p in p2]
    work_score += len(common_p)
    
    l1 = work1['location']
    l2 = work2['location']
    common_l = [l for l in l1 if l in l2]
    work_score += len(common_l)
    
    return work_score


def compare_education(edu1, edu2):
    edu_score = 0
    s1 = edu1['school']
    s2 = edu2['school']
    common_s = [s for s in s1 if s in s2]
    edu_score += len(common_s)
    
    m1 = edu1['major']
    m2 = edu2['major']
    common_m = [m for m in m1 if m in m2]
    edu_score += len(common_m)
    
    return edu_score
    
    
# convert nominal data into numerical data
def create_training_data(my_info, friends_dict):
    training_data = []
    
    for f_info in friends_dict.values():
        gender_diff = compare_str(my_info['gender'], f_info['gender'])
        hometown_diff, dist, common_likes, common_work, common_education = -1, -1, -1, -1, -1
        if my_info['hometown'] != None and f_info['hometown'] != None:
            hometown_diff = compare_str(my_info['hometown'], f_info['hometown'])
        if my_info['location'] != None and f_info['location'] != None:
            dist = get_distance(my_info['location'], f_info['location'])
        if my_info['likes'] != None and f_info['likes'] != None:
            common_likes = compare_likes(my_info['likes'], f_info['likes'])
        if my_info['work'] != None and f_info['work'] != None:
            common_work = compare_work(my_info['work'], f_info['work'])
        if my_info['education'] != None and f_info['education'] != None:
            common_education = compare_education(my_info['education'], f_info['education'])
        fpair = [gender_diff, hometown_diff, dist, common_likes, common_work, common_education]
        training_data.append(fpair)
        
    return training_data


def rescale_data(numerical_rows):
    results = []
    row_num = len(numerical_rows[0])
    maxs = [-sys.maxint-1]*row_num
    mins = [sys.maxint]*row_num
    
    # get max, min for each column
    for r in numerical_rows:
        for i in range(row_num):
            if r[i] > maxs[i]: maxs[i] = r[i]
            if r[i] < mins[i]: mins[i] = r[i]
                       
    # rescale each row
    for r in numerical_rows:
        for i in range(row_num):
            if maxs[i] == mins[i]: r[i] = 0
            else: r[i] = float(r[i] - mins[i])/(maxs[i]-mins[i])
        results.append(r)
            
    return results


class fb_numerical_data:
    def __init__(self, data_lst, match):
        self.data = [float(d) for d in data_lst]
        self.match = match         
       
        
def main():
    # Get a temporary access token: https://developers.facebook.com/tools/explorer/
    access_token = '[your temporary token]'    
    user = 'me'
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)

    # Get and simplify your own info
    my_info = get_user_info(user, graph)
    
    print my_info 
    
    # Get and simplify friends' info
    friends_dict = get_friends_ids(profile, graph)
    for fid,v in friends_dict.items():
        f_info = get_user_info(fid, graph)
        friends_dict[fid].update(f_info)
        
    for k,v in friends_dict.items():
        print k
        print v
        
    training_data = create_training_data(my_info, friends_dict)
        
#     # my friends data does not have features with largers numbers, so I swon't do rescaling here
#     rescaled_training_data = rescale_data(training_data)
#     print rescaled_training_data

    training_data = [fb_numerical_data(r,1) for r in training_data]
    matches = []
    features = []
    for itm in training_data:
        matches.append(itm.match)
        features.append(itm.data)
    
    # use the output here as libsvm input
    print matches,',',features
    
    # open terminal and go to the path under libsvm/pyhton folder, then type "python"+Enter
    # put the matches, features output in the terminal
    # put the code below into your terminal
    from svmutil import *
    prob = svm_problem(matches, features)
    pm_matchmaker = svm_parameter('-t 2')  # indicates using radial-basis function
    m = svm_train(prob, pm_matchmaker)
    # this is my test point, you can change to other points
    p_labels, p_acc, p_vals = svm_predict([0], [[0.0, -1.0, -1.0, 0.0, -1.0, -1.0]], m)  
    
if __name__ == '__main__':
    main()





