import time, os, json, argparse
import bunzbar.infos, bunzbar.config #module imports
import tsv_calendar 

available = ["infos.battery",
        "infos.clck",
        "tsv.current.all",
        "tsv.current.name",
        "tsv.current.description",
        "tsv.current.start_time",
        "tsv.current.end_time",
        "tsv.current.end_timer",
        "tsv.next.all",
        "tsv.next.name",
        "tsv.next.description",
        "tsv.next.start_time",     
        "tsv.next.end_time",
        "tsv.next.end_timer"]

options = ["tsv_path",
           "info_len"]

class config:
    def __init__(self):        
        self.CFGPATH = os.path.join(os.path.expanduser('~'), ".config/bunzbar/")
        self.CONFIGFILE = os.path.join(self.CFGPATH, "config.json")
 
    def update(self):
        if not os.path.exists(self.CFGPATH): #Create config folder
            os.makedirs(self.CFGPATH, exist_ok=True)

        if not os.path.exists(self.CONFIGFILE): #Create config file
            data = json.loads('{"available":["infos.clck"],"active":["infos.clck"]}')
            open(self.CONFIGFILE, 'w').write(json.dumps(data, indent=4))
        
        config = json.load(open(self.CONFIGFILE, 'r'))
        config["available"] = available

        if "active" in config:
            for info in config["active"]:
                if not info in available:
                    config["active"].remove(info)
        else:
            config["active"] = []

        open(self.CONFIGFILE, 'w').write(json.dumps(config, indent=4))

    def active(self): 
        config = json.load(open(self.CONFIGFILE, 'r'))
        return(config["active"])
    
    def exists(self, name):
        config = json.load(open(self.CONFIGFILE, 'r'))
        return(name in config)
    
    def setc(self, key, value):
        config = json.load(open(self.CONFIGFILE, 'r'))
        if key in options:
            config[key] = value
        open(self.CONFIGFILE, 'w').write(json.dumps(config, indent=4))
        
    def getv(self, name): 
        config = json.load(open(self.CONFIGFILE, 'r'))
        return(config[name])

    def getf(self, name):
        info = bunzbar.infos.infos()
        if name == "infos.battery": return(info.battery())
        elif name == "infos.clck": return(info.clck())

        #elif name == "tsv.current.all": return str(tsv_calendar.current(tsv_calendar.GET.ALL))
        #elif name == "tsv.current.all": return str(tsv_calendar.current(tsv_calendar.GET.ALL))
        #elif name == "tsv.current.all": return str(tsv_calendar.current(tsv_calendar.GET.ALL))
        #elif name == "tsv.current.all": return str(tsv_calendar.current(tsv_calendar.GET.ALL))
        #elif name == "tsv.current.all": return str(tsv_calendar.current(tsv_calendar.GET.ALL))

        else:
            return(0)
