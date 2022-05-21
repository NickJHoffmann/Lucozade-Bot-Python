from botdriver import BotDriver
import argparse


def get_codes_from_file(filename):
    with open(filename, 'r') as file:
        while code := file.readline().strip():
            yield code


def main():
    parser = argparse.ArgumentParser(description="Redeem codes on Halo Waypoint")
    parser.add_argument("file", help="Codes file to input")
    parser.add_argument("-s", "--start", help="Code number to start inputting. Defaults to beginning of the file", type=int, default=0)
    parser.add_argument("-n", "--number", help="Number of codes to input from starting point. Defaults to submit all codes after starting point", type=int)

    args = parser.parse_args()

    bot = BotDriver()
    bot.driver.get(bot.WAYPOINT_URL)
    bot.login_microsoft()

    submitted = 0
    for i, code in enumerate(get_codes_from_file(args.file)):
        if args.number is not None and submitted >= args.number:
            break

        if i >= args.start:
            succeeded = bot.redeem_waypoint_code(code, True)
            print(f"{code}{'' if succeeded else ' - Failed'}")
            submitted += 1


if __name__ == "__main__":
    main()
