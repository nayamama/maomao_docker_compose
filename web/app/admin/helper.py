import psutil

def get_system_info():
    used_cpu_percent = psutil.cpu_percent() / 100
    used_disk_percent = psutil.disk_usage('/').percent / 100
    free_disk_size = psutil.disk_usage('/').free 

    return used_cpu_percent, used_disk_percent, free_disk_size

