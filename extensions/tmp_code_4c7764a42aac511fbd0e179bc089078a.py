import datetime

def get_current_time():
    current_time = datetime.datetime.now()
    return current_time

result = get_current_time()
print(result)