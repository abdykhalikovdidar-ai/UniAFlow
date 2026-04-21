import os

def print_project_tree(startpath, exclude_dirs=None):
    # Папки, которые мы не хотим видеть в выводе (чтобы не засорять экран)
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'venv', '__pycache__', '.idea', 'migrations', 'staticfiles'}

    print(f"Структура проекта: {os.path.abspath(startpath)}\n")
    
    for root, dirs, files in os.walk(startpath):
        # Удаляем исключенные папки из списка, чтобы os.walk в них не заходил
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Вычисляем уровень вложенности для красивых отступов
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        
        # Печатаем название папки
        folder_name = os.path.basename(root)
        if folder_name:
            print(f'{indent}📂 {folder_name}/')
            
        subindent = ' ' * 4 * (level + 1)
        
        # Печатаем файлы внутри папки
        for f in files:
            # Игнорируем скрытые файлы (например .DS_Store) и скомпилированные файлы питона
            if not f.startswith('.') and not f.endswith('.pyc'):
                print(f'{subindent}📄 {f}')

if __name__ == '__main__':
    # Запускаем скрипт для текущей директории
    print_project_tree('.')