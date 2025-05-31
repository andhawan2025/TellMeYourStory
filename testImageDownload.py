import shutil
import os
import ast

# Convert file URL to Windows path
from urllib.parse import urlparse, unquote

def file_url_to_path(file_url):
    path = urlparse(file_url).path
    # Remove leading slash for Windows paths
    if path.startswith('/'):
        path = path[1:]
    return unquote(path.replace('/', '\\'))

result = "file:///C://Users//andha//AppData//Local//Temp//gradio//ebda6052ae3b8fe2fd51169e7333c5c21d26399e0e11f54b830c5d8c936eade1//image.webp"
result_2 = "('C:\\Users\\andha\\AppData\\Local\\Temp\\gradio\\cea06f53560d2743eaa807357f66f40a0e53ac519642aeed422cccd2cabe2eb2\\image.webp', 1458288794)"
local_outputs_dir = r"C:\Users\andha\OneDrive\Documents\GitHub\TellMeYourStory\outputs"

def main():
    #print (file_url_to_path (result))

    print(type(result_2))
    print(result_2)
    #file_path = str(result_2)
    #print (file_path)
    
    # Escape backslashes
    safe_str = result_2.replace("\\", "\\\\")
    my_tuple = ast.literal_eval(safe_str)
    file_path = my_tuple[0]
    number = my_tuple[1]

    print("File path:", file_path)
    print("Number:", number)

    #file_url_to_path (result)
    #os.makedirs(local_outputs_dir, exist_ok=True)

    #src_path = file_url_to_path(result)
    #dst_path = os.path.join(local_outputs_dir, os.path.basename(src_path))
    #shutil.copy(src_path, dst_path)
    #print(f"Copied to {dst_path}")
    
if __name__ == "__main__":
    main()
