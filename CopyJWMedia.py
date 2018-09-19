## TODO:
## * Split code into functions rather than one big script
## * Copy files to only the relevant week (need to read .db sqlite file to get salient info)
## * Only copy files of preferred resolution
## * Change filename to description as per Soundbox media subscriptions
## * Set routine to only copy years from 2019 onwards
## * Copy WatchTower images

import os, calendar, shutil, time, sqlite3

jwlibrary_package = "WatchtowerBibleandTractSo.45909CDBADF3C_5rz59y55nfz3e"

print("Copying images from JW Library Meeting Workbooks to Soundbox...")

meeting_parts = {
    '10': '3',  # Living as Christians
    '21': '1',  # Treasures from God's Word
    '107': '3'  # Living as Christians
    }

start = time.time()
# By using os.path.join() instead of backslashes we make this script cross-platform compatible. You know for when we get JWlibrary and Soundbox for Linux and Mac! ;) teehee...
targetpath_base = os.path.join(os.getenv("ProgramData"), "SoundBox", "MediaCalendar")
path = os.path.join(os.getenv("LOCALAPPDATA"), "packages", jwlibrary_package, "LocalState", "Publications")
array = os.listdir(path)
search_string = "mwb_E_"
mwb_folders = list(filter(lambda x: search_string in x, array))
for source_folder in mwb_folders:
    print("Copying " + source_folder)
    year = source_folder[-6:-2]
    month = source_folder[-2:]

    source_path = os.path.join(path, source_folder)
    dbpath = os.path.join(source_path, source_folder+".db")

    conn = sqlite3.connect(dbpath)
    conn.row_factory = sqlite3.Row # allows accessing columns using column name - see https://docs.python.org/2/library/sqlite3.html#row-objects
    c = conn.cursor()
    for row in c.execute("SELECT * FROM Document ORDER BY DocumentId"):
        # print(row['Title'])
        row_class = row['Class']
        if row_class == '106':
            # This is a new week
            week = row['Title']
            #print("Week: ", week)
            split_week = week.split('-')    #splits into 'from' and 'to' sections
            if len(split_week) == 1:
                split_week = week.split('–')
            #print("split_week", split_week)
            #print("split_week[0]", split_week[0])
            #print("split_week[1]", split_week[1])
            #print('Month', split_week[0])
            #print('Dates', split_week[1])   #get first character
            from_date = split_week[0].split()  # splits into month and date
            first_date = from_date[1]
            #print("first_date", first_date)
            #print("First Date:", first_date)
            target_folder = year + "-" + month + "-" + str(first_date).zfill(2)
            #print("target_folder", target_folder)
            targetpath = os.path.join(targetpath_base, year, target_folder)
            print("Writing files to", targetpath)
            if not os.path.exists(targetpath):
                os.makedirs(targetpath)

        if row_class in ['21','107','10']:
            # Treasures from God's word or Living as Christians
            document_id = row['DocumentId']
            #print("Document: ", document_id)

            # Get all of the multimedia records for this document
            d = conn.cursor()
            t_doc = (document_id, )
            counter = 0
            for row2 in d.execute("SELECT DocumentMultimedia.MultimediaId, Label, Filepath FROM DocumentMultimedia JOIN Multimedia ON DocumentMultimedia.MultimediaId = Multimedia.MultimediaId WHERE DocumentId = ? AND CategoryType = 8", t_doc):
                counter += 10
                #print(row2['MultimediaId'])
                sourcefile = row2['Filepath']
                meeting_part = meeting_parts[row_class]
                target_file_name = "M" + meeting_part + "-" + str(counter).zfill(3) + " " + row2['Label'] + ".jpg"
                #print("Source file:", sourcefile)
                #print("Target file:", target_file_name)
                target_file_path = os.path.join(targetpath, target_file_name)
                if not os.path.exists(target_file_path):
                    source_file_path = os.path.join(source_path, sourcefile)
                    shutil.copyfile(source_file_path, target_file_path)

    conn.close()

##    newcal = calendar.Calendar().itermonthdates(int(year), int(month))    #get all the dates in this month
##
##    # filter the list to only Mondays
##    filtered_list = list(filter(lambda x: x.weekday() == 0, newcal)) # If we need Sundays in the future then the filter expression becomes x.weekday() in [0,6]
##
##    # Loop through the filtered list of dates copying all the files as we go
##    for day in filtered_list:
##        targetpath = os.path.join(targetpath_base, year, str(day))
##        if not os.path.exists(targetpath):
##            os.makedirs(targetpath)
##
##        sourcepath = os.path.join(path, source_folder)
##        sourcefiles = os.listdir(sourcepath)
##        for file in sourcefiles:
##            targetfile = os.path.join(targetpath, file)
##            if not os.path.exists(targetfile):
##                sourcefile = os.path.join(sourcepath, file)
##                shutil.copyfile(sourcefile, targetfile)
            
elapsed = str(time.time() - start)
print("Finished")
print("Time taken: " + elapsed + " seconds")
