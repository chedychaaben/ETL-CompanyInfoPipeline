import re
import csv

#Readme
'''
General Description of this script's life cycle
1) We will get the path of the LIST text file and then try to open the path and store it's data to list_file
2) We will get the path of the MAPS text file and then try to open the path and store it's data to maps_file
3) Create a csv file and intialize it's header.
4) We will loop through every line of list_file whenever we find a line with one of these values "Pending\n","Hemp\n","Verified\n" OR "Ancillary\n"
    then we will do 2 things:
        1)Get what's of top of that line until we find an empty line , We will store all the info from the empty line to the status in the company name
            if there are two lines then we will store line 1 as company name  and line 2 as company name 2
        2) We will store all the info from the status to then first empty line we find in the Type
        NB: We are storing the values in a dict that will be stored the the list info_objects
5) We stored all the company name 1 to a list called company_names_main_from_list So then:
    1) We will loop through every line of the maps file and if we found that company name matches we will stop and add all the other data
        Inspect the script more to understand...
6) After Looping now we have a list called info_objects that is filled with all the dict instances And ready to export
7) We loop through info_objects and write to the csv rows.
8) Print the new csv file name.
'''
#Readme
# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ Getting Files from user ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
'''
try:
    list_file_path = input("Please Enter the List File path : ")
    list_file = open(list_file_path, "r",encoding="UTF-8")
except:
    raise('List file couldnt be open')

try:
    maps_file_path = input("Please Enter the Maps File path : ")
    maps_file = open(maps_file_path, "r",encoding="UTF-8")
except:
    raise('Maps file couldnt be open')
'''
# Dev (Comment this in production)
list_file = open("all-industry-list.txt", "r",encoding="UTF-8")
maps_file = open("all-industry-maps.txt", "r",encoding="UTF-8")
# Dev (Comment this in production)

# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ abbreviations_state ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
abbreviations_state = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NB": "Nebraska",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming"
}
abbreviations = list(abbreviations_state.keys())
states = list(abbreviations_state.values())

 
# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ Choosing csv file name and Writing the csv Header ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
csvname = f"{list_file.name} + {maps_file.name}.csv"

header_elements = ['Company Name','Company Name2', 'Email', 'Phone' , 'Status', 'DBA', 'License', 'Type','License Number', 'Adress']

with open(csvname, 'w', encoding="UTF-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header_elements)
    writer.writeheader()

# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ Settings ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

# Converting list file to a list of line called content_list_file
content_list_file = list_file.readlines()
#Setting status we will be searching for a line that has one of status values
status = ["Pending\n","Hemp\n","Verified\n","Ancillary\n"]

# Converting map file to a list of line called maps_content_file
maps_content_file = maps_file.readlines()

# Choosing how many lines up and how many lines down to look for (in the for loop below ) once we find a line that contains the value of status
lookup = 10
lookdown = 10

# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ List File Handeling ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

#Init the list where we will be storing data as dict elements
info_objects = [] 
#Init the lists where we will be storing the company names(The First Line above the statut) and secondary names(The Second Line above the statut if there is more than one)
company_names_main_from_list = []
company_names_secondary_from_list = []

#For each line content_list_file[i] in the content_list_file...
for i in range(len(content_list_file)):
    if content_list_file[i] in status : 
        lines_before = []
        lines_after = []

        #Getting data from where we find \n to this status line
        for l in range(1,lookup+1):
            if content_list_file[i-l] == '\n':
                break
            else:
                lines_before.append(content_list_file[i-l].strip().strip('\n'))

        #Getting data from this status line to just before the \n
        for l in range(1,lookdown+1):
            if content_list_file[i-l] == '\n':
                break
            else:
                lines_after.append(content_list_file[i+l].strip().strip('\n'))
        #Geting all after this lines data
        this_license_number_to_set = ""
        this_type_to_set = ""
        for line_after_this in lines_after:
            this_type_to_set += line_after_this
        ''' If you want the first line to be stored in the type and the second line to the lisence number
        if len(lines_after) > 0:
            if lines_after[0] == "Unknown":
                this_type_to_set = ""
            else:
                this_type_to_set = lines_after[0]

            if len(lines_after) > 1:
                if lines_after[1] != '':
                    this_license_number_to_set = lines_after[1]
        ''' 
        #Storing those data to company names 1 From List and company names 2 From List and also putting what's after lines to the brand new dict we r creating
        #No duplicates
        if len(lines_before) == 2:
            if lines_before[1] not in company_names_main_from_list:
                company_names_main_from_list.append(lines_before[1])
                info_objects.append(
                    {
                        'Company Name' : lines_before[1],
                        'Company Name2' : '',
                        'Email' : '',
                        'Phone' : '' ,
                        'Status' : content_list_file[i],
                        'DBA' : '',
                        'License' : '',
                        'Type' : this_type_to_set,
                        'License Number' : this_license_number_to_set,
                        'Adress' : ''
                    }
                )

            if lines_before[0] not in company_names_secondary_from_list:
                company_names_secondary_from_list.append(lines_before[0])
                info_objects[len(info_objects)-1]['Company Name2'] = lines_before[0]
    
        elif len(lines_before) == 1:
            if lines_before[0] not in company_names_main_from_list:
                company_names_main_from_list.append(lines_before[0])

                info_objects.append(
                    {
                        'Company Name' : lines_before[0],
                        'Company Name2' : '',
                        'Email' : '',
                        'Phone' : '' ,
                        'Status' : content_list_file[i],
                        'DBA' : '',
                        'License' : '',
                        'Type' : this_type_to_set,
                        'License Number' : this_license_number_to_set,
                        'Adress' : ''
                    }
                )
        
# Now taking care of after lines with another loop

        #Handeling lines after of the list file
         # OKAY The lines after Are : The first line is always the type and if there is second it will be lisence_number
        if len(lines_after) > 0:
            if lines_after[0] == "Unknown":
                info_objects[len(info_objects)-1]["Type"] = ""
            else:
                info_objects[len(info_objects)-1]["Type"] = lines_after[0]

            if len(lines_after) > 1:
                if lines_after[1] != '':
                    info_objects[len(info_objects)-1]["License Number"] = lines_after[1]

#Here We should see well structrude objects with ids
# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ Now we will see if We can find matches in Maps File ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
for i in range(len(maps_content_file)):
    if 'Open In Google Maps' in maps_content_file[i]:
        this_line = i+1
        # + ≡≡≡≡≡≡≡≡≡Before the open in maps (company name , adress, license) ≡≡≡≡≡≡≡≡≡≡
        lines_before = []
        #Getting data from where we find double \n \n to this Open In Google Maps line and storing it to lines_before
        for l in range(1,lookup+1):
            if maps_content_file[i-l] == '\n':
                break#if maps_content_file[i-l-1] == '\n':
                    #break
            else:
                lines_before.append(maps_content_file[i-l].strip())
        
        # If company main is in here for each in before lines  from the company main list
        # then remove it from the lines before
        for line in lines_before:
            this_line_counter = 0
            if line in company_names_main_from_list:
                this_line_counter += 1
                index = company_names_main_from_list.index(line)
                lines_before.remove(line)

                if len(lines_before) > 0 :
                    for other_line in reversed(lines_before) :
                        #If we find DBA in it then write it to the dba of the info object with this i
                        if 'DBA' in other_line.upper():
                            #IF THIS LINE NOT IN THE EMAIL THEN DON'T ADD IT
                            if other_line not in info_objects[index]['DBA']:
                                info_objects[index]['DBA'] += other_line.upper().split('DBA')[1]+ " "
                        # if number format the it might be lisence
                        elif re.match("(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|(\d{3})\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})",other_line):
                            #IF THIS LINE NOT IN THE EMAIL THEN DON'T ADD IT
                            if other_line not in info_objects[index]['License Number']:
                                info_objects[index]['License Number'] += other_line.upper().split('License Number')[1]+ " "
                        #Else put everything in the adress
                        else:
                            #IF THIS LINE NOT IN THE EMAIL THEN DON'T ADD IT
                            if other_line not in info_objects[index]['Adress']:
                                info_objects[index]['Adress'] += other_line + " "

                # + ≡≡≡≡≡≡≡≡≡ After the open in maps (phone and email) ≡≡≡≡≡≡≡≡≡≡
                lines_after = []
                #Getting data from this Open In Google Maps line to just before the lines × + -  Leaflet Lines
                for l in range(1,lookdown+1):
                    lines_after.append(maps_content_file[i+l].strip())
                # This Lines After Logic
                for line_after in lines_after:
                    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$)",line_after):
                        #IF THIS LINE NOT IN THE EMAIL THEN DON'T ADD IT
                        if line_after not in info_objects[index]['Email']:
                            info_objects[index]['Email'] += line_after.strip()  + " " 
                    elif re.match("(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|(\d{3})\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})",line_after):
                        #IF THIS LINE NOT IN THE PHONE THEN DON'T ADD IT
                        if line_after not in info_objects[index]['Phone']:
                            info_objects[index]['Phone'] +=  line_after.strip()  + " " 
                    else:
                        pass
                # This Lines After Logic


# + ≡≡≡ Replacing every cammas with a space and remove the \n so the csv dosen't mess up ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
for info_object in info_objects:
    for col in info_object:
        info_object[col] = info_object[col].replace(","," ").strip("\n")


# + ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ Putting info_objects data to the csv ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
with open(csvname, 'a',encoding="UTF-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header_elements)

    for info in info_objects:
        writer.writerow(info)

print(f"CSV file: {csvname}")