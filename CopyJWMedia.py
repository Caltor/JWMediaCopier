## TODO:
## * Split code into functions rather than one big script
## * Copy files to only the relevant week (need to read .db sqlite file to get salient info)
## * Only copy files of preferred resolution
## * Change filename to description as per Soundbox media subscriptions
## * Set routine to only copy years from 2019 onwards
## * Copy WatchTower images

import os, calendar, shutil, time

jwlibrary_package = "WatchtowerBibleandTractSo.45909CDBADF3C_5rz59y55nfz3e"

print("Copying images from JW Library Meeting Workbooks to Soundbox...")

start = time.time()
# By using os.path.join() instead of backslashes we make this script cross-platform compatible. You know for when we get JWlibrary and Soundbox for Linux and Mac! ;) teehee...
targetpath_base = os.path.join(os.getenv("ProgramData"), "SoundBox", "MediaCalendar")
path = os.path.join(os.getenv("LOCALAPPDATA"), "packages", jwlibrary_package, "LocalState", "Publications")
array = os.listdir(path)
search_string = "mwb_E_"
filtered_list = list(filter(lambda x: search_string in x, array))
for folder in filtered_list:
    print("Copying " + folder)
    year = folder[-6:-2]
    month = folder[-2:]
    newcal = calendar.Calendar().itermonthdates(int(year), int(month))    #get all the dates in this month

    # filter the list to only Mondays
    filtered_list = list(filter(lambda x: x.weekday() == 0, newcal)) # If we need Sundays in the future then the filter expression becomes x.weekday() in [0,6]

    # Loop through the filtered list of dates copying all the files as we go
    for day in filtered_list:
        targetpath = os.path.join(targetpath_base, year, str(day))
        if not os.path.exists(targetpath):
            os.makedirs(targetpath)

        sourcepath = os.path.join(path, folder)
        sourcefiles = os.listdir(sourcepath)
        for file in sourcefiles:
            targetfile = os.path.join(targetpath, file)
            if not os.path.exists(targetfile):
                sourcefile = os.path.join(sourcepath, file)
                shutil.copyfile(sourcefile, targetfile)
            
elapsed = str(time.time() - start)
print("Finished")
print("Time taken: " + elapsed + " seconds")
