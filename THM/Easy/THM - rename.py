import os

# Get the current directory
current_directory = os.getcwd()

# Iterate over all files in the directory
for filename in os.listdir(current_directory):
    # Check if the entry is a file
    if os.path.isfile(os.path.join(current_directory, filename)):
        # Prepend "test" to the filename
        new_filename = "THM - " + filename
        # Rename the file
        os.rename(os.path.join(current_directory, filename), os.path.join(current_directory, new_filename))
        print(f"Renamed '{filename}' to '{new_filename}'")
