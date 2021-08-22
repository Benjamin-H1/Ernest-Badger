import datetime

class Scheduler:
    def __init__ (self):
        self.tasks = []
        self.dates = []


    def schedule(self, target, task):
        self.tasks.append(task)
        self.date.append(target)

    def check(self, today):
        dt = datetime.datetime.today()
        dtToday = str(dt.year)+str(dt.month)+str(dt.day)
        for i in range (0, len(self.dates)):
            if self.dates[i] == today:
                job = self.tasks[i]
                self.tasks.remove(i)
                self.dates.remove(i)
                return job
        return None
