import datetime

class Scheduler:
    def __init__ (self):
        self.tasks = []
        self.dates = []


    def schedule(self, target, task):
        self.tasks.append(task)
        self.dates.append(target)

    def check(self):
        dt = datetime.datetime.today()
        today = str(dt.year)+str(dt.month)+str(dt.day)
        print("Today: ", today)
        for i in range (0, len(self.dates)):
            date = self.dates[i]
            print("Target: ", date)
            if self.dates[i] == today:
                job = self.tasks[i]
                self.tasks.remove(job)
                self.dates.remove(date)
                return job
        return None
