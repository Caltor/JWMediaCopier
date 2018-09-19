WARNING: PLEASE NOTE THIS SCRIPT WILL COPY LOTS OF SUPERFLUOUS FILES INTO YOUR SOUNDBOX FOLDERS AND PROBABLY CAUSE MASS CONFUSION FOR YOUR SOUND OPERATORS. IT IS STRONGLY ADVISED TO MAKE A BACKUP OF YOUR SOUNDBOX MEDIA FOLDER BEFORE PROCEEDING. There you have been warned!!!

Description:
With the imminent demise of Soundbox Media subscriptions there is no inbuilt way to automatically get the images into Soundbox for the meetings. This script will automatically copy all of the images from the meeting workbooks in JW Library to Soundbox.

Limitations:
* The images for the Congregation Bible Study are NOT copied.
* The WatchTower images are NOT copied.
* The script will copy the images from ALL meeting workbooks found in JW Library. This includes 2018 and before. Be aware this could cause LOTS of files and folders to appear in your Soundbox media folders.

PreRequisites:
Soundbox installed and working
JWLibrary installed and working

Testing:
Before testing this program you might want to disable the Soundbox MediaJuice service and delete all of your Soundbox media files. This will prove that all of the media files in soundbox have come from this program and not from Soundbox Media subscription. Note as always you should not perform testing on a live (production) system and it is your responsibility to backup any files before deleting them and ensure correct operation of this program.

Installation:
1. Download and install the latest version of Python 3 from https://www.python.org/downloads/windows/. Make sure to tick the checkbox for "Add Python to PATH" during the installation.
2. Download and save the CopyJWMedia.py script to a suitable location on your computer such as C:\Scripts
3. Edit line 9 of the CopyJWMedia.py script to reflect the name of your JWLibrary app package folder. This folder is typically found in C:\Users\username\AppData\Local\Packages. Once you have made this change save and close the script file.

Usage:
1. Download the required meeting workbooks in JWLibrary.
2. Open up a command prompt (Windows key+R > cmd)
3. Type 'python' (without the quotes) followed by a space and the path to the downloaded script. E.g.
>python C:\Scripts\CopyJWMedia.py

For repeated usage you can create a scheduled task in Windows to run this python script on a regular basis.
 
Troubleshooting:
If you get the message 'python is not recognized as an internal or external command, operable program or batch file' then you have probably forgotten to add the python installation folder to the path during installation. There are 3 ways you can address this:
1. Edit the Environment Variables on your PC to add the path to your python folder.
2. Reinstall Python and remember to check the box this time.
3. Specify the full path to python when running the script. E.g.
>C:\Users\username\AppData\Local\Programs\Python\Python37\python C:\Scripts\CopyJWMedia.py


Version History
---------------
Version 1:
* Initial Release

Version 2:
* Images are now copied to the correct week and prefixed with the listing codes.
* Only the high resolution images are copied to Soundbox.

