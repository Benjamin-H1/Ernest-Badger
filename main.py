import ftplib

# Procedure to download all files specified
# files - List of files on server to be downloaded
# conn - The connection to the server to download from
def download(files, conn):
    for filename in files:
        with open(filename, "wb") as file:
            conn.retrbinary(f"RETR {filename}", file.write)

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
    try:
        conn = ftplib.FTP(address, login, password)
        return conn
    except:
        return False


def gui():
    #runs the program with the graphical interface
    pass

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
    conn = connect("87.115.189.50", "21", "Roadrunner", "M33pM33p")
    if conn == False:
        print("Error connecting to server")
        exit()
    print("Connection successful!!")
    conn.quit()
