import time, psutil

class infos: 
    def __init__(self):
        pass

    def clck(self):
        return(time.strftime("%H:%M:%S", time.localtime()))

    def battery(self):
        percentage = round(psutil.sensors_battery().percent, 3)
        return( str(percentage) )
        
    def cpu(self):
        return(str(psutil.cpu_percent)+"%")

    
