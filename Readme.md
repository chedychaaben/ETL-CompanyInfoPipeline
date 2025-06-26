File Processing Script
Overview
This Python script processes two text files, all-industry-list.txt and all-industry-maps.txt, to extract company information and generate a consolidated CSV file. It identifies specific statuses in the list file, matches company names with the maps file, and organizes the data into a structured CSV format with fields like Company for Name, headers Company such as Company Name, EmailName2, and Address`.
Features

Input Handling: Reads two text files (all-industry-list.txt and all-industry-maps.txt) encoded in UTF-8.
Data Extraction: Extracts company names (primary and secondary), status, type, and license number from the list file.
Data Matching: Matches company names with the maps file to gather additional details like address, email, and DBA (Doing Business As).
CSV Output: Generates a CSV file combining data from both files with headers: Company Name, CompanyName2, Email, Phone, Status, DBA, License, Type, License Number, Address.
State Abbreviations: Includes a dictionary mapping state abbreviations to full names for potential address formatting (not fully implemented in this script).
Data Cleaning: Removes commas and newlines to ensure CSV compatibility.

How It Works

File Reading: Opens and reads input files into lists of lines.
List File Processing List File:
Searches for lines with statuses (Pending, Hemp, Verified, Ancillary).
Captures up to two lines above the status as company names (primary and secondary`)).
Extracts lines below the status for type and license number information.
Stores data in a dictionary list (info_objects)).


Maps File Processing:
Identifies entries marked by "Open In Google Maps".
Matches company names from the list file.
Extracts preceding lines for address, DBA, or license number.
Extracts following lines for email or phone numbers using regex.
Appends matched data to corresponding info_objects entries.


CSV Generation:
Creates a CSV file with a name derived from input filenames (e.g., all-industry-list_all-industry-maps.csv)).
Writes headers and rows from info_objects.
Cleans data by replacing commas and removing newlines.


Output: Prints the generated CSV file name and closes input files.

Assumptions

Input files are well-structured with consistent patterns (e.g., company names above status, empty lines as separators).
Lines following "Open In Google Maps" contain valid emails or phone numbers.
The script processes only specified statuses and assumes UTF-8 encoding.

Limitations

Hardcoded file paths limit production flexibility.
No error handling for malformed inputs (e.g., missing files or invalid formats).
State abbreviation dictionary is included but unused.
Regex patterns for phone and email may miss some formats.
Assumes unique company names to avoid duplicates.

Usage

Place all-industry-list.txt and all-industry-maps.txt in the same directory as the script.
Run the script:python process_files.py


Check the generated CSV file (e.g., all-industry-list_all-industry-maps.csv) in the same directory.

Future Improvements

Add user input for file paths.
Enhance error handling for file access and data parsing.
Support more data formats (e.g., additional phone/email patterns).
Utilize state abbreviations for address standardization.
Add validation for duplicate handling or and data consistency.

Dependencies

Python 3.x
Standard libraries: re, csv

This script provides a foundation for processing structured text data into CSV, with opportunities for customization based on input variations.```