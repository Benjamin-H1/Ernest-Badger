import datetime

# Class to manage scheduling of jobs
# In testing demonstrated that it was capable of handling multiple scheduled tasks
#   however this functionality has not been used
class Scheduler:
    # self.tasks -> a list of tasks to be performed, initially was planned to hold
    #    objects
    # self.dates -> holds the dates for the opposite number tasks to be run on
    def __init__ (self):
        self.tasks = []
        self.dates = []

    # SImply appends the task and it's target date to their lists for use later
    def schedule(self, target, task):
        self.tasks.append(task)
        self.dates.append(target)

    # Gets the current date and compares it against the dates in the list
    #   self.dates. If they match; it retrieves the opposite task and prior
    #   to returning it deletes both items from their lists.
    # Also checks the date isn't before the present to avoid an infinitely scheduled job
    # Can easily be modified to be more precise down to the second.
    def check(self):
        dt = datetime.datetime.today()
        today = str(dt.year)+str(dt.month)+str(dt.day)
        print("Today: ", today)
        for i in range (0, len(self.dates)):
            date = self.dates[i]
            print("Target: ", date)
            if date < today:
                exit()
            if self.dates[i] == today:
                job = self.tasks[i]
                self.tasks.remove(job)
                self.dates.remove(date)
                return job
            if self.dates[i] < today
        return None
