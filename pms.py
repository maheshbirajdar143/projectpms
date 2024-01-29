# python3 /Mahesh_Work/Pipeline_VFX/pms/openslate/manage.py runserver 0.0.0.0:8000
# nohup = no hang up ( running continuosly in background)
# ps aux | grep manage.py  (to stop the project)
# kill PID
# code --no-sandbox --user-data-dir



import subprocess
import os

def run_server():
    virtualenv_path = "/core/Software/IT/Mahesh_Work/Pipeline_VFX/pms/openslate20122023/os1/bin/activate"
    manage_py_path = "/core/Software/IT/Mahesh_Work/Pipeline_VFX/pms/openslate20122023/openslate/manage.py"
    runserver_command = f"source {virtualenv_path} && python3 {manage_py_path} runserver 0.0.0.0:8000"

    try:
        subprocess.run(runserver_command, shell=True, check=True, executable='/bin/bash')
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_server()









