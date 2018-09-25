# Overview

The Student Database Preparer App takes in raw enrolment data and prepares
it for uploading to the Student Database. It cleans the data and ensures that
it is compatible with the database.

## Inputs

The app takes in csv files containing raw data to be uploaded to the Student
Database.

## Outputs

The app outputs txt files that can be uploaded into the Student Database to
update the required tables.

## Version

Version Number 1.0  
Last updated 25 September 2018

# Operation

- Place the required, updated data files into the same directory as the app file
- Run the Student_Database_Preparer.py file from within Spyder or from the command
line
- Select the desired function from the menu
- Provide the names for any required files or press enter to open the Open file 
dialog.

# Functions

## Prepare Students Table Data

Prepares the upload file for updating the Students table in the Student Database.

### Required Files

- Combined Data File
- Course_Ids.csv
- Enrolment Data Sheet
- Student_IDs.csv

## Prepare Tutors Table

Prepares the upload file for updating the Tutors table in the Student Database.

### Required Files

- Tutor Data File
- Tutor_IDs.csv

## Prepare Courses Table Data

Prepares the upload file for updating the Courses table in the Student Database.

### Required Files

- Course_Ids.csv
- Courses Data File

## Prepare Workshops Table Data

Prepares the upload file for updating the Workshops table in the Student Database.

### Required Files

- Workshops Data File
- Workshops_IDs.csv

## Prepare Course Tutors Table Data

Prepares the upload file for updating the Course Tutors table in the Student Database.

### Required Files

- Course Tutors Data File
- Course_IDs.csv
- Course_Tutors.csv
- Tutor_IDs.csv

## Prepare Workshop Tutors Table Data

Prepares the upload file for updating the Workshop Tutors table in the Student Database.

### Required Files

- Tutor_IDs.csv
- Workshop_IDs.csv
- Workshop Tutors Data File
- Workshop_Tutors.csv

## Prepare Enrolments Table Data

Prepares the upload file for updating the Enrolments table in the Student Database.

### Required Files

- Course_Ids.csv
- Enrolment Data Sheet
- Student_IDs.csv
- Tutor_IDs.csv

## Prepare Course Attendance Table Data

Prepares the upload file for updating the Course Attendance table in the Student Database.

### Required Files

- Course Attendance Data File
- Course_IDs.csv
- Student_Course File
- dates.csv

## Prepare Workshop Attendance Table Data

Prepares the upload file for updating the Workshop Attendance table in the Student 
Database.

### Required Files

- Student-Workshop File
- Workshop Attendance Data File
- Workshop_IDs.csv

## Prepare Graduates Table Data

Prepares the upload file for updating the Graduates table in the Student 
Database.

### Required Files

- Enrolment_Codes.csv
- Graduate Data
- Graduates_Current.csv

## Prepare Extensions Table Data

Prepares the upload file for updating the Extensions table in the Student 
Database.

### Required Files

- Enrolment_Codes.csv
- Extension_Codes.csv
- Extensions Data

## Prepare ADV Course Assessment Table Data

Prepares the upload file for updating the ResultsADV table in the Student 
Database.

### Required Files

- Course Assessment Data File
- adv_assessments
- enrolment_ids.csv

# Files used

## Combined Data File

### Contents

State contents and structure of file

### Source

State how to source the file

# Dependencies

List the libraries that must be imported

# Development

## Known bugs

List any known issues

## Items to fix

List items requiring fixing

## Current development step

State the step currently being worked on

## Required development steps

List items that need to be done for current build

## Future additions

List items not currently being worked on but to be incorporated in future
