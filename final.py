import unittest
import json
import requests
import pickle
import csv



################################################################################
#########################   Catching from Tumblr   #############################

def getWithCaching(keyword):
    if keyword == 'yoga':
        CACHE_FNAME = "yoga.txt"
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        response_dictionary = json.loads(cache_contents) # CACHE_DICTION = cache_contents
        cache_file.close()
        return response_dictionary

    else:
        CACHE_FNAME = "t_search.txt"
        try:
            cache_file = open(CACHE_FNAME, 'r')
            cache_contents = cache_file.read()
            CACHE_DICTION = json.loads(cache_contents) # CACHE_DICTION = cache_contents
            cache_file.close()
        except:
            CACHE_DICTION={}
        BASE_URL = "https://api.tumblr.com/v2/tagged"
        t_param={}
        t_param['tag']=keyword
        t_param['api_key']='xdEwduFXtM4g9fYf98hMnuvzIzwCnejsUZOEUqqBL0038ipmjL'
        full_url = requestURL(BASE_URL,t_param)

        if full_url in CACHE_DICTION:
            print 'using cache' # use stored response
            response_text = CACHE_DICTION[full_url]
        else:
            print 'fetching' # do the work of calling the API
            response = requests.get(full_url) # store the response
            CACHE_DICTION[full_url] = response.text
            response_text = response.text

            cache_file = open(CACHE_FNAME, 'w')
            cache_file.write(json.dumps(CACHE_DICTION))
            cache_file.close()

        response_dictionary = json.loads(response_text)
        return response_dictionary

def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url


################################################################################
# ######fetching data from meetup by using each elements
# ###in the list of most_common_tags(from Tumblr)
#
# BASE_URL2= "https://api.meetup.com/find/groups"
# m_param={}
# m_param["zip"]=48104
# m_param['upcoming_events']='true'
# m_param['key']='71584565545fb2045795d5c2e3a6d'
#
# CACHE_M_DICTION={}
#
# for tag in each(most_common_tags):
#     m_param['text']= tag  #from tumblr
#     full_url = requestURL(BASE_URL2,m_param)
#     a=requests.get(full_url)
#     CACHE_M_DICTION[full_url] = a.text
#
# f=open('meetup_all_tag.txt','w')
# f.write(json.dumps(CACHE_M_DICTION))

################################################################################
#########################   Catching from Meetup   #############################

CACHE_MNAME = "meetup_all_tag.txt"

try:
    m_cache_file = open(CACHE_MNAME, 'r')
    m_cache_contents = m_cache_file.read()
    CACHE_M_DICTION = json.loads(m_cache_contents) # CACHE_DICTION = cache_contents
    m_cache_file.close()
except:
    CACHE_M_DICTION = {}


def getWithCaching_meetup(tag):
    BASE_URL2= "https://api.meetup.com/find/groups"
    m_param={}
    m_param["zip"]=raw_zip
    m_param['upcoming_events']='true'
    m_param['key']='71584565545fb2045795d5c2e3a6d'
    m_param['text']= tag  #from tumblr
    full_url = requestURL(BASE_URL2,m_param)

    if full_url in CACHE_M_DICTION:
        print 'using cache' # use stored response
        m_response_text = CACHE_M_DICTION[full_url]
    else:
        print 'fetching' # do the work of calling the API
        m_response = requests.get(full_url) # store the response
        CACHE_M_DICTION[full_url] = m_response.text
        m_response_text = m_response.text

        cache_file = open(CACHE_MNAME, 'w')
        cache_file.write(json.dumps(CACHE_M_DICTION))
        cache_file.close()

    m_response_dictionary = json.loads(m_response_text)
    return m_response_dictionary


################################################################################
############################  Class Tumblr   ###################################

class Tumblr():
    def __init__(self, tumblr_dic={}):
        self.blog_name=tumblr_dic['blog_name']
        self.post_url=tumblr_dic['post_url']
        self.tags=[]
        for n in tumblr_dic['tags']:
            self.tags.append(n)

    def len_tags(self):
        return len(self.tags)

    def __str__(self):
        return "The name of the blog : {}\n The number of tags : {}".format(self.blog_name, self.len_tags())


################################################################################
############################   Class Meetup  ###################################

class Meetup():
    def __init__(self, each_post={}):
        if 'category' in each_post:
            self.category=each_post['category']['name']
        else:
            self.category=''

        if 'city' in each_post:
            self.city=each_post['city']
        else:
            self.city=''

        if 'score' in each_post:
            self.relevance=each_post['score']
        else:
            self.relevance=''

        if 'photos' in each_post:
            self.photo=each_post['photos']#type: dictionary list
        else:
            self.photo=''

        if 'next_event' in each_post:
            self.time=each_post['next_event']['time']
        else:
            self.time=''

        if 'name' in each_post:
            self.group_name=each_post['name']
        else:
            self.group=''

        if 'next_event' in each_post:
            self.event_name=each_post['next_event']['name']
        else:
            self.event=''

        if 'members' in each_post:
            self.members=each_post['members']
        else:
            self.members=''

    def mem_scr(self):
        return (self.members/self.relevance) *100

    def retime(self):
        ss=(self.time/1000)%60
        mm=(self.time/(1000*60))%60
        hh=(self.time/(1000*60*60))%24
        a= (str(hh),str(mm),str(ss))
        b=':'
        return b.join(a)


    def __str__(self):
        seconds=(self.time/1000)%60
        minutes=(self.time/(1000*60))%60
        hours=(self.time/(1000*60*60))%24
        return "{} event is at hr:{},min:{},sec:{}".format(self.event_name, hours ,minutes, seconds)


################################################################################
############################ Let's start   #####################################
################################################################################

interest=raw_input("please enter your interest\n") # 'yoga'

if interest == 'yoga':
    apicall=json.loads(getWithCaching(interest)[getWithCaching(interest).keys()[0]])
else:
    apicall=getWithCaching(interest)

blogs = [] #a list of instances for each dictionaries(0-20) under 'response'
for sub_dict in apicall['response']: #sub dictionaries(0-20) of each cached data
    blogs.append(Tumblr(sub_dict))

# which tags are searched generally related to main interest?
counts_diction={}
for blog in blogs:
    for ta in blog.tags:
        if ta in counts_diction:
            counts_diction[ta]=counts_diction[ta]+1
        else:
            counts_diction[ta]=1


sorted_tag=sorted(counts_diction.items(), key = lambda x: x[0])
sorted_ta=sorted(sorted_tag,key=lambda x:x[1],reverse=True)
sorted_tags=[interest]
for x in sorted_ta:
    sorted_tags.append(x[0])

# top 10 tags related to the Primary interest
most_common_tags=sorted_tags[:10]
print "most_common_tags are \n {}".format(most_common_tags)


def each(most_common_tags):
    if type(most_common_tags)==str:
        if 'yoga' == most_common_tags:
            return [most_common_tags]
        elif ' ' in most_common_tags:
            return each(most_common_tags.split(' '))
        elif 'yoga' in most_common_tags:
            return [most_common_tags.replace('yoga','')]
        else:
            return [most_common_tags]
    elif len(most_common_tags)==1:
        if ' ' in most_common_tags[0]:
            return each(most_common_tags[0].split(' '))
        elif 'yoga' in most_common_tags[0]:
            return [most_common_tags[0].replace('yoga','')]
        else:
            return [most_common_tags[0]]
    else:
        return each(most_common_tags[0])+each(most_common_tags[1:])

################################################################################
raw_zip=raw_input("enter your zipcode\n")
inst_lst=[]

for tag in most_common_tags:
    p=getWithCaching_meetup(tag)
    for a in p:
        inst_lst.append(Meetup(a))


score_dic={}
for inst in inst_lst:
    score_dic[inst.group_name]=inst.relevance
top_relevent_meetup=sorted(score_dic.items(), key=lambda x: x[1],reverse=True)[:5]
top_name=[top[0] for top in top_relevent_meetup]


top_inst_lst={}
for inst in inst_lst:
    if inst.group_name in top_name:
        top_inst_lst[inst.relevance]=inst
so_top=sorted(top_inst_lst.items(),  key=lambda x: x[1],reverse=True)
soo_top=[so[1] for so in so_top]
# print soo_top

#
# for i in soo_top:
#     print i.retime()

def avg_score(x):
    s=0
    for e in x:
        s+=e.score
    return s//len(x)

top_relevance=[top[1] for top in top_relevent_meetup]
top_event_name=[str(ins.event_name) for ins in soo_top]
top_time=[ins.retime()for ins in soo_top]

tup=zip(top_name,top_event_name, top_relevance, top_time)

a=len(top_relevent_meetup)
if a ==1 :
    print "There is a "+ str(a) +" relevant MEETUP group around you!"
elif a==0:
    print "I am sorry that there is no relevant MEETUP group around you \n How about creating your own group?"
else:
    if a>5:
        print "There is "+ str(a) +" relevant MEETUP group around you!\nHere is top 5 groups!!"
        for top in top_name:
            print top,"\n"
    elif a==5:
        print "There is "+ str(a) +" relevant MEETUP groups around you!"

################################################################################
############################ Making CSV file   #################################

rec=open('final.csv','w')
rec.write("{},{},{},{}\n".format('group','next event','relevance','time'))

for tu in tup:
    rec.write("{},{},{}.{}\n".format(*tu))
rec.close()


################################################################################
##############################   unittest   ####################################

class Problem1(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(blogs), type([]))

class Problem2(unittest.TestCase):
    def test_len(self):
        self.assertEqual(len(most_common_tags), 10)
        # self.assertEqual(counts_diction['Sky'], 2, "testing that the count for the key sunset is 50")

class Problem3(unittest.TestCase):
    def test_01(self):
        self.assertEqual(most_common_tags[0],interest)

class Problem4(unittest.TestCase):
    def test_02(self):
        self.assertFalse(len(counts_diction.keys()) < 0)

class Problem5(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(inst_lst[0].city),unicode)

class Problem6(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(sorted_tag), type([]))

if interest=='yoga':
    class Problem7(unittest.TestCase):
        def test(self):
            self.assertEqual(inst_lst[0].relevance, 4538.0)

    class Problem8(unittest.TestCase):
        def test(self):
            self.assertEqual(inst_lst[0].members, 156)


## BELOW THIS LINE IS CODE THAT WILL RUN ANY UNIT TESTS YOU WRITE INSIDE THIS FILE. DO NOT WRITE CODE BELOW IT OR DELETE IT.
unittest.main(verbosity=2)
