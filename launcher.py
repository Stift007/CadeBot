from bot import MusicBot

def main():
    bot = MusicBot(load_dotenv=True)
    bot.run()

if __name__ == "__main__":
    main()