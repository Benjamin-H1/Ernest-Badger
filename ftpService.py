import ftplib
import os
import sys
from datetime import date


class FTPDownload:
    # Procedure to download all files specified
    # files - List of files on server to be downloaded
    # conn - The connection to the server to download from
    def download(files, conn):
        wd = os.getcwd()
        os.chdir(wd+"/allFiles") #Changing the working directory to files so the files are stored in the right place
        for filename in files:
            with open(filename, "wb") as file:
                print("Downloading ", filename)
                conn.retrbinary(f"RETR {filename}", file.write)
                print("Downloaded ", filename)
        os.chdir(wd)

    # Function to establish connection to the server
    # address - The IP address of the server
    # port - The port the server is running on. At present not required but may be
    #   useful in the future
    # login - The login username
    # password - The password accompanying the login
    # Returns the connection for use in scanning and downloading files, in the event
        # of failure to connect it returns false so as to alert the system of a
        # failure to connect
    def connect(address, port, login, password):
        print("Hi")
        try:
            conn = ftplib.FTP(address, login, password)
            return conn
        except:
            return False

    # Function to locate files on the server matching the user's criteria
    # conn - The connection to the server
    # instruction - What sort of search is required
    # year - The year to search
    # month - The month to search
    # day - The day to search
    # hour - The hour to search
    # second - The second to search
    def find(conn, instruction, year=None, month=None, day=None, hour=None, minute=None, second=None):
        files = []
        if instruction == "all":
            for file in conn.nlst():
                files.append(file)
        else:
            print("Checking")
            for file in conn.nlst():
                fileraw = file
                for character in file:
                    if character not in ("1234567890"):
                        file = file.replace(character, '')
                fileyear = file[0:4]
                filemonth = file[4:6]
                fileday = file[6:8]
                filehour = file[8:10]
                fileminute = file[10:12]
                filesecond = file[12:14]
                if year is False or year == fileyear:
                    if month is False or month == filemonth:
                        if day is False or day == fileday:
                            if hour is False or hour == filehour:
                                if minute is False or minute == fileminute:
                                    if second is False or second == filesecond:
                                        print("Found ", fileraw)
                                        files.append(fileraw)
        return files

    def gui():
        #runs the program with the graphical interface
        pass

    def main():
        conn = connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        if conn == False:
            print("Error connecting to server")
            exit()
        print("Connection successful!!")
        yearActive = monthActive = dayActive = hourActive = minuteActive = secondActive = False
        year = month = day = hour = minute = second = False
        instruction = "selected"
        for i in range(5, len(sys.argv)):
            if sys.argv[i] == "--help":
                print("Use -ymdhs to declare year, month, day, hour second respectively")
                print("Example usage:\npython3 main.py {IP} {port} {username} {password} -ydm 2021 07 01")
                print("Would get files from the first of July 2021\n")
                print("Use --help to bring up this prompt")
            else: #Since the word help has the letter h in it which I wish to use to specify the hour, I have contained the other checks inside an else statement
                if yearActive == True and year == False:
                    year = sys.argv[i]
                elif monthActive == True and month == False:
                    month = sys.argv[i]
                elif dayActive == True and day == False:
                    day = sys.argv[i]
                elif hourActive == True and hour == False:
                    hour = sys.argv[i]
                elif minuteActive ==True and minute == False:
                    minute = sys.argv[i]
                elif secondActive == True and second == False:
                    second = sys.argv[i]
                if "y" in sys.argv[i]:
                    yearActive = True
                if "m" in sys.argv[i]:
                    monthActive = True
                if "d" in sys.argv[i]:
                    dayActive = True
                if "h" in sys.argv[i]:
                    hourActive = True
                if "m" in sys.argv[i]:
                    minuteActive = True
                if "s" in sys.argv[i]:
                    secondActive = True
                elif "a" in sys.argv[i]:
                    instruction = "all"
                '''
                else:
                    today = str(date.today()).split("-")
                    year, month, day = today[0], today[1], today[2]
                '''
        files = find(conn, instruction, year, month, day, hour, minute, second)
        try:
            download(files, conn)
        except TypeError:
            print("No files in specified range")
        conn.quit()

if __name__ == '__main__':
    #Check if run as a GUI or not
    #if GUI, run gui()
    #else check the arguments and extract relevant information such as:
        #IP address
        #port
        #login
        #password
        #date/time for scheduled download
        #date/time of data to be retrieved
    #for now I am going to rather irresponsibly hard code the login details
    main()
