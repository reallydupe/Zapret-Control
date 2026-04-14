import subprocess

startupinf = subprocess.STARTUPINFO()
startupinf.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinf.wShowWindow = subprocess.SW_HIDE


STARTF_USESHOWWINDOW = 0x00000001
SW_HIDE = 0
CREATE_NO_WINDOW = 0x08000000

def Check_stat(depth):
    if depth == 1:
        return test_service('WinDivert') #Если че эта фигня не нужна если честно я ее по приколу оставил так как она почти всегда будет True
    elif depth == 2:
        TS1 = test_service('WinDivert')
        CPR = check_process_running('winws.exe')
        return TS1, CPR
    else:
        Check_stat(1)


def get_service_status(service_name):
    try:
        result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True, encoding='cp866', startupinfo=startupinf, creationflags=subprocess.CREATE_NO_WINDOW)
        
        for line in result.stdout.split('\n'):
            if 'STATE' in line:
                parts = line.split()
                if len(parts) >= 4:
                    return parts[3]
        
        return None
    except Exception as e:
        print(f"Ошибка при проверке службы {service_name}: {e}")
        return None
def check_service_exists(service_name):
    """Проверяет, существует ли служба с таким именем"""
    try:
        result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True, encoding='cp866', startupinfo=startupinf, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.returncode == 0
    except:
        return False


def check_process_running(process_name):
    try:
        result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}'], capture_output=True, text=True, startupinfo=startupinf, creationflags=subprocess.CREATE_NO_WINDOW)
        return process_name in result.stdout
    except:
        return False

def test_service(service_name, soft_check=False):
    status = get_service_status(service_name)
    
    if status == 'RUNNING':
        if soft_check:
            return False
        else:
            return True
    elif status == 'STOP_PENDING':
        return False
    else:
        return False