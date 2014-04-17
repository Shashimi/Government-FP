import requests
from pprint import pprint 
import json 
import govapp
import os 


# @param url string api url string 
# @return json 
def get_json(url):
    r = requests.get(url)
    r = json.loads(r.text)
    return r 

# @param l list list of url strings 
# @return list of get_json 

def api_calls(l):
    my_list = []
    for i in l:
        my_list.append(get_json(i))
    return my_list

api_list = ["http://openstates.org/api/v1//legislators/?state=nv&active=true&apikey=d2d67bda8f124cbdb77636a4305c1196",
"http://congress.api.sunlightfoundation.com/legislators?state=NV&apikey=d2d67bda8f124cbdb77636a4305c1196"]


r = api_calls(api_list)
# print r

# Loop through each json api response
for jsonobj in r:
    if type(jsonobj) == list:
        list_of_reps = jsonobj
    elif type(jsonobj) == dict:
        list_of_reps = jsonobj.get('results', [])
    else:
        print "Error, I don't know how to handle type: ", type(jsonobj)

    # Loop through each representative in the response, 
    #   creating a new Official object in the database if
    #   they do not already exist
    for representative in list_of_reps:
        #print "rep: %r" % representative

        # Email might be in the "email" key or the "+email" key
        email = representative.get("email", representative.get("+email", representative.get("contact_form",'')))
                
        title = representative.get("title","State Legislator")

        address = representative.get("office", representative.get("+address", representative.get("1234 Main Street #12 \nCarson City, NV 89701", '')))
        try:
            if "phone" in representative.keys():
                phone = representative["phone"]
            elif "offices" in representative.keys() and len(representative["offices"])> 0 and \
            "phone" in representative["offices"][0].keys():
                phone = representative["offices"][0]["phone"]
            else:
                phone = "775-684-6827"
        except Exception:
            pass
            # print representative


        if title == "Sen":
            rank = "3"
        elif title == "Rep":
            rank = "4"
        elif title == "State Legislator" and representative.get("chamber") == "upper":
            rank = "6"
        elif title == "State Legislator" and representative.get("chamber", 'lower') == "lower":
            rank = "7"
        else:
            continue

        # office = representative.get("offices", [])
        
        # # phone = representative.get("phone", representative["offices"][0].get("phone", "775-684-6827"))
        # if len(office):
        #   phone = office[0].get('phone', '775-684-6827')
        # else:
        #   phone = "775-684-6827"

        # phone = representative.get("phone", representative.get("office", representative.get("775-684-6827", '')))





        official = govapp.Official(
                            first_name=representative.get("first_name", ''),
                            last_name=representative.get("last_name",''),
                            state=representative.get("state", ''),
                            chamber=representative.get("chamber", ''),
                            title=representative.get("title", "State Legislator"),
                            party_affiliation=representative.get("party", ''),
                            email=email,
                            phone=phone,
                            address=address, 
                            facebook=None,
                            twitter=None,
                            rank=rank)
        govapp.session.add(official)


governor = govapp.Official(
                            first_name="Brian",
                            last_name="Sandoval",
                            state="NV",
                            chamber=None,
                            title="NV Governor",
                            party_affiliation="Republican",
                            email="gov.nv.gov/Contact/Governor",
                            phone="775-851-2014",
                            address="""State Capitol Building\n101 N. Carson Street\nCarson City, NV 89701""",
                            facebook="http://www.facebook.com/BrianSandoval", 
                            twitter="http://www.twitter.com/govsandoval",
                            rank="5")



president = govapp.Official(
                            first_name="Barack",
                            last_name="Obama",
                            state=None,
                            chamber=None,
                            title="President of the U.S.A",
                            party_affiliation="Democrat",
                            email="http://www.whitehouse.gov/contact/submit-questions-and-comments",
                            phone="202-456-1111", 
                            address="""The White House\n1600 Pennsylvania Avenue NW\nWashington, DC 20500""",
                            facebook="http://www.facebook.com/WhiteHouse",
                            twitter="http://www.twitter.com/BarackObama", 
                            rank="1")

vice_president  =   govapp.Official(
                            first_name="Joseph",
                            last_name="Biden",
                            state=None,
                            chamber=None,
                            title="Vice President of the U.S.A",
                            party_affiliation="Democrat",
                            email="mailto:vice.president@whitehouse.gov",
                            phone="202-456-1414",
                            address="""The White House\n1600 Pennsylvania Avenue NW\nWashington, DC 20500""",
                            facebook="http://www.facebook.com/joebiden",
                            twitter="http://www.twitter/VP",
                            rank="2")

govapp.session.add(governor)
govapp.session.add(president)
govapp.session.add(vice_president)
govapp.session.commit()

# print done with officials 

def get_officials():
    official_dict = {}
    db = govapp.session.query(govapp.Official).all()
    for official in db:
        official_dict[official.last_name] = official.id
    return official_dict

def find_json_files(path):
    l = []
    for item in os.listdir(path):
        if not os.path.isdir(path+'/'+item) and item[-5:] == ".json":
            #print path+'/'+item
            l.append(path+'/'+item)
        if (os.path.isdir(path+'/'+item)):
            l.extend(find_json_files(path+'/'+item))
    return l



def parse_bills_votes(l):
# instantiate the empty values in the list, l
    myl = {}
    myl['votes'] = []
    myl['bills'] = []

    for path in l:
        # add the path to either votes or bills based on which one appears  
        # in the path string
        if 'votes' in path:
            print "Adding " + path + " to votes"
            pathsplit = path.split('/')
            if not (pathsplit[3].startswith("hr") or pathsplit[3].startswith("s")):
                print "continuing because " + path + " doesn't begin with hr or s"
                continue
            if pathsplit[4] != "data.json":
                print "continuing because " + pathsplit[4] + " not data.json"
                continue 
            print "appending to myl"
            myl['votes'].append(path)
        
        if 'bills' in path:
            print "Adding " + path + " to bills"
            pathsplit = path.split('/')
            if pathsplit[2] != "hr" and pathsplit[2] != "s":
                continue
            if pathsplit[4] != "data.json":
                continue
            myl['bills'].append(path)

    # print ("in parse_bills_votes, myl is:")
    # print myl
    return myl


def load_bills(session, myl):
    # function to create bill objects to database
    all_officials = get_officials()
    counter = 0
    for bill in myl['bills']:
        counter += 1
        b = open(bill)
        bill_in_dict = json.load(b)

        if counter%20 == 0:
            print "Every 20th: " + bill     

        if bill_in_dict["sponsor"]:
            sponsorname = bill_in_dict["sponsor"]["name"]
        elif bill_in_dict["cosponsor"]:
            sponsorname = bill_in_dict["cosponsor"]["name"]
        else:
            continue

        sponsorLastName = sponsorname.split(',')
        sponsorLastName = sponsorLastName[0]

        if sponsorLastName in all_officials:
            official_id = all_officials[sponsorLastName]
        else:
            continue


        
        if bill_in_dict['short_title']:
            bill_name = bill_in_dict["short_title"]
        else:
            bill_name = bill_in_dict["official_title"]

        if bill_in_dict['summary'] and bill_in_dict["summary"]["text"]:
            bill_description = bill_in_dict['summary']['text']
        else:
            bill_description = ""       


        bill = govapp.Bill(name=bill_name,
                          description=bill_description,
                          official_id=official_id
                          )
        
        govapp.session.add(bill)
        govapp.session.commit()

def load_votes(session, myl):
    # function to create votes objects to database
    all_officials = get_officials()
    counter = 0
    # print "*** load_votes"
    # print "myl votes is "
    # print myl['votes']
    for vote in myl['votes']:
        counter += 1
        v = open(vote)
        vote_in_dict = json.load(v)

        # print "Parsing..."
        # print vote_in_dict

        if "Aye" in vote_in_dict["votes"]:
            yes_vote = "Aye"
        elif "Yea" in vote_in_dict["votes"]:
            yes_vote = "Yea"
        elif "Yes" in vote_in_dict["votes"]:
            yes_vote = "Yes"
        else:
            yes_vote = "None"
        if "Nay" in vote_in_dict["votes"]:
            no_vote = "Nay"
        elif "No" in vote_in_dict["votes"]:
            no_vote="No"
        else:
            no_vote = "None"

        vote_names = vote_in_dict["votes"][yes_vote] 
        vote_names2 = vote_in_dict["votes"][no_vote]
    
        # print "*** vote_names: " + str(vote_names)
        
        for vote_name in vote_names:
            #vote_official_name = vote_names[i]["display_name"] 
            vote_official_name = vote_name["last_name"]

            #AyeOfficialLastName = vote_official_name.split('')
            #AyeOfficialLastName = AyeOfficialLastName[0]
            AyeOfficialLastName = vote_official_name
            if AyeOfficialLastName in all_officials:
                official_id = all_officials[AyeOfficialLastName]
            else:
                continue 

            ayevote = govapp.Voting_Record( name=vote_official_name,
                                            outcome="aye", 
                                            official_id=official_id,
                                            question=vote_name.get("question", ''))
            govapp.session.add(ayevote)
            govapp.session.commit()
        

    
        for vote_name in vote_names2:
            vote_official_name = vote_name["last_name"]


            #NoOfficialLastName = vote_official_name.split('')
            #NoOfficialLastName = NoOfficialLastName[0]
            NoOfficialLastName = vote_official_name
            
            if NoOfficialLastName in all_officials:
                official_id = all_officials[NoOfficialLastName]
            else:
                continue

            novote = govapp.Voting_Record(  name=vote_official_name,
                                            outcome="no", 
                                            official_id=official_id,
                                            question=vote_name.get("question", ''))
                    
            # print "Adding this novote: "
            # print novote.name
            # print novote.official_id
            # exit

            govapp.session.add(novote)
            govapp.session.commit()

def main(session):
    parsed_votes = parse_bills_votes(find_json_files("112/votes"))
    load_votes(session, parsed_votes)

    parsed_bills = parse_bills_votes(find_json_files("112/bills"))
    load_bills(session, parsed_bills)

    parsed_votes = parse_bills_votes(find_json_files("113/votes"))
    load_votes(session, parsed_votes)

    parsed_bills = parse_bills_votes(find_json_files("113/bills"))
    load_bills(session, parsed_bills)



if __name__ == "__main__":
    main(govapp.session)
