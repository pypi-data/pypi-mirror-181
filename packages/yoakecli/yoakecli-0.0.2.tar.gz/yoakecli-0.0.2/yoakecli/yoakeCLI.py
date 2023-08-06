import os
from .simpleRequest import *
from .styling import *
from .player import Player

def get_input(options, dialog=''):
    if len(options) == 0:
        return None

    if isinstance(options, list):
        options = dict(map(lambda x: (str(x[0]), x[1]), enumerate(options, start=1)))

    if 'q' not in options:
        options.update({'q': 'Thoát'})
        
    if isinstance(options, dict):
        count = 0
        for key, value in options.items():
            if key in ('b', 'q'):
                print_style('{}. {}'.format(key, value), Text.BOLD, Text.RED)
            else:
                print_style('{}. {}'.format(key, value), Text.YELLOW if count % 2 == 0 else Text.CYAN)
                count += 1
        while True:
            value = input(string_style('> ' + dialog, Text.ITALIC, Text.MAGENTA)).strip().casefold()
            if not value in options.keys():
                print('Vui lòng nhập lựa chọn hợp lệ!')
                continue
            if value == 'q':
                exit()
            return value

def get_key():
    key_path = os.path.expanduser("~/.ykey")
    key = ''
    if os.path.isfile(key_path):
        with open(key_path, mode='r') as file:
            content = file.read().strip()
            if len(content) > 0:
                key = content

    fail = 0
    while True:
        if not key:
            key = input(string_style('> Nhập key: ', Text.ITALIC, Text.MAGENTA)).strip()
            fail += 1
            continue
        
        if request(f'{domain}{endpoint["testuserkey"]}', params={'key':key}, data_as_json=False).status == 200:
            with open(key_path, mode='w') as file:
                file.write(key)
            if fail > 0:
                cursor_up(fail)
                erase_screen_from_cursor()
            return key
        key = ''
        print_style('Key không tồn tại!', Text.BOLD, Text.RED)
        fail += 1

def lastest_season(key):
    response = request(f'{domain}{endpoint["lastestseason"]}', params={'key':key})

    if response.status == 200:
        data = response.json()
        while True:
            print_style('Anime mùa mới nhất gồm có', Text.UNDERSCORE, Text.BOLD, Text.BLUE)
            option = get_input({
                **dict(map(lambda x: (str(x[0]), x[1]['name']), enumerate(data, start=1))),
                'b': 'Quay lại',
            }, 'Chọn anime: ')
            if option == 'b':
                break
            anime = data[int(option) - 1]
            print()
            choose_eps(key, anime)
            print()

def choose_eps(key, anime):
    season = anime['videos_includes']
    while True:
        print_style('Chọn tập mà bạn muốn xem', Text.UNDERSCORE, Text.BOLD, Text.BLUE)
        option = get_input({
            **dict(map(lambda x: (str(x[0]), 'Tập ' + x[1]['eps']), enumerate(season, start=1))),
            'b': 'Quay lại',
        }, 'Chọn tập: ')
        if option == 'b':
            break
        ep_index = int(option) - 1

        while True:
            eps = season[ep_index]
            print_style('Player đang khởi động', Text.BLUE, endchar='\r')
            playable = Player.play(eps, anime)
            erase_line()
            if playable:
                response = request(f'{domain}{endpoint["updateprogress"]}', params={'key':key,'videoid':eps['id']})
            else:
                print_style('Không tìm thấy player phù hợp để phát.', Text.RED, Text.BOLD)
            print()

            available_options = {
                'p': 'Tập trước',
                'n': 'Tập sau',
                'r': 'Xem lại',
                'b': 'Quay lại',
                'q': 'Thoát'
            }

            if ep_index == 0:
                available_options.pop('p')
            if ep_index == len(season) - 1:
                available_options.pop('n')

            option = get_input(available_options, 'Nhập 1 trong các lựa chọn trên: ')
            if option == 'p':
                ep_index -= 1
            elif option == 'n':
                ep_index += 1
            elif option == 'b':
                break
        print()

def main():
    start_sentence = string_style('Chào mừng đến với Yoake.moe CLI bạn muốn chọn gì', Text.UNDERSCORE, Text.BOLD, Text.GREEN) + '\n'
    key = None
    while True:
        if not key:
            key = get_key()
        print(start_sentence, end='')
        start_sentence = string_style('Menu chính', Text.UNDERSCORE, Text.BOLD, Text.BLUE) + '\n'
        option = get_input([
            'Anime mùa mới nhất',
            'Chức năng này đang xây dựng',
        ], 'Nhập 1 trong các lựa chọn trên: ')

        option_function = call_dict.get(option)
        if callable(option_function):
            print()
            option_function(key)
        print()

endpoint = {
    'testuserkey': '/test.php',
    'lastestseason': '/latestinseason.php',
    'updateprogress': '/useranimeprogress.php'
}
# domain = 'http://localhost'
# domain = 'http://192.168.1.8'
domain = 'https://api.huydofumi.tech'
call_dict = {
    '1': lastest_season,
}

if __name__ == "__main__":
    main()