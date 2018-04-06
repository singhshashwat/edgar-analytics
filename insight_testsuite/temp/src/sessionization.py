# Library function import
import os
import sys
from collections import OrderedDict     #Package to create odered dictionary
from datetime import datetime, timedelta
import csv

file_odict = OrderedDict()  #  Dictionary object
dattimeformat = '%Y-%m-%d %H:%M:%S'  # Date time format


def checkfile(file_log, file_inacttime, file_outsess):
    if os.path.isfile(file_log) == False:
        print("Unable to find Log File at :" + file_log + ".\n Program terminating session.")
        exit()

    if os.path.isfile(file_inacttime) == False:
        print("Unable to find Inactive time File at :" + file_inacttime + ".\n Program terminating session.")
        exit()

    if os.path.isfile(file_outsess) == False:
        try:
            print('Creating File at :', file_outsess)
        except (NameError, ValueError, FileNotFoundError):
            print('Error in Output \n Program terminating')
            exit()
    else:
        print('File with same name found and updating')


# Dont have to update same file based on user input

# if os.path.isfile(file_outsess)==True:
# 	warnmsg = "file with same name detected "
# 	print(warnmsg)
# 	a = str(input('please select y or n',))
# 	print(a)
#
# 	if a==('y'or'Y'):
# 		pass
# 	else:
# 		exit()


# Function to Read CSV file as Dictionary
def readcsvfile(file_name):
    f = open(file_name, 'r')
    reader = csv.DictReader(f)   # Read as dictionary
    return (reader)
    file.close()



#Function to print output string

def outputstring(key, file_odict):
    output_string = ",".join([key,  # IP address
                              file_odict[key]['entry_date'].strftime(dattimeformat),  # Date/time of first request
                              file_odict[key]['exit_date'].strftime(dattimeformat),  # Date/time of last request
                              str(file_odict[key]['duration']),
                              str(file_odict[key]['file_count'])]) + '\n'
    return output_string




def main():

    try:
        INPUT_PATH =  sys.argv[1]
        OUTPUT_PATH =  sys.argv[3]
        INACTIVITY_PATH = sys.argv[2]
    except(IndexError):
        print("Please provide appropiate path 'Index Error' \n Program Terminating")
        exit()

    checkfile(INPUT_PATH ,INACTIVITY_PATH,OUTPUT_PATH)


    # Open inactivity_period.txt and extract the inactivity period
    with open(INACTIVITY_PATH, "r") as file_open:
        # inactivity_period1 = int(fo.read())
        inactivity_period = timedelta(seconds=(int(file_open.read())))
    # Clear the output file
    with open(OUTPUT_PATH, "w+") as file_open:
        file_open.write("")


        file_read = readcsvfile(INPUT_PATH)  # Read Input log.csv file
        time_previous = 0
        # Start scanning through each line in the CSV
        for row in file_read:
            ip = row['ip']
            datt = row['date'] + ' ' + row['time']
            time_present = datetime.strptime(datt, dattimeformat)
            # If ip is already present dict will be updated
            if ip in file_odict:
                file_odict[ip]['file_count'] += 1
                file_odict[ip]['exit_date'] = time_present
                file_odict[ip]['duration'] = int(
                    (file_odict[ip]['exit_date'] - file_odict[ip]['entry_date']).total_seconds()) + 1
            # If it is not present in dictionary  then add it to the dictionary
            else:
                file_odict[ip] = {'entry_date': time_present, 'exit_date': time_present, 'duration': 1, 'file_count': 1}
                # check for lapsed time if any
            if (time_present != time_previous):
                time_previous = time_present

                for key in list(file_odict.keys()):
                    # Time to close a session  if greater than inactivity_period
                    if time_present - file_odict[key]['exit_date'] > inactivity_period:
                        # Append entry to Outputfile and write it
                        with open(OUTPUT_PATH, "a+") as file_out:
                            file_out.write(outputstring(key, file_odict))
                        file_odict.pop(key)



        # File end all ip session closed and added to output file

        with open(OUTPUT_PATH, "a+") as file_out:
            for key in file_odict:
                file_out.write(outputstring(key, file_odict))


#Main Function
if __name__ == "__main__":
    main()