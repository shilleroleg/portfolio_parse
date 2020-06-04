import os

# текущая рабочая директория
work_dir = os.getcwd()

tree = os.walk('report')

file_list = []

for root, dirs, files in tree:
    if not dirs and files:
        # print(root, files)
        for file_ in files:
            if len(file_) > 24:     # Выделяем только ежедневные отчеты, не ежемесячные
                path = os.path.join(work_dir, root, file_)  # формирование адреса
                file_list.append(path)

print(file_list)
