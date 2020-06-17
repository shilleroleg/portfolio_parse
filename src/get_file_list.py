import os


def get_file_list(file_name):
    # # текущая рабочая директория
    # work_dir = os.getcwd()
    tree = os.walk(file_name)

    file_list = []

    for root, dirs, files in tree:
        if not dirs and files:
            for file_ in files:
                file_ext = file_.split(".")[-1]
                if len(file_) > 24 \
                        and (file_ext == "xls" or file_ext == "xlsx") \
                        and file_.startswith("18645"):     # Выделяем только ежедневные отчеты, не ежемесячные
                    path = os.path.join(file_name, root, file_)  # формирование адреса
                    file_list.append(path)

    return file_list
