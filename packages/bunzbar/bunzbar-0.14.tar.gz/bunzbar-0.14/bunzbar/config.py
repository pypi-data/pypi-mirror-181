import time, os, json, argparse #standard imports
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

class config:
    def __init__(self):        
        self.CFGPATH = os.path.join(os.path.expanduser('~'), ".config/bunzbar/")
        self.CONFIGFILE = os.path.join(self.CFGPATH, "config.json")
 
    def update(self):
        if not os.path.exists(self.CFGPATH): #Create config folder
            os.makedirs(self.CFGPATH, exist_ok=True)

        if not os.path.exists(self.CONFIGFILE):
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

    def genstr(self):
        mstr = ''
        data = json.load(open(self.CONFIGFILE))
        for d in (data["active"]):
            mstr += d.upper() + ' '
            mstr += eval(f"{d}()")
            mstr += " | "
        return mstr
