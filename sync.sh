rm -rfv ./cadebot
git clone https://github.com/Stift007/cadebot.git
echo "client.run('OTEyNzQ1Mjc1NzcxMjE1OTUy.YZ0aRw.0MEWLF_9UZsTGacbxH91Zx1vu-g',reconnect=True)" >> cadebot/main.py
python3 cadebot/main.py