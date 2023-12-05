from Config import *
import requests
import json


class GitlabManager:
    def __init__(self):
        self.approved_data = {}
        self.need_approve_data = {}

    def get_dev_telegram_name(self, users_from_description):
        telegram_names = []
        for user in users_from_description:
            name = user.removeprefix('@')
            if name in developers.keys():
                telegram_names.append(developers[name])
            else:
                telegram_names.append(f'{developers["noSuchUser"]} {user}')

        return telegram_names

    def get_not_in_draft_mrs(self):
        response = requests.get(opened_merge_requests_url, headers=headers).text
        opened_merge_requests = json.loads(response)
        return filter(lambda item: item['draft'] is False, opened_merge_requests)

    def clear_data(self):
        self.need_approve_data.clear()
        self.approved_data.clear()

    def get_approved_developers(self, mr):
        iid = str(mr['iid'])
        url = merge_requests_url + iid + '/approvals'
        get_approved_mrs = requests.get(url, headers=headers).text
        approved_mrs_dict = json.loads(get_approved_mrs)
        return approved_mrs_dict['approved_by']

    def get_users_from_description(self, mr):
        users_from_description_str = str(mr['description'])
        users_from_description_with_task = users_from_description_str.split()
        users_from_description_filtered = filter(lambda word: '@' in word, users_from_description_with_task)
        return list(users_from_description_filtered)

    def load_mr_data(self):
        not_in_draft = self.get_not_in_draft_mrs()

        for mr in not_in_draft:
            approved_developers = self.get_approved_developers(mr)
            assignee = 'none' if mr['assignee'] is None else str((mr['assignee'])['username'])
            assignee_telegram_name = developers[assignee]
            web_url = str(mr['web_url'])

            has_conflicts = mr['has_conflicts']
            has_conflicts_msg = '\n🎪 Ветки конфликтуют' if has_conflicts else ''

            discussions_resolved = mr['blocking_discussions_resolved']
            discussions_resolved_msg = '' if discussions_resolved is True else "\n💥 Нашла замечания"

            need_send_ready_to_merge_msg = len(
                approved_developers) >= required_approves_count and discussions_resolved and not has_conflicts
            ready_to_merge_msg = f'\n🐢 Assignee: {assignee_telegram_name}, можно вливать 🚀' if need_send_ready_to_merge_msg else ''

            key = web_url + discussions_resolved_msg + ready_to_merge_msg + has_conflicts_msg
            mr_data = {key: approved_developers}
            users_from_description = self.get_users_from_description(mr)
            to_telegram_names = self.get_dev_telegram_name(users_from_description)

            if need_send_ready_to_merge_msg:
                to_telegram_names = []
            else:
                try:
                    to_telegram_names.append(assignee_telegram_name)
                except BaseException as error:
                    if error:
                        to_telegram_names.append(f'{developers["noSuchUser"]} {assignee}')

            need_approve_developers = {key: to_telegram_names}
            self.need_approve_data.update(need_approve_developers)
            self.approved_data.update(mr_data)

    def create_msg(self):
        self.load_mr_data()
        msg = ''

        for merge_request in self.approved_data:
            web_url = str(merge_request)
            all_developers = self.approved_data[merge_request]
            approved_developers = [developers[user['user']['username']] for user in all_developers]
            need_approve_developers = self.need_approve_data[merge_request]
            approved_but_not_merged = len(need_approve_developers) == 0
            developers_to_send_message = [] if approved_but_not_merged else list(
                set(need_approve_developers) - set(approved_developers))
            developers_str = '👨‍💻 Z-z-z....' if approved_but_not_merged else ''.join(
                [('👨‍💻 ' + dev + '\n') for dev in developers_to_send_message])
            msg += f'{developers_str[: -1]}\n➡️ {web_url}\n\n\n'

        self.clear_data()
        found = len(msg) != 0
        return f'{msg} 👮‍ Вы арестованы 🚔' if found else '👮🏻 Уровень преступности в норме, в городе спокойно 💅'
