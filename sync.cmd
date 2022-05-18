@echo off
rmdir cadebot /s/q
git clone https://github.com/Stift007/cadebot.git
echo client.run('OTEyNzQ1Mjc1NzcxMjE1OTUy.YZ0aRw.0MEWLF_9UZsTGacbxH91Zx1vu-g',reconnect=True) >> cadebot\bot.py
py cadebot\bot.py