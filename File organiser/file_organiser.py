#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess


# def disk


def print_files(dir,option):
    if option:
        result=subprocess.run(["ls",option,dir],capture_output=True)
    else:
        result=subprocess.run(["ls",dir],capture_output=True)
    if result.returncode==0:
        return result.stdout.decode()
    return result.stderr.decode()

def organise_file(source_dir,dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    try:
        for file_name in os.listdir(source_dir):
            source_path=os.path.join(source_dir,file_name)

            if os.path.isfile(source_path):
                file_extension=file_name.split(".")[-1].lower()
                dest_subdir=os.path.join(dest_dir,file_extension)
                
                if not os.path.exists(dest_subdir):
                    os.makedirs(dest_subdir)
                
                dest_path=os.path.join(dest_subdir,file_name)

                shutil.move(source_path,dest_path)
                print(f"Moved {file_name} to {dest_path}")
        return "Task completed"
    except:
        return "Task Failed"

if __name__=="__main__":
    source_dir=sys.argv[1]
    dest_dir=sys.argv[2]
    organise_file(source_dir,dest_dir)