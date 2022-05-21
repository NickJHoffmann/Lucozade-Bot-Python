from botdriver import BotDriver
import sys


def main():
    bot = BotDriver()
    bot.driver.get(bot.WAYPOINT_URL)

    bot.login_microsoft()

    with open(sys.argv[1], 'r') as code_file:
        code = code_file.readline().strip()
        while code:
            bot.redeem_waypoint_code(code)
            code = code_file.readline().strip()


if __name__ == "__main__":
    main()
