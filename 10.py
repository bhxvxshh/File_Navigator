import os
from difflib import get_close_matches
import platform

def find_similar_files(file_name, locations):
    all_files = []
    for location in locations:
        all_files.extend(os.listdir(location))

    matches = get_close_matches(file_name, all_files, n=5, cutoff=0.6)  # Adjust cutoff as needed
    
    # Find the closest matching location
    best_match_location = None
    best_match_ratio = 0

    for location in locations:
        location_files = os.listdir(location)
        common_files = set(matches) & set(location_files)
        match_ratio = len(common_files) / len(location_files)

        if match_ratio > best_match_ratio:
            best_match_location = location
            best_match_ratio = match_ratio

    return matches, best_match_location

def suggest_correct_file_name(file_name, suggested_names):
    if suggested_names:
        print(f"File '{file_name}' not found. Did you mean one of these?")
        for i, suggestion in enumerate(suggested_names, start=1):
            print(f"{i}. {suggestion}")

        choice = input("Enter the number corresponding to your choice (or press Enter to cancel): ")
        if choice.isdigit() and 1 <= int(choice) <= len(suggested_names):
            return suggested_names[int(choice) - 1]
        else:
            print("Invalid choice or canceled.")
    else:
        print(f"No similar files found in any location.")

def open_file_or_folder(file_path):
    try:
        if os.path.isdir(file_path):
            # If it's a directory, display its contents
            navigate_folder(file_path)
        elif os.path.isfile(file_path):
            # If it's a file, ask the user if they want to open it
            open_choice = input(f"Do you want to open the file '{os.path.basename(file_path)}'? (yes/no): ").lower()
            if open_choice == 'yes':
                open_file(file_path)
            else:
                print(f"File '{os.path.basename(file_path)}' not opened.")
    except Exception as e:
        print(f"Error: {e}")

def navigate_folder(folder_path):
    while True:
        print(f"\nContents of folder: {folder_path}")
        for i, item in enumerate(os.listdir(folder_path), start=1):
            print(f"{i}. {item}")

        user_input = input("Enter the number corresponding to an item to navigate or 'open' to open a file/folder (or 'exit' to go back): ").lower()

        if user_input == 'exit':
            break
        elif user_input.isdigit() and 1 <= int(user_input) <= len(os.listdir(folder_path)):
            selected_item = os.listdir(folder_path)[int(user_input) - 1]
            selected_path = os.path.join(folder_path, selected_item)

            if os.path.isdir(selected_path):
                # If it's a directory, navigate into it
                folder_path = selected_path
            else:
                # If it's a file, ask the user if they want to open it
                open_choice = input(f"Do you want to open the file '{selected_item}'? (yes/no): ").lower()
                if open_choice == 'yes':
                    open_file(selected_path)
                    break  # Exit the loop after opening the file
                else:
                    print(f"File '{selected_item}' not opened.")
        elif user_input == 'open':
            open_choice = input("Enter the name of the file or folder you want to open: ")
            selected_path = os.path.join(folder_path, open_choice)
            open_file_or_folder(selected_path)
        else:
            print("Invalid input. Please enter a valid number, 'open', or 'exit'.")

def open_file(file_path):
    try:
        if platform.system() == 'Windows':
            os.startfile(file_path)
        elif platform.system() == 'Darwin':
            os.system(f"open {file_path}")
        elif platform.system() == 'Linux':
            os.system(f"xdg-open {file_path}")
    except Exception as e:
        print(f"Error opening file: {e}")

# Example usage
while True:
    file_name = input("Enter the file name (or type 'exit' to quit): ")
    if file_name.lower() == 'exit':
        break
    
    locations = [
        r"\\10.10.6.15\File Share",
    ]

    matches, best_match_location = find_similar_files(file_name, locations)

    if matches:
        suggested_name = suggest_correct_file_name(file_name, matches)
        if suggested_name:
            file_path = os.path.join(best_match_location, suggested_name)
            open_file_or_folder(file_path)
    else:
        print(f"No similar files found in any location.")
