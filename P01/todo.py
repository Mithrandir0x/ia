
from time import time, strftime

class Task():
    """
    The class that stores a task's information.
    """
    """
    Static member that allows to have a unique identifier
    for each task.
    """
    uid = 0
    def __init__(self, title = None):
        self.id = Task.uid
        self.title = "T%d" % self.id
        if title: self.title = title
        self.creationTime = strftime("%d/%m/%Y %H:%M")
        self.endTime = None
        self.done = False
        Task.uid += 1
    def setTitle(self, title):
        """
        Allows to change the title of the task.
        """
        self.title = title
    def complete(self):
        """
        Allows to finish the task. And marks its time.
        """
        self.endTime = strftime("%d/%m/%Y %H:%M")
        self.done = True
    def __str__(self):
        """
        Returns the string representation of the task.
        """
        return "(%s, %sh, %s)" % ( self.id, self.creationTime, self.endTime )
    def __repr__(self):
        return self.__str__()

class TaskManager():
    """
    This class is in charge of storing and offering functionality to manage the tasks.
    """
    def __init__(self):
        self.tasks = {}
        self.option = None
    def run(self):
        """
        Main process.
        """
        print "The Task Manager"
        self.showTasks()
        self.showOptions()
        self.getUserOption()
        while self.option != 6:
            if self.option == 1:
                self.addTask()
            elif self.option == 2:
                self.removeTask()
            elif self.option == 3:
                self.editTask()
            elif self.option == 4:
                self.endTask()
            elif self.option == 5:
                self.showCompletedTasks()
            self.showTasks()
            self.showOptions()
            self.getUserOption()
    def getUserOption(self):
        """
        Gets the option that wants the user to be performed.
        """
        self.option = input("Choose: ")
    def showOptions(self):
        """
        Show at the standard output the available options to perform.
        """
        print ""
        print " 1. Add new task"
        print " 2. Remove task"
        print " 3. Edit task"
        print " 4. Complete task"
        print " 5. Show completed tasks"
        print " 6. Close application"
        print ""
    def printTask(self, task):
        """
        Print throught the standard output the task passed by.
        """
        print " (%d) %s, created at %s" % ( task.id, task.title, task.creationTime )
        if task.done:
            print "      Finished at %s" % task.endTime
    def showTasks(self):
        """
        Print all the tasks to be done.
        """
        print ""
        print "Tasks available:"
        for id, task in self.tasks.iteritems():
            if not task.done:
                self.printTask(task)
        print ""
    def showCompletedTasks(self):
        """
        Print all the finished tasks.
        """
        print ""
        print "Tasks finished:"
        for id, task in self.tasks.iteritems():
            if task.done:
                self.printTask(task)
        print ""
    def addTask(self, desc):
        """
        Add programatically a task with the description passed by.
        """
        t = Task(desc)
        self.tasks[t.id] = t
    def addUserTask(self):
        """
        Add a new task with the description issued by the user.
        """
        desc = input("Task Description: ")
        self.addTask(desc)
    def getTaskAnd(self, f):
        """
        Execute a function passed by, with the task issued by the user.
        """
        i = input("Task ID: ")
        if i in self.tasks:
            f(i, self.tasks[i])
        else:
            print "There is no Task with supplied ID."
    def editTask(self):
        """
        Edit the task's description required by the user.
        """
        def editDescription(i, t):
            """
            Ask the user which description wants and edit the task's description passed by.
            """
            desc = input("New Task Description: ")
            t.setTitle(desc)
        self.getTaskAnd(editDescription)
    def endTask(self):
        """
        Finish the task required by the user.
        """
        def endIt(i, t):
            """
            Finish the task passed by.
            """
            t.complete()
        self.getTaskAnd(endIt)
    def removeTask(self):
        """
        Remove the task required by the user.
        """
        def removeIt(i, t):
            """
            Remove the task passed by from the store.
            """
            del self.tasks[i]
        self.getTaskAnd(removeIt)

if __name__ == '__main__':
    tm = TaskManager()
    tm.addTask("Hello World!!")
    tm.addTask("Botch the VM")
    tm.addTask("Beer-Beer-Beer Diddle Beer-Beer-Beer")
    tm.run()
