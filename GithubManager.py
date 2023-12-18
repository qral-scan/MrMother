import random
import requests
import json
from Config import *


class GithubManager:
    def get_reviewers(self, pr):
        users_str = str(pr['body'])
        users_with_task = users_str.split()
        users_filtered = filter(lambda word: '@' in word, users_with_task)
        return list(users_filtered)

    def get_not_drafts(self):
        response = requests.get(PRS_URL, headers=HEADERS).text
        prs = json.loads(response)

        not_drafts = []

        for pr in prs:
            labels = pr['labels']
            assignee = f'@{pr["assignee"]["login"]}' if pr["assignee"] else "no_assignee"
            reviewers = self.get_reviewers(pr) if self.get_reviewers(pr) else ["no_reviewers"]

            is_draft = False

            for label in labels:
                if label['name'] == 'DRAFT':
                    is_draft = True

            if not is_draft:
                pr_data = {
                    'url': pr['url'],
                    'html_url': pr['html_url'],
                    'assignee': assignee,
                    'reviewers': reviewers
                }
                not_drafts.append(pr_data)

        return not_drafts

    def create_msg(self):
        prs = self.get_not_drafts()

        if len(prs) == 0:
            return '👮🏻 Уровень преступности в норме, в городе спокойно 💅'

        msg = ''

        for pr in prs:
            url = pr['url']
            html_url = pr['html_url']
            assignee = pr['assignee']

            response = requests.get(f'{url}/reviews', headers=HEADERS).text
            pr_data = json.loads(response)

            not_approved_devs = self.get_not_approved_devs(pr, pr_data)

            for dev in not_approved_devs:
                msg += f'{self.get_avatar(dev)} {DEVELOPERS[dev]}\n'

            msg += f'→ {html_url}\n'

            comments = self.get_comments(pr_data)
            msg += f'{comments}\n' if comments else ''

            conflicts = self.get_conflicts(url)
            msg += f'{conflicts}\n' if conflicts else ''

            ready_msg = f'🐢 Assignee: {assignee}, можно вливать 🚀'
            msg += f'{ready_msg}\n' if not conflicts and not comments and not not_approved_devs else ''

            msg += '\n\n\n'

        msg += '👮🏻 Вы арестованы 🚔'
        return msg

    def get_not_approved_devs(self, pr, pr_data):
        need_approve_devs = pr['reviewers'] + [pr['assignee']]
        approved = filter(lambda dev: dev['state'] == 'APPROVED', pr_data)
        approved_devs = [f'@{dev["user"]["login"]}' for dev in approved]
        return list(set(need_approve_devs) - set(approved_devs))

    def get_avatar(self, dev):
        avatars = [
            '🚴🏼‍♂️', '🧗🏼‍♂️', '🧘🏽‍♂️', '🏄‍♂️', '🤸🏼‍♂️',
            '🏋🏾', '🏂', '💆‍♂️', '🧟‍♂️', '🧛🏼‍♂️', '🧌', '🧙🏿‍♂️',
            '🥷🏿', '👨🏻‍💻', '👨‍💻', '🕵🏻‍♂️', '👮🏽‍♂️'
        ]
        return random.choice(avatars) if dev not in ['no_reviewers', 'no_assignee'] else '💥'

    def get_conflicts(self, url):
        # response = requests.get(url, headers=HEADERS).text
        # data = json.loads(response)
        # mergeable = data['mergeable']
        # print(mergeable)
        # if mergeable is not None:
        #     return '🎪 Ветки конфликтуют' if mergeable else ''
        # else:
        #     return ''
        pass

    def get_comments(self, pr_data):
        # comments = filter(lambda dev: dev['state'] == 'COMMENTED', pr_data)
        # devs = set([f'@{dev["user"]["login"]}' for dev in comments])
        # tg_names = ', '.join([DEVELOPERS[dev] for dev in devs])
        # return f"❓🙋‍♂️ Есть вопросы: {tg_names}" if devs else ''
        pass
