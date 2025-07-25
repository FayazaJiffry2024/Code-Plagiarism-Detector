# test_compare.py

from compare import calculate_similarity

# Load both test files
with open("../test_files/file1.py", "r") as f1, open("../test_files/file2.py", "r") as f2:
    code1 = f1.read()
    code2 = f2.read()

similarity = calculate_similarity(code1, code2)
print(f"Similarity: {similarity}%")
