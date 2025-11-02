import os

def resource_path(relative_path):
    base = os.path.abspath(os.path.dirname(__file__) + "/..")
    return os.path.join(base, "resources", relative_path)