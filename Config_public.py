# devs in format: {'gitlab_nick_name': '@telegram_nick_name'}
# sample: 'mike1989': '@m_petrov'
developers = {
    'none': '❌ Не указан assignee, штраф 1000 золотых',
    'noSuchUser': '💢🤦‍♀ Не поняла, это кто?'
}

debug_mode_is_on = False
sound_is_on = True
boss_on_vacation = True

api_bot_token = your_api_bot_token
dev_chat_id = your_dev_chat_id

headers = {'PRIVATE-TOKEN': 'your_token'}
project_number = your_project_number

opened_merge_requests_url = f'https://gitlab.com/api/v4/projects/{project_number}/merge_requests?state=opened'
merge_requests_url = f'https://gitlab.com/api/v4/projects/{project_number}/merge_requests/'
animation_url = 'https://media.giphy.com/media/3o85xLah7LslQEqldm/giphy.gif?cid=ecf05e4732m4x06zxgt7guej7ljpxpzfg2wn1h6aa9g5of4e&ep=v1_gifs_related&rid=giphy.gif&ct=g'
delay_in_seconds = 60
required_approves_count = 3
work_days_count = 5
work_days = list(range(work_days_count))

schedule = {
    '10:00',
    '13:00',
    '16:00'
}

daily_schedule = {
    0: '17:00',
    1: '17:00',
    2: '17:00',
    3: '17:00',
    4: '16:00'
}
