import time, os, json, argparse
import tsv_calendar
import bunzbar.config

CFGDIR = os.path.join(os.path.expanduser('~'), '.config/bunzbar/')
CONFIGFILE = os.path.join(CFGDIR, 'config.json')

class bar:
    def __init__(self, cfgdir, config):
        self.cfgdir = cfgdir
        self.config = config

    def compose(self):
        mstr = ""
        for name in self.config.active():
            mstr += name.upper() + " "
            mstr += self.config.getf(name)
            mstr += " | "
        return mstr

    def shift(self, s, k):
        return(((s+" ")[-k-1:-1])+((s+" ")[0:-k-1]))

    def serve(self, speed=1):
        try:
            while True:
                compstr = self.compose()
                shift = round((time.time()*(1/speed))%len(compstr))
                sstr = self.shift(compstr, shift)
                os.system(f'xsetroot -name "{sstr}"')
        except KeyboardInterrupt:
            exit(0)

def main():                                  
    parser = argparse.ArgumentParser(
        prog = 'bunzbar',
        description = 'display information in status bar',
        epilog = 'stay hydrated kidz')
    
    parser.add_argument('-t', "--toggle", metavar="<info>", type=str, nargs='+')
    parser.add_argument('-c', "--config", action="store_true")
    parser.add_argument('-s', "--service", action="store_true") 

    args = vars(parser.parse_args()) 
    
    c = bunzbar.config.config()
    c.update()
    
    b = bar(CONFIGFILE, c)

    if args['toggle']:
        c.toggle(args['toggle'])
    if args['service']:
        b.serve()
