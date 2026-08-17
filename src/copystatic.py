import os
import shutil

#def outer_function(source, destination):
#    delete destination
#    recreate destination
#    def inner function(source, destination):
#    look at files in source
#    copy files from source to destination
# This function needs no test suite because you can just check your files and see that it worked

# This function handles one level of folders
# But if it has nested folders, then each folder level needs its own call
# hence recursion.
def copystatic_recursive(source_path: str, destination_path: str) -> None:
    source_files = os.listdir(source_path)
    for filename in source_files:
        full_source_path = os.path.join(source_path, filename)
        full_destination_path = os.path.join(destination_path, filename)

        if os.path.isfile(full_source_path):
            print(f"Copying {full_source_path} -> {full_destination_path}")
            shutil.copy(full_source_path, full_destination_path)
        else:
            os.mkdir(full_destination_path)
            copystatic_recursive(full_source_path, full_destination_path)

def copystatic(source_path: str, destination_path: str) -> None:
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    copystatic_recursive(source_path, destination_path)
