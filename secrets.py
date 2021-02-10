
class Secrets(dict):
    def __init__(self):            
        with open(".secret","r") as secret:
            for line in secret.read().splitlines():
                k,v = line.split("=")
                self[k.strip()] =v.strip()

    def __getattr__(self, item):
        return self[item]

