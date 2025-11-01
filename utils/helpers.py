import os

# def resource_path(relative_path):
#     base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#     path = os.path.join(base, "resources", relative_path)
#     print("Resolved path:", path)
#     return path

def resource_path(relative_path):
    base = os.path.abspath(os.path.dirname(__file__) + "/..")
    return os.path.join(base, "resources", relative_path)