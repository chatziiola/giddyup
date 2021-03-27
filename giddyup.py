# You need to improve this code in the future but till then:
# TODO works pretty smoothly if you only intend to run it once but it doesn't
# check whether any of these files exist -> duplicate files
import os.path
from os import listdir
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Simply the path of your local folder
localdir = ''
# This should be 'root' or the ID of the "target directory"
remotedir = 'root'

def getdirid(dirname, parentdir):
   dirfiles = drive.ListFile({'q': "'%s' in parents and trashed=false" % parentdir}).GetList() 
   for file in dirfiles:
       if(file['title'] == dirname):
           return file['id']
   return 'zoe'

def uploadFile(filepath, dirid):
    filename = filepath.rsplit('/',1)[1]
    # TODO change that function so that it updates existing files if they've 
    #       have been recently changed
    fileid = getdirid(filename, dirid)
    if( fileid == 'zoe'):
        myfile = drive.CreateFile({"title": filename,
            "mimeType": "application/pdf",
            "parents": [{"id": dirid}] })
        myfile.SetContentFile(filepath)
        myfile.Upload()
        print('File %s uploaded' % filename)

def uploadDirectory(dirlpath, parentdir):
    # First things first, getting our directory's remote id
    dirname = dirlpath.rsplit('/',1)[1]
    dirid = getdirid(dirname, parentdir)
    # If such a folder doesnt exist create it for yourself
    if(dirid == 'zoe'):
        folder = drive.CreateFile({'title': dirname,
            "parents": [{"id": parentdir}],
            "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        uploadDirectory(dirlpath, parentdir)
    # Search local directory
    for file in os.listdir(dirlpath):
        if os.path.isfile(os.path.join(dirlpath+'/',file)):
            if file.endswith('.pdf'):
                print('Uploading file %s' % file)
                uploadFile(os.path.join(dirlpath+'/',file), dirid)
        elif os.path.isdir(os.path.join(dirlpath+'/',file)):
            print('Uploading dir %s' % file)
            uploadDirectory(dirlpath+'/'+file,dirid)
    print('Finished with folder %s' % dirname)

# To upload a directory there is only one command needed -> utilizing recursion
uploadDirectory(localdir, remotedir)
