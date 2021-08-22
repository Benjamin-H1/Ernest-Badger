import ftpService
import time
import sys
import scheduler

# This is where the program is run from if using the CLI
# It's very basic but works (something of a rush job as it was originally strictly utilitarian)
def main(instructions):
    ftpserv = ftpService.FTPDownload()
    targetday = False
    # Connect to the server using the details provided by the command line
    conn = ftpserv.connect(instructions[1], instructions[2], instructions[3], instructions[4])
    if conn == False:
        print("Error connecting to server")
        exit()
    print("Connection successful!!")
    yearActive = monthActive = dayActive = hourActive = minuteActive = secondActive = False
    year = month = day = hour = minute = second = False
    instruction = "selected"
    for i in range(5, len(instructions)):
        if instructions[i] == "--help":
            print("Use -p to set when to download. eg -p 2021822 would set a target schedule of 22nd of August 2021. DO NOT PUT 0s BEFORE NUMBERS")
            print("Use -ymdhs to declare year, month, day, hour second respectively")
            print("Example usage:\npython3 ftpService.py {IP} {port} {username} {password} -p 2021822 -ydm 2021 07 01")
            print("Would get files from the first of July 2021\n")
            print("Use --help to bring up this prompt")
        elif instructions[i] == "-p":
            targetday = instructions[i+1]
        else: #Since the word help has the letter h in it which I wish to use to specify the hour, I have contained the other checks inside an else statement
            if yearActive == True and year == False:
                year = instructions[i]
            elif monthActive == True and month == False:
                month = instructions[i]
            elif dayActive == True and day == False:
                day = instructions[i]
            elif hourActive == True and hour == False:
                hour = instructions[i]
            elif minuteActive ==True and minute == False:
                minute = instructions[i]
            elif secondActive == True and second == False:
                second = instructions[i]
            if "y" in instructions[i]:
                yearActive = True
            if "m" in instructions[i]:
                monthActive = True
            if "d" in instructions[i]:
                dayActive = True
            if "h" in instructions[i]:
                hourActive = True
            if "m" in instructions[i]:
                minuteActive = True
            if "s" in instructions[i]:
                secondActive = True
            elif "a" in instructions[i]:
                instruction = "all"
            '''
            else:
                today = str(date.today()).split("-")
                year, month, day = today[0], today[1], today[2]
            '''

    if targetday == False:
        files = ftpserv.find(conn, instruction, year, month, day, hour, minute, second)
        try:
            ftpserv.download(files, conn)
        except TypeError:
            print("No files in specified range")
    else: #This means the user has specified a date for the download to take place
        task = [instruction, year, month, day, hour, minute, second]
        sched =scheduler.Scheduler()
        sched.schedule(targetday, task)
        while True: # The program enters a while loop until the date is met
            doit = sched.check()
            if doit is not None:
                files = ftpserv.find(conn, doit[0], doit[1], doit[2], doit[3], doit[4], doit[5], doit[6])
                try:
                    ftpserv.download(files, conn)
                except TypeError:
                    print("No files in specified range")
                break
            time.sleep(10)
    conn.quit()

if __name__ == '__main__':
    main(sys.argv)
