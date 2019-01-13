## Description
From 31st December 2018 Soundbox will no longer be supported and the media subscriptions will no longer be active. From 1st January 2019 there will be no inbuilt way to automatically get the media (images and videos) into Soundbox for the meetings. This script automatically copies all of the images from the Meeting Workbooks and Watchtowers in JW Library to Soundbox.

## Limitations
* The listing codes for videos are not yet correct so may appear out of sequence in Soundbox
* Media before 2018 is not copied. This is by design because the DB structure before this does not include the necessary tables for this script to operate.
* The images for the Congregation Bible Study are NOT copied.
* The script will copy the images from ALL meeting workbooks found in JW Library. Be aware this could cause LOTS of files and folders to appear in your Soundbox media folders.

## PreRequisites
* Soundbox installed and working
* JWLibrary installed and working

## Testing
Before testing this program you might want to stop (and disable) the "Soundbox MediaJuice" service and delete all of your Soundbox media files. This will prove that all of the media files in soundbox have come from this program and not from Soundbox Media subscription. Note as always you should not perform testing on a live (production) system and it is your responsibility to backup any files before deleting them and ensure correct operation of this program.

## Installation
1. Download and install the latest version of Python 3 from https://www.python.org/downloads/windows/. Make sure to tick the checkbox for "Add Python to PATH" during the installation.
2. Download and save the CopyJWMedia.py script to a suitable location on your computer such as C:\Scripts
3. By default this program will copy media from 2019 onwards. If you want to limit the copying of publications to a different year you can  edit line 1 of the CopyJWMedia.py script to specify the starting year. DO NOT SPECIFY A YEAR BEFORE 2017 OR YOU WILL GET ERROR MESSAGES AND THE SCRIPT WILL FAIL!

## Usage
1. Download the required meeting workbooks in JWLibrary.
2. Open up a command prompt (Windows key+R > cmd)
3. Type 'python' (without the quotes) followed by a space and the path to the downloaded script. E.g.
>python C:\Scripts\CopyJWMedia.py

For repeated usage you can create a scheduled task in Windows to run this python script on a regular basis.
 
## Troubleshooting
If you get the message 'python is not recognized as an internal or external command, operable program or batch file' then you have probably forgotten to add the python installation folder to the path during installation. There are 3 ways you can address this:
1. Edit the Environment Variables on your PC to add the path to your python folder.
2. Reinstall Python and remember to check the box this time.
3. Specify the full path to python when running the script. E.g.
>C:\Users\username\AppData\Local\Programs\Python\Python37\python C:\Scripts\CopyJWMedia.py

## Additional Information
A log file 'JWMediaCopier.log' will be created in the same folder as the script itself. This file will list any missing video files that have been skipped.

This script does not access the internet or in any way alter the publications provided by Watchtower Bible and Tract Society. It merely copies files from one location on your computer's hard drive to another location on your hard drive. To the best of my knowledge it does not violate any terms and conditions of JWLibrary but you must also ensure any usage is in harmony with your Bible-trained conscience.
