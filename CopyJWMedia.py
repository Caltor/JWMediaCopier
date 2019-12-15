starting_year = 2019
study_publication = "jy"
study_publication_full = study_publication + "_E"
jwlibrary_package = "WatchtowerBibleandTractSo.45909CDBADF3C_5rz59y55nfz3e"

## TODO:
## * Split code into functions rather than one big script
## * Allow user to copy only Watchtower or only Meeting Workbooks using command line switches
## * Filter out all characters that aren't valid in Windows filename- see line 227, currently using replace(). Could possibly use regex for this
import os, calendar, shutil, time, sqlite3, logging
from datetime import date, timedelta

def get_filtered_folders(search_string, array):
    return list(filter(lambda x: search_string in x, array))

def get_year_month_from_folder(folder_name):
    year = folder_name[-6:-2]
    month = folder_name[-2:]
    return (year, month)

def get_db_connection(dbpath):
    conn = sqlite3.connect(dbpath)
    conn.row_factory = sqlite3.Row # allows accessing columns using column name - see https://docs.python.org/2/library/sqlite3.html#row-objects
    return conn

def get_documents(conn):
    c = conn.cursor()
    return c.execute("SELECT * FROM Document ORDER BY DocumentId")

def get_documents_by_meps_document_id(conn, documentid):
    c = conn.cursor()
    return c.execute("SELECT * FROM Document WHERE MepsDocumentId = ?", (str(documentid),) )

def get_document_multimedia(conn, documentid):
    c = conn.cursor()
    return c.execute("SELECT MultimediaId FROM DocumentMultimedia WHERE DocumentId = ?", (str(documentid),) )

def get_document_multimedia_info(conn, documentid):
    c = conn.cursor()
    return c.execute("SELECT DocumentMultimedia.MultimediaId, Label, Filepath FROM DocumentMultimedia JOIN Multimedia ON DocumentMultimedia.MultimediaId = Multimedia.MultimediaId WHERE CategoryType = 8 AND DocumentId = ?", (str(documentid),))  #need the extra comma as we pass in a tuple

def get_media_keys(media_conn, issuetag, track):
    c = media_conn.cursor()
    return c.execute("SELECT * FROM MediaKey WHERE IssueTagNumber = ? AND Track = ?", (issuetag, track))
 
def get_media_key(media_conn, issuetagnumber, track):
    c = media_conn.cursor()
    c.execute("SELECT MediaKeyId FROM MediaKey WHERE IssueTagNumber = ? AND Track = ?", (issuetagnumber, track))
    row = c.fetchone()
    if row is None:
        return
    return row['MediaKeyId']

def get_first_date_wt(conn):
    c = conn.cursor()
    c.execute("SELECT FirstDatedTextDateOffset FROM Publication")
    row = c.fetchone()
    return int2date(row[0])

def get_meps_document_ids(conn, documentid):
    c = conn.cursor()
    c.execute("select RefMepsDocumentId from Extract inner join RefPublication on Extract.RefPublicationId = RefPublication.RefPublicationId inner join DocumentExtract on Extract.ExtractId = DocumentExtract.ExtractId where DocumentExtract.DocumentId = ? and RefPublication.RootSymbol = ?", (str(documentid), study_publication))
    return c

def get_multimedia_tag(conn, multimedia_id):
    c = conn.cursor()
    c.execute("SELECT KeySymbol, IssueTagNumber, Track FROM Multimedia WHERE MultimediaId = ?", (str(multimedia_id),) )
    row = c.fetchone() 
    return (row['KeySymbol'], row['IssueTagNumber'], row['Track'])

def get_video_details(media_conn, media_key):
    c = media_conn.cursor()
    c.execute("SELECT Title, Filepath FROM Video WHERE MediaKeyId = ?", (media_key,) )
    return c.fetchone()
    
def copyfile_nooverwrite(source, target):
    if not os.path.exists(target):
        shutil.copy2(source, target)

def sanitise_filename(filename):
    for char in "<>:\"/\\|?*":
        filename = filename.replace(char, '')
    return filename

def int2date(argdate: int) -> date:
    """
    If you have date as an integer, use this method to obtain a datetime.date object.

    Parameters
    ----------
    argdate : int
      Date as a regular integer value (example: 20160618)

    Returns
    -------
    dateandtime.date
      A date object which corresponds to the given value `argdate`.
    """
    year = int(argdate / 10000)
    month = int((argdate % 10000) / 100)
    day = int(argdate % 100)

    return date(year, month, day)
                    
## Main program ##
print("Copying images from JW Library Meeting Workbooks to Soundbox...")

meeting_parts = {
    '10': '3',  # Living as Christians
    '21': '1',  # Treasures from God's Word
    '107': '3' # Living as Christians
    }

start = time.time()

## setup the logger
logging.basicConfig(filename='JWMediaCopier.log', level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s', filemode='w')  ##overwrites the log each time

## Open Media Catalog
media_catalog_path = os.path.join(os.getenv("LOCALAPPDATA"), "packages", jwlibrary_package, "LocalState", "Data", "mediaCollection.db")
media_conn = get_db_connection(media_catalog_path)

# By using os.path.join() instead of backslashes we make this script cross-platform compatible. You know for when we get JWlibrary and Soundbox for Linux and Mac! ;) teehee...
targetpath_base = os.path.join(os.getenv("ProgramData"), "SoundBox", "MediaCalendar")
path = os.path.join(os.getenv("LOCALAPPDATA"), "packages", jwlibrary_package, "LocalState", "Publications")

## Open Congregation Bible Study catalog
book_study_path = os.path.join(path, study_publication_full)
book_study_database = os.path.join(book_study_path, study_publication_full + ".db")
book_study_conn = get_db_connection(book_study_database)

array = os.listdir(path)


print("\r\nMeeting Workbooks:")
filtered_folders = get_filtered_folders("mwb_E_", array)
for source_folder in filtered_folders:
    year, month = get_year_month_from_folder(source_folder)
    
    ## Ignore years before 2017
    if int(year) < starting_year:
        continue

    print("Copying " + source_folder)
        
    source_path = os.path.join(path, source_folder)
    dbpath = os.path.join(source_path, source_folder+".db")

    conn = get_db_connection(dbpath)
    c = conn.cursor()
    for row in c.execute("SELECT * FROM Document ORDER BY DocumentId"):
        row_class = row['Class']
        if row_class == '106':
            # This is a new week
            documentid = row['DocumentId']
            week = row['Title']
            split_week = week.split('-')    #splits into 'from' and 'to' sections
            if len(split_week) == 1:
                split_week = week.split('–')

            from_date = split_week[0].split()  # splits into month and date
            first_date = from_date[1]
            target_folder = year + "-" + month + "-" + str(first_date).zfill(2)
            targetpath = os.path.join(targetpath_base, year, target_folder)
            print("Writing files to", targetpath)
            if not os.path.exists(targetpath):
                os.makedirs(targetpath)

            ## Get the Congregation Bible Study images
            document_ids = get_meps_document_ids(conn, documentid)
            for row in document_ids:
                ## Get jy.db -> Document -> DocumentMultimedia -> Multimedia etc
                counter=0
                for book_study_doc in get_documents_by_meps_document_id(book_study_conn, row['RefMepsDocumentId']):
                    counter += 10
                    for media in get_document_multimedia_info(book_study_conn, book_study_doc["DocumentId"]):
                        book_study_source_file = media['Filepath']
                        target_file_name = "M3-" + str(counter).zfill(3) + " " + media['Label'].replace('?', '')
                        target_file_path = os.path.join(targetpath, target_file_name)[:255] + ".jpg"
                        if not os.path.exists(target_file_path):
                            source_file_path = os.path.join(book_study_path, book_study_source_file)
                            shutil.copyfile(source_file_path, target_file_path)
                
                
            ## Get the Videos!!!
            document_multimedia_records = get_document_multimedia(conn, documentid)
            counter = 0
            for document_multimedia in document_multimedia_records:
                multimedia_id = document_multimedia['MultimediaId']
                keysymbol, issuetag, track = get_multimedia_tag(conn, multimedia_id)
                if keysymbol == 'nwtsv' or issuetag > 0:
                    media_key = get_media_key(media_conn, issuetag, track)
                    row = get_video_details(media_conn, media_key)
                    if row:
                        source_file_path = row['Filepath']
                        title = row['Title']
                        valid_file_name = sanitise_filename(title)
                        meeting_part = '1'
                        counter += 10
                        target_file_name = "M" + meeting_part + "-" + str(counter).zfill(3) + " " + valid_file_name + ".mp4"
                        target_file_path = os.path.join(targetpath, target_file_name)
                        if os.path.exists(source_file_path):
                            if not os.path.exists(target_file_path):
                                shutil.copyfile(source_file_path, target_file_path)
                        else:
                            warning_message = "File " + source_file_path + " was not found - skipped"
                            logging.warning(warning_message)
                            print("Warning: " + warning_message)


        if row_class in ['21','107','10']:
            # Treasures from God's word or Living as Christians
            document_id = row['DocumentId']

            # Get all of the multimedia records for this document
            d = conn.cursor()
            t_doc = (document_id, )
            counter = 0
            for row2 in d.execute("SELECT DocumentMultimedia.MultimediaId, Label, Filepath FROM DocumentMultimedia JOIN Multimedia ON DocumentMultimedia.MultimediaId = Multimedia.MultimediaId WHERE DocumentId = ? AND CategoryType = 8", t_doc):
                counter += 10
                sourcefile = row2['Filepath']
                meeting_part = meeting_parts[row_class]
                target_file_name = "M" + meeting_part + "-" + str(counter).zfill(3) + " " + row2['Label'].replace('?','').replace('/','').replace(':','')
                target_file_path = os.path.join(targetpath, target_file_name)[:255] + ".jpg"
                if not os.path.exists(target_file_path):
                    source_file_path = os.path.join(source_path, sourcefile)
                    shutil.copyfile(source_file_path, target_file_path)

    conn.close()


## WatchTower
print("\r\nWatchtowers:")
filtered_folders = get_filtered_folders("w_E_", array)
for source_folder in filtered_folders:
    dbpath = os.path.join(path, source_folder, source_folder+".db")
    conn = get_db_connection(dbpath)
    study_date = get_first_date_wt(conn)
    study_date += timedelta(days=6) # Change w/c date from Monday to Sunday

    ## Create target folder
    year = str(study_date.year)

    ## Ignore years before 2017
    if int(year) < starting_year:
        continue
    
    print("Copying "+source_folder)

    for document in get_documents(conn):
        document_class = document['Class']
        if document_class == '40':
            folder_name = str(study_date)
            targetpath = os.path.join(targetpath_base, year, folder_name)
            print("Writing files to", targetpath)
            if not os.path.exists(targetpath):
                os.makedirs(targetpath)
                
            counter = 0
            images = get_document_multimedia_info(conn, document['DocumentId'])
            for image in images:
                counter += 10
                source_file_path = os.path.join(path, source_folder, image['Filepath'])
                target_file_name = "W2-" + str(counter).zfill(3) + " " + image['Label'].replace('?','')
                target_file_path = os.path.join(targetpath, target_file_name)[:255] + ".jpg"
                copyfile_nooverwrite(source_file_path, target_file_path)

            study_date += timedelta(days=7) #Increment the week
            
    conn.close()

media_conn.close()

elapsed = str(time.time() - start)
print("\r\nFinished")
print("Time taken: " + elapsed + " seconds")


