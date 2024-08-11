"""
Reading Data in Chunks
When processing large amounts of data, the walrus operator helps read and process chunks efficiently:
"""

# # Traditional approach
# buffer = file.read(1024)
# while buffer:
#     process(buffer)
#     buffer = file.read(1024)

# # Using walrus operator
# while (buffer := file.read(1024)):
#     process(buffer)


"""
This avoids the need for an additional buffer variable outside the loop, making the code cleaner and more readable.
"""