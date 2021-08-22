import ftplib
import os
import sys
import scheduler
import fileprocessing
from datetime import date


class FTPDownload:
    # Procedure to download all files specified
    # files - List of files on server to be downloaded
    # conn - The connection to the server to download from
    def download(self, files, conn):
        wd = os.getcwd()
        os.chdir(wd+"/allFiles") #Changing the working directory to files so the files are stored in the right place
        for filename in files:
            with open(filename, "wb") as file:
                print("Downloading ", filename)
                conn.retrbinary(f"RETR {filename}", file.write)
                print("Downloaded ", filename)
        os.chdir(wd)
        fileprocessing.processDownloads()

    # Function to establish connection to the server
    # address - The IP address of the server
    # port - The port the server is running on. At present not required but may be
    #   useful in the future
    # login - The login username
    # password - The password accompanying the login
    # Returns the connection for use in scanning and downloading files, in the event
        # of failure to connect it returns false so as to alert the system of a
        # failure to connect
    def connect(self, address, port, login, password):
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
    def find(self, conn, instruction, year=None, month=None, day=None, hour=None, minute=None, second=None):
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
