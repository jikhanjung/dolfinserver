import re,os,sys
from pathlib import Path

rootdir = 'P:\JikhanJung\dolfinimage'

for (root,dirs,files) in os.walk(rootdir, topdown=True):
    jpg_count = 0
    for file in files:
        filepath = Path(root,file).resolve()
        if filepath.suffix.upper() != '.JPG':
            #print(file_path, file_path.suffix)
            continue
        jpg_count += 1
        break

    if root.find('thumbnail') > -1:
        continue

    if jpg_count > 0:
        print(root)

    continue
    #print(root,dirs,len(files),files[:10])
    #print(dirs)
    #for dir in dirs:
    #print(files)
    jpg_count = 0
    for file in files:
        filepath = Path(root,file).resolve()
        if filepath.suffix.upper() != '.JPG':
            #print(file_path, file_path.suffix)
            continue
        jpg_count += 1
        #stat_result = os.stat(filepath)

        #exif_info = self.get_exif_info(filepath)
        image_record = DolfinImageFile.get_or_none( path=str(filepath.as_posix()) )
        if image_record is None:
            self.temp_file_list.append({'path':str(filepath),'type':'file'})
            continue

    if jpg_count + len(dirs) > 0:
        dirpath = Path(root).resolve()
        self.temp_dir_list.append({'path':str(dirpath),'type':'dir','size':jpg_count})
        
        continue               
