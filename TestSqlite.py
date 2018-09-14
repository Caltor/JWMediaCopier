import sqlite3

dbpath = "C:\\Users\\darren\\AppData\\Local\\Packages\\WatchtowerBibleandTractSo.45909CDBADF3C_5rz59y55nfz3e\\LocalState\\Publications\\mwb_E_201809\\mwb_E_201809.db"
year = "2018"
month = "09"

conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row # allows accessing columns using column name - see https://docs.python.org/2/library/sqlite3.html#row-objects
c = conn.cursor()
for row in c.execute("SELECT * FROM Document ORDER BY DocumentId"):
    # print(row['Title'])
    if row['Class'] == '106':
        # This is a new week
        week = row['Title']
        print("Week: ", week)
        split_week = week.split()
        print('Month', split_week[0])
        print('Dates', split_week[1])   #get first character
        first_and_last = split_week[1].split('-')
        date = first_and_last[0]
        print("First Date:", date)
        targetpath = year + "-" + month + "-" + str(date).zfill(2)
        print("targetpath", targetpath)

    if row['Class'] in ['21','107','10']:
        # Treasures from God's word or Living as Christians
        document_id = row['DocumentId']
        #print("Document: ", document_id)

        # Get all of the multimedia records for this document
        d = conn.cursor()
        t_doc = (document_id, )
        for row2 in d.execute("SELECT DocumentMultimedia.MultimediaId, Label, Filepath FROM DocumentMultimedia JOIN Multimedia ON DocumentMultimedia.MultimediaId = Multimedia.MultimediaId WHERE DocumentId = ? AND CategoryType = 8", t_doc):
            print(row2['MultimediaId'])
            sourcefile = row2['Filepath']
            targetfile = row2['Label'] + ".jpg"
            print("Source file:", sourcefile)
            print("Target file:", targetfile)

conn.close()
