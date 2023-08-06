import time
import multiprocessing as mp
from google.cloud import datastore



def create_record_table1(datastore_client, task, id):
    kind = task
    id = id
    task_key = datastore_client.key(kind, id)
    task = datastore.Entity(key=task_key)
    task["description"] = "new records created by scripts"
    datastore_client.put(task)

    print(f"Saved {task.key.name}: {task['description']}")


def create_recod_table2(datastore_client, task, id):
    kind = task
    id = id
    task_key = datastore_client.key(kind, id)
    task = datastore.Entity(key=task_key)
    # task["description"] = "new records created by scripts"
    task.update({'address':"Nagpur", "age":"27", "designation":"QA", "emp_name":"Test1", "description":"New Test employee record created by python scripts"})
    datastore_client.put(task)
    

    print(f"Saved {task.key.name}: {task['description']}")



# Instantiates a client


# create_record_table1(datastore_client, "demo_new","425435543")