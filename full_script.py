import re
import csv

list_file = open("all-industry-list.txt", "r", encoding="UTF-8")
maps_file = open("all-industry-maps.txt", "r", encoding="UTF-8")

abbreviations_state = {
    "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DC": "District of Columbia", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "IA": "Iowa", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
    "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NB": "Nebraska", "NC": "North Carolina",
    "ND": "North Dakota", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NV": "Nevada", "NY": "New York", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
    "PA": "Pennsylvania", "PR": "Puerto Rico", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia",
    "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming"
}

csvname = f"{list_file.name.replace('.txt', '')}_{maps_file.name.replace('.txt', '')}.csv"
header_elements = ['Company Name', 'Company Name2', 'Email', 'Phone', 'Status', 'DBA', 'License', 'Type', 'License Number', 'Address']

with open(csvname, 'w', encoding="UTF-8", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header_elements)
    writer.writeheader()

content_list_file = list_file.readlines()
status = ["Pending\n", "Hemp\n", "Verified\n", "Ancillary\n"]
maps_content_file = maps_file.readlines()
lookup = 10
lookdown = 10

info_objects = []
company_names_main_from_list = []
company_names_secondary_from_list = []

for i in range(len(content_list_file)):
    if content_list_file[i] in status:
        lines_before = []
        lines_after = []

        for l in range(1, lookup + 1):
            if i - l < 0 or content_list_file[i - l] == '\n':
                break
            lines_before.append(content_list_file[i - l].strip())

        for l in range(1, lookdown + 1):
            if i + l >= len(content_list_file) or content_list_file[i + l] == '\n':
                break
            lines_after.append(content_list_file[i + l].strip())

        this_type_to_set = " ".join(lines_after) if lines_after else ""
        this_license_number_to_set = ""

        if len(lines_before) >= 1:
            company_name = lines_before[-1]
            company_name2 = lines_before[-2] if len(lines_before) >= 2 else ""

            if company_name not in company_names_main_from_list:
                company_names_main_from_list.append(company_name)
                info_objects.append({
                    'Company Name': company_name,
                    'Company Name2': company_name2,
                    'Email': '',
                    'Phone': '',
                    'Status': content_list_file[i].strip(),
                    'DBA': '',
                    'License': '',
                    'Type': this_type_to_set,
                    'License Number': this_license_number_to_set,
                    'Address': ''
                })

            if company_name2 and company_name2 not in company_names_secondary_from_list:
                company_names_secondary_from_list.append(company_name2)

        if len(lines_after) > 0:
            info_objects[-1]["Type"] = lines_after[0] if lines_after[0] != "Unknown" else ""
            if len(lines_after) > 1 and lines_after[1]:
                info_objects[-1]["License Number"] = lines_after[1]

for i in range(len(maps_content_file)):
    if 'Open In Google Maps' in maps_content_file[i]:
        lines_before = []
        for l in range(1, lookup + 1):
            if i - l < 0 or maps_content_file[i - l] == '\n':
                break
            lines_before.append(maps_content_file[i - l].strip())

        for line in lines_before[:]:
            if line in company_names_main_from_list:
                index = company_names_main_from_list.index(line)
                lines_before.remove(line)

                for other_line in reversed(lines_before):
                    if 'DBA' in other_line.upper():
                        if other_line not in info_objects[index]['DBA']:
                            info_objects[index]['DBA'] += other_line.upper().split('DBA')[1].strip() + " "
                    elif re.match(r"(\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{3}[-.\s]?\d{4})", other_line):
                        if other_line not in info_objects[index]['License Number']:
                            info_objects[index]['License Number'] += other_line + " "
                    else:
                        if other_line not in info_objects[index]['Address']:
                            info_objects[index]['Address'] += other_line + " "

                lines_after = []
                for l in range(1, lookdown + 1):
                    if i + l >= len(maps_content_file):
                        break
                    line = maps_content_file[i + l].strip()
                    if line:
                        lines_after.append(line)

                for line_after in lines_after:
                    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", line_after):
                        if line_after not in info_objects[index]['Email']:
                            info_objects[index]['Email'] += line_after + " "
                    elif re.match(r"(\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{3}[-.\s]?\d{4})", line_after):
                        if line_after not in info_objects[index]['Phone']:
                            info_objects[index]['Phone'] += line_after + " "

for info_object in info_objects:
    for col in info_object:
        info_object[col] = info_object[col].replace(",", " ").strip()

with open(csvname, 'a', encoding="UTF-8", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header_elements)
    for info in info_objects:
        writer.writerow(info)

print(f"CSV file generated: {csvname}")

list_file.close()
maps_file.close()