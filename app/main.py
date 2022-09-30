import json

PATH = 'D:/Projects/Python/allure-results-parser/app/data'


def read_json_behavior() -> dict:
    """Чтения данных с ошибками из behaviors.json
    """
    with open(PATH + '/behaviors.json', encoding="utf8") as f:
        raw_data = json.load(f)
    return raw_data


def get_uid_error_tests(raw_data: dict) -> list:
    """Получение uid тестов, которые упали
    """
    ids: list = []
    with open(PATH + '/behaviors.json', encoding="utf8") as f:
        raw_data = json.load(f)
    for epic in raw_data['children']:
        if epic.get('children'):
            for feature in epic['children']:
                if feature.get('children'):
                    for story in feature['children']:
                        if story.get('children'):
                            for title in story['children']:
                                if title.get('status') == 'broken' or title.get('status') == 'failed':
                                    ids.append(title['uid'])
                        else:
                            if story.get('status') == 'broken' or story.get('status') == 'failed':
                                ids.append(story['uid'])
                else:
                    if feature.get('status') == 'broken' or feature.get('status') == 'failed':
                        ids.append(feature['uid'])
        else:
            if epic.get('status') == 'broken' or epic.get('status') == 'failed':
                ids.append(epic['uid'])
    return ids





def read_json_test_description(uid: str) -> dict:
    """Чтение данных из файла с именем test-cases/<uid>.json
    """
    with open(PATH + f'/test-cases/{uid}.json', encoding="utf8") as f:
        raw_data = json.load(f)
    return raw_data


def get_data_tests(uids: list) -> dict:
    """Получение полей с данными об упавших тестах
    """
    result: dict = dict()
    for uid in uids:
        data = read_json_test_description(uid)
        result[data['name']] = {'status': data['status'], 
                'error': data['statusMessage'], 
                'descriptionHtml': data['descriptionHtml']
            }
    return result

with open('result.txt', 'w', encoding="utf8") as f:
    f.write(f'Всего ошибок: {len(get_data_tests(get_uid_error_tests(read_json_behavior())).items())}\n\n\n\n')
    for name, value in get_data_tests(get_uid_error_tests(read_json_behavior())).items():
        f.write(f'Название: {name}\n')
        f.write(f'\tСтатус: {value["status"]}\n')
        f.write(f'\tОшибка: {value["error"]}\n')
        f.write(f'\tОписание: {value["descriptionHtml"]}\n\n\n\n')


# def test_json_result():
#     result = []
#     with open(PATH + '/behaviors.json', encoding="utf8") as f:
#         raw_data = json.load(f)
#     for epic in raw_data['children']:
#         print('Epic: ' + epic['name'])
#         if epic.get('children'):
#             for feature in epic['children']:
#                 print('Feature: ' + feature['name'])
#                 if feature.get('children'):
#                     for story in feature['children']:
#                         print('Story: ' + story['name'])
#                         if story.get('children'):
#                             for title in story['children']:
#                                 if title.get('status') == 'broken' or title.get('status') == 'failed':
#                                     print(title['name'])
#                                     print(title['status'])
#                                     print(title['uid'])
#                                     result.append(title['uid'])
#                         else:
#                             if story.get('status') == 'broken' or story.get('status') == 'failed':
#                                 print(story['name'])
#                                 print(story['status'])
#                                 print(story['uid'])
#                                 result.append(story['uid'])
#                 else:
#                     if feature.get('status') == 'broken' or feature.get('status') == 'failed':
#                         print(feature['name'])
#                         print(feature['status'])
#                         print(feature['uid'])
#                         result.append(feature['uid'])
#         else:
#             if epic.get('status') == 'broken' or epic.get('status') == 'failed':
#                 print(epic['name'])
#                 print(epic['status'])
#                 print(epic['uid'])
#                 result.append(epic['uid'])

#     print(result)

# test_json_result()
