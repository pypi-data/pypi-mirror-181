import os
from sparrow import rel_to_abs


def milvus(flag='start'):
    db_path = rel_to_abs('./milvus_db')
    if flag == "start":
        os.system(f"cd {db_path} &&make start")
    elif flag == "stop":
        os.system(f"cd {db_path} &&make stop")
    elif flag == 'rm':
        os.system(f"cd {db_path} &&make rm-data")
    else:
        raise ValueError("flag must be 'start' or 'stop' or 'rm'")

