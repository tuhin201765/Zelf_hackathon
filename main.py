from instabot import InstaBot

def story():
    bot = InstaBot(username="Ecosdid",pw="Ecosdid@123")
    bot.login()
    bot.scrape_stories()
    bot.stop()

def like():
    bot = InstaBot(username="Ecosdid",pw="Ecosdid@123")
    bot.login()
    bot.like()
    bot.stop()
    
if __name__=='__main__':
    # story()
    like()