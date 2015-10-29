import dependency_structure as dep

def get_tok():
    file_name = 'file name here'
    with open(file_name, 'r') as f:
        ds = dep.Dependency_Structure(f.read())

    return ds.get_tokenzed_sentences()

get_tok()
