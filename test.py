from auto_huatai import AutoHuatai
import configparser,time
import pywinauto 

def get_config(cfg_file):
    config = configparser.ConfigParser()
    config.read(cfg_file)
    app_path=config.get('huatai','app_path')
    account=config.get('huatai','account')
    pwd=config.get('huatai','pwd')
    pwd2=config.get('huatai','pwd2')
    return (app_path,account,pwd,pwd2)

# exe_path,account,pwd,pwd2=get_config('huatai_me.config')
exe_path,account,pwd,pwd2=get_config('huatai.config')
ht=AutoHuatai(exe_path, account, pwd, pwd2)
# ht._main_frame.print_control_identifiers(depth=2)
time.sleep(1)
ht.change_menu('信用')
time.sleep(1)
ht.credit_holds()
