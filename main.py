import first_part
import  second_part

programm_type = int(input('Укажите режим работы программы:'
                          '\n1 - извлечение битовых плоскостей, '
                          '\n2 - внедрение данных в битовую плоскость\n'))

if programm_type == 1:
    first_part.main()
if programm_type == 2:
    second_part.main()