# Sourcing
The following repository provides an automated scraper to help with project sourcing. As a disclaimer, it does not scrape emails. It attempts to scrape the names of people who have worked at a particular company with a particular role and "guess" the email format using the Hunter.io API.

## Installation
Dependencies are currently supported on Python 3 and Python 2.7.X and can be found in `requirements.txt`.
To setup the scraper, open Terminal and run the following commands.
```
git clone https://github.com/eric-gan/Sourcing
cd Sourcing
pip install -r requirements.txt
```

Next, download `chromedriver` from [here](https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/) and move the executable file into the Sourcing directory.

## Usage
Open `scraper.py` in your favorite editor and make the following changes:
1. On line 26, update `TITLES` to the positions you want to scrape for. Defaults are Data Scientist, Data Engineer, Machine Learning Engineer, Product Manager, and Engineering Manager.
2. On line 28, update `PAGE_DEPTH` to the number of LinkedIn pages you want to scrape. Default is 7.
3. On line 30, update `USERNAME_AUTH` to your LinkedIn username.
4. On line 31, update `PASSWORD_AUTH` to your LinkedIn password.
5. On line 33, update `DRIVER_PATH` to the full path of `chromedriver.exe`. On Mac one can find the full path by right clicking on the file, holding option key, and clicking *Copy "chromedriver" as pathname*.

Open `Company List.xlsx` and make the following changes:
1. `Company List.xlsx` should have the word "Company" in A1. For each company you would like to get contacts from, add the Company name **exactly as it appears on LinkedIn** in Column A below Company (one company per row).

Finally, in the Sourcing directory, run `python3 main.py`

Enter your Hunter API Key when prompted. [See Hunter API Key for setup instructions](#hunter-api-key).

Open `sourcing.csv`, and you should see the output, which you can then copy over to Google Sheets. If emails do not appear for a company, the format will need to be manually scraped from Hunter, and merged in using an Excel function.

## Hunter API Key
Because this application uses Hunter.io's API, individual users are required to create an API Key to use (API Requests are throttled). To generate a Hunter.io API Key:
1. Visit [Hunter.io](https://hunter.io) to create an account. 
2. After creating an account, go to your name in the top right corner and select API in the dropdown. Copy and paste your API secret key
3. You are able to access your personal API Key and view your Hunter.io API Usage.
4. Should you run out of monthly requests (50 companies per month), simply make a new account and get a new key.

## Debugging
The file for `chromedriver` is not found:

```
FileNotFoundError: [Errno 2] No such file or directory: 'chromedriver.exe': 'chromedriver.exe'
```

Fix: Make sure chromedriver has been downloaded and it is in your Sourcing directory

The `chromedriver` executable needs to be in PATH
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home
```

Fix: Makes sure you have downloaded `chromedriver` and it is in your Sourcing directory. Open `scraper.py` and on line 33, make sure `DRIVER_PATH` contains the full path to the chromedriver.


Scraper stops halfway with this message
```
File "scraper.py", line 141, in <module>
    all_filters_button.click()
AttributeError: 'NoneType' object has no attribute 'click'
```
Fix: Quit the current running instance and **quit chrome** all together and rerun. If that does not work, on line 128 in `scraper.py`, try increasing the number of seconds in `time.sleep(3)` by a little.


Permission Error
```
PermissionError: [Errno 13] Permission denied: 'sourcing.csv'
```
Fix: Make sure you delete any existing 'sourcing.csv' before running again.

## Authors
* [Eric Gan](https://github.com/eric-gan)
* [Rick Zhang](https://github.com/wsxdrorange)
