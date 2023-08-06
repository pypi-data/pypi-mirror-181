import time, os, json, argparse #standard imports
import tsv_calendar
from bunzbar import config, infos
from sh import xsetroot

CFGDIR = os.path.join(os.path.expanduser('~'), '.config/bunzbar/')
CONFIGFILE = os.path.join(CFGDIR, 'config.json')

c = config.config()

if "tsv" in c.active():
    if c.exists("tsv_path"):
        tsv = tsv_calendar.TSV_Read(os.path.join(CFGDIR, "ht.tsv"))

class bar:
    def __init__(self):
        #smash or
        pass
    
    
    def getstr(self, name):
        if name.startswith('infos'):
            return str(eval(f'infos.{name}(self)'))
        elif name.startswith('tsv'):
            if name.split(".")[1] == 'current':
                return str(tsv.current(eval(f'tsv_calendar.GET.{name.split(".")[2].upper()}')))
            else: 
                return str(tsv.next(eval(f'tsv_calendar.GET.{name.split(".")[2].upper()}')))
        else:
            return '<error>'

    def compose(self):
        mstr = ""
        for name in c.active():
            mstr += name.upper() + " "
            mstr += self.getstr(name)
            mstr += " | "
        return mstr

    def updatebar(self, speed=1):
        while 1:
            mstr = self.compose()
            shift = round((time.time()*(1/speed))%len(mstr))
            sstr = self.shiftstr(mstr, shift)
            self.changeprop(sstr)

    def changeprop(self, txt):
        xsetroot('-name', txt)

    def shiftstr(self, s, k):
        return(  ((s+" ")[-k-1:-1])  +  ((s+" ")[0:-k-1])  )    

    #toggle info
    def toggle(self, arr):
        data = json.load(open(CONFIGFILE))
        for info in arr:
            if info in data["active"]:
                data["active"].remove(info)
            else:
                if info in data["available"]:
                    data["active"].append(info)
        open(CONFIGFILE, 'w').write(json.dumps(data, indent=4))

def main():                                  
    parser = argparse.ArgumentParser(
        prog = 'bunzbar',
        description = 'display information in status bar',
        epilog = 'stay hydrated kidz')
    
    parser.add_argument('-t', '--toggle', metavar='<info>', type=str, nargs='+')
    parser.add_argument('-s', '--service', action='store_true') 

    args = vars(parser.parse_args())
    
    c.update()

    barn = bar()
    if args['toggle']:
        barn.toggle(args['toggle'])
    if args['service']:
        barn.updatebar()
