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
datastore_client = datastore.Client()
start_time = time.perf_counter()
p1 = mp.Process(target=create_record_table1, args=(datastore_client, "Task", "12345623784574"))
p2 = mp.Process(target=create_recod_table2, args=(datastore_client, "Employee_table", "234564438589475"))

p1.start()
p2.start()
p1.join()
p2.join()

end_time = time.perf_counter()
print(f"Done with datastore update... in {round(end_time- start_time, 2)} second(s)")

# create_record_table1(datastore_client, "demo_new","425435543")