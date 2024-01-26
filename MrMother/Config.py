# GITHUB configuration
GIT_HUB_TOKEN = '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'
HEADERS = {'Authorization': f'Bearer {GIT_HUB_TOKEN}'}
PRS_URL = 'https://api.github.com/repos/qral-scan/usb/pulls'

# devs in format: {'github_nick_name': '@telegram_nick_name'}
DEVELOPERS = {
    'no_reviewers': 'Не указаны reviewers, арест на 15 суток 👮🏻♥️',
    'no_assignee': 'Не указан assignee, лишение прав 👮🏻♥️',
    '@KalininArtemVal': '@kalinin_artem_val',
    '@Weysinaction' : '@Weysinaction',
    '@RuslanMirosh' : '@r_miroshnichenko',
    '@OsyaginMaxim' : '@m_osyagin',
    '@MatveyBlackman' : '@Elrik_Shefa',
    '@perlinleo' : '@lperlin'
}

# GITLAB configuration
headers = {'PRIVATE-TOKEN': 'your token'}
project_number = 11111111
opened_merge_requests_url = f'https://gitlab.com/api/v4/projects/{project_number}/merge_requests?state=opened'
merge_requests_url = f'https://gitlab.com/api/v4/projects/{project_number}/merge_requests/'

# devs in format: {'gitlab_nick_name': '@telegram_nick_name'}
developers = {
    'none': '❌ Не указан assignee, штраф 1000 золотых',
    'noSuchUser': '💢🤦‍♀ Не поняла, это кто?'
}

# Common
animation_url = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDhlZ3IwenJjNThybGFkbnN2NW56ODJ6YWZkcXVlcHRpdHk0ZTFyMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10M8Yr4WKJK63e/giphy.gif'
delay_in_seconds = 60
required_approves_count = 3
work_days_count = 5
work_days = list(range(work_days_count))

# Change to switch between Copy bot and MrMother bot:
debug_mode_is_on = False
sound_is_on = True

# copy bot for testing
api_copy_bot_token = 'api_copy_bot_token'
# another bot for production
api_mr_mother_bot_token = '6526138195:AAHf0fmswwE3ipP-IcFBhFKO8ITQ13wX3Tw'

dev_copy_chat_id = -1001683561519
dev_ios_internal_chat_id = -1001683561519

api_bot_token = api_copy_bot_token if debug_mode_is_on else api_mr_mother_bot_token
dev_chat_id = dev_copy_chat_id if debug_mode_is_on else dev_ios_internal_chat_id

schedule = {
    '10:00',
    '12:05',
    '15:30',
    '17:30',
}

daily_schedule = {
    0: '16:00',
    1: '16:00',
    2: '16:00',
    3: '16:00',
    4: '16:00'
}