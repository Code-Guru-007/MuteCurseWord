import numpy as np

# Generate a (12, 2) numpy array with sample data
data = np.random.rand(12, 2)

# Modify rows from index 3 to 8 to zero
start, end = 3, 8
modified_data = data.copy()
modified_data[start:end] = 0

# Concatenate the original and modified data vertically
concatenated_data = np.concatenate((data, modified_data), axis=0)
print(data)
# Print the concatenated result
print("Concatenated Data:")
print(modified_data)