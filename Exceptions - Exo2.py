#Pour ce script, le fichier 'Ressource 1.txt' trouvable dans le même repository est requis.
def ReadFile(file):
    try:
        open(file)
    except FileNotFoundError:
        return("file not found") 
    except IOError :
        return("an error as occured while accessing the file")
    except FileExistsError:
        return("error, file already exists")
    except PermissionError :
        return("error, check permissions")
    else:
        r = ""
        with open(file, 'r') as f:
            for l in f:
                r += l
            return r

if __name__== "__main__":
    print(ReadFile("C:/Users/knobl/Desktop/fichier.txt"))
