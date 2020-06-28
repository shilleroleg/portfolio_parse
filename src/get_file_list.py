import os


def get_file_list(directory_name):
    """Получаем список всех файлов из заданной директории.
    Возвращаем список файлов с полными путями"""
    # # текущая рабочая директория
    # work_dir = os.getcwd()
    tree = os.walk(directory_name)

    file_list = []

    for root, dirs, files in tree:
        if not dirs and files:
            for file_ in files:
                file_ext = file_.split(".")[-1]
                if len(file_) > 24 \
                        and (file_ext == "xls" or file_ext == "xlsx") \
                        and file_.startswith("18645"):     # Выделяем только ежедневные отчеты, не ежемесячные
                    path = os.path.join(directory_name, root, file_)  # формирование адреса
                    file_list.append(path)

    return file_list


def get_unique_file(full_file_list, short_file_list):
    """Сравниваем два списка файлов (с полными путями)
    и возвращем список имен файлов присутствующий только в одном списке"""
    list_dif = [i for i in full_file_list + short_file_list if i not in full_file_list or i not in short_file_list]
    return list_dif

