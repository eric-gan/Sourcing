from sourcer import Sourcer

import scraper

import os


def main():
    print('Starting Email Sourcer:\n')
    hunter_api_key = input('Enter hunter.io api key (Press Enter for no Hunter.io email lookups): ')
    existing_info_ind = input('1. Creating New Info Sheet (Scraping LinkedIn)\n2. Modifying Email Pattern on Existing Sheet\nChoose Option (1/2): ')
    if existing_info_ind == '1':
        # run scraper
        print('running scraper')
        scraper.run()

        print('fetching emails')
        sourcer = Sourcer(hunter_api_key)
        sourcer.read_client_info_csv(os.getcwd() + '/sourcing.csv')
        sourcer.write_client_info_csv(os.getcwd() + '/sourcing.csv')
    elif existing_info_ind == '2':
        print('fetching emails')
        sourcer = Sourcer(hunter_api_key)
        num_companies = int(input('Enter number of email patterns (# companies) you wish to modify: '))
        custom_patterns = {}
        for i in range(num_companies):
            company = input('\nEnter the Company Name exactly how it is written on your Spreadsheet: ')
            pattern = input('Search the exact domain name of the company you wish to modify on hunter.io (e.g sony.com)\nEnter new email pattern for domain exactly listed on hunter.io: ')
            custom_patterns[company] = pattern
        sourcer.read_client_info_csv(os.getcwd() + '/sourcing.csv', custom_pattern=custom_patterns)
        sourcer.write_client_info_csv(os.getcwd() + '/sourcing.csv')

    print('DONE')
    print("Your file is located at: " + os.getcwd() + '/sourcing.csv')
    return 0


if __name__ == "__main__":
    main()
