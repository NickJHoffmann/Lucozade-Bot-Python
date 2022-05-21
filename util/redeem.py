from botdriver import BotDriver
import argparse


def main():
    parser = argparse.ArgumentParser(description="Redeem codes on Halo Waypoint")
    parser.add_argument("file", help="Codes file to input")
    parser.add_argument("-s", "--start", help="Code number to start inputting. Defaults to beginning of the file", type=int, default=0)
    parser.add_argument("-n", "--number", help="Number of codes to input from starting point. Defaults to submit all codes after starting point", type=int)

    args = parser.parse_args()

    bot = BotDriver()
    bot.driver.get(bot.WAYPOINT_URL)
    bot.login_microsoft()

    with open(args.file, 'r') as code_file:
        num = 0
        submitted = 0
        code = code_file.readline().strip()
        while code and (submitted < args.number if args.number is not None else True):
            if num >= args.start:
                succeeded = bot.redeem_waypoint_code(code, True)
                print(f"{code}{'' if succeeded else ' - Failed'}")
                submitted += 1
            num += 1
            code = code_file.readline().strip()


if __name__ == "__main__":
    main()
