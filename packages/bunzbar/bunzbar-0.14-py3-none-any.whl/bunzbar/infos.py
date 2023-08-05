import time
from sh import acpi

class infos: 
    def __init__(self):
        pass

    def battery(self):
        acpi_text = str(acpi())

        acpi_split = acpi_text.replace(',', '').replace('\n', ' ').split(' ')
        acpi_per = []
        for acpi_lul in acpi_split:
            if '%' in acpi_lul:
                acpi_per.append(int(acpi_lul.replace('%', '')))
            
        if len(acpi_per):
            return(str(sum(acpi_per)/len(acpi_per))+'%')
        else:
            return("no battery")
            
    def clck(self):
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        return(curr_time)

