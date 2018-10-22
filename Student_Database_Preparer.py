# Access Data - Student Database
# Version 1.0 25 September 2018
# Created by Jeff Mitchell
# Takes in data files and prepares them for uploading into the
# Student Database


# Still to do:
# - Check Enrolment Sheet and make conform to 'Email and Mobile'
# - Remove warning for Course Code missing for ADV-ON-001

# Future additions:
# - Group warnings e.g. by student or warning type (e.g. mobile number)
# - Add progress status to long processes
# - Graduates certificates - strip and remove any spaces in code
# - Course attendance- take course code and use in save file rather than time


# To Fix:
# - Add loading and loaded statements to Extensions processing, Graduates
# - Additional comma at end of ADV processing needs removal if possible
# - Check if 0 being added to mobile numbers (works for phone numbers)

# Known issues:
# - Won't catch empty Student ID number (or any first row field) as does not
# - read it as a line
# - Process results - if file name changed, original file name saved
# - need to get updated file name somehow


import copy
import custtools.admintools as ad
import custtools.databasetools as db
import custtools.datetools as da
import custtools.filetools as ft
import sys


def check_ass_data(ass_data, number):
    """Return list of warnings for information in Assessments Data file.

    Checks the Assessments data has the correct number of entries for the
    course and that none of the entries are empty. If there are errors an error
    file is saved and the program to exit.

    Args:
        ass_data (list): A list of the names of each assessment in the course.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (adv_data):
        Name for each assessment.
    """
    errors = []
    warnings = ['\nAssessments Data Warnings:\n']
    # Make sure the correct number of assessments are present
    if len(ass_data[0]) != number:
        errors.append('The number of assessments should be {}. Instead, {} '
                      'assessments were found. Please make sure the correct '
                      'number of assessments are present. If they are, please '
                      'update the App with the correct number to check '
                      'for.'.format(number, len(ass_data[0])))
    for assessment in ass_data[0]:
        # Check Assessment item is not blank
        if assessment in (None, ''):
            errors.append('An assessment item is empty.')
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Assessments_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_ca(ca_data):
    """Return list of warnings for information in Course Attendance Data file.

    Checks the Course Attendance data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        ca_data (list): A list with the Course Attendance data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (ca_data):
        StudentFK, First Name, Last Name, Date1, Date2,...
    """
    errors = []
    warnings = ['\nCourse Attendance Data Warnings:\n']
    for student in ca_data:
        # Check Student ID is correct
        if len(student[0]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{}'.format(student[0]))
        # Check that each class has either a '0' or a '1' in it
        i = 3
        while i < len(student):
            if str(student[i]) not in ['0', '1']:
                errors.append('Invalid class data for Student ID {}.'.format(
                        student[0]))
            i += 1
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Course_Attendance_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_cc(course_codes):
    """Return list of warnings for information in Course IDs file.

    Checks the Course IDs data to see if the Course Date is present.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        course_codes (list): A list of course codes

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (course_codes):
        CoursePK, CourseDate
    """
    errors = []
    warnings = ['\nCourse Codes Warnings:\n']
    for course in course_codes:
        if course[1] in (None, ''):
            warnings.append('Course Date is missing for course code {}.'.format
                            (course[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Course Codes')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_cd(course_data):
    """Return list of warnings for information in Course Data file.

    Checks the Course data to see if the required information is present.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        course_data (list): A list of the data for each course.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (course_data):
        CoursePK, CourseName, Venue, Mode, Status.
    """
    errors = []
    allowed_status = [None, '', 'active', 'expired', 'on hold', 'cancelled',
                      'n/a']
    warnings = ['\nCourse Data Warnings:\n']
    for course in course_data:
        if course[1] in (None, ''):
            errors.append('Course Name is missing for course {}. Please '
                          'check and correct the file.'.format(course[0]))
        if course[2] in (None, '') and course[3].strip() not in ('Online'):
            warnings.append('Venue is missing for course {}'.format(
                    course[0]))
        if course[3] in (None, ''):
            warnings.append('Mode is missing for course {}'.format(
                    course[0]))
        if course[4].lower() not in (allowed_status):
            errors.append('Course Status is incorrect for course with the '
                          'Course ID {}'.format(course[0]))
        elif course[4] in (None, ''):
            warnings.append('Course Status is missing for course '
                            '{}'.format(course[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Course Data')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_cdf(combined_data):
    """Return list of warnings for information in CDF file.

    Checks the Combined Data Form for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        coumbined_data (list): A list with the data for each student.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (combined_data):
        Student ID, Preferred Method of Study, Part-time Class Schedules,
        Name (Prefix), Name (Given Name), Name (Middle), Name (Surname),
        Name (Suffix), Preferred Name (Prefix), Preferred Name (Given Name),
        Preferred Name (Middle), Preferred Name (Surname),
        Preferred Name (Suffix), Gender, Date of Birth, Guardian Name (Prefix),
        Guardian Name (Given Name), Guardian Name (Middle),
        Guardian Name (Surname), Guardian Name (Suffix),
        Guardian Identification, Please tick to confirm...,
        Telephone, Mobile, Email, Mobile, Email, Nationality, Ethnicity,
        Please identify:, Which country were you born in?, Iwi, Citizenship,
        If other, please explain:, Is English your first language?,
        What is your first language?, Address (Number/Unit),
        Address (Street Address), Address (Suburb), Address (City),
        Address (Postcode), Address (Country), Disability, Please explain:,
        Employment, Qualification, Year, National Student Number,
        Reason for Study, Please explain:, How did you hear about us?, 
        Please state:, Please tick to confirm..., Created By (User Id), 
        Entry Id, Entry Date, Source Url, Transaction Id, Payment Amount,
        Payment Date, Payment Status, Post Id, User Agent, User IP.
    """
    errors = []
    warnings = ['\nCombined Data Form Warnings:\n']
    for student in combined_data:
        if len(student[0]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{}'.format(student[0]))
        if student[1].strip() not in ('Online', 'Part-time class'):
            errors.append('Preferred method of study missing for student '
                          '{}'.format(student[0]))
        if student[4] in (None, ''):
            errors.append('First name missing for student {}'.format(
                    student[0]))
        if student[6] in (None, ''):
            errors.append('Last name missing for student {}'.format(
                    student[0]))
        if student[13].strip() not in ('Male', 'Female'):
            warnings.append('Gender is missing for student {}'.format(
                    student[0]))
        # Check Birth Date is valid
        if not da.validate_date(student[14].strip()):
            errors.append('Date of birth is not valid for student '
                          '{}'.format(student[0]))
        if not ad.check_lead_zero(student[22].strip()):
            warnings.append('Telephone is missing a leading 0 for student '
                            '{}. A 0 will be added to the start of their '
                            'telephone number.'.format(student[0]))
        if not ad.check_lead_zero(student[23].strip()):
            warnings.append('Mobile is missing a leading 0 for student '
                            '{}. A 0 will be added to the start of their '
                            'mobile number.'.format(student[0]))
        # Check email address is present and in valid format
        if student[24] in (None, ''):
            errors.append('Email missing for student {}'.format(student[0]))
        elif not ad.check_email(student[24]):
            errors.append('Email format is not valid for student '
                          '{}'.format(student[0]))
        # Check if post code is four digitd (if NZ)
        code = db.check_post_code(student[40].strip(), student[41].strip())
        if code == 'Short':
            warnings.append('Post code is missing a leading 0 for student '
                            '{}. A 0 will be added to the start of their '
                            'post code.'.format(student[0]))
        elif code == 'Fail':
            warnings.append('Post code is incorrect for student '
                            '{}'.format(student[0]))
        elif code == 'Missing':
            warnings.append('Post code is missing for student '
                            '{}'.format(student[0]))
        if student[52] in (None, ''):
            errors.append('Terms and Conditions missing for student '
                          '{}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Combined_Data_Form')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_ctd(source_tutor_data, source, source_type):
    """Check for errors in the Workshop or Course-Tutor data file.

    Checks the Workshop or Course-Tutor data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.

    Args:
        source_tutor_data (list): A list with the data to be checked.
        source (str): The source of the data to be checked
        source_type (str): What the data is checking, e.g. Course or Workshop

    Returns:
        False if there are no errors.
        warnings (list): Warnings that have been identified in the data.

    File structure:
        CourseFK, Tutor Name, TutorFK.
    """
    errors = []
    warnings = []
    for tutor in source_tutor_data:
        if tutor[1] in (None, ''):
            warnings.append('Tutor name is missing for {} Code {}. '
                          'Please check and correct the file.'.format(
                                  source_type, tutor[0]))
        if tutor[2] in (None, ''):
            errors.append('Tutor Code is missing for {} Code {}. '
                          'Please check and correct the file.'.format(
                                  source_type, tutor[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)
    return False, warnings


def check_da(da_data):
    """Return list of warnings for information in Course Attendance Dates file.

    Checks the Course Attendance Dates data for the required information.
    Required information that is missing causes an error file to be saved and
    the program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        da_data (list): A list with the Course Attendance Dates data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (da_data):
        date 1, date 2, ...
    """
    errors = []
    warnings = ['\Course Attendance Dates Data Warnings:\n']
    i = 0
    while i < len(da_data[0]):
        # Check that each item is a valid date
        if not da.validate_date(da_data[0][i]):
            errors.append('Incorrect Date found:{}.'.format(da_data[0][i]))
        i += 1
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Course_Attendance_Dates_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_ec(ec_data):
    """Return list of warnings for information in Enrolment Codes Data file.

    Checks the Enrolment Codes data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        ec_data (list): A list with the Enrolment Codes data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (ec_data):
        EnrolmentPK, StudentFK.
    """
    errors = []
    warnings = ['\Enrolment Codes Data Warnings:\n']
    for code in ec_data:
        # Check that there is Student ID Number
        if code[1] in (None, ''):
            errors.append('Student ID Number missing for EnrolmentPK '
                          '{}.'.format(code[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Enrolment_Codes_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_e_id_data(e_id_data):
    """Return list of warnings for information in Enrolment Details data file.

    Checks the Enrolment Details data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        e_id_data (list): A list with the data for each student.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (e_id_data):
        EnrolmentPK, StudentPK, NameGiven, NameSurname, CoursePK, Status,
        Tutor.
        
    File source (e_id_data):
        qryEnrolmentDetailsAll from the Student Database.
    """
    errors = []
    warnings = ['\nEnrolment Details Warnings:\n']
    for student in e_id_data:
        # Check Student ID is valid length
        if len(student[1]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{} {}.'.format(student[2], student[3]))
        if student[2] in (None, ''):
            warnings.append('First name missing for student {}.'.format(
                    student[1]))
        if student[3] in (None, ''):
            warnings.append('Last name missing for student {}.'.format(
                    student[1]))
        if student[4] in (None, ''):
            errors.append('Course Code missing for student {}'.format(
                    student[1]))
        if student[5] in (None, ''):
            warnings.append('Course status missing for student {}'.format(
                    student[1]))
        if student[6].strip() in (None, ''):
            warnings.append('Tutor missing for student {}.'.format(student[1]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Enrolment_Sheet')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_es(es_data):
    """Return list of warnings for information in Enrolment Sheet file.

    Checks the Enrolment Sheet data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        es_data (list): A list with the data for each student.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (es_data):
        Student ID, First Name, Last Name, Preferred Name,
        Mobile, Email, Preferred Contact Mode, Course, Date Enrolled,
        Start Date, End Date, Tutor, Tutor contact, Username, Status, Tag
        Enrolment Code, National Student Number.
    """
    errors = []
    warnings = ['\nEnrolment Sheet Warnings:\n']
    for student in es_data:
        # Check Student ID is valid length
        if len(student[0]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{} {}.'.format(student[1], student[2]))
        if student[1] in (None, ''):
            warnings.append('First name missing for student {}.'.format(
                    student[0]))
        if student[2] in (None, ''):
            warnings.append('Last name missing for student {}.'.format(
                    student[0]))
        if not ad.check_lead_zero(student[4].strip()):
            warnings.append('Mobile is missing a leading 0 for student {}'
                            '. A 0 will be added to the start of their '
                            'mobile number.'.format(student[0]))
        # Check email address is present and in valid format
        if student[5] in (None, ''):
            errors.append('Email missing for student {}'.format(student[0]))
        elif not ad.check_email(student[5]):
            errors.append('Email format is not valid for student '
                          '{}'.format(student[0]))
        if student[7] in (None, ''):
            errors.append('Course code missing for student '
                          '{}'.format(student[0]))
        if not da.validate_date(student[8].strip()):
            errors.append('Enrolment date is not valid for student '
                          '{}'.format(student[0]))
        if student[9].strip() in (None, ''):
            warnings.append('Start date missing for student {}.'.format(
                    student[0]))
        elif not da.validate_date(student[9].strip()):
            errors.append('Start date is not valid for student {}.'.format(
                    student[0]))
        if student[10].strip() in (None, ''):
            warnings.append('End date missing for student {}'.format(
                    student[0]))
        elif not da.validate_date(student[10].strip()):
            errors.append('End date is not valid for student {}.'.format(
                    student[0]))
        if student[11] in (None, ''):
            warnings.append('Tutor is missing for student {}.'.format(
                    student[0]))
        # Check username is present and valid
        if student[13].strip() in (None, ''):
            warnings.append('Username is missing for student {}.'.format(
                    student[0]))
        elif not db.check_username(student[13]):
            errors.append('Username is not valid for student {}. Please '
                          'make sure it contains lower-case letters only '
                          'and no digits or special characters.'.format(
                                  student[0]))
        if not check_status(student[14].strip()):
            errors.append('Status is not valid for student {}.'.format(
                    student[0]))
        if not check_tag(student[15].strip()):
            errors.append('Tag is not valid for student {}.'.format(
                    student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Enrolment_Sheet')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_ex(ext_data):
    """Return list of warnings for information in Extensions Data file.

    Checks the Extensions data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        ext_data (list): A list with the extensions data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (ext_data):
        Student ID Number, Name, Enrolment Code, Extension Length, Acceptance
        Date, New Expiry Date.
    """
    errors = []
    warnings = ['\nExtensions Data Warnings:\n']
    for student in ext_data:
        # Check StudentID is correct format
        if len(student[0]) != 9:
            errors.append('StudentID is incorrect format for Enrolment '
                          'Code {}. Please check and correct the '
                          'file.'.format(student[2]))
        # Check that Enrolment Code is present and is a number
        if not ad.check_is_int(student[2] ):
            errors.append('Enrolment code is not a valid number for '
                          'StudentID {}'.format(student[0]))
        # Check that Extension Length is present and is a number
        if not ad.check_is_int(student[3] ):
            errors.append('Extension Length is not a valid number for '
                          'StudentID {}'.format(student[0]))
        # Check that the Acceptance Date is in a valid format
        if not da.validate_date(student[4].strip()):
            errors.append('Acceptance date is not valid for student '
                          '{}.'.format(student[0]))
        # Check that the New Expiry Date is in a valid format
        if not da.validate_date(student[5].strip()):
            errors.append('New Expiry Date is not valid for student '
                          '{}.'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Extensions_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_exc(exc_data):
    """Return list of warnings for information in Extension Codes Data file.

    Checks the Extension Codes data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        exc_data (list): A list with the extension codes data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (ext_data):
        EnrolmentFK, AcceptanceDate.
    """
    errors = []
    warnings = ['\nExtension Codes Data Warnings:\n']
    for code in exc_data:
        # Check EnrolmentFK is present and a number
        if not ad.check_is_int(code[0] ):
            errors.append('Enrolment code is not a valid number for '
                          'Acceptance Date {}.'.format(code[1]))
        # Check that Acceptance Date is present and is a valid date
        if not da.validate_date(code[1].strip()):
            errors.append('Acceptance date is not valid for Enrolment ID '
                          '{}.'.format(code[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Extension_Codes_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_gc(gc_data):
    """Return list of warnings for information in Graduates Current Data file.

    Checks the Graduates Current data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        gc_data (list): A list with the graduates current data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (gc_data):
        GraduatePK, EnrolmentFK.
    """
    errors = []
    warnings = ['\nGraduates Current Data Warnings:\n']
    for student in gc_data:
        # Check that Enrolment Code is present and is a number
        if not ad.check_is_int(student[1] ):
            errors.append('Enrolment code is not a valid number for '
                          'GraduatePK  {}.'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Graduates_Current_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_gd(gd_data):
    """Return list of warnings for information in Graduate Data file.

    Checks the Graduate data for the required information. Required information
    that is missing causes an error file to be saved and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        gd_data (list): A list with the graduation data for each student.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (gd_data):
        Student ID Number, Name, Enrolment Code, Graduation Date,
        Certificate Number.
    """
    errors = []
    warnings = ['\nGraduate Data Warnings:\n']
    for student in gd_data:
        # Check Student ID is valid length
        if len(student[0]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{}'.format((student[0])))
        # Check that there is an Enrolment Code
        if not ad.check_is_int(student[2]):
            errors.append('Enrolment code is not a valid number for '
                          'Student ID {}'.format(student[0]))
        # Check that Graduation Date is in a valid format
        if not da.validate_date(student[3].strip()):
            errors.append('Graduation date is not valid for Student ID {}'
                          .format(student[0]))
        # Check that the Certificate Number is present
        if student[4] in (None, ''):
            errors.append('Certificate number is missing for Student ID {}'
                          .format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Graduate_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings            
            

def check_os(os_data):
    """Return list of warnings for info in old students csv file.

    Checks the Old Students list data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        os_data (list): A list with the old student data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (os_data):
        StudentPK, NameGiven, NameSurname, NamePreferred, DateOfBirth,
        Username, Telephone, Mobile, Email, PreferredContactMode,
        AddressNumber, AddressStreet, AddressSuburb, AddressCity,
        AddressPostcode, AddressCountry, Nationality, Iwi, Citizenship,
        GuardianNameGiven, GuardianNameSurname, GuardianId, Under18Auth,
        HowHeard, AgreeTandC, EnrolmentDate, Gender, Ethnicity, CountryOfBirth,
        Language, Disability, PreviousEducation, PreviousEdYear, Employment,
        ReasonForStudy.
    """
    # print('check os_data:')
    # ad.debug_list(os_data)
    errors = []
    warnings = ['\nOld Student File Warnings:\n']
    for student in os_data:
        if len(student[0].strip()) != 9:
            errors.append('Student ID number is not the required length '
                          'for student in position {} {}.'.format(
                                  student[1], student[2]))
        if student[1] in (None, ''):
            warnings.append('First Name for student with Student ID Number {}'
                            ' is missing.'.format(student[0]))
        if student[2] in (None, ''):
            warnings.append('Last name missing for student {}'.format(
                    student[0]))
        # Check Date of Birth in correct format
        if student[4].strip() in (None, ''):
                warnings.append('Date of birth date missing for student '
                                '{}.'.format(student[0]))
        elif not da.validate_date(student[4].strip()):
            errors.append('Date of birth date is not valid for student '
                          '{}.'.format(student[0]))
        # Check username is present and valid
        if student[5].strip() in (None, ''):
            warnings.append('Username is missing for student {}.'.format(
                    student[0]))
        elif not db.check_username(student[5]):
            errors.append('Username is not valid for student {}. Please make '
                          'sure it contains lower-case letters only and no '
                          'digits or special characters.'.format(student[0]))
        # Check mobile number has leading 0
        if not ad.check_lead_zero(student[7].strip()):
            warnings.append('Mobile is missing a leading 0 for student {}. '
                            'A 0 will be added to the start of their mobile '
                            'number.'.format(student[0]))
        # Check email address is present and in valid format
        if student[8] in (None, ''):
            warnings.append('Email missing for student {}.'.format(student[0]))
        elif not ad.check_email(student[8]):
            errors.append('Email format is not valid for student {}.'.format(
                    student[0]))
        # Check Enrolment Date in correct format
        if student[25].strip() in (None, ''):
                warnings.append('Enrolment Date missing for student '
                                '{}.'.format(student[0]))
        elif not da.validate_date(student[25].strip()):
            errors.append('Enrolment Date is not valid for student '
                          '{}.'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Old_Students_Data')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_present(database_ids, source_data, a_id_pos, b_id_pos, source,
                  id_type):
    """Check that an identifier is present before it is used.

    If an identifier is missing from database an error file is saved and the
    program exits.

    Args:
        database_ids (list): List of identifiers present in the database.
        source_data (list): List of data to be checked.
        a_id_pos (int): Position of identifier in the list of ids in database.
        b_id_pos (int): Position of identifier in the data list being checked.
        id_type (str): Type of identifier (singular). e.g. Course code.

    File structure (database_ids):
        Course Code, Course Name.

    File structure (source_data):
        Course Code, Course Name.
    """
    errors = []
    ids = []
    # Separate identifiers into a list
    for identifier in database_ids:
        a = identifier[a_id_pos].strip()
        ids.append(a)
    # print('Contents of ids: ')
    # ad.debug_list(ids)
    # Check if provided code is in the list of Course codes
    for item in source_data:
        if item[b_id_pos].strip() in ids or item[b_id_pos].strip() in (None,
                                                                       ''):
            continue
        else:
            errors.append('{} {} not found in the list of {}s. Please check '
                          'the list of {}s.'.format(id_type,
                                       item[b_id_pos].strip(), id_type,
                                       id_type))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)


def check_scc(scc_data):
    """Return list of warnings for information in Student Course Codes file.

    Checks the Student Course Codes data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        scc_data (list): A list with the Student Course Codes data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (scc_data):
        StudentFK, CourseFK.
    """
    errors = []
    
    warnings = ['\Student Course Codes Data Warnings:\n']
    for student in scc_data:
        # Check that there is Student ID Number
        if student[1] in (None, ''):
            errors.append('Course ID Number missing for Student ID {}.'
                          .format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Student_Course_Codes_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_si(si_data):
    """Return list of warnings for information in Student IDs file.

    Checks that the Student ID number is the required length (9).
    If a Student ID number length is incorrect an error file is saved and the
    program exits.

    Args:
        si_data (list): List of Student ID numbers.

    Returns:
        False if there are no errors.
        warnings (list): Warnings that have been identified in the data.

    File structure (si_data:
        Student ID Number, First Name, Last Name.
    """
    errors = []
    warnings = ['\nStudent ID Numbers Warnings:\n']
    for student in si_data:
        if len(student[0].strip()) != 9:
            errors.append('Student ID number is not the required length '
                          'for student {} {}.'.format(student[1], student[2]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Student_ID_Numbers')
    return False, warnings


def check_source_tutor_unique(source_data, pairings, source):
    """Check pairing is not already in the database.

    Checks that each pairing is unique (not already in the database).
    If pairings are found to already be in the database an error log is saved
    and the program exits.

    Args:
        source_data (list): The source data that is to be checked.
        pairings (list): The list of pairings in the database currently.
        source (str): The source that source_data comes from.

    File structure (source_data):
        CourseFK, TutorFK.

    File structure (pairings):
        CourseFK, TutorFK.
    """
    errors = []
    for pair in pairings:
        for source_pair in source_data:
            if pair == source_pair:
                errors.append('The pairing {} is already in the database. '
                              'Please correct file.'.format(pair))
                break
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)


def check_status(status):
    """Return True if status is in allowed values.

    Checks the status of student's enrolment against the list of allowed
    values.

    Args:
        status (str): Status for student from the data source.

    Returns:
        True if status is in the allowed values, False otherwise.
    """
    allowed = ['Active', 'Suspended', 'Withdrawn', 'Graduated',
               'Expired', 'On Hold', 'Cancelled']
    if status.strip() in allowed:
        return True
    else:
        return False


def check_swc(swc_data):
    """Return list of warnings for information in Student Workshop Codes file.

    Checks the Student Workshop Codes data for the required information.
    Required information that is missing causes an error file to be saved and
    the program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        scc_data (list): A list with the Student Workshop Codes data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (swc_data):
        StudentFK, WorkshopFK.
    """
    errors = []
    warnings = ['\Student Workshop Codes Data Warnings:\n']
    for student in swc_data:
        # Check that there is Student ID Number
        if student[1] in (None, ''):
            errors.append('Workshop ID Number missing for Student ID {}.'
                          .format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Student_Workshop_Codes_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_tag(tag):
    """Return True if tag is in allowed values.
    
    Checks that the student's tag is in the list of allowed values.
    
    Args:
        tag (str): Tag for student from the data source.
    
    Returns:
        True if tag is in the allowed values, False otherwise.
    """
    allowed = [None, '', 'N/A', 'Green', 'Orange', 'Red', 'Purple', 'Black',
               'Expired', 'Withdrawn', 'Graduated', 'Suspended', 'On Hold',
               'Cancelled']
    if tag.strip() in allowed:
        return True
    else:
        return False


def check_td(td_data):
    """Return list of warnings for information in Tutor Data file.

    Checks the Tutor data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        td_data (list): A list with the data for each tutor.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (td_data):
        TutorID, First Name, Last Name, Email, Phone.
    """
    errors = []
    warnings = ['\nTutor Data File Warnings']
    for tutor in td_data:
        if len(tutor[0].strip()) != 6:
            errors.append('Tutor ID number is not the required length '
                          'for tutor {} {}.'.format(tutor[1], tutor[2]))
        if tutor[1] in (None, ''):
            errors.append('First Name for tutor with Tutor ID Number {} '
                          'is missing.'.format(tutor[0]))
        if tutor[2] in (None, ''):
            errors.append('Last Name for tutor with Tutor ID Number {} '
                          'is missing.'.format(tutor[0]))
        # Check email address is present and in valid format
        if tutor[3] in (None, ''):
            warnings.append('Email for tutor with Tutor ID Number {} '
                          'is missing.'.format(tutor[0]))
        elif not ad.check_email(tutor[3]):
            errors.append('Email format is not valid for tutor with Tutor '
                          'ID Number {}.'.format(tutor[0]))
        if tutor[4] in (None, ''):
            warnings.append('Phone number for tutor with Tutor ID Number {} '
                          'is missing.'.format(tutor[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Tutor_Data_File')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_tu(tu_data):
    """Return list of warnings for information in Tutor_IDs.csv file.

    Checks the Tutor ID list data for the required information.
    Required information that is missing causes an error file to be saved
    and the program to exit.
    Missing or incorrect information that is non-fatal is appended to a
    warnings list and returned.

    Args:
        tu_data (list): A list with the ID number and name for each tutor.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (tu_data):
        TutorID, First Name, Last Name.
    """
    errors = []
    warnings = ['\nTutor File Warnings:\n']
    for tutor in tu_data:
        if len(tutor[0].strip()) != 6:
            errors.append('Tutor ID number is not the required length '
                          'for tutor {} {}.'.format(tutor[1], tutor[2]))
        if tutor[1] in (None, ''):
            errors.append('First Name for tutor with Tutor ID Number {} '
                          'is missing.'.format(tutor[0]))
        if tutor[2] in (None, ''):
            errors.append('Last Name for tutor with Tutor ID Number {} '
                          'is missing.'.format(tutor[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Tutor_ID_Numbers')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_unique(database_ids, source_data, a_id_pos, b_id_pos, source,
                 id_type):
    """Check an identifier is not already in the database before it is used.

    Required information that is missing causes an error file to be saved
    and the program to exit.

    Args:
        database_ids (list): List of identifiers present in the database.
        source_data (list): List of identifiers to be checked.
        a_id_pos (int): Position of identifier in the list of ids in database.
        b_id_pos (int): Position of identifier in the data list being checked.
        source (str): Source of data that is being checked.
        id_type (str): Type of identifier (singular). e.g. Course code

    File structure (database_ids):
        Course Code, Course Name.

    File structure (source_data):
        Course Code, Course Name.
    """
    errors = []
    ids = []
    # Separate identifiers into a list
    for identifier in database_ids:
        a = identifier[a_id_pos].strip()
        ids.append(a)
    # Check if provided identifier is in the list of identifiers in database
    for item in source_data:
        if item[b_id_pos].strip() in ids:
            errors.append('{} {} already appears in the list of {}s. Please '
                          'check the list of {}s.'.format(
                                  id_type, item[b_id_pos].strip(), id_type,
                                  id_type))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)


def check_unique_extension(existing, to_check, ex_ec_pos, ex_ad_pos, ch_ec_pos,
                           ch_ad_pos):
    """Check that an Enrolment Code - Acceptance Date combination is unique.
    
    Checks that the combination of Enrolment Code and Acceptance Date are not
    contained in the Extension Codes list. If they are already there, this
    indicates that the extension has alerady been added to the Student
    Database and therefore must be removed.
    
    Args:
        existing (list): The list of pairings currently in the database.
        to_check (list): The list of pairings to be checked (in the submitted
                         data).
        ex_ec_pos (int): Position of Enrolment Code in Extension Codes data.
        ex_ad_pos (int): Position of Acceptance Date in Extension Codes data.
        ch_ec_pos (int): Position of Enrolment Code in data to be checked.
        ch_ad_pos (int): Position of Acceptance Date in data to be checked.
    
    File structure (existing):
        EnrolmentFK, AcceptanceDate.

    File structure (to_check):
        Student ID Number, Enrolment Code, Extension Length, Acceptance Date, 
        New Expiry Date.        
    """
    errors = []
    i = 0
    # Check each pair in to_check data
    while i < len(to_check):
        # Extract Enrolment Code from to_check
        tc_ec = to_check[i][ch_ec_pos]
        # Extract Acceptance Date from to_check
        tc_ad = to_check[i][ch_ad_pos]
        # Look for Enrolment Code in existing data
        j = 0
        found = False
        while j < len(existing) and not found:
            # Extract Enrolment Code from existing
            ex_ec = existing[j][ex_ec_pos]
            # Extract Acceptance Date from existing
            ex_ad = existing[j][ex_ad_pos]
            if ex_ec == tc_ec:
                # Enrolment code is found in existing data
                # Check if Acceptance Dates also match
                if ex_ad == tc_ad:
                    # Acceptance Date also matches - duplicate
                    found = True
                    errors.append('The combination of Enrolment Code {} and '
                                  'Acceptance Date {} already exists in the '
                                  'Student Database. Please correct the data '
                                  'and try again.'.format(tc_ec, tc_ad))
            # Combination not found, try the next row in existing data
            j += 1
        # Check the next row in the data to be checked
        i += 1
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Extensions_Data')


def check_valid_course(course_codes, course, a_id_pos, source):
    """Check that course code is a valid course code.

    If the supplied code does not appear in the list of valid course codes, an
    error file is saved and the program exits.

    Args:
        course_codes (list): List of valid courses.
        course (str): The course to be checked.
        a_id_pos (int): Position of course code in the list of course codes.
        source (str): Source of data that is being checked.
        
    File structure (database_ids):
        Course Code, Course Name.
    """
    errors = []
    ids = []
    # Separate identifiers into a list
    for identifier in course_codes:
        a = identifier[a_id_pos].strip()
        ids.append(a)
    # print('Contents of ids: ')
    # ad.debug_list(ids)
    # Check if provided code is in the list of Course codes
    if course.strip() not in ids and course.strip() not in (None, ''):
        errors.append('Course code {} not found in the list of Course codes. '
                      'Please check the list of Course codes.'.format(
                              course.strip()))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)


def check_valid_scc(sup_data, scc_data, course, s_sfk_pos, source):
    """Check that the Student ID and Course ID combination is valid.
    
    Checks that each Student ID and Course ID combination in the
    supplied data file is a valid student enrolment. If the combination
    cannot be found, it is added to the warnings list.
    
    Args:
        sup_data (list): Data that needs to be checked.
        scc_data (list): Data from the Student Course Codes Data file.
        course (str): Course Code for course being updated.
        s_sfk_pos (int): Position of the StudentID in the supplied data.
        source (str): File source for data to be checked.
        
    File structure (Course Attendance Data file (sup_data_)):
        Student ID Number, First Name, Last Name, Date 1, Date 2...
        
    File structure (Student Course Codes file (scc_data)):
        Student ID Number, Course Code.
    
    File Source (scc_data):
        StudentFK and CourseFK columns from Enrolments Table in Student
        Database.
    """
    i = 0
    warnings = ['\nStudent Course Codes Warnings:\n']
    # Work through each student in sup_data
    while i < len(sup_data):
        # Extract a single student
        student = extract_student_2(sup_data, i)
        # print(student)
        j = 0
        matched = False
        # Check if Student ID Numbers match
        while j < len(scc_data) and not matched:
            # Extract a StudentID - Course Code combination
            student_codes = extract_student_2(scc_data, j)
            # Check if Student ID Numbers match
            if student[s_sfk_pos] == student_codes[0]:
                # Check if Course Codes also match
                if course == student_codes[1]:
                    matched = True
                    # If do not match, continue looking for Student ID
                    # Relevant if Student has enrolled in more than one course
            j += 1
        # Create error if not matched
        if not matched:
            warnings.append('{} could not be found with the course code {} '
                          'in the list of existing course codes. Please '
                          'check the file and try again.'.format(
                                  student[s_sfk_pos], course))
        i += 1
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_valid_stud(sup_data, ec_data, s_epk_pos, s_sfk_pos, source):
    """Check that the Student ID and Enrolment Code combination is valid.
    
    Checks that each Student ID and Enrolment Code combination in the
    supplied data file is a valid student enrolment. If the combination
    cannot be found, it is added to the errors list and the system exits.
    
    Args:
        sup_data (list): Data that needs to be checked.
        ec_data (list): Data from the Enrolment Codes Data file.
        s_epk_pos (int): Position of the EnrolmentFK in the supplied data.
        s_sfk_pos (int): Position of the StudentID in the supplied data.
        source (str): File source for data to be checked.
        
    File structure (graduate file):
        Student ID Number, Enrolment Code, Graduation Date, Certificate Number.
        
    File structure (extensions file):
        Student ID Number, Enrolment Code, Extension Length, Acceptance Date, 
        New Expiry Date.
    
    File structure (ec_data):
        EnrolmentPK, StudentFK.
    """
    i = 0
    errors = []
    # Work through each student in gd_data
    while i < len(sup_data):
        # Extract a single student
        student = extract_student_2(sup_data, i)
        # print(student)
        j = 0
        matched = False
        # Check if Student ID Numbers match
        while j < len(ec_data) and not matched:
            # Extract an Enrolment Code combination
            student_codes = extract_student_2(ec_data, j)
            # Check if Student ID Numbers match
            if student[s_sfk_pos] == student_codes[1]:
                # Check if Enrolment Codes also match
                if student[s_epk_pos] == student_codes[0]:
                    matched = True
                    # If do not match, continue looking for Student ID
                    # Applicable if Student has graduated more than one course
            j += 1
        # Create error if not matched
        if not matched:
            errors.append('{} could not be found with the enrolment code {} '
                          'in the list of existing enrolment codes. Please '
                          'check the file and try again.'.format(
                                  student[s_sfk_pos], student[s_epk_pos]))
        i += 1
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)        


def check_wa(wa_data):
    """Return list of warnings for Workshop Attendance Data file.

    Checks the Workshop Attendance data for the required information. Required 
    information that is missing causes an error file to be saved and the 
    program to exit. Missing or incorrect information that is non-fatal is 
    appended to a warnings list and returned.

    Args:
        wa_data (list): A list with the Workshop Attendance data.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (wa_data):
        WorkshopFK, StudentFK, First Name, Last Name.
    """
    errors = []
    warnings = ['\nWorkshop Attendance Data Warnings:\n']
    for student in wa_data:
        # Check Student ID is correct
        if student[1] in (None, ''):
            errors.append('Student ID Number is missing for an entry')
        elif len(student[1]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{}'.format(student[1]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Workshop_Attendance_Data')
    # Check if any warnings have been identified, return if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_wc(workshop_codes):
    """Check that the workshop name is present in the workshop codes file.

    Args:
        workshop_codes (list): A list with the ID number and name for each
        workshop.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (workshop_codes):
        Woekshop Code, Workshop Name.
    """
    warnings = ['\nWorkshop Codes Warnings:\n']
    for workshop in workshop_codes:
        if workshop[1] in (None, ''):
            warnings.append('Workshop name is missing for workshop code '
                            '{}.'.format(workshop[0]))
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_wd(workshop_data):
    """Check that data is correct in the workshop data file.

    Args:
        workshop_data (list): A list with the data for each workshop.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (workshop_data):
        Workshop Code, Workshop Name, Location, Venue, Date, Cost, Status,
        Type.
    """
    errors = []
    allowed_status = ["Active","Completed","On Hold","Cancelled","N/A"]
    allowed_type = ["Assessment","Compulsory","Non Compulsory","N/A"]
    warnings = ['\nWorkshop Data Warnings:\n']
    for workshop in workshop_data:
        if workshop[1] in (None, ''):
            errors.append('Workshop Name is missing for workshop {}. '
                          'Please check and correct the file.'.format(
                                  workshop[0]))
        if workshop[2] in (None, ''):
            warnings.append('Location is missing for workshop {}.'.format(
                    workshop[0]))
        if workshop[3] in (None, ''):
            warnings.append('Venue is missing for workshop {}.'.format(
                    workshop[0]))
        if workshop[4] in (None, ''):
            warnings.append('Workshop Date is missing for workshop '
                            '{}.'.format(workshop[0]))
        if workshop[5] in (None, ''):
            warnings.append('Workshop Cost is missing for workshop '
                            '{}.'.format(workshop[0]))
        # Check Status is present and valid
        if workshop[6] in (None, ''):
            warnings.append('Workshop Status is missing for workshop '
                            '{}.'.format(workshop[0]))
        elif workshop[6] not in allowed_status:
            errors.append('Workshop Status is incorrect for workshop '
                          '{}'.format(workshop[0]))
        # Check Type is present and valid
        if workshop[7] in (None, ''):
            warnings.append('Workshop Type is missing for workshop '
                            '{}.'.format(workshop[0]))
        elif workshop[7] not in allowed_type:
            errors.append('Workshop Type is incorrect for workshop '
                          '{}'.format(workshop[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Workshop Data')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_we(enrolment_data):
    """Check that data is correct in the workshop enrolments file.

    Args:
        enrolment_data (list): List with the data for each workshop enrolment.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (enrolment_data):
        Student ID, First Name, Last Name, Workshop.
    """
    errors = []
    warnings = ['\nWorkshop Enrolment Sheet Warnings:\n']
    for enrolment in enrolment_data:
        if len(enrolment[0]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{}.'.format(enrolment[0]))
        if enrolment[1] in (None, ''):
            warnings.append('First name missing for student {}.'.format(
                    enrolment[0]))
        if enrolment[2] in (None, ''):
            warnings.append('Last name missing for student {}.'.format(
                    enrolment[0]))
        if enrolment[3] in (None, ''):
            errors.append('Workshop code is missing for  {}. Please '
                          'correct and try again.'.format(enrolment[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Workshop Enrolment Data')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def check_wtd(workshop_tutor_data, source):
    """Check that data is correct in the workshop tutor data file.

    Args:
        workshop_tutor_data (list): A list with the data for each tutor -
        workshop pairing.
        source (str): String naming the source of the data.

    Returns:
        False indicating the warnings list has not been appended to.
        warnings (list): Warnings that have been identified in the data.

    File structure (workshop_tutor_data):
        Workshop Code, Tutor ID.
    """
    errors = []
    warnings = []
    for pairing in workshop_tutor_data:
        if pairing[1] in (None, ''):
            errors.append('Tutor Code is missing for Workshop Code {}. '
                          'Please check and correct the file.'.format(
                                  pairing[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, source)
    return False, warnings


def clean_cc(raw_data):
    """Clean the data in the course codes file.

    Args:
        raw_data (list): A list with the data for the course codes.

    Returns:
        cleaned_data (list): A list with cleaned course data.

    File structure (raw_data):
        Course Code, Course Name.
    """
    cleaned_data = []
    for item in raw_data:
        cleaned_course = []
        cleaned_course.append(item[0].strip())
        cleaned_course.append(item[1].strip())
        cleaned_data.append(cleaned_course)
    return cleaned_data


def clean_cd(raw_data):
    """Clean the data in the course or workshop upload data.

    Args:
        raw_data (list): A list with the data for the course or workshop
        upload files.

    Returns:
        cleaned_data (list): A list with cleaned course or workshop data.

    File structure (raw_data):
        CoursePK, CourseName, Venue, Mode, Status.
    """
    cleaned_data = []
    for course in raw_data:
        cleaned_course = []
        cleaned_course.append(course[0].strip())
        cleaned_course.append(course[1].strip())
        cleaned_course.append(course[2].strip())
        cleaned_course.append(course[3].strip())
        cleaned_course.append(course[4].strip())
        cleaned_data.append(cleaned_course)
    return cleaned_data


def clean_cdf(processing_data, course_data):
    """Clean the data in the combined data form data and convert required
    items.

    Args:
        processing_data (list): A list with the data read from the combined
        data form file.
        course_data (list): A list with the data for each course.

    Returns:
        cleaned_data (list): A list with cleaned combined data form data.

    File structure (processing_data):
        Student ID, Preferred Method of Study, Part-time Class Schedules,
        Name (Prefix), Name (Given Name), Name (Middle), Name (Surname),
        Name (Suffix), Preferred Name (Prefix), Preferred Name (Given Name),
        Preferred Name (Middle), Preferred Name (Surname),
        Preferred Name (Suffix), Gender, Date of Birth, Guardian Name (Prefix),
        Guardian Name (Given Name), Guardian Name (Middle),
        Guardian Name (Surname), Guardian Name (Suffix),
        Guardian Identification, Please tick to confirm...,
        Telephone, Mobile, Email, Mobile, Email, Nationality, Ethnicity,
        Please identify:, Which country were you born in?, Iwi, Citizenship,
        If other, please explain:, Is English your first language?,
        What is your first language?, Address (Number/Unit),
        Address (Street Address), Address (Suburb), Address (City),
        Address (Postcode), Address (Country), Disability, Please explain:,
        Employment, Qualification, Year, National Student Number,
        Reason for Study, Please explain:, How did you hear about us?, 
        Please state:, Please tick to confirm...

    File structure (course_data):
        Course Code, Class Date.
    """
    cleaned_data = []
    for student in processing_data:
        cleaned_student = []
        # Process each column as required
        cleaned_student.append(student[0].strip())
        # Convert to a course code
        course = convert_course(student[1].strip(), student[2].strip(),
                                course_data)
        cleaned_student.append(course)
        cleaned_student.append(student[4].strip())
        cleaned_student.append(student[6].strip())
        cleaned_student.append(student[9].strip())
        cleaned_student.append(student[13].strip())
        # Process Date of Birth so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[14].strip()))
        cleaned_student.append(student[16].strip())
        cleaned_student.append(student[18].strip())
        cleaned_student.append(student[20].strip())
        # Convert Under age tick to 'Yes' or 'No'
        cleaned_student.append(clean_u18(student[21]))
        # Add a leading 0 to Telephone if required and remove spaces
        clean_tele = clean_telephone(student[22])
        cleaned_student.append(clean_tele)
        # If mobile is empty take from telephone else clean up
        clean_mob = clean_mobile_cdf(student[23], clean_tele)
        cleaned_student.append(clean_mob)
        cleaned_student.append(student[24].lower().strip())
        # Process preferred contact mode and replace Mobile Email with it
        contact_preference = preferred_contact(student[25].strip(),
                                               student[26].strip())
        cleaned_student.append(contact_preference)
        cleaned_student.append(student[27].strip())
        # Process Ethnicity and set if Other selected
        ethnicity = get_ethnicity(student[28].strip(), student[29].strip())
        cleaned_ethnicity = ad.replace_string(ethnicity, ',', '')
        cleaned_student.append(cleaned_ethnicity)
        cleaned_student.append(student[30].strip())
        iwi = ad.replace_string(student[31].strip(), ',', ' and')
        cleaned_student.append(iwi)
        # Process Citizenship and set if Other selected
        citizen = get_citizenship(student[32].strip(), student[33].strip())
        cleaned_citizen = ad.replace_string(citizen, ',', '')
        cleaned_student.append(cleaned_citizen)
        # Process first language
        language = get_language(student[34].strip(), student[35].strip())
        cleaned_language = ad.replace_string(language, ',', '')
        cleaned_student.append(cleaned_language)
        add_num = ad.replace_string(student[36].strip(), ',', '')
        cleaned_student.append(add_num)
        add_street = ad.replace_string(student[37].strip(), ',', '')
        cleaned_student.append(add_street)
        add_suburb = ad.replace_string(student[38].strip(), ',', '')
        cleaned_student.append(add_suburb)
        add_city = ad.replace_string(student[39].strip(), ',', '')
        cleaned_student.append(add_city)
        # Process post code to make sure it has four digits
        post_code = get_post_code(student[40].strip(), student[41].strip())
        cleaned_student.append(post_code)
        cleaned_student.append(student[41].strip())
        # Get disability
        disability = get_disability(student[42].strip(), student[43].strip())
        cleaned_disability = ad.replace_string(disability, ',', '')
        cleaned_student.append(cleaned_disability)
        cleaned_student.append(student[44].strip())
        qualification = ad.replace_string(student[45].strip(), ',', ' and')
        cleaned_student.append(qualification)
        cleaned_student.append(student[46].strip())
        cleaned_student.append(student[47].strip())
        # Get reason for study
        study_reason = get_study_reason(student[48].strip(),
                                        student[49].strip())
        cleaned_study_reason = ad.replace_string(study_reason, ',', '')
        cleaned_student.append(cleaned_study_reason)
        # Get how heard
        how_heard = get_how_heard(student[50].strip(), student[51].strip())
        cleaned_how_heard = ad.replace_string(how_heard, ',', '')
        cleaned_student.append(cleaned_how_heard)
        # Process Terms and conditions
        cleaned_student.append(process_tc(student[52].strip()))
        cleaned_data.append(cleaned_student)
    # ad.debug_list(cleaned_data)
    return cleaned_data


def clean_ctd(raw_data):
    """Clean the data in the course or workshop tutor data.
    
    Removes any unnecessary spaces. Also removes the Tutor Name from the data
    as it is not required.

    Args:
        raw_data (list): A list with the data for the course or workshop
        tutor pairings.

    Returns:
        cleaned_data (list): A list with cleaned course or workshop tutor data.

    File structure (raw_data):
        CourseFK, Tutor Name, TutorFK.
    """
    cleaned_data = []
    for pairing in raw_data:
        cleaned_source_tutor = []
        cleaned_source_tutor.append(pairing[0].strip())
        cleaned_source_tutor.append(pairing[2].strip())
        cleaned_data.append(cleaned_source_tutor)
    return cleaned_data


def clean_ec(raw_data):
    """Clean the data in the Enrolment Codes file data.

    Args:
        raw_data (list): A list with the data from the Enrolment Codes file.

    Returns:
        cleaned_data (list): A list with cleaned Enrolement Codes file data.

    File structure (raw_data):
        EnrolmentPK, StudentFK.
    """
    cleaned_data = []
    for code in raw_data:
        cleaned_student = []
        # Process each column
        cleaned_student.append(code[0].strip())
        cleaned_student.append(code[1].strip())
        cleaned_data.append(cleaned_student)
    return cleaned_data


def clean_es(processing_data):
    """Clean the data in the enrolment sheet file data.

    Args:
        processing_data (list): A list with the data from the Enrolment Sheet
        file.

    Returns:
        cleaned_data (list): A list with cleaned enrolment sheet file data.

    File structure (es_data):
        Student ID, First Name, Last Name, Preferred Name,
        Mobile, Email, Preferred Contact Mode, Course, Date Enrolled,
        Start Date, End Date, Tutor, Tutor contact, Username, Status, Tag,
        Enrolment Code, National Student Number.
    """
    cleaned_data = []
    for student in processing_data:
        cleaned_student = []
        # Process each column
        # Student ID Number, name columns
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[1].strip())
        cleaned_student.append(student[2].strip())
        cleaned_student.append(student[3].strip())
        # Clean the mobile number
        cleaned_student.append(clean_mobile(student[4].strip()))
        # Email, Contact Mode and Course Codes
        cleaned_student.append(student[5].lower().strip())
        cleaned_student.append(student[6].strip())
        cleaned_student.append(student[7].strip())
        # Process Date of enrolment so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[8].strip()))
        # Process Start Date so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[9].strip()))
        # Process End Date so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[10].strip()))
        cleaned_student.append(student[11].strip())
        # Process Tutor Contact Date so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[12].strip()))
        cleaned_student.append(student[13].lower().strip())
        # Process status
        cleaned_student.append(get_status(student[14].strip()))
        # Add tag
        cleaned_student.append(student[15].strip())
        cleaned_student.append(student[16].strip())
        cleaned_student.append(student[17].strip())
        cleaned_data.append(cleaned_student)
    # ad.debug_list(cleaned_data)
    return cleaned_data


def clean_exc(exc_data):
    """Clean the data in the Extension Codes file data.
    
    Args:
        exc_data (list): A list with the data from the Extension Codes file.
        
    Returns:
        cleaned_data (list): A list with cleaned Extension Codes file data.
        
    File structure (exc_data):
        EnrolmentFK, AcceptanceDate.
    """
    cleaned_data = []
    for code in exc_data:
        cleaned_student = []
        # Process each column
        cleaned_student.append(code[0].strip())
        cleaned_student.append(da.clean_date(code[1].strip()))
        cleaned_data.append(cleaned_student)
    return cleaned_data


def clean_ext(raw_data):
    """Clean the data in the Extensions Table file data.
    
    Args:
        raw_data (list): A list with the data from the Extensions file.
        
    Returns:
        cleaned_data (list): A list with cleaned Extensions file data.
        
    File structure (raw_data):
        Student ID Number, Name, Enrolment Code, Extension Length,
        Acceptance Date, New Expiry Date.
    """
    cleaned_data = []
    for student in raw_data:
        cleaned_student = []
        # Process each column
        # Student ID Number, Enrolment Code, Extension Length
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[2].strip())
        cleaned_student.append(student[3].strip())
        # Acceptance Date, New Expiry Date
        cleaned_student.append(da.clean_date(student[4].strip()))
        cleaned_student.append(da.clean_date(student[5].strip()))
        cleaned_data.append(cleaned_student)
    return cleaned_data            


def clean_gc(raw_data):
    """Clean the data in the Graduates Current file data.

    Args:
        raw_data (list): A list with the data from the Graduates Current file.

    Returns:
        cleaned_data (list): A list with cleaned Graduates Current file data.

    File structure (raw_data):
        GraduatePK, EnrolmentFK.
    """
    cleaned_data = []
    for student in raw_data:
        cleaned_student = []
        # Process each column
        # GraduatePK, EnrolmentFK
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[1].strip())
        cleaned_data.append(cleaned_student)
    return cleaned_data


def clean_gd(raw_data):
    """Clean the data in the Graduate file data.

    Args:
        raw_data (list): A list with the data from the Graduate file.

    Returns:
        cleaned_data (list): A list with cleaned Graduate file data.

    File structure (raw_data):
        Student ID Number, Name, Enrolment Code, Graduation Date,
        Certificate Number.
    """
    cleaned_data = []
    for student in raw_data:
        cleaned_student = []
        # Process each column
        # Student ID Number, Enrolment Code
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[2].strip())
        # Graduation Date
        cleaned_student.append(da.clean_date(student[3].strip()))
        # Certificate Number
        cleaned_student.append(student[4].strip())
        cleaned_data.append(cleaned_student)
    return cleaned_data    


def clean_mobile_cdf(student_mobile, student_telephone):
    """Check and correct for leading 0 in mobile number.

    Checks if the mobile number is missing a leading 0 and adds it if it is.
    If there is no mobile number, returns the telephone number if one is
    present.

    Args:
        student_mobile (str): Input moblie number as a string.
        student_telephone (str): Input telephone number as a string.

    Returns:
        clean_mob (str): Cleaned mobile or phone number with a leading '0'.
    """
    if student_mobile not in (None, '') and not ad.check_lead_zero(
            student_mobile):
        mob = '0{}'.format(student_mobile[:])
        clean_mob = mob.strip().replace(' ', '')
    elif student_mobile not in (None, ''):
        clean_mob = student_mobile.strip().replace(' ', '')
    elif student_mobile in (None, '') and student_telephone not in (None, ''):
        clean_mob = clean_telephone(student_telephone)
    else:
        clean_mob = student_mobile
    return clean_mob


def clean_mobile(mobile):
    """Check and correct for leading 0 in mobile number.

    Checks if the mobile number is missing a leading 0 and adds it if it is.

    Args:
        mobile (str): Input moblie number as a string.

    Returns:
        clean_mob (str): Cleaned mobile number with a leading '0'.
    """
    if mobile not in (None, '') and not ad.check_lead_zero(mobile):
        mob = '0{}'.format(mobile[:])
        clean_mob = mob.strip().replace(' ', '')
    elif mobile not in (None, ''):
        clean_mob = mobile.strip().replace(' ', '')
    else:
        return mobile
    return clean_mob


def clean_os(os_data):
    """Clean the data in the Old Students file data.

    Args:
        os_data (list): A list with the data from the Old Students file.

    Returns:
        cleaned_data (list): A list with cleaned Old Students file data.

    File structure (os_data):
        StudentPK, NameGiven, NameSurname, NamePreferred, DateOfBirth,
        Username, Telephone, Mobile, Email, PreferredContactMode,
        AddressNumber, AddressStreet, AddressSuburb, AddressCity,
        AddressPostcode, AddressCountry, Nationality, Iwi, Citizenship,
        GuardianNameGiven, GuardianNameSurname, GuardianId, Under18Auth,
        HowHeard, AgreeTandC, EnrolmentDate, Gender, Ethnicity, CountryOfBirth,
        Language, Disability, PreviousEducation, PreviousEdYear, Employment,
        ReasonForStudy.
    """
    cleaned_data = []
    for student in os_data:
        cleaned_student = []
        # Process each column
        # Student ID Number, name columns
        cleaned_student.append(student[0].strip())
        cleaned_student.append(student[1].strip())
        cleaned_student.append(student[2].strip())
        cleaned_student.append(student[3].strip())
        # Process Date of Birth so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[4].strip()))
        # Username
        cleaned_student.append(student[5].strip())
        # Blank for telephone
        cleaned_student.append('')
        # Mobile number
        cleaned_student.append(clean_mobile(student[7].strip()))
        # Email, Preferred Contact Mode
        cleaned_student.append(student[8].strip())
        cleaned_student.append(student[9].strip())
        cleaned_data.append(cleaned_student)
        # Address details
        cleaned_student.append(student[10].strip())
        cleaned_student.append(student[11].strip())
        cleaned_student.append(student[12].strip())
        cleaned_student.append(student[13].strip())
        # Clean Post Code
        post_code = get_post_code(student[14].strip(), student[15].strip())
        cleaned_student.append(post_code)
        cleaned_student.append(student[15].strip())
        # Blanks for Nationality, Iwi, Citizenship, GuardianNameGiven.
        # GuardianNameSurname, GuardianId, Under18Auth
        cleaned_student.append('')
        cleaned_student.append('')
        cleaned_student.append('')
        cleaned_student.append('')
        cleaned_student.append('')
        cleaned_student.append('')
        cleaned_student.append('')
        # How heard
        cleaned_student.append(student[23].strip())
        # Agree T & C
        cleaned_student.append('Yes')
        # Process Enrolment Date so that it is dd/mm/yyyy
        cleaned_student.append(da.clean_date(student[25].strip()))
        # Gender
        cleaned_student.append(student[26].strip())
        cleaned_student.append(student[27].strip())
        cleaned_student.append(student[28].strip())
        cleaned_student.append(student[29].strip())
        cleaned_student.append(student[30].strip())
        cleaned_student.append(student[31].strip())
        cleaned_student.append(student[32].strip())
        cleaned_student.append(student[33].strip())
        cleaned_student.append(student[34].strip())
    return cleaned_data
    

def clean_pt_dates(raw_data):
    """Clean the data in the Course Attendance Dates file data.

    Args:
        raw_data (list): A list of course dates.

    Returns:
        cleaned_data (list): A list with dates with leading 0's added.

    File structure (raw_data):
        date1, date2,....
    """
    cleaned_dates = []
    i = 0
    while i < len(raw_data[0]):
        clean_date = da.clean_date(raw_data[0][i])
        cleaned_dates.append(clean_date)
        i += 1
    return cleaned_dates


def clean_results(results, ass_names) :
    """Return just assessment rows.
    
    Checks each row in the results data for a valid assessment name from
    ass_names in position 0. If a valid assessment name is found, the row is
    extracted and added to the cleaned results data.
    
    Args:
        results (list): Raw results data (list of lists).
        ass_names (list): List of names for each assessment.
        
    Returns:
        cleaned_results (list): List with just assessment rows.
    """
    cleaned_results = []
    for row in results:
        if row[0] in ass_names:
            cleaned_results.append(row)
    return cleaned_results

    
def clean_telephone(student_tele):
    """Check and correct for leading 0 in telephone number.

    Checks if the telephone number is missing a leading 0 and adds it if it is.

    Args:
        student_tele (str): Input telephone number as a string.

    Returns:
        clean_tele (str): Cleaned telephonr number with a leading '0'.
    """
    if student_tele not in (None, '') and not ad.check_lead_zero(student_tele):
        tele = '0{}'.format(student_tele[:])
        clean_tele = tele.strip().replace(' ', '')
    elif student_tele not in (None, ''):
        clean_tele = student_tele.strip().replace(' ', '')
    else:
        clean_tele = student_tele
    return clean_tele


def clean_td(processing_data):
    """Clean the data in the tutor data file data.

    Args:
        processing_data (list): A list with the data from the Tutor Data file.

    Returns:
        cleaned_data (list): A list with cleaned Tutor Data file data.

    File structure (processing_data):
        TutorID, First Name, Last Name, Email, Phone.
    """
    cleaned_data = []
    for tutor in processing_data:
        cleaned_tutor = []
        # Process each column
        cleaned_tutor.append(tutor[0].strip())
        cleaned_tutor.append(tutor[1].strip())
        cleaned_tutor.append(tutor[2].strip())
        cleaned_tutor.append(tutor[3].strip())
        cleaned_tutor.append(clean_mobile(tutor[4]))
        cleaned_data.append(cleaned_tutor)
    return cleaned_data


def clean_tu(processing_data):
    """Clean the data in the TutorIDs.csv data.

    Args:
        processing_data (list): A list with the data from the TutorIDs.csv data
        file.

    Returns:
        cleaned_data (list): A list with cleaned TutorIDs.csv file data.

    File structure (processing_data):
        TutorID, First Name, Last Name.
    """
    cleaned_data = []
    for tutor in processing_data:
        cleaned_tutor = []
        # Process each column
        cleaned_tutor.append(tutor[0].strip())
        cleaned_tutor.append(tutor[1].strip())
        cleaned_tutor.append(tutor[2].strip())
        cleaned_data.append(cleaned_tutor)
    return cleaned_data


def clean_u18(repsonse):
    """Return value for confirmation of under 18.

    Args:
        response (str): String for Under 18 column in cdf file data.

    Returns:
        under (str): String indicating if data for confirmation of under 18 is
        'Yes' or 'No'.
    """
    if repsonse not in (None, ''):
        under = 'Yes'
    else:
        under = 'No'
    return under


def clean_wa(raw_data):
    """Clean the data in the Workshop Attedance file data.

    Args:
        raw_data (list): Data from the Workshop attendance file.

    Returns:
        cleaned_data (list): A list with cleaned Workshop attendance file data.

    File structure (raw_data):
        Workshop Code, Student ID, First Name, Last Name.
    """
    cleaned_data = []
    for student in raw_data:
        cleaned_workshop = []
        # Add '' for AttendancePK
        cleaned_workshop.append('')
        # Add Student ID
        cleaned_workshop.append(student[1].strip())
        # Add Workshop ID
        cleaned_workshop.append(student[0].strip())
        cleaned_data.append(cleaned_workshop)
    return cleaned_data


def clean_wc(raw_data):
    """Clean the data in the Workshop codes file data.

    Args:
        raw_data (list): A list with the data from the Workshop codes file.

    Returns:
        cleaned_data (list): A list with cleaned Workshop codes file data.

    File structure (raw_data):
        Workshop Code, Workshop Name.
    """
    cleaned_data = []
    for code in raw_data:
        cleaned_workshop = []
        cleaned_workshop.append(code[0].strip())
        cleaned_workshop.append(code[1].strip())
        cleaned_data.append(cleaned_workshop)
    return cleaned_data


def clean_wd(raw_data, ):
    """Clean the data in the Workshop Data upload file.

    Args:
        raw_data (list): A list with the data from the Workshop data upload
        file.

    Returns:
        cleaned_data (list): A list with cleaned Workshop data.

    File structure (raw_data):
        Workshop Code, Workshop Name, Location, Venue, Date, Cost, Status,
        Type.
    """
    
    cleaned_data = []
    for workshop in raw_data:
        cleaned_workshop = []
        cleaned_workshop.append(workshop[0].strip())
        cleaned_workshop.append(workshop[1].strip())
        cleaned_workshop.append(workshop[2].strip())
        cleaned_workshop.append(workshop[3].strip())
        cleaned_workshop.append(da.clean_date(workshop[4].strip()))
        cleaned_workshop.append(workshop[5].strip())
        cleaned_workshop.append(workshop[6].strip())
        cleaned_workshop.append(workshop[7].strip())
        cleaned_data.append(cleaned_workshop)
    return cleaned_data


def clean_we(processing_data):
    """Clean the data in the Workshop enrolment file data.

    Args:
        processing_data (list): A list with the data from the Workshop
        enrolment file.

    Returns:
        cleaned_data (list): A list with cleaned Workshop enrolment file data.

    File structure:
        Student ID, First Name, Last Name, Workshop.
    """
    cleaned_data = []
    for enrolment in processing_data:
        cleaned_enrolment = []
        # Process each column
        cleaned_enrolment.append(enrolment[0].strip())
        cleaned_enrolment.append(enrolment[1].strip())
        cleaned_enrolment.append(enrolment[2].strip())
        cleaned_enrolment.append(enrolment[3].strip())
        cleaned_data.append(cleaned_enrolment)
    return cleaned_data


def compare_cdf_es(cdf, es):
    """Check that data is consistent between the cdf and es files.

    Checks that data such as names and contact details are consistent in the
    cdf and es files. If there are differences these are noted as warnings
    (non-fatal) and errors (fatal).

    Args:
        cdf (list): Combined Data Form data in a list.
        es (list): Enrolment Sheet data in a list.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.

    File structure (cdf):
        Student ID, Preferred Method of Study, Part-time Class Schedules,
        Name (Prefix), Name (Given Name), Name (Middle), Name (Surname),
        Name (Suffix), Preferred Name (Prefix), Preferred Name (Given Name),
        Preferred Name (Middle), Preferred Name (Surname),
        Preferred Name (Suffix), Gender, Date of Birth, Guardian Name (Prefix),
        Guardian Name (Given Name), Guardian Name (Middle),
        Guardian Name (Surname), Guardian Name (Suffix),
        Guardian Identification, Please tick to confirm...,
        Telephone, Mobile, Email, Mobile, Email, Nationality, Ethnicity,
        Please identify:, Which country were you born in?, Iwi, Citizenship,
        If other, please explain:, Is English your first language?,
        What is your first language?, Address (Number/Unit),
        Address (Street Address), Address (Suburb), Address (City),
        Address (Postcode), Address (Country), Disability, Please explain:,
        Employment, Qualification, Year, National Student Number,
        Reason for Study, Please explain:, How did you hear about us?, 
        Please state:, Please tick to confirm...

    File structure (es):
        Student ID, First Name, Last Name, Preferred Name,
        Mobile, Email, Preferred Contact Mode, Course, Date Enrolled,
        Start Date, End Date, Tutor, Tutor contact, Username, Status, Tag,
        Enrolment Code, National Student Number.
    """
    errors = []
    warnings = ['\nComparison Between cdf and es Warnings:\n']
    if len(cdf) != len(es):
        errors.append('The two files are of different length! Check which '
                      'students are missing. Also check that each student has '
                      'a Student ID Number.')
        ft.process_error_log(errors, 'Sheets_Comparison')
    i = 0
    while i < len(cdf):
        j = 0
        found = False
        while not found and j < len(es):
            student = cdf[i][0]
            if student == es[j][0]:
                found = True
                if cdf[i][2] != es[j][1]:
                    errors.append('First names are not consistent for '
                                  'Student: {}'.format(student))
                if cdf[i][3] != es[j][2]:
                    errors.append('Last names are not consistent for '
                                  'Student: {}'.format(student))
                if cdf[i][4] != es[j][3]:
                    warnings.append('Preferred names are not consistent for '
                                    'Student: {}'.format(student))
                if cdf[i][12] != es[j][4]:
                    warnings.append('Mobile numbers are not consistent for '
                                    'Student: {}'.format(student))
                if cdf[i][13] != es[j][5]:
                    errors.append('Email addresses are not consistent for '
                                  'Student: {}'.format(student))
                if cdf[i][14] != es[j][6]:
                    warnings.append('Preferred contact modes are not '
                                    'consistent for Student: {}'.format(
                                            student))
                if cdf[i][1] != es[j][7]:
                    warnings.append('Course codes are not consistent for '
                                    'Student: {}'.format(student))
                # print('Contact Mode c ' + student + ' ' + cdf[i][14])
                # print('Contact Mode e ' + student + ' ' + es[j][7])
            else:
                j += 1
        if not found:
            errors.append('Student {} does not appear in the Enrolment form. '
                          'Please check!'.format(student))
        i += 1
    if len(errors) > 0:
        ft.process_error_log(errors, 'Sheets_Comparison')
    # Check if any warnings have been identified, save error log if they have
    if len(warnings) > 1:
        return True, warnings
    else:
        return False, warnings


def convert_course(mode, p_class, course_codes):
    """Convert study mode to a course code.

    If the study mode is 'Online' then 'ADV-ON-001' is the course code.
    Converts a part-time class to its course code.

    Args:
        mode (str): The study mode ('Online' or 'Part-time').
        p_class (str): The class name from the enrolment form.
        course_codes (dict): Dictionary of course codes: course names.

    Returns:
        course_code (str): If mode is 'Online' returns online course code.
        code (str): If mode is part-time returns the course code.
        (str): Empty string returned if course cannot be found.
    """
    if mode == 'Online':
        course_code = 'ADV-ON-001'
        return course_code
    elif p_class.strip() in course_codes.values():
        for code, session in course_codes.items():
            if session == p_class.strip():
                return code
    else:
        return ''


def create_codes(received_codes):
    """Create a dictionary with the course codes.

    Args:
        received_codes (list): List of course codes to process.

    Returns:
        processed_codes (dict): Dictionary of course codes with the course
        name as the values.

    File structure (received_codes):
        Course Code, Course Name.
    """
    processed_codes = {}
    for course in received_codes:
        code = course[0]
        class_date = course[1].strip()
        processed_codes[code] = class_date
    return processed_codes


def extract_source_tutor(source_data, source_pos):
    """Extract a single Course or Workshop - Tutor pairing.

    Args:
        source_data (list): List containing source data.
        source_pos (int): Location of the pairing to be extracted.

    Returns:
        source_tutor (list): A single course or workshop-tutor pairing.

    File structure (source_data):
        Course ID, Tutor ID.
    """
    source_tutor = []
    source_tutor.append(source_data[source_pos])
    # print('source_tutor: ' + str(source_pos))
    # ad.debug_list_item(source_tutor)
    return source_tutor


def extract_student_2(student_data, student_pos):
    """Extract a single student.

    Args:
        student_data (list): List containing student data.
        student_pos (int): Location of the student to be extracted.

    Returns:
        student (list): A single student in a list.
    """
    return student_data[student_pos]


def extract_workshop(workshop_data, workshop_pos):
    """Extract a single workshop.

    Args:
        workshop_data (list): List containing worskhop data.
        workshop_pos (int): Location of the workshop to be extracted.

    Returns:
        workshop (list): A single workshop in a list.
    """
    workshop = workshop_data[workshop_pos]
    # print('Workshop: ' + str(workshop_pos))
    # ad.debug_list_item(workshop)
    return workshop


def extract_workshop_tutor(workshop_tutor_data, workshop_tutor_pos):
    """Extract a single workshop-tutor pairing.

    Args:
        workshop_tutor_data (list): List containing worskhop-tutor pairings
        data.
        workshop_tutor_pos (int): Location of the workshop-tutor pairing to be
        extracted.

    Returns:
        workshop_tutor (list): A single workshop-tutor pairing in a list.

    File structure (workshop_tutor_data):
        Workshop ID, Tutor ID.
    """
    workshop_tutor = workshop_tutor_data[workshop_tutor_pos]
    # print('workshop_tutor: ' + str(workshop_pos))
    # ad.debug_list_item(workshop_tutor)
    return workshop_tutor


def get_assess_date(raw_date):
    """Return assessment date in the format DD/MM/YYYY.
    
    Extracts the assessment date and converts it to DD/MM/YYYY. Finds the days,
    adding a leading 0 if required. Finds the text for the month and then finds
    the appropriate digits for the month from a dict. Finds the years and then
    combines them all to make the date.
    
    Args:
        raw_date (str): Date in the format of day, dd monthh yyyy.
        
    Returns:
        cleaned_date (str): Date in the format DD/MM/YYYY.
    """
    # Create a dict to hold the values for each month
    months_dict = {'January' : '01', 'February' : '02', 'March' : '03',
                  'April' : '04', 'May' : '05', 'June' : '06', 'July' : '07',
                  'August' : '08', 'September' : '09', 'October' : '10',
                  'November' : '11', 'December' : '12'}
    if raw_date in (None, ''):
        return ''
    # Extract days and add leading zero if needed
    # Get position of first space
    first_space_pos = raw_date.find(' ')
    # Get from the start of the day to the end of the date
    days_rest = raw_date[first_space_pos + 1:]
    second_space_pos = days_rest.find(' ')
    # Days is from start of days_rest to second_space_pos
    days = days_rest[:second_space_pos]
    # Add leading 0 if needed
    if len(days) == 1:
        days = '0{}'.format(days)
    # Extract Month and convert to MM
    # Get from start of month to end of date
    months_rest = days_rest[second_space_pos + 1:]
    # Get position of space after month
    third_space = months_rest.find(' ')
    # Month is from start of months_rest to third_space
    raw_month = months_rest[:third_space]
    # Convert raw_month to DD/MM/YYYY
    months = months_dict.get(raw_month)
    # Get years - from the place after third_space and the next 3 places
    years = months_rest[third_space + 1:third_space + 5]
    # Combine days, months and years
    return '{}{}{}{}{}'.format(days, '/', months, '/', years)


def get_attendance_upload(attendance, dates, course):
    """Prepare data for Course Attendance table upload file.
    
    Args:
        attendance (list): Student attendance data.
        dates (list): Course dates list.
        course (str): Course code for the course being processed.
    
    Returns:
        save_data (list): Data to be saved.
        headings (str): Column of headings to be saved.
    """
    save_data = []
    # Process each session for each student
    for student in attendance:
        # Start with first class session (column 3)
        i = 3
        while i < len(student):
            # If student did not attend the class
            if str(student[i]) == '1':
                i += 1
            # If student did attend the class
            else:
                class_entry = []
                # Add space for PK, Student ID and Course FK
                class_entry.append('')
                class_entry.append(student[0])
                class_entry.append(course)
                # Add relevant date (location is i - 3)
                class_entry.append(dates[i - 3])
                save_data.append(class_entry)
                i += 1
    headings = ('CourseAttendancePK,StudentFK,CourseFK,CourseDate')
    return save_data, headings


def get_citizenship(cit_col, oth_col):
    """Return citizenship value.

    If the citizenship value is 'other' then the value of the 'other' column is
    returned for the citizenship value.

    Args:
        cit_col (str): Value in the citizenship column.
        oth_col (str): Value in the other column for citizenship.

    Returns:
        citizenship (str): Value of citizenship.
    """
    if cit_col not in (None, '') and cit_col.strip().lower() != 'other':
        citizenship = cit_col.strip()
    elif cit_col not in (None, '') and cit_col.strip().lower() == 'other':
        citizenship = oth_col.strip()
    else:
        citizenship = cit_col.strip()
    return citizenship


def get_course_data(cd):
    """Prepare data for Course table upload file.

    Args:
        cd (list): Source data to be processed.

    Returns:
        course_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (cd):
        CoursePK, CourseName, Venue, Mode, Status.
    """
    course_upload_data = []
    for course in cd:
        extracted_course = []
        # Add Course Code
        extracted_course.append(course[0])
        # Add Course Name
        extracted_course.append(course[1])
        # Add Course Venue
        extracted_course.append(course[2])
        # Add Course Mode
        extracted_course.append(course[3])
        extracted_course.append(course[4])
        course_upload_data.append(extracted_course)
    headings = 'CoursePK,CourseName,Venue,Mode,Status'
    return course_upload_data, headings


def get_course_tutor_data(ct_data):
    """Prepare data for Course tutor table upload file.

    Args:
        ct_data (list): Source data to be processed.

    Returns:
        ct_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (raw_data):
        CourseFK, TutorFK.
    """
    ct_upload_data = []
    for pair in ct_data:
        pairing = []
        # Add blank for CourseTutorPK
        pairing.append('')
        # Add Course FK
        pairing.append(pair[0])
        # Add TutorFK
        pairing.append(pair[1])
        ct_upload_data.append(pairing)
    headings = 'CourseTutorPK,CourseFK,TutorFK'
    return ct_upload_data, headings


def get_disability(response, disability_ex):
    """Return disability value.

    If the disability value is 'other' then the value of the 'other' column is
    returned for the disability value.

    Args:
        response (str): Value in the disability column.
        disability_ex (str): Value in the other column for disability.

    Returns:
        disability (str): Value of disability.
    """
    if response.lower() == 'no':
        disability = 'No'
    elif response.lower() == 'yes' and disability_ex not in (None, ''):
        disability = disability_ex.strip()
    elif response.lower() == 'yes':
        disability = 'Yes - no details provided'
    else:
        disability == response.strip()
    return disability


def get_enrolment_data(es):
    """Prepare data for Enrolments table upload file.

    Args:
        es (list): Source data to be processed.

    Returns:
        enrol_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (es):
        Student ID, First Name, Last Name, Preferred Name,
        Mobile, Email, Preferred Contact Mode, Course, Date Enrolled,
        Start Date, End Date, Tutor, Tutor contact, Username, Status, Tag,
        Enrolment Code, National Student Number.
    """
    enrol_upload_data = []
    for student in es:
        extracted_student = []
        # Add empty column for auto number
        extracted_student.append('')
        # Add Student ID
        extracted_student.append(student[0])
        # Add Course code
        extracted_student.append(student[7])
        # Add Tutor code
        extracted_student.append(student[11])
        # Add start and end dates
        extracted_student.append(student[9])
        extracted_student.append(student[10])
        # Add status
        extracted_student.append(student[14])
        # Add tag
        extracted_student.append(student[15])
        enrol_upload_data.append(extracted_student)
    headings = ('EnrolmentPK,StudentFK,CourseFK,TutorFK,StartDate,ExpiryDate,'
                'Status,Tag')
    return enrol_upload_data, headings


def get_ethnicity(eth_col, oth_col):
    """Return ethnicity value.

    If the ethnicity value is 'other' then the value of the 'other' column is
    returned for the ethnicity value.

    Args:
        eth_col (str): Value in the ethnicity column.
        oth_col (str): Value in the other column for ethnicity.

    Returns:
        ethnicity (str): Value of ethnicity.
    """
    if eth_col not in (None, '') and eth_col.strip().lower() != 'other':
        ethnicity = eth_col.strip()
    elif eth_col not in (None, '') and eth_col.strip().lower() == 'other':
        ethnicity = oth_col.strip()
    else:
        ethnicity = eth_col.strip()
    return ethnicity


def get_ext_data(ext_data):
    """Prepare data for Extensions table upload file.

    Args:
        ext_data (list): Source data to be processed.

    Returns:
        ext_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (ext_data):
        Student ID Number, Enrolment Code, Extension Length, Acceptance Date, 
        New Expiry Date.
    """
    ext_upload_data = []
    for student in ext_data:
        extracted_student = []
        # Add empty column for auto number
        extracted_student.append('')
        # Add EnrolmentFK
        extracted_student.append(student[1])
        # Add Extension Length
        extracted_student.append(student[2])
        # Add Acceptance Date
        extracted_student.append(student[3])
        # Add New Expiry Date
        extracted_student.append(student[4])
        ext_upload_data.append(extracted_student)
    headings = ('ExtensionPK,EnrolmentFK,ExtensionLength,AcceptanceDate,'
                'ExpiryDate')
    return ext_upload_data, headings


def get_gd_data(gd_data):
    """Prepare data for Graduates table upload file.

    Args:
        gd_data (list): Source data to be processed.

    Returns:
        gd_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (gd_data):
        Student ID Number, Enrolment Code, Graduation Date, Certificate Number.
    """
    gd_upload_data = []
    for student in gd_data:
        extracted_student = []
        # Add empty column for auto number
        extracted_student.append('')
        # Add EnrolmentFK
        extracted_student.append(student[1])
        # Add Graduation Date
        extracted_student.append(student[2])
        # Add Certificate Number
        extracted_student.append(student[3])
        gd_upload_data.append(extracted_student)
    headings = ('GraduatePK,EnrolmentFK,GraduationDate,CertificateNumber')
    # print(gd_upload_data)
    return gd_upload_data, headings
        

def get_grade(raw_grade):
    """Extract the grade from a raw grade.
    
    Retruns the grade. Takes the data from the position after Grade: (including
    the space after the e) to the end of the string. If the grade is '-' then
    it returns an empty string.
    
    Args:
        raw_grade (str): Grade data.
        
    Returns:
        grade (str): Extracted grade.
    """
    grade = raw_grade[7:]
    if grade == '-':
        return ''
    # Catch Lessons that have not been attempted
    elif grade[0] == 'm':
        return ''    
    # Catch assessments that have been started by not completed
    elif grade[0] == 'h':
        return ''
    else:
        return grade


def get_headings(code):
    """Return headings for save file.
    
    Adds each assessment name to the list of headings. Headings are identified
    based on the code that is passed.
    
    Args:
        code (str): Course code.
    
    Returns:
        headings (list): List of headings.
    """
    if code == 'ADV':
        headings = ('ID,EnrolmentFK,M0T1Grade,M0T1Date,M0T2Grade,M0T2Date,'
                    'M0T3Grade,M0T3Date,M1L1Grade,M1L1Date,M2Q1Grade,M2Q1Date,'
                    'M2T1Grade,M2T1Date,M2T2Grade,M2T2Date,M2T3Grade,M2T3Date,'
                    'M2T4Grade,M2T4Date,M2T5Grade,M2T5Date,M3Q1Grade,M3Q1Date,'
                    'M3L1Grade,M3L1Date,M3T1Grade,M3T1Date,M3T2Grade,M3T2Date,'
                    'M3T3Grade,M3T3Date,M4Q1Grade,M4Q1Date,M4T1Grade,M4T1Date,'
                    'M4T2Grade,M4T2Date,M4T3Grade,M4T3Date,M4T4Grade,M4T4Date,'
                    'M5Q1Grade,M5Q1Date,M5T1Grade,M5T1Date,M5T2Grade,M5T2Date,'
                    'M5T3Grade,M5T3Date,M5T4Grade,M5T4Date,M6Q1Grade,M6Q1Date,'
                    'M6T1Grade,M6T1Date,M6T2Grade,M6T2Date,M6T3Grade,M6T3Date,'
                    'M6T4Grade,M6T4Date,M6T5Grade,M6T5Date,M7Q1Grade,M7Q1Date,'
                    'M7T1Grade,M7T1Date,M7T2Grade,M7T2Date,M7T3Grade,M7T3Date,'
                    'M7T4Grade,M7T4Date,M7T5Grade,M7T5Date,M8Q1Grade,M8Q1Date,'
                    'M8T1Grade,M8T1Date,M8T2Grade,M8T2Date,M8T3Grade,M8T3Date,'
                    'M8T4Grade,M8T4Date,M8T5Grade,M8T5Date,M9Q1Grade,M9Q1Date,'
                    'M9T1Grade,M9T1Date,M9T2Grade,M9T2Date,M9T3Grade,M9T3Date,'
                    'M9T4Grade,M9T4Date,M9T5Grade,M9T5Date,M9T6Grade,M9T6Date,'
                    'M10Q1Grade,M10Q1Date,M10T1Grade,M10T1Date,M10T2Grade,'
                    'M10T2Date,M10T3Grade,M10T3Date,M10T4Grade,M10T4Date,'
                    'M11Q1Grade,M11Q1Date,M11T1Grade,M11T1Date,M11T2Grade,'
                    'M11T2Date,M11T3Grade,M11T3Date,M12Q1Grade,M12Q1Date,'
                    'M12T1Grade,M12T1Date,M12T2Grade,M12T2Date,M12T3Grade,'
                    'M12T3Date,M12T4Grade,M12T4Date,M13T1Grade,M13T1Date')
    return headings


def get_how_heard(h_reason, pl_state):
    """Return how heard value.

    If the how heard value is 'other' then the value of the 'other' column is
    returned for the how heard value.

    Args:
        h_reason (str): Value in the how heard column.
        pl_state (str): Value in the other column for how heard.

    Returns:
        how_heard (str): Value of how heard.
    """
    if h_reason not in (None, '') and h_reason.lower() != 'other':
        how_heard = h_reason.strip()
    elif h_reason.lower() == 'other' and pl_state not in (None, ''):
        how_heard = pl_state.strip()
    elif h_reason.lower() == 'other':
        how_heard = 'Other - not specified'
    else:
        how_heard = h_reason.strip()
    return how_heard


def get_language(lang_col, oth_col):
    """Return language value.

    If the language value is 'other' then the value of the 'other' column is
    returned for the language value.

    Args:
        lang_col (str): Value in the language column.
        oth_col (str): Value in the other column for language.

    Returns:
        language (str): Value of language.
    """
    if lang_col.lower() == 'yes':
        language = 'English'
    elif lang_col.lower() == 'no':
        language = oth_col.strip()
    else:
        language = ''
    return language


def get_post_code(post_code, country):
    """Return post code value.

    If the country value is 'New Zealand' then makes sure the post code has
    four digits. Adds a leading 0 if only three digits present.

    Args:
        post_code (str): Value in the post code column.
        country (str): Value in the country column.

    Returns:
        post_code (str): Value of post code.
        or
        updated_post_code (str): Value of post code that has been updated
        to include a leading 0.
    """
    if post_code in (None, ''):
        return post_code
    elif country != 'New Zealand':
        return post_code
    elif len(post_code) not in (3, 4):
        return post_code
    # NZ post code missing leading 0
    elif len(post_code) == 3:
        updated_post_code = '0{}'.format(post_code)
        return updated_post_code
    else:
        return post_code


def get_results_upload_data(cleaned_results, e_id):
    """Create upload file for student data.
    
    Creates an upload file with the EnrolmentID along with the Grade and Date
    for each assessment. Saves the data into a list. Extracts the Grade from
    the data. Converts the raw dates into DD/MM/YYYY.
    
    Args:
        cleaned_results(list): List of lists where each list is the data for
        one assessment.
        e_id (str): Enrolment ID.
        
    Returns:
        upload_data (list): Extracted assessment grades and dates.
    """
    upload_data = []
    # Add blank entry for autonumber
    upload_data.append('')
    # Add Enrolment ID
    upload_data.append(e_id)
    # Add assessment data
    for assessment in cleaned_results:
        # Extract grade
        upload_data.append(get_grade(assessment[1]))
        # Extract date and convert
        # Check that there is a date column
        # (Students with nothing submitted will not have a date column)
        if len(assessment) == 2:
            upload_data.append('')
        else:
            upload_data.append(get_assess_date(assessment[2]))
    return upload_data


def get_status(student_status):
    """Return student status value.

    Returns the status of the student or an empty string if the value is not
    in the allowed values.

    Args:
        student_status (str): Value in the student status column.

    Returns:
        status (str): Value of student status.
    """
    allowed = [None, '', 'Active', 'Suspended', 'Withdrawn', 'Graduated',
                  'Expired', 'On Hold', 'Cancelled']
    status = student_status.strip()
    if status in allowed:
        return status
    else:
        return ''


def get_student_data(cdf, es):
    """Prepare data for Student table upload file.

    Args:
        cdf (list): Data from the Combined Data Form.
        es (list): Data from the Enrolment Sheet.

    Returns:
        student_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (cdf):
        Student ID, Preferred Method of Study, Part-time Class Schedules,
        Name (Prefix), Name (Given Name), Name (Middle), Name (Surname),
        Name (Suffix), Preferred Name (Prefix), Preferred Name (Given Name),
        Preferred Name (Middle), Preferred Name (Surname),
        Preferred Name (Suffix), Gender, Date of Birth, Guardian Name (Prefix),
        Guardian Name (Given Name), Guardian Name (Middle),
        Guardian Name (Surname), Guardian Name (Suffix),
        Guardian Identification, Please tick to confirm...,
        Telephone, Mobile, Email, Mobile, Email, Nationality, Ethnicity,
        Please identify:, Which country were you born in?, Iwi, Citizenship,
        If other, please explain:, Is English your first language?,
        What is your first language?, Address (Number/Unit),
        Address (Street Address), Address (Suburb), Address (City),
        Address (Postcode), Address (Country), Disability, Please explain:,
        Employment, Qualification, Year, National Student Number,
        Reason for Study, Please explain:, How did you hear about us?, 
        Please state:, Please tick to confirm...

    File structure (es):
        Student ID, First Name, Last Name, Preferred Name,
        Mobile, Email, Preferred Contact Mode, Course, Date Enrolled,
        Start Date, End Date, Tutor, Tutor contact, Username, Status, Tag,
        Enrolment Code, National Student Number.
    """
    errors = []
    student_upload_data = []
    i = 0
    while i < len(cdf):
        j = 0
        found = False
        while not found and j < len(es):
            student = cdf[i][0]
            if student == es[j][0]:
                found = True
                student_data = []
                student_data.append(student)
                student_data.append(cdf[i][2])
                student_data.append(cdf[i][3])
                student_data.append(cdf[i][4])
                student_data.append(cdf[i][5])
                student_data.append(cdf[i][6])
                # Username
                student_data.append(es[j][13])
                # Telephone
                student_data.append(cdf[i][11])
                student_data.append(cdf[i][12])
                student_data.append(cdf[i][13])
                # Preferred contact mode
                student_data.append(cdf[i][14])
                # Address Number
                student_data.append(cdf[i][21])
                student_data.append(cdf[i][22])
                student_data.append(cdf[i][23])
                student_data.append(cdf[i][24])
                student_data.append(cdf[i][25])
                student_data.append(cdf[i][26])
                # Nationality
                student_data.append(cdf[i][15])
                student_data.append(cdf[i][16])
                student_data.append(cdf[i][17])
                student_data.append(cdf[i][18])
                student_data.append(cdf[i][19])
                student_data.append(cdf[i][20])
                # Guardian First Name
                student_data.append(cdf[i][7])
                student_data.append(cdf[i][8])
                student_data.append(cdf[i][9])
                student_data.append(cdf[i][10])
                # Disability
                student_data.append(cdf[i][27])
                # Previous Education
                student_data.append(cdf[i][29])
                student_data.append(cdf[i][30])
                student_data.append(cdf[i][31])
                # Employment
                student_data.append(cdf[i][28])
                # Reason for study
                student_data.append(cdf[i][32])
                student_data.append(cdf[i][33])
                student_data.append(cdf[i][34])
                # Enrolment Date
                student_data.append(es[j][8])
                student_upload_data.append(student_data)
            else:
                j += 1
        if not found:
            errors.append('Student {} does not appear in the Enrolment form. '
                          'Please check!'.format(student))
        i += 1
    headings = ('StudentPK,NameGiven,NameSurname,NamePreferred,Gender,'
                'DateOfBirth,Username,Telephone,Mobile,Email,'
                'PreferredContactMode,AddressNumber,AddressStreet,'
                'AddressSuburb,AddressCity,AddressPostcode,AddressCountry,'
                'Nationality,Ethnicity,CountryOfBirth,Iwi,Citizenship,'
                'Language,GuardianNameGiven,GuardianNameSurname,GuardianId,'
                'Under18Auth,Disability,PreviousEducation,PreviousEdYear,'
                'NationalStudentID,Employment,ReasonForStudy,HowHeard,'
                'AgreeTandC,EnrolmentDate')
    if len(errors) > 0:
        ft.process_error_log(errors, 'Student_Update_Data')
    return student_upload_data, headings


def get_study_reason(resp_reason, pl_explain):
    """Return study reason value.

    If the study reason value is 'other' then the value of the 'other' column
    is returned for the study reason value.

    Args:
        resp_reason (str): Value in the study reason column.
        pl_explain (str): Value in the please explain column for study reason.

    Returns:
        study_reason (str): Value of study reason.
    """
    if resp_reason not in (None, '') and resp_reason.lower() != 'other':
        study_reason = resp_reason.strip()
    elif resp_reason.lower() == 'other' and pl_explain not in (None, ''):
        study_reason = pl_explain.strip()
    elif resp_reason.lower() == 'other':
        study_reason = 'Other - not specified'
    else:
        study_reason = resp_reason.strip()
    return study_reason


def get_w_enrolment_data(we):
    """Prepare data for Workshop enrolment table upload file.

    Args:
        we (list): Data from the Workshop enrolment file.

    Returns:
        enrol_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (we):
        Student ID, First Name, Last Name, Workshop.
    """
    enrol_upload_data = []
    for enrolment in we:
        extracted_enrolment = []
        # Add empty column for auto number
        extracted_enrolment.append('')
        # Add Student ID
        extracted_enrolment.append(enrolment[0])
        # Add Workshop code
        extracted_enrolment.append(enrolment[5])
        enrol_upload_data.append(extracted_enrolment)
    headings = ('WorkshopEnrolmentPK,StudentFK,WorkshopFK')
    return enrol_upload_data, headings


def get_workshop_data(wd):
    """Prepare data for Workshops table upload file.

    Args:
        wd (list): Data from the Workshop file.

    Returns:
        workshop_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (wd):
        Workshop Code, Workshop Name, Location, Venue, Date, Cost, Status,
        Type.
    """
    workshop_upload_data = []
    for workshop in wd:
        extracted_workshop = []
        # Add Workshop Code
        extracted_workshop.append(workshop[0])
        # Add Workshop Name
        extracted_workshop.append(workshop[1])
        # Add Workshop Location
        extracted_workshop.append(workshop[2])
        # Add Workshop Venue
        extracted_workshop.append(workshop[3])
        # Add Workshop Date
        extracted_workshop.append(workshop[4])
        # Add Workshop Cost
        extracted_workshop.append(workshop[5])
        # Add Workshop Status
        extracted_workshop.append(workshop[6])
        # Add Workshop Type
        extracted_workshop.append(workshop[7])
        workshop_upload_data.append(extracted_workshop)
    headings = ('WorkshopPK,WorkshopName,Location,Venue,WorkshopDate,Cost,'
                'Status,Type')
    return workshop_upload_data, headings


def get_workshop_tutor_data(wt_data):
    """Prepare data for Workshop-tutor table upload file.

    Args:
        wt_data (list): Data from the Workshop-tutor file.

    Returns:
        wt_upload_data (list): The data to be saved to file.
        headings (str): Column headings to be saved to file.

    File structure (wt_data):
        Workshop Code, Tutor ID.
    """
    wt_upload_data = []
    for pair in wt_data:
        pairing = []
        # Add blank for WorkshopTutorPK
        pairing.append('')
        # Add Workshop FK
        pairing.append(pair[0])
        # Add TutorFK
        pairing.append(pair[1])
        wt_upload_data.append(pairing)
    headings = 'WorkshopTutorPK,WorkshopFK,TutorFK'
    return wt_upload_data, headings


def help_1():
    """Print Student Table Help information"""
    print('\nStudents Table Files\n')
    print('The following files are required:\n')
    print('Combined Data File')
    print('Enrolment Data Sheet')
    print('Course_IDs.csv')
    print('Student_IDs.csv')
    help_cdf()
    help_es()
    help_course_id()
    help_student_id()
    

def help_2():
    """Print Tutor Table Help information"""
    print('\nTutor Table Files\n')
    print('The following files are required:\n')
    print('Tutor Data File')
    print('Tutor_IDs.csv')
    help_tutor_df()
    help_tutor_id()


def help_3():
    """Print Course Table Help information"""
    print('\nCourse Table Files\n')
    print('The following files are required:\n')
    print('Courses Data File')
    print('Course_IDs.csv')
    help_courses_df()
    help_course_id()


def help_4():
    """Print Course Tutors Table Help information"""
    print('\nCourse Tutors Table Files\n')
    print('The following files are required:\n')
    print('Course Tutors Data File')
    print('Course_Tutors.csv')
    print('Course_IDs.csv')
    print('Tutor_IDs.csv')
    help_course_tutor_df()
    help_course_tutor_id()
    help_course_id()
    help_tutor_id()


def help_5():
    """Print Enrolments Table Help information"""
    print('\nEnrolments Table Files\n')
    print('The following files are required:\n')
    print('Enrolment Data')
    print('Student_IDs.csv')
    print('Tutor_ID.csv')
    print('Course_IDs.csv')
    help_es()
    help_student_id()
    help_tutor_id()
    help_course_id()
    

def help_6():
    """Print Graduates Table Help information"""
    print('\nGraduates Table Files\n')
    print('The following files are required:\n')
    print('Graduates Data')
    print('Enrolment_Codes.csv')
    print('Current_Graduates.csv')
    help_graduates_df()
    help_enrolment_codes()
    help_graduates_current()


def help_7():
    """Print Extensions Table Help information"""
    print('\nEnrolments Table Files\n')
    print('The following files are required:\n')
    print('Extensions Data')
    print('Enrolment_Codes.csv')
    print('Extension_Codes.csv')
    help_extensions_df()
    help_enrolment_codes()
    help_extension_codes()


def help_cdf():
    print('\nCombined Data Form\n')
    print('Sourced From:\n')
    print('Enrolment form data (downloaded from website) with the Student ID '
          'added to the first column.')
    print('\nDescription:\n')
    print('Contains the information the student submitted when they completed '
          'the online enrolment form, with the Student ID added to the first '
          'column.')
    print('\nColumns:\n')
    print('Student ID, Preferred Method of Study, Part-time Class Schedules, '
          'Name (Prefix), Name (Given Name), Name (Middle), Name (Surname), '
          'Name (Suffix), Preferred Name (Prefix), Preferred Name (Given Name)'
          ', Preferred Name (Middle), Preferred Name (Surname), Preferred Name '
          '(Suffix), Gender, Date of Birth, Guardian Name (Prefix), Guardian '
          'Name (Given Name), Guardian Name (Middle), Guardian Name (Surname)'
          ' Guardian Name (Suffix), Guardian Identification, Please tick to '
          'confirm..., Telephone, Mobile, Email, Mobile, Email, Nationality, '
          'Ethnicity, Please identify:, Which country were you born in?, Iwi, '
          'Citizenship, If other, please explain:, Is English your first '
          'language?, What is your first language?, Address (Number/Unit), '
          'Address (Street Address), Address (Suburb), Address (City), '
          'Address (Postcode), Address (Country), Disability, Please explain:'
          ', Employment, Qualification, Year, National Student Number, '
          'Reason for Study, Please explain:, How did you hear about us?, '
          'Please state:, Please tick to confirm..., Created By (User Id), '
          'Entry Id, Entry Date, Source Url, Transaction Id, Payment Amount, '
          'Payment Date, Payment Status, Post Id, User Agent, User IP.')


def help_courses_df():
    print('\nCourses Data File\n')
    print('Sourced From:\n')
    print('Courses tab on the Enrolments Google Sheet.')
    print('\nDescription:\n')
    print('Information for courses to be added to the Student Database '
          '(Access).')
    print('\nColumns:\n')
    print('CoursePK, CourseName, Venue, Mode, Status.')


def help_course_id():
    print('\nCourse_IDs.csv\n')
    print('Sourced From:\n')
    print('Courses tab on the Enrolments Google Sheet.')
    print('\nDescription:\n')
    print('The list of courses that are currently in the Student Database '
          '(Access). Compiled by taking the list of courses and course dates '
          'from the Courses sheet of the Enrolments Google Sheet. Note: Only '
          'take the courses already added to the Student Database (check the '
          'Courses Table in the Student Database).')
    print('\nColumns:\n')
    print('CoursePK, CourseDate.')


def help_course_tutor_df():
    print('\nCourse Tutor Data File\n')
    print('Sourced From:\n')
    print('Course Tutors sheet in the Enrolments Google Sheet.')
    print('\nDescription:\n')
    print('The list of course-tutor pairings to be added to the Student '
          'Database (Access). Each tutor on a course should have their tutor '
          'code and the course code pairing in the database.')
    print('\nColumns:\n')
    print('CourseFK, Tutor Name, TutorFK.')


def help_course_tutor_id():
    print('\nCourse_Tutors.csv\n')
    print('Sourced From:\n')
    print('The list of Course - Tutor pairings that are currently in the '
          'Course Tutors table of the student database. Can be taken from the '
          'Course Tutors sheet in the Enrolments Google Sheet provided you '
          'remove those that are not already in the Student Database.')
    print('\nDescription:\n')
    print('The list of course-tutor pairings that are currently in the '
          'Course-Tutors table of the Student Database.')
    print('\nColumns:\n')
    print('CourseFK, Tutor Name, TutorFK.')


def help_enrolment_codes():
    print('\nEnrolment_Codes.csv File\n')
    print('Sourced From:\n')
    print('Student ID Number and Enrolment Code taken from the Enrolments '
          'table of the Student Database.')
    print('\nDescription:\n')
    print('The Student ID Number and Enrolment Code for each entry in the '
          'Enrolments Table of the Student Database. This is used to make sure'
          ' that each enrolment code is valid and that the combination of '
          'Student ID Numbers and Enrolment Codes are also valid (already in '
          'the Student Database).')
    print('\nColumns:\n')
    print('EnrolmentPK, StudentFK.')


def help_es():
    print('\nEnrolment Data Sheet\n')
    print('Sourced From:\n')
    print('Enrolments tab on the Enrolments Google Sheet')
    print('\nDescription:\n')
    print('The information contained on the Enrolments Google Sheet, which has'
          ' had the course and tutor information added to it. It should only '
          'contain enrolment information that has not been added to the '
          'Student Database (there will not be an enrolment code in the '
          'Enrolment Code column).')
    print('\nColumns:\n')
    print('Student ID, First Name, Last Name, Preferred Name, Mobile, Email, '
          'Preferred Contact Mode, Course, Date Enrolled, Start Date, End '
          'Date, Tutor, Tutor contact, Username, Status, Tag, Enrolment Code, '
          'National Student Number.')


def help_extension_codes():
    print('\nExtension_Codes.csv File\n')
    print('Sourced From:\n')
    print('Extensions table of the Student Database.')
    print('\nDescription:\n')
    print('The EnrolmentFK and AcceptanceDate column data from the Extensions '
          'table of the Student Database. Used to make sure that the extension'
          ' has not already been added to the database.')
    print('\nColumns:\n')
    print('EnrolmentFK, AcceptanceDate.')


def help_extensions_df():
    print('\nExtensions Data File\n')
    print('Sourced From:\n')
    print('Extensions tab of the Enrolments Google Sheet.')
    print('\nDescription:\n')
    print('Each column from the Extensions tab is copied except for the Name '
          'column. The Enrolment Code, if it is missing, can be found in the '
          'Enrolments tab of the Enrolments Google Sheet.')
    print('\nColumns:\n')
    print('Student ID Number, Enrolment Code, Extension Length, Acceptance '
          'Date, New Expiry Date.')


def help_graduates_current():
    print('\nGraduates_Current.csv File\n')
    print('Sourced From:\n')
    print('Graduate Number and Enroment Code taken from the Graduates Table '
          'of the Student Database.')
    print('\nDescription:\n')
    print('The Graduate Number and Enroment Code for each student who has had'
          ' their graduation recorded in the Graduates Table of the Student '
          'Database. Used to make sure that the student has not already had '
          'their graduation recorded.')
    print('\nColumns:\n')
    print('GraduatePK, EnrolmentFK.')


def help_graduates_df():
    print('\nGraduates Data File\n')
    print('Sourced From:\n')
    print('Graduates Google Sheet and the Enrolment tab of the Enrolments '
          'Google Sheet for the Enrolment Code.')
    print('\nDescription:\n')
    print('The graduation information contained in the Graduates Google Sheet'
          ' with the Enrolment Code added from the Enrolments tab of the '
          'Enrolments Google Sheet.')
    print('\nColumns:\n')
    print('Student ID Number, Name, Enrolment Code, Graduation Date,'
          'Certificate Number.')


def help_menu():
    """Display the required help information."""
    repeat = True
    high = 8
    low = 1
    while repeat:
        try_again = False
        help_menu_message()
        try:
            action = int(input('\nPlease enter the number for your '
                               'selection --> '))
        except ValueError:
            print('Please enter a number between {} and {}.'.format(low, high))
            try_again = True
        else:
            if int(action) < low or int(action) > high:
                print('\nPlease select from the available options ({} - {})'
                      .format(low, high))
                try_again = True
            elif action == low:
                help_1()
            elif action == 2:
                help_2()
            elif action == 3:
                help_3()
            elif action == 4:
                help_4()
            elif action == 5:
                help_5()
            elif action == 6:
                help_6()
            elif action == 7:
                help_7()
            elif action == high:
                repeat = False
        if not try_again:
            repeat = ad.check_repeat_help()           


def help_menu_message():
    """Display the help menu options."""
    print('\nPlease enter the number for the item you would like help on:\n')
    print('1: Students Table')
    print('2: Tutors Table')
    print('3: Courses Table')
    print('4: Course Tutors Table')
    print('5: Enrolments Table')
    print('6: Graduates Table')
    print('7: Enrolments Table')
    print('8: Exit Help Menu')


def help_student_id():
    print('\nStudent_IDs.csv\n')
    print('Sourced From:\n')
    print('Students Table in the Students Database (Access).')
    print('\nDescription:\n')
    print('The list of students that are currently in the Student Database '
          '(Access). Compiled by exporting the data in the Students Table and '
          'then keeping the Student ID, First Name and Last Name columns.')
    print('\nColumns:\n')
    print('Student ID Number, First Name, Last Name')


def help_tutor_df():
    print('\nTutor Data File\n')
    print('Sourced From:\n')
    print('Tutors sheet of the Enrolments Google Sheet.')
    print('\nDescription:\n')
    print('Information for tutors that need to be added to the Student '
          'Database.')
    print('\nColumns:\n')
    print('TutorID, First Name, Last Name, Email, Phone')
    
    
def help_tutor_id():
    print('\nTutor.IDs.csv\n')
    print('Sourced From:\n')
    print('Tutors table in the Students Database (Access).')
    print('\nDescription:\n')
    print('The list of tutors that are currently in the Student Database '
          '(Access). Compiled by exporting the data in the Tutors Table and '
          'then keeping the Tutor ID, First Name, Last Name.')
    print('\nColumns:\n')
    print('Tutor ID, First Name, Last Name')


def load_data(source, f_name=''):
    """Read data from a CSV file.

    Args:
        source (str): The code for the table that the source data belongs to.
        f_name (str): (Optional) File name to be loaded. If not provided, user
        will be prompted to provide a file name.

    Returns:
        read_data (list): A list containing the data read from the file.
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.
    """
    read_data = []
    warnings = []
    # Load file
    if f_name in (None, ''): # Get from user
        read_data = ft.get_csv_fname_load(source)
    else:
        read_data = ft.load_csv(f_name, 'e')
    # Check that data has entries for each required column
    if source == 'ADV Assessments':
        # Update with required number of assessments if changed
        to_add, items_to_add = check_ass_data(read_data, 65)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Course Attendance':
        to_add, items_to_add = check_ca(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Course IDs':
        to_add, items_to_add = check_cc(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Course Data':
        to_add, items_to_add = check_cd(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Combined Data Form':
        to_add, items_to_add = check_cdf(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Course Tutors':
        to_add, items_to_add = check_ctd(read_data,
                                         'Course Tutor Data',
                                         'Course')
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Dates':
        to_add, items_to_add = check_da(read_data)
    elif source == 'Enrolment Codes':
        to_add, items_to_add = check_ec(read_data)
    elif source == 'Existing Course Tutors':
        to_add, items_to_add = check_ctd(read_data,
                                         'Course_Tutors.csv',
                                         'Course')
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Enrolment IDs':
        to_add, items_to_add = check_e_id_data(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Enrolment Sheet':
        to_add, items_to_add = check_es(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Existing Workshop Tutors':
        to_add, items_to_add = check_ctd(read_data,
                                         'Workshop_Tutors.csv',
                                         'Workshop')
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Extensions Data':
        to_add, items_to_add = check_ex(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Extension Codes':
        to_add, items_to_add = check_exc(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Graduates Current':
        to_add, items_to_add = check_gc(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Graduates Data':
        to_add, items_to_add = check_gd(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Old Students':
       to_add, items_to_add = check_os(read_data)
       if to_add:
           for item in items_to_add:
                warnings.append(item)
    elif source == 'Student ID Course Codes':
        to_add, items_to_add = check_scc(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Workshop Student IDs':
        to_add, items_to_add = check_swc(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Student ID Numbers':
        to_add, items_to_add = check_si(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Tutor Data':
        to_add, items_to_add = check_td(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Tutor IDs':
        to_add, items_to_add = check_tu(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Workshop Attendance':
        to_add, items_to_add = check_wa(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Workshop IDs':
        to_add, items_to_add = check_wc(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Workshop Data':
        to_add, items_to_add = check_wd(read_data)
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    elif source == 'Workshop Tutor Data':
        to_add, items_to_add = check_ctd(read_data,
                                         'Workshop Tutor Data',
                                         'Workshop')
        if to_add:
            for item in items_to_add:
                warnings.append(item)
    if len(warnings) > 0:
        return read_data, True, warnings
    else:
        return read_data, False, warnings


def main():
    repeat = True
    low = 1
    high = 16
    while repeat:
        try_again = False
        main_message()
        try:
            action = int(input('\nPlease enter the number for your '
                               'selection --> '))
        except ValueError:
            print('Please enter a number between {} and {}.'.format(low, high))
            try_again = True
        else:
            if int(action) < low or int(action) > high:
                print('\nPlease select from the available options ({} - {})'
                      .format(low, high))
                try_again = True
            elif action == low:
                help_menu()
                try_again = True
            elif action == 2:
                process_student_data()
            elif action == 3:
                process_tutors_data()
            elif action == 4:
                process_courses_data()
            elif action == 5:
                process_workshops_data()
            elif action == 6:
                process_course_tutors_data()
            elif action == 7:
                process_workshop_tutors_data()
            elif action == 8:
                process_enrolment_data()
            elif action == 9:
                process_course_attendance()    
            elif action == 10:
                process_workshop_attendance()
            elif action == 11:
                process_graduates()
            elif action == 12:
                process_old_student_data()
            elif action == 13:
                process_extensions_data()
            elif action == 14:
                process_adv()
            elif action == 15:
                process_find_students()
            elif action == high:
                print('\nIf you have generated any files, please find them '
                      'saved to disk. Goodbye.')
                sys.exit()
        if not try_again:
            repeat = ad.check_repeat()
    print('\nPlease find your files saved to disk. Goodbye.')


def main_message():
    """Print the menu of options."""
    print('\n\n*************==========================*****************')
    print('\nDatabase Preparer version 1.0')
    print('Created by Jeff Mitchell, 2018')
    print('\nOptions:')
    print('\n1 Help')
    print('2 Prepare Students Table Data')
    print('3 Prepare Tutors Table Data')
    print('4 Prepare Courses Table Data')
    print('5 Prepare Workshops Table Data')
    print('6 Prepare Course Tutors Table Data')
    print('7 Prepare Workshop Tutors Table Data')
    print('8 Prepare Enrolments Table Data')
    print('9 Prepare Course Attendance Table Data')
    print('10 Prepare Workshop Attendance Table Data')
    print('11 Prepare Graduates Table Data')
    print('12 Prepare Existing Students Table Data')
    print('13 Prepare Extensions Table Data')
    print('14 Prepare ADV Results Table Data')
    print('15 Find Students to add to Results Table')
    print('16 Exit')


def preferred_contact(mobile_pref, email_pref):
    """Return preferred contact mode.

    Examines the values for the mobile and email columns and returns the
    preferred contact mode. Could be 'Email', 'Mobile' or 'Email or Mobile'.

    Args:
        mobile_pref (str): 'Mobile' if mobile is preferred contact mode.
        email_pref (Str): 'Email' if email is preferred contact mode.

    Returns:
        preference (str): Preferred contact mode.
    """
    if mobile_pref.strip() == 'Mobile' and email_pref.strip() == 'Email':
        preference = 'Email or Mobile'
    elif mobile_pref.strip() == 'Mobile' and email_pref.strip() != 'Email':
        preference = 'Mobile'
    elif mobile_pref.strip() != 'Mobile' and email_pref.strip() == 'Email':
        preference = 'Email'
    elif mobile_pref.strip() != 'Mobile' and email_pref.strip() != 'Email':
        preference = ''
    return preference


def process_adv():
    """To Be written"""
    

def process_adv_archive():
    """Prepare upload file for ADV assessments."""
    # TO BE REWRITTEN
    warnings = ['\nProcessing ADV Assessment Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing ADV Assessments.')
    # Confirm the required files are in place
    required_files = ['Course Assessment Data File', 'adv_assessments',
                      'enrolment_ids.csv']
    ad.confirm_files('Course Assessment Data', required_files)
    # Load adv_assessments file (list of assessment names)
    adv_ass_data, to_add, warnings_to_add = load_data('ADV Assessments',
                                                      'adv_assessments')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Convert Assessment Names to a list of names
    ass_names_listed = ad.extract_lists(adv_ass_data)
    # print('\nClean Assessment Names: {}'.format(ass_names_listed))
    # Load course assessment data file (student results)
    
    results_data, to_add, warnings_to_add = load_data('Student_Results_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # print(results_data)
    # Load list of enrolment details. Used to check correct e_id entered
    e_id_name = 'enrolment_ids'
    e_id_data, to_add, warnings_to_add = load_data('Enrolment IDs', e_id_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get student enrolment ID (user input)
    e_id = input('\nWhat is the Enrolment ID for the student? --> ')
    # Check that enrolment ID is correct and get Student ID, First Name and Last Name
    e_id, s_id, s_fn, s_ln = validate_e_id(e_id, e_id_data)
    # Get from course assessment data just the rows that contain assessments
    cleaned_results = clean_results(results_data, ass_names_listed) 
    # Look for item[0] to be in adv_assessments
    # print(cleaned_results)
    # Process data to get info for student
    upload_data = get_results_upload_data(cleaned_results, e_id)
    # print(upload_data)
    headings = get_headings('ADV')
    f_name = '{}_{}_{}_Grades_Upload_File.txt'.format(s_id, s_fn, s_ln)
    # Save upload data to a text file
    ft.save_list_to_text_single(upload_data, headings, f_name)
    # Display output so user can check without opening file
    print('\nText output:\n')
    print(upload_data)
    ft.process_warning_log(warnings, warnings_to_process)


def process_course_attendance():
    """Process a Course Attendance Table upload form.

    Loads the course attendance data file and processes it.
    Saves the processed data to a file for uploading to the Course
    attendance table in the student database.
    """
    warnings = ['\nProcessing Course Attendance Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Course Attendance Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Course Attendance Data File', 'Student-Course File',
                      'dates.csv', 'Course_IDs.csv']
    ad.confirm_files('Course Attendance Data', required_files)
    # Get name for Course Attendance Data File and then load
    att_data, to_add, warnings_to_add = load_data('Course Attendance')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load the Student ID and Course Codes combinations
    # Used to make sure the Course Code and Student ID Number combination is
    # correct
    scc_file_name = 'scc'
    scc_data, to_add, warnings_to_add = load_data('Student ID Course Codes',
                                                  scc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Get name for Dates Data File and then load
    date_data, to_add, warnings_to_add = load_data('Dates')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load Course ID Numbers
    cc_file_name = 'Course_IDs'
    cc_data, to_add, warnings_to_add = load_data('Course IDs', cc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Course Codes data
    cleaned_cc = clean_cc(cc_data)
    # Get the course code to be processed
    course = input('What is the code for the course being processed? --> ')
    # Check that is an actual course
    check_valid_course(cleaned_cc, course, 0, 'Course_Codes')
    # ad.debug_list(att_data)
    # ad.debug_list(date_data)
    # Clean the dates data
    cleaned_date_data = clean_pt_dates(date_data)
    # print(cleaned_date_data)
    # Check that each student is actually enrolled in the course
    to_add, warnings_to_add = check_valid_scc(att_data, scc_data, course, 0, 
                                              'Course_Attendance_Data_')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
        print('\nWarning! Some of the students do not have the correct Course '
              'code. Please review the warnings file. If the student has '
              'transferred course and this is their old course that is being '
              'updated, you can ignore this warning. Otherwise, please correct'
              ' the file before processing again.')
    # Create data for file upload
    save_data, headings = get_attendance_upload(att_data, cleaned_date_data,
                                                course)
    ft.save_lists_to_text(save_data, headings, 'Course_Attendance_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_courses_data():
    """Process a Course Table upload form.

    Loads the course data file and processes it.
    Saves the processed data to a file for uploading to the Courses table in
    the student database.
    """
    warnings = ['\nProcessing Courses Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Courses Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Courses Data File', 'Course_IDs.csv']
    ad.confirm_files('Course Data', required_files)
    # Get name for Course Data File and then load
    course_data, to_add, warnings_to_add = load_data('Course Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the course data
    cleaned_courses = clean_cd(course_data)
    # print('Check cleaned courses data:')
    # ad.debug_list(cleaned_courses)
    # Load Course Codes
    cc_file_name = 'Course_IDs'
    cc_data, to_add, warnings_to_add = load_data('Course IDs', cc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Course Codes data
    cleaned_cc = clean_cc(cc_data)
    # Check that each Course is unique
    # print('Checking cleaned_cc:')
    # ad.debug_list(cleaned_cc)
    # print('Checking course codes are unique')
    check_unique(cleaned_cc, cleaned_courses, 0, 0, 'Course Data',
                 'Course code')
    # Get course data for file
    save_data, headings = get_course_data(cleaned_courses)
    # Save Course Data Upload file
    ft.save_lists_to_text(save_data, headings, 'Course_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_course_tutors_data():
    """Process a Course-Tutors Table upload form.

    Loads the course-tutors data file and processes it.
    Saves the processed data to a file for uploading to the Course-tutors table
    in the student database.
    """
    warnings = ['\nProcessing Course Tutors Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Course Tutors Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Course Tutors Data File', 'Course_Tutors.csv',
                      'Course_IDs.csv', 'Tutor_IDs.csv']
    ad.confirm_files('Course Tutor Data', required_files)
    # Get name for Course Tutor Data File and then load
    ct_data, to_add, warnings_to_add = load_data('Course Tutors')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the course-tutors data
    cleaned_ct_data = clean_ctd(ct_data)
    # print('cleaned_ct_data:')
    # ad.debug_list(cleaned_ct_data)
    # Check that each course exists already
    cc_file_name = 'Course_IDs'
    cc_data, to_add, warnings_to_add = load_data('Course IDs', cc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Course Codes data
    cleaned_cc = clean_cc(cc_data)
    check_present(cleaned_cc, cleaned_ct_data, 0, 0,
                  'Course Tutor Data', 'Course code')
    # Check that each Tutor exists already
    tu_file_name = 'Tutor_IDs'
    tu_data, to_add, warnings_to_add = load_data('Tutor IDs', tu_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    clean_tutor_ids = clean_tu(tu_data)
    # print('clean_tu_data:')
    # ad.debug_list(clean_tutor_ids)
    check_present(clean_tutor_ids, cleaned_ct_data, 0, 1,
                  'Course Tutors Data', 'Tutor ID')
    # Load existing Course-Tutor pairings
    ect_file_name = 'Course_Tutors'
    ect_data, to_add, warnings_to_add = load_data('Existing Course Tutors',
                                                  ect_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Course Codes data
    cleaned_ect = clean_ctd(ect_data)
    # Check that each Course-Tutor pairing is unique
    check_source_tutor_unique(cleaned_ct_data, cleaned_ect,
                              'Course-Tutors Data')
    # Get data for save file
    save_data, headings = get_course_tutor_data(cleaned_ct_data)
    # Save the data
    ft.save_lists_to_text(save_data, headings, 'Course_Tutors_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_enrolment_data():
    """Process an Enrolment Table upload form.

    Loads the enrolment data file and processes it.
    Saves the processed data to a file for uploading to the Enrolments table
    in the student database.
    """
    warnings = ['\nProcessing Enrolment Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Enrolment Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Enrolment Data', 'Student_IDs.csv', 'Tutor_ID.csv',
                      'Course_IDs.csv']
    ad.confirm_files('Enrolment Data', required_files)
    # Get name for Enrolment Sheet data and then load
    es_data, to_add, warnings_to_add = load_data('Enrolment Sheet')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Enrolment Sheet file
    cleaned_es = clean_es(es_data)
    # Load the Student ID Numbers
    si_file_name = 'Student_IDs'
    si_data, to_add, warnings_to_add = load_data('Student ID Numbers', 
                                                 si_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Check that students are already present in the Student ID list
    check_present(si_data, cleaned_es, 0, 0,
                  'Enrolment_Sheet_ID_Student', 'Student ID')
    # Load the Tutor ID Numbers
    tu_file_name = 'Tutor_IDs'
    tu_data, to_add, warnings_to_add = load_data('Tutor IDs', tu_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    enrolment_data, headings = get_enrolment_data(cleaned_es)
    # Replace Tutor name with Tutor ID
    to_add, warnings_to_add, updated_es = replace_tutors(enrolment_data,
                                                         tu_data)
    # Check that Tutors are present in the list
    check_present(tu_data, updated_es, 0, 3, 'Enrolment_Sheet_Tutor_ID',
                  'Tutor ID')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load Course ID Numbers
    cc_file_name = 'Course_IDs'
    cc_data, to_add, warnings_to_add = load_data('Course IDs', cc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Course Codes data
    cleaned_cc = clean_cc(cc_data)
    # Check that course codes are already present in the list
    check_present(cleaned_cc, enrolment_data, 0, 2,
                  'Enrolment Data', 'Course code')
    # Save Enrolment Data upload file
    ft.save_lists_to_text(updated_es, headings, 'Enrolment_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_extensions_data():
    """Process an Extensions Table upload form.
    
    Loads the extensions data file and processes it.
    Saves the processed data to a file for uploading to the Extensions table
    in the student database.
    """
    warnings = ['\nProcessing Extensions Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Extensions Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Extensions Data', 'Enrolment_Codes.csv',
                      'Extension_Codes.csv']
    ad.confirm_files('Extensions Data', required_files)
    # Get name for Extensions data and then load
    ext_data, to_add, warnings_to_add = load_data('Extensions Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Extensions Data file
    cleaned_ext = clean_ext(ext_data)
    # Load the Extensions table enrolment codes and acceptance dates
    # Used to make sure the extension is not already contained in the
    # Extensions table
    exc_file_name = 'Extension_Codes'
    exc_data, to_add, warnings_to_add = load_data('Extension Codes',
                                                  exc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Extensions Codes Data file
    cleaned_exc = clean_exc(exc_data)
    # Load the Student ID and Enrolment Codes combinations
    # Used to make sure the Enrolment Code and Student ID Number combination is
    # correct
    ec_file_name = 'Enrolment_Codes'
    ec_data, to_add, warnings_to_add = load_data('Enrolment Codes',
                                                 ec_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Enrolment Codes Data file
    cleaned_ec = clean_ec(ec_data)
    # Check that Enrolment Code and Acceptance Date combination is not already
    # in the Extensions Table
    # print(cleaned_exc)
    check_unique_extension(cleaned_exc, cleaned_ext, 0, 1, 1, 3)
    # Check that Student ID and Enrolment Code combinations are valid
    check_valid_stud(cleaned_ext, cleaned_ec, 1, 0, 'Extensions_Data')
    # Prepare the data to be saved
    updated_ext, headings = get_ext_data(cleaned_ext)
    # Save Extensions Data upload file
    ft.save_lists_to_text(updated_ext, headings, 'Extensions_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_find_students():
    """To be written"""


def process_graduates():
    """Process a Graduates Table upload form.
    
    Loads the graduate data file and processes it.
    Saves the processed data to a file for uploading to the Graduates table
    in the student database.
    """
    warnings = ['\nProcessing Graduate Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Graduate Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Graduate Data', 'Enrolment_Codes.csv',
                      'Graduates_Current.csv']
    ad.confirm_files('Graduate Data', required_files)
    # Get name for Graduate data and then load
    grad_data, to_add, warnings_to_add = load_data('Graduates Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Graduates Data file
    cleaned_gd = clean_gd(grad_data)
    # Load the Graduates table enrolment codes
    # Used to make sure the Enrolment Code is not already contained in the
    # Graduates table
    gc_file_name = 'Graduates_Current'
    gc_data, to_add, warnings_to_add = load_data('Graduates Current',
                                                 gc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Graduates Current Data file
    cleaned_gc = clean_gc(gc_data)
    # Load the Student ID and Enrolment Codes combinations
    # Used to make sure the Enrolment Code and Student ID Number combination is
    # correct
    ec_file_name = 'Enrolment_Codes'
    ec_data, to_add, warnings_to_add = load_data('Enrolment Codes',
                                                 ec_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the data in the Enrolment Codes Data file
    cleaned_ec = clean_ec(ec_data)
    # Check that Enrolment Code is not already in the Graduates Table
    check_unique(cleaned_gc, cleaned_gd, 1, 1, 'Graduates Data',
                 'Enrolment Code')   
    # Check that Student ID and Enrolment Code combinations are valid
    check_valid_stud(cleaned_gd, cleaned_ec, 1, 0, 'Graduates_Data')
    # Prepare the data to be saved
    updated_gd, headings = get_gd_data(cleaned_gd)
    # Save Graduates Data upload file
    ft.save_lists_to_text(updated_gd, headings, 'Graduate_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_old_student_data():
    """Process a Students Table upload form (existing students).

    Loads the enrolment data file and processes it.
    Saves the processed data to a file for uploading to the Enrolments table
    in the student database.
    """
    warnings = ['\nProcessing Existing Student Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Existing Student Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Old Students Enrolment Data File', 'Student_IDs.csv']
    ad.confirm_files('Student Data', required_files)
    # Get name for Old Students Enrolment Data File and then load
    os_data, to_add, warnings_to_add = load_data('Old Students')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # ad.debug_list(os_data)
    # Load the Student ID Numbers
    si_file_name = 'Student_IDs'
    si_data, to_add, warnings_to_add = load_data('Student ID Numbers',
                                                 si_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # print('Loaded Student IDs ok')
    # Clean os_data
    cleaned_os = clean_os(os_data)
    # Clean the data in the Enrolment Sheet file
    # Check each student is not already in the database
    check_unique(si_data, cleaned_os, 0, 0, 'Old_Students_ID', 'Student ID')
    # Create Student data upload file
    headings = ('StudentPK,NameGiven,NameSurname,NamePreferred,DateOfBirth,'
                'Username,Telephone,Mobile,Email,PreferredContactMode,'
                'AddressNumber,AddressStreet,AddressSuburb,AddressCity,'
                'AddressPostcode,AddressCountry,Nationality,Iwi,Citizenship,'
                'GuardianNameGiven,GuardianNameSurname,GuardianId,Under18Auth,'
                'HowHeard,AgreeTandC,EnrolmentDate,Gender,Ethnicity,'
                'CountryOfBirth,Language,Disability,PreviousEducation,'
                'PreviousEdYear, Employment,ReasonForStudy')
    # Save Student data upload file
    ft.save_lists_to_text(cleaned_os, headings, 'Old_Student_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_student_data():
    """Process a Students Table upload form.

    Loads the enrolment data file and processes it.
    Saves the processed data to a file for uploading to the Enrolments table
    in the student database.
    """
    warnings = ['\nProcessing Student Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Student Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Combined Data File', 'Enrolment Data Sheet',
                      'Course_IDs.csv', 'Student_IDs.csv']
    ad.confirm_files('Student Data', required_files)
    # Get name for Combined Data form and then load
    cdf_data, to_add, warnings_to_add = load_data('Combined Data Form')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # ad.debug_list(cdf_data)
    # Get name for Enrolment Sheet data and then load
    es_data, to_add, warnings_to_add = load_data('Enrolment Sheet')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load Course Codes
    cc_file_name = 'Course_IDs'
    cc_data, to_add, warnings_to_add = load_data('Course IDs', cc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Course Codes data
    cleaned_cc = clean_cc(cc_data)
    # print('cleaned cc data ok')
    # Load the Student ID Numbers
    si_file_name = 'Student_IDs'
    si_data, to_add, warnings_to_add = load_data('Student ID Numbers',
                                                 si_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # print('Loaded Student IDs ok')
    # Create a dictionary with the Course Codes
    course_codes = create_codes(cleaned_cc)
    # print('Cleaned course codes successfully')
    # ad.debug_dict(course_codes)
    # Process cdf data into desired columns
    cleaned_cdf = clean_cdf(cdf_data, course_codes)
    # Clean the data in the Enrolment Sheet file
    # Check each student is not already in the database
    check_unique(si_data, cleaned_cdf, 0, 0, 'Combined_Data_Form_ID',
                 'Student ID')
    # print('checked students cdf')
    cleaned_es = clean_es(es_data)
    # print('cleaned es')
    # Compare data from CDF and ES to make sure they are consistent
    to_add, warnings_to_add = compare_cdf_es(cleaned_cdf, cleaned_es)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Create Student data upload file
    student_data, headings = get_student_data(cleaned_cdf, cleaned_es)
    # Save Student data upload file
    ft.save_lists_to_text(student_data, headings, 'Student_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_tc(user_response):
    """Return the Terms and Conditions value.

    If there is a value in the Terms and Conditions column then it returns
    'Yes' as this indicates that the box has been ticked. If there is no value
    then it returns 'No' as this indicates it has not been ticked.

    Args:
        user_response (str): Value from the Terms and Conditions column.

    Returns:
        t_and_c (str): Value for Terms and conditions. Can be either 'Yes' or
        'No'.
    """
    if user_response not in (None, ''):
        t_and_c = 'Yes'
    else:
        t_and_c = 'No'
    return t_and_c


def process_tutors_data():
    """Process a Tutors Table upload form.

    Loads the tutors data file and processes it.
    Saves the processed data to a file for uploading to the Tutors table
    in the student database.
    """
    warnings = ['\nProcessing Tutors Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Tutor Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Tutor Data File', 'Tutor_IDs.csv']
    ad.confirm_files('Tutor Data', required_files)
    # Get name for Tutor Data and then load
    tutor_data, to_add, warnings_to_add = load_data('Tutor Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean Tutor Data File
    clean_tutor_data = clean_td(tutor_data)
    # Load the Tutor ID Numbers
    tu_file_name = 'Tutor_IDs'
    tu_data, to_add, warnings_to_add = load_data('Tutor IDs', tu_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean Tutor_IDs.csv
    clean_tutor_ids = clean_tu(tu_data)
    # Check Tutor ID not already in Tutor_IDs.csv
    check_unique(clean_tutor_ids, clean_tutor_data, 0, 0, 'Tutor Data File',
                 'Tutor ID')
    # Save Tutor Upload file
    headings = 'TutorPK,TFirstName,TLastName,TEmail,TPhoneNumber'
    ft.save_lists_to_text(clean_tutor_data, headings, 'Tutor_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_workshop_attendance():
    """Process a Workshop Attendance Table upload form.
    
    Loads the workshop attendance data file and processes it.
    Saves the processed data to a file for uploading to the Course
    attendance table in the student database.
    """
    warnings = ['\nProcessing Workshop Attendance Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Workshop Attendance Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Workshop Attendance Data File', 'Student-Workshop File',
                      'Workshop_IDs.csv']
    ad.confirm_files('Workshop Attendance Data', required_files)
    # Get name for Workshop Attendance Data File and then load
    att_data, to_add, warnings_to_add = load_data('Workshop Attendance')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load the Student ID and Workshop Codes combinations
    # Used to make sure the Workshop Code and Student ID Number combination is
    # correct
    swc_file_name = 'swc'
    swc_data, to_add, warnings_to_add = load_data('Workshop Student IDs',
                                                  swc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Load Workshop ID Numbers
    wc_file_name = 'Workshop_IDs'
    wc_data, to_add, warnings_to_add = load_data('Workshop IDs', wc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Workshop Codes data
    cleaned_wc = clean_wc(wc_data)
    # Extract codes into a list
    wc_list = ad.extract_list_item(cleaned_wc, 0)
    # Check the Student-Workshop data is valid
    validate_swc(swc_data, wc_list)
    # Check the Workshop Attendance data is valid
    validate_wa(att_data, swc_data, 0, 1, 1, 0)
    # Clean the Workshop attendance data
    cleaned_wa = clean_wa(att_data)
    # Create data for file upload
    headings = 'AttendancePK,StudentFK,WorkshopFK'    
    ft.save_lists_to_text(cleaned_wa, headings, 'Workshop_Attendance_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_workshops_data():
    """Process a Workshops Table upload form.

    Loads the workshops data file and processes it.
    Saves the processed data to a file for uploading to the Workshops table
    in the student database.
    """
    warnings = ['\nProcessing Workshops Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Workshops Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Workshops Data File', 'Workshops_IDs.csv']
    ad.confirm_files('Workshops Data', required_files)
    # Get name for Workshops Data File and then load
    workshops_data, to_add, warnings_to_add = load_data('Workshop Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the workshop data
    cleaned_workshops = clean_wd(workshops_data)
    # print('Check cleaned workshops data:')
    # ad.debug_list(cleaned_workshops)
    # Load Workshop Codes
    wc_file_name = 'Workshop_IDs'
    wc_data, to_add, warnings_to_add = load_data('Workshop IDs', wc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Workshop Codes data
    cleaned_wc = clean_wc(wc_data)
    # Check that each Course is unique
    # print('Checking cleaned_wc:')
    # ad.debug_list(cleaned_wc)
    # print('Checking workshop codes are unique')
    check_unique(cleaned_wc, cleaned_workshops, 0, 0, 'Workshop Data',
                 'Workshop ID')
    # Get workshop data for file
    save_data, headings = get_workshop_data(cleaned_workshops)
    # Save Workshop Data Upload file
    ft.save_lists_to_text(save_data, headings, 'Workshop_Data_')
    ft.process_warning_log(warnings, warnings_to_process)


def process_workshop_tutors_data():
    """Process a Workshop-Tutors Table upload form.

    Loads the workshop-tutors data file and processes it.
    Saves the processed data to a file for uploading to the Workshop-tutors
    table in the student database.
    """
    warnings = ['\nProcessing Workshop Tutors Data Warnings:\n']
    warnings_to_process = False
    print('\nProcessing Workshop Tutors Data Upload Form.')
    # Confirm the required files are in place
    required_files = ['Workshop Tutors Data File', 'Workshop_Tutors.csv',
                      'Workshop_IDs.csv', 'Tutor_Ids.csv']
    ad.confirm_files('Workshop Tutor Data', required_files)
    # Get name for Workshop Tutor Data File and then load
    wt_data, to_add, warnings_to_add = load_data('Workshop Tutor Data')
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the workshop-tutors data
    cleaned_wt_data = clean_ctd(wt_data)
    # print('cleaned_wt_data:')
    # ad.debug_list(cleaned_wt_data)
    # Check that each Workshop exists already
    wc_file_name = 'Workshop_IDs'
    wc_data, to_add, warnings_to_add = load_data('Workshop IDs', wc_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Workshop Codes data
    cleaned_wc = clean_cc(wc_data)
    check_present(cleaned_wc, cleaned_wt_data, 0, 0,
                  'Workshop Tutor Data', 'Workshop code')
    # Check that each Tutor exists already
    tu_file_name = 'Tutor_IDs'
    tu_data, to_add, warnings_to_add = load_data('Tutor IDs', tu_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    clean_tutor_ids = clean_tu(tu_data)
    # print('clean_tu_data:')
    # ad.debug_list(clean_tutor_ids)
    check_present(clean_tutor_ids, cleaned_wt_data, 0, 1,
                  'Workshop Tutors Data', 'Tutor ID')
    # Load existing Workshop-Tutor pairings
    ewt_file_name = 'Workshop_Tutors'
    ewt_data, to_add, warnings_to_add = load_data('Existing Workshop Tutors',
                                                  ewt_file_name)
    if to_add:
        warnings_to_process = True
        for line in warnings_to_add:
            warnings.append(line)
    # Clean the Workshop Codes data
    cleaned_ewt = clean_ctd(ewt_data)
    # Check that each Workshop-Tutor pairing is unique
    check_source_tutor_unique(cleaned_wt_data, cleaned_ewt, 'Workshop-Tutors '
                              + 'Data')
    # Get data for save file
    save_data, headings = get_workshop_tutor_data(cleaned_wt_data)
    # Save the data
    ft.save_lists_to_text(save_data, headings, 'Workshop_Tutors_Data_')
    ft.process_warning_log(warnings, warnings_to_process)
    return


def replace_tutors(old_es, tutor_data):
    """Replace Tutor Name with Tutor ID.

    Args:
        old_es (list): List containing data from the enrolment sheet.
        tutor_data (list): List of tutor names and ID numbers.

    Returns:
        True if warnings list has had items appended to it, False otherwise.
        warnings (list): Warnings that have been identified in the data.
        new_es (list): Enrolment sheet data with the Tutor names replaced by
        Tutor IDs.

    File Structure (old_es):
        EnrolmentPK, StudentFK, CourseFK, TutorFK, StartDate, ExpiryDate,
        Status

    File Structure (tutor_data):
        TutorID, FirstName, LastName.
    """
    new_es = copy.deepcopy(old_es)
    warnings = ['\nTutor Data Warnings:\n']
    errors = []
    # Clean the data in the Tutor file
    # print('Replace_tutors input data:')
    # ad.debug_list(tutor_data)
    cleaned_tu = clean_tu(tutor_data)
    # Place Tutors into a dictionary
    tutors = tutors_to_dict(cleaned_tu)
    # Replace tutor names with Tutor IDs
    i = 0
    while i < len(new_es):
        # Skip if no Tutor provided
        if new_es[i][3] not in (None, ''):
            tutor_found = False
            for tutor_ID, tutor_name in tutors.items():
                if new_es[i][3].lower().strip() == 'tbc':
                    warnings.append('Tutor is \'tbc\' for student {}'.format(
                            new_es[i][1]))
                    new_es[i][3] = ''
                    tutor_found = True
                    break
                elif new_es[i][3] == tutor_name:
                    new_es[i][3] = tutor_ID
                    tutor_found = True
                    break
                else:
                    continue
            if not tutor_found:
                errors.append('Could not find the tutor {} for student {}.'
                              .format(new_es[i][3], new_es[i][1]))
        i += 1
    if len(errors) > 0:
        ft.process_error_log(errors, 'Enrolment_Data_Tutors')
    if len(warnings) > 1:
        return True, warnings, new_es
    else:
        return False, warnings, new_es


def tutors_to_dict(cleaned_tu):
    """Create a dictionary with tutors from a list.

    Args:
        cleaned_tu (list): List of tutors.

    Returns:
        tutor_dict (dict): Dictionary with tutors.
    """
    tutor_dict = {}
    for tutor in cleaned_tu:
        key = tutor[0]
        value = '{} {}'.format(tutor[1], tutor[2])
        tutor_dict[key] = value
    # ad.debug_dict(tutor_dict)
    return tutor_dict


def validate_wa(att_data, swc_data, swc_si_pos, swc_wi_pos, att_si_pos,
                           att_wi_pos):
    """Check each student-workshop pairing is unique.
    
    Checks that the combination of Student ID and WorkshopID are not already
    in the database. If any errors are found, error log is processed and the
    program exits.
    
    Args:
        att_data (list): The list of pairings to be checked (in the submitted
                         data).
        swc_data (list): The list of pairings currently in the database.
        swc_si_pos (int): Position of StudentID in swc_data data.
        swc_wi_pos (int): Position of WorkshopID in swc_data data.
        att_si_pos (int): Position of StudentID Code in data to be checked.
        att_wi_pos (int): Position of WorkshopID in data to be checked.
    
    Returns:
        True if data is valid. Processes error log if data is invalid and then
        exits.
        
    File structure (att_data):
        WorkshopFK, StudentFK, First Name, Last Name.
        
    File structure (swc_data):
        StudentFK, WorkshopFK       
    """
    errors = []
    i = 0
    # Check each pair in att_data
    while i < len(att_data):
        # Extract Student ID from att_data
        si_att = att_data[i][att_si_pos]
        # Extract Workshop ID from att_data
        wi_att = att_data[i][att_wi_pos]
        # Look for Student ID in existing data
        j = 0
        found = False
        while j < len(swc_data) and not found:
            # Extract Student ID from swc_data
            si_swc = swc_data[j][swc_si_pos]
            # Extract Workshop ID from swc_data
            wi_swc = swc_data[j][swc_wi_pos]
            if si_swc == si_att:
                # Student ID is found in existing data
                # Check if Workshop ID also matches
                if wi_swc == wi_att:
                    # Workshop ID also matches - duplicate
                    found = True
                    errors.append('The combination of Student ID {} and '
                                  'Workshop ID {} already exists in the '
                                  'Student Database. Please correct the data '
                                  'and try again.'.format(si_att, wi_att))
            # Combination not found, try the next row in existing data
            j += 1
        # Check the next row in the data to be checked
        i += 1
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Workshop_Attendance_Data')


def validate_e_id(e_id, e_id_data):
    """Check Enrolment ID is valid and for the desired student.

    Checks that the Enrolment ID is a valid Enrolment ID. If not, asks user to
    enter a valid Enrolment ID before progressing. Displays the details of the
    entered Enrolment ID to make sure that it is the correct student. If user
    cannot provide a valid Enrolment ID, they are given the option to quit.

    Args:
        e_id (str): Enrolment ID to be checked.
        e_id_data (list): Enrolment data for all students.
    
    Returns:
        enrolment_id (str): Correct EnrolmentID.
    """
    # print(e_id_data)
    # Check that e_id is in the e_id_data
    found = False
    stud_id = ''
    stud_fname = ''
    stud_lname = ''
    while not found:
        reattempt = False
        for student in e_id_data:
            # Student found
            if student[0] == e_id:
                # Confirm it is the desired student
                print('\nThese are the details for the student with the '
                      'Enrolment ID {}. Please confirm that this is the '
                      'correct student.\n'.format(e_id))    
                print(student)
                valid_response = False
                while not valid_response:
                    correct = input('\nIs this the correct student (y/n)? '
                                    '--> ')
                    if correct.lower() not in ('y', 'n'):
                        print('\nThat is not a valid response. Please enter '
                              'either \'y\' or \'n\'. --> ')
                    elif correct.lower() == 'y':
                        valid_response = True
                        found = True
                        enrolment_id = e_id
                        stud_id = student[1]
                        stud_fname = student[2]
                        stud_lname = student[3]
                        break
                    # Response is 'n': get a new enrolment ID
                    else:
                        print('\nPlease enter the correct Enrolment ID or '
                              'enter \'quit\' to exit.')
                        e_id = input('\nWhat is the Enrolment ID for the '
                                     'student? --> ')
                        valid_response = True
                        reattempt = True
                        if e_id.lower() == 'quit':
                            print('\nNo data has been saved.')
                            sys.exit()
        # Student not found
        # Prevent a reattempt automatically stating new e_id cannot be found
        if not reattempt:
            if not found:
                print('\nEnrolment ID {} could not be found. Please enter the '
                      'correct Enrolment ID or enter \'quit\' to exit.'.format(
                              e_id))
                e_id = input('\nWhat is the Enrolment ID for the student? '
                             '--> ')
                if e_id.lower() == 'quit':
                    print('\nNo data has been saved.')
                    sys.exit()
    return enrolment_id, stud_id, stud_fname, stud_lname


def validate_swc(swc_data, wc_list):
    """Check data in the Student-Workshop codes file is valid.
    
    Checks that the Workshop Code is valid and that the Student ID is of a
    valid length (9). If any errors are found, error log is processed
    and the program exits. 
    
    Args:
        swc_data (list): Workshop ID and Student ID combinations.
        wc_list (list): List of Workshop IDs in the database.
    
    File structure (swc_data):
        StudentFK, WorkshopFK
    """
    errors = []
    for student in swc_data:
        # Check Workshop Code is valid
        if student[1] not in wc_list:
            errors.append('Workshop ID Number {} is invalid!'.format(
                    student[1]))
        # Check Student ID is correct
        if student[0] in (None, ''):
            errors.append('Student ID Number is missing for an entry')
        elif len(student[0]) != 9:
            errors.append('Student ID Number incorrect length for student '
                          '{}'.format(student[0]))
    # Check if any errors have been identified, save error log if they have
    if len(errors) > 0:
        ft.process_error_log(errors, 'Student_Workshop_Data')
    return


if __name__ == '__main__':
    main()
