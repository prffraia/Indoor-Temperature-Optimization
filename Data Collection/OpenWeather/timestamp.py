import datetime
# Create a datetime object for February 9th, 2024
timestamp = 1707515287
dt_object = datetime.datetime.utcfromtimestamp(timestamp)

# Convert the datetime object to a Unix timestamp
print("Timestamp:", timestamp)
print("UTC Date & Time:", dt_object)
