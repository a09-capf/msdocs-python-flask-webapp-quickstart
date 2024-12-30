import os
AUTHORITY= os.getenv("AUTHORITY")

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")
THUMBPRINT = os.getenv("THUMBPRINT")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

SCOPE = ["https://cognitiveservices.azure.com/.default"]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"