from datetime import datetime, timedelta
class UserPostData:
    def __init__(self, user, user_id, title, date, posting_index):
        self.user = user
        self.user_id = user_id
        self.title = title
        self.date = date
        self.posting_index = int(posting_index)

    def get_user(self):
        return self.user
    def get_user_id(self): 
        return self.user_id
    def get_date(self):
        return self.date
    def get_data_index(self):
        return self.posting_index
    def get_title(self):
        return self.title[1:]
    
class UserPostDataList:
    def __init__(self):
        self.user_list = []
        self.user_id_list = []
        self.title_list = []
        self.date_list = []
        self.posting_index_list = []
        #self.user_dict = {}
        #self.user_posting_dict = {}
        self.earliest_date = ""
        self.latest_date = ""
        self.min_posting_id = 0
        self.max_posting_id = 0
        self.length = 0

    def add_user_post_data(self, user_post):
        self.user_list.append(user_post.get_user())
        self.user_id_list.append(user_post.get_user_id())
        self.title_list.append(user_post.get_title())
        self.date_list.append(user_post.get_date())
        self.posting_index_list.append(user_post.get_data_index())
        self.length += 1
        return self
    
    def get_earliest_and_latest_date(self):
        if self.date_list == []:
            self.earliest_date = "1999-01-01 00:00:00"
            self.latest_date = "1999-01-01 23:39:39"
            return self
        else:
            self.earliest_date = self.date_list[self.length-1]
            self.latest_date = self.date_list[0]    
            return self

    def get_earliest_and_latest_posting(self):
        if self.posting_index_list == []:
            self.min_posting_id = 0
            self.max_posting_id = 0
            return self
        else:
            self.min_posting_id = self.posting_index_list[self.length-1]
            self.max_posting_id = self.posting_index_list[0]
            return self

    def compare(self, target_time):
        if target_time >= self.earliest_date and target_time <= self.latest_date:
            return 0
        elif target_time < self.earliest_date:
            return -1
        else:
            return 1  

    def __add__(self, other_datalist, debug = False): #Adding UserPoistDataList
        if self.length == 0:
            self.user_list = other_datalist.user_list
            self.user_id_list = other_datalist.user_id_list
            self.title_list = other_datalist.title_list
            self.date_list = other_datalist.date_list
            self.posting_index_list = other_datalist.posting_index_list
            self.length = other_datalist.length
            self.earliest_date = other_datalist.earliest_date
            self.latest_date = other_datalist.latest_date
            self.min_posting_id = other_datalist.min_posting_id
            self.max_posting_id = other_datalist.max_posting_id
            return self
        cut = 0
        if debug == True:
            print("Adding UserPostDataList of length " +str(other_datalist.length))
            print("current min_posting id: " + str(self.min_posting_id))
            print("other min_posting id: " + str(other_datalist.min_posting_id))
            print("current max_posting id: " + str(self.max_posting_id))
            print("other max_posting id: " + str(other_datalist.max_posting_id))
            
        for i in range(other_datalist.length):
            if other_datalist.posting_index_list[i] >= self.min_posting_id:
                cut = i+1
                print("We are cutting " + str(cut))
            else:
                break
            
        if cut == 0:
            print("No cutting")
        self.user_list = self.user_list + other_datalist.user_list[cut:]
        self.user_id_list = self.user_id_list + other_datalist.user_id_list[cut:]
        self.title_list = self.title_list + other_datalist.title_list[cut:]
        self.date_list = self.date_list + other_datalist.date_list[cut:]
        self.posting_index_list = self.posting_index_list + other_datalist.posting_index_list[cut:]
        self.length = self.length + other_datalist.length - cut
        self.min_posting_id = other_datalist.min_posting_id
        self.earliest_date = other_datalist.earliest_date
        return self
    
    def get_user_post_data_list(self):
        return self.user_post_data_list

    def __str__(self, min = 0, max = 0, get_content = False):
        print("Earliest Date: " + str(self.earliest_date) + ", Latest Date: " + str(self.latest_date))
        print("Min Posting ID: " + str(self.min_posting_id) + ", Max Posting ID: " + str(self.max_posting_id) + ", Length: " + str(self.length))
        if get_content == True:
            if max == 0:
                max = self.length

            for i in range(min, max):
                print("Title: " + str(self.title_list[i]))
                print("ID: " + str(self.user_list[i]) + ", " + str(self.user_id_list[i]))
                print("Index: " + str(i) + ", posting_index: " + str(self.posting_index_list[i]) + ", Date:" + str(self.date_list[i]))
                print()

        #return "UserPostDat: " + str(self.user_list) + ", " + str(self.user_id_list) + ", " + str(self.title_list) + ", " + str(self.date_list) + ", " + str(self.posting_index_list)

        return ""

class UserPostDataDict:
    def __init__(self, UserPostList):
        self.userPostList = UserPostList
        self.user_dict = {}
        self.user_posting_dict = {}

    def match_user_id_to_user_name(self):
        for i in range(self.userPostList.length):
            if self.userPostList.user_id_list[i] in self.user_dict:
                if self.userPostList.user_list[i] not in self.user_dict[self.userPostList.user_id_list[i]]:
                    self.user_dict[self.userPostList.user_id_list[i]].append(self.userPostList.user_list[i])
            else:
                self.user_dict[self.userPostList.user_id_list[i]] = [self.userPostList.user_list[i]]
        return self
    
    def collect_user_activities_by_user_id(self):
        for user_id in self.userPostList.user_id_list:
            if user_id in self.user_posting_dict:
                self.user_posting_dict[user_id] += 1
            else:
                self.user_posting_dict[user_id] = 1
        return self
    
    def build(self):
        self.match_user_id_to_user_name()
        self.collect_user_activities_by_user_id()
        return self

    def search_user_id_by_user(self, user):
        for key in self.user_dict:
            if user in self.user_dict[key]:
                return key
        return -1
    
    def search_user_posing_count(self,user):
        user_id = self.search_user_id_by_user(user)
        if user_id == -1:
            return 0
        else:
            return self.user_posting_dict[user_id]

    def __str__(self):
        print("User Dictionary: " + str(self.user_dict))
        print("User Posting Dictionary: " + str(self.user_posting_dict))
        return ""
