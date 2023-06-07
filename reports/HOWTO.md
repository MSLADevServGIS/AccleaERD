# Task Scheduling How-To
This process is simple: We schedule `.bat` scripts to fire at various intervals.

## `.bat` Scripts
A `.bat` script is a file that contains command-line executable code.  

1. I've already created `.bat` scripts for various scheduling intervals.
2. Open the appropriate file and add a line of code that you want to execute for that schedule.
* e.g. `conda activate py11 && python <folder>/<python file> <args>`

This setup won't allow us to have Task Scheduler pass arguments, so default arguments must be defined inside each `.py` file (not in the `.bat` file).  

Test the `.bat` file from the command-line by calling the filename. e.g.:  
```cmd
scheduled_weekly.bat
```

## Schedule a Task
1. Open Microsoft's "Task Scheduler" app (I've pinned it to Start)
2. On the far-right choose "Create Basic Task"
3. Give it a name (the interval at which it runs) and a description. Next.
4. Choose the interval to run. Next.
5. Configure the interval. Next.
6. Choose "Start a Program" and point it to the appropriate `.bat` file.
7. Set the "Start in (optional)" option to `C:\workspace\AccelaERD\reports`
8. Finish.
9. Now right-click the new task and choose "Properties" ("General" tab)
10. Select "Run whether user is logged in or not" and choose "Do not store password"
11. In the "Settings" tab change these options:
  * Run task as soon as possible after a scheduled start is missed: `CHECK`
  * Stop if the task runs longer than: `8 hours`
12. You're done.
