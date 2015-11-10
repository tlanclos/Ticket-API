import argparse
import getpass
import re
from ticketapi.datalayer.procedures import add_auth


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Tool to generate authorization rows and add them to the database based on a company name',
            epilog='\n'.join([
                'I would have written a nice ncurses tui instead of this cli, but I figured someone would',
                'eventually write a nice gui of some sort to add these rows in here :)'
            ])
        )

        parser.add_argument(
            '--company', '-c',
            help='CompanyName from the Techneaux Company table'
        )
        parser.add_argument(
            '--username', '-u',
            help='CompanyID for the new company, this should be a unique string'
        )
        parser.add_argument(
            '--password', '-p',
            help='Although strongly discouraged to use on commandline, the password for the new company username'
        )

        args = parser.parse_args()

        if not all([args.company, args.username]):
            exit(1)

        print('Adding company: "{company}"'.format(company=args.company))
        print('   Username   : "{username}"'.format(username=args.username))
        if not args.password:
            password = getpass.getpass(prompt='Password for {username}: '.format(username=args.username))
            confirm_password = getpass.getpass(prompt='Confirm password for {username}: '.format(username=args.username))
            if password != confirm_password:
                print('Passwords do not match')
                exit(2)
        else:
            password = args.password

        cont = input('Continue (y/n)? ')
        if re.match(r'y(es)?', cont, re.IGNORECASE):
            success, reason = add_auth(companyName=args.company, companyID=args.username, password=args.password)
            if not success:
                print('Failed to add authentication for "{company}"'.format(company=args.company))
                print(reason)
        else:
            print('User said no')
    except (SystemExit, KeyboardInterrupt) as e:
        print('Exiting on user command')
