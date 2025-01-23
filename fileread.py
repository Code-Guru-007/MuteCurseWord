file_path = "badwords.txt"  # Replace with the actual path to your text file

# Read the file and store each line as a list element
with open(file_path, 'r') as file:
    curse_words = [line.strip() for line in file.readlines()]

# Print the list of curse words
curse_words = set(["specifically", "different", "website"]) 
print(type(curse_words))