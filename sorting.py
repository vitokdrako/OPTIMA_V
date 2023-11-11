# Додати функцію для сортування в main.py, вона буде приймати шлях до теки, яку потрібно буде відсортувати - def sort_files_handler()
# Додати команду для сортування в COMMANDS (пропоную - sort_files_handler: "sort file")
# Додати в main обробку команди сортування

# Code:
import sys
from pathlib import Path
import shutil
import re


CATEGORIES = {'images':['.jpeg', '.png', '.jpg', '.svg'],
             'video':['.avi', '.mp4', '.mov', '.mkv'],
             'documents':['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
             'audio':['.mp3', '.ogg', '.wav', '.amr'],
             'archives':['.zip', '.gz', '.tar']}

dict_of_categories_files = {}

known_formats, other_formats = set(), set()

dict_of_files_for_duplicates = {}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANSLATION_DICT = {}


def create_translation_dict() -> dict:  
    for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANSLATION_DICT[ord(cyr)] = lat
        TRANSLATION_DICT[ord(cyr.upper())] = lat.upper()
    
    return TRANSLATION_DICT


def normalize(name_of_path:str) -> str:         
    return re.sub('\W', '_', name_of_path.translate(TRANSLATION_DICT))


def define_category(file_format:str) -> str:
    if [k for k in CATEGORIES if file_format in CATEGORIES[k]]:
        return [d for d in CATEGORIES if file_format in CATEGORIES[d]][0]
    else:
        return 'other'
    

def sort_files_for_lists(category:str, file_name:str, file_format:str) -> None:  
    if category not in (dict_of_categories_files):
        dict_of_categories_files.update({category:[file_name]})
    else:
        dict_of_categories_files[category].append(file_name) 

    other_formats.add(file_format) if category == 'other' else known_formats.add(file_format)


def check_duplicates(file_name:str) -> int:
    if file_name not in dict_of_files_for_duplicates:
        dict_of_files_for_duplicates.update({file_name:1})
    else:
        dict_of_files_for_duplicates[file_name] = dict_of_files_for_duplicates[file_name] + 1

    return dict_of_files_for_duplicates[file_name]


def unpack_archive(archive:Path) -> None:
    path_for_unpacking_archives = str(archive)[:-(len(archive.suffix))]
    shutil.unpack_archive(archive, path_for_unpacking_archives)      


def removing_folders(current_folder:Path) -> None:
    if len([f for f in current_folder.iterdir()]) == 0:
        current_folder.rmdir()
        removing_folders(current_folder.parent)


def sort_folders(path:Path) -> None:    
    for i in path.iterdir():
        new_name = normalize(i.name.replace(i.suffix,'')) 
        
        if i.is_dir() and i.name not in (CATEGORIES):
            if len([f for f in i.iterdir()]) == 0:
                i.rmdir()       
            else:          
                i = i.rename(Path(i.parent).joinpath(new_name))
                path = (path).joinpath(i)                
                sort_folders (path)
                
        if i.is_file():
            category = define_category(i.suffix)
            target_path_to_create = Path(sys.argv[1]).joinpath(category)
            
            if not target_path_to_create.exists():
                target_path_to_create.mkdir()

            sort_files_for_lists(category, i.name, i.suffix)
            count_of_duplicates = check_duplicates (i.name)
                
            new_name = new_name + '_' + str(count_of_duplicates) + i.suffix if count_of_duplicates > 1 else new_name + i.suffix
            
            destination_folder = Path(sys.argv[1]).joinpath(category, new_name)  
            i.replace(destination_folder)
            
            if category == 'archives':
                unpack_archive(destination_folder)

            removing_folders(i.parent)


def sort_folders_and_return_result(path: Path) -> str:
    create_translation_dict()
    sort_folders(path)

    result = ""
    for k, v in dict_of_categories_files.items():
        result += f'{k.upper():^100}\n{v}\n'

    result += f'known_formats={known_formats}\nother_formats={other_formats}\n'
    
    return result

def main() -> None:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        print('Шлях до теки не вказаний')
        return

    if not path.exists():
        print('Тека не існує')
        return

    create_translation_dict()
    sort_folders(path)

    # Визначте ім'я файлу для зберігання результатів
    output_filename = 'output.txt'

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for k, v in dict_of_categories_files.items():
            output_file.write(f'{k.upper():^100}\n{v}\n\n')

        output_file.write(f'known_formats={known_formats}\nother_formats={other_formats}')

    print(f'Результати збережено у файлі {output_filename}')

if __name__ == '__main__':
    main()