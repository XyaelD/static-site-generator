import os
import shutil

source_path = "./static"
dest_path = "./public"

def copy_static(path):
    if os.path.exists(path):
        files_and_directories = os.listdir(path)
        for f_d in files_and_directories:
            current_path = os.path.join(path, f_d)
            if os.path.isfile(current_path):
                print(f"Copying {current_path} to {current_path.replace(source_path, dest_path)}")
                shutil.copy(current_path, current_path.replace(source_path, dest_path))
            else:
                new_directory = current_path.replace(source_path, dest_path)
                if not os.path.exists(new_directory):
                    print(f"Creating new directory: {new_directory}")
                    os.mkdir(new_directory)
                copy_static(current_path)

def delete_destination_directory(path):            
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def main():
    delete_destination_directory(dest_path)
    copy_static(source_path)

main()
