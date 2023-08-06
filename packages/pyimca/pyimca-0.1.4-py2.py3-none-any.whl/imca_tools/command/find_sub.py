import os  

def find_yaml(file_dir):   
    L=[]   
    for dirpath, dirnames, filenames in os.walk(file_dir):  
        for file in filenames :  
            if os.path.splitext(file)[1] == '.yaml':  
                L.append(os.path.join(dirpath, file))  
    return L

def find_sub(file_dir):
    Lis = []
    for file in find_yaml(file_dir):
        right_index = str(file).rfind('/')
        Lis.append(file[:right_index])
    return Lis



