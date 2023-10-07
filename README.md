
![photo_2023-09-02 09 17 34](https://github.com/fresh-Blood/MrMother/assets/88098218/6f050098-e126-452e-aa32-ee015e3ca720)

# 🤖 MrMother 👧

MrMother is customizable, extendable gitlab telegram bot to remind if merge request is waiting for someones approval. 
You should edit data.py for your personal team customization.

## 💜 Quick start:
1) install Python :З
2) get gitLab project number 
3) get your bot personal token 
4) get your personal gitlab token 
5) get tg chat id (optional)
6) get your tg id (optional)
7) get developers nick names

Now it's time to make it work. After you refilled data in config.py with yours for:

## 💜 Windows: 
1) press cmd + r
2) type shell:startup
3) then create txt with path to MrMother.py
4) then rename it with name.cmd

Launch if needed now, or wait for next pc start up, bot will be launched automatically in command line.

## 💜 Mac OS, Linux: 
1) open terminal
2) open directory with MrMother.py
3) run MrMother.py 

## 💜 How it works: 
- MrMother was created to avoid stress situations between developers, connected with code review time. Some developers, unfortunately, are sleeping; but business wants speed.
- The default settings in MrMother.py and Data.py assume one assignee, chosen in gitlab, when merge request was created, and two reviewers written in info block like: @gitlab_nickName.
- So if merge request is approved by less than three developers and is not in draft state, bot'll send info about such merge request to chat. 
- Also bot'll notify if unresolved comments exist.
- Just in case you are busy, bot'll also notify you if sent message with Celero neural network nice female voice.

![Снимок экрана 2023-09-09 в 22 53 29](https://github.com/fresh-Blood/MrMother/assets/88098218/c13d3841-871f-4f15-a299-3812a7a579fa)

### Enjoy!
