import os, time, psutil
from psutil import _common
from psutil._common import bcat, cat, sbattery

POWER_SUPPLY_PATH = "/sys/class/power_supply"

def sensors_battery_multi():
    """Return battery information.
    Implementation note: it appears /sys/class/power_supply/BAT0/
    directory structure may vary and provide files with the same
    meaning but under different names, see:
    https://github.com/giampaolo/psutil/issues/966
    """
    null = object()

    def multi_bcat(*paths):
        """Attempt to read the content of multiple files which may
        not exist. If none of them exist return None.
        """
        for path in paths:
            ret = bcat(path, fallback=null)
            if ret != null:
                try:
                    return int(ret)
                except ValueError:
                    return ret.strip()
        return None

    bats = [x for x in os.listdir(POWER_SUPPLY_PATH) if x.startswith('BAT') or
            'battery' in x.lower()]
    if not bats:
        return None

    def batsum(arr):
        while None in arr:
            arr.remove(None)
        if len(arr):
            return(sum(arr))
        else:
            return(None)

    energy_now_array = []
    power_now_array = []
    energy_full_array = []
    time_to_empty_array = []

    

    # Get the first available battery. Usually this is "BAT0", except
    # some rare exceptions:
    # https://github.com/giampaolo/psutil/issues/1238
    for bat in sorted(bats):
        root = os.path.join(POWER_SUPPLY_PATH, bat)

        # Base metrics.
        energy_now_array.append(multi_bcat(
            root + "/energy_now",
            root + "/charge_now"))
        power_now_array.append(multi_bcat(
            root + "/power_now",
            root + "/current_now"))
        energy_full_array.append(multi_bcat(
            root + "/energy_full",
            root + "/charge_full"))
        time_to_empty_array.append(multi_bcat(root + "/time_to_empty_now"))

    
    energy_now = batsum(energy_now_array)
    power_now = batsum(power_now_array)
    energy_full = batsum(energy_full_array)
    time_to_empty = batsum(time_to_empty_array)

    # Percent. If we have energy_full the percentage will be more
    # accurate compared to reading /capacity file (float vs. int). 
    percent = 0.0

    for bat in sorted(bats):
        root = os.path.join(POWER_SUPPLY_PATH, bat)

        if energy_full is not None and energy_now is not None:
            try:
                percent = 100.0 * energy_now / energy_full
            except ZeroDivisionError:
                percent = 0.0
        else:
            percent = int(cat(root + "/capacity", fallback=-1))
            if percent == -1:
                return None

    # Is AC power cable plugged in?
    # Note: AC0 is not always available and sometimes (e.g. CentOS7)
    # it's called "AC".
    power_plugged = None
    online = multi_bcat(
        os.path.join(POWER_SUPPLY_PATH, "AC0/online"),
        os.path.join(POWER_SUPPLY_PATH, "AC/online"))
    
    
    for bat in sorted(bats):
        root = os.path.join(POWER_SUPPLY_PATH, bat)
        if online is not None:
            power_plugged = online == 1
        else:
            status = cat(root + "/status", fallback="").strip().lower()
            if status == "discharging":
                power_plugged = False
            elif status in ("charging", "full"):
                power_plugged = True

    # Seconds left.
    # Note to self: we may also calculate the charging ETA as per:
    # https://github.com/thialfihar/dotfiles/blob/
    #     013937745fd9050c30146290e8f963d65c0179e6/bin/battery.py#L55
    if power_plugged:
        secsleft = _common.POWER_TIME_UNLIMITED
    elif energy_now is not None and power_now is not None:
        try:
            secsleft = int(energy_now / power_now * 3600)
        except ZeroDivisionError:
            secsleft = _common.POWER_TIME_UNKNOWN
    elif time_to_empty is not None:
        secsleft = int(time_to_empty * 60)
        if secsleft < 0:
            secsleft = _common.POWER_TIME_UNKNOWN
    else:
        secsleft = _common.POWER_TIME_UNKNOWN

    return percent

class infos: 
    def __init__(self):
        pass

    def clck(self):
        return(time.strftime("%H:%M:%S", time.localtime()))

    def battery(self):
        try:
            percent = sensors_battery_multi()
            return(str(percent))
        except:
            return None
        
    def cpu(self):
        return(str(psutil.cpu_percent)+"%")

    
