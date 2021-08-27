import json
import time
import sys


# Open JSON file
def open_file(filename: str) -> list:
    try:
        with open(filename, 'r') as f:
            data: list = json.load(f)
            f.close()
    except OSError:
        print("Couldn't open/read file: {0}".format(filename))
        sys.exit()
    return data


# Cut lines if needed
def cut_lines(data: list) -> list:
    for idx in range(len(data)):
        if len(data[idx]) >= 50:
            data[idx] = data[idx].rstrip()[:50] + '...'
    return data


# Create a user file and write data
def write_to_file(user_id, completed: list, uncompleted: list):
    filename: str = '{id}_{date}T{time}.txt'.format(
        id=user_id,
        date=time.strftime("%Y-%m-%d"),
        time=time.strftime("%H-%M"))
    f = open(filename, 'w')
    completed = cut_lines(completed)
    uncompleted = cut_lines(uncompleted)

    data: str = '# Сотрудник №{id}\n{date}\n\n' \
                '## Завершённые задачи:\n' \
                '{completed}\n\n' \
                '## Оставшиеся задачи:\n' \
                '{uncompleted}'.format(id=user_id,
                                       date=time.strftime("%d.%m.%Y %H:%M"),
                                       completed='\n'.join(completed),
                                       uncompleted='\n'.join(uncompleted))
    f.write(data)
    f.close()


# Parse JSON
def parse_file(all_users: list):
    cur_user_id = all_users[0]['userId']
    completed: list = []
    uncompleted: list = []

    for idx in range(len(all_users)):
        try:
            if cur_user_id != all_users[idx]['userId']:
                write_to_file(cur_user_id, completed, uncompleted)
                completed.clear()
                uncompleted.clear()

        except KeyError:
            write_to_file(cur_user_id, completed, uncompleted)
            completed.clear()
            uncompleted.clear()
            break

        cur_user_id = all_users[idx]['userId']
        if all_users[idx]['completed']:
            completed.append(all_users[idx]['title'])
        else:
            uncompleted.append(all_users[idx]['title'])


file = open_file('venv/todos.json')
parse_file(file)
