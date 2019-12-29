# Sourcing
The following repository provides an automated scraper to help with project sourcing. As a disclaimer, it does not scrape emails. It attempts to scrape the names of people who have worked at a particular company with a particular role.

## Usage
Dependencies are currently supported on Python 3 and Python 2.7.X and can be found in `requirements.txt`.
To setup the scraper, open Terminal and run the following commands.
```
git clone https://github.com/eric-gan/Sourcing
cd Sourcing
pip install -r requirements.txt
```

Next, download `chromedriver` from [here](https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/) and move the executable file into the Sourcing directory.

Open `emails.py` in your favorite editor and make the following changes:
1. On line 27, update `TITLES` to the roles you want to scrape for. Default are Data Scientist, Manager, Director.
2. On line 29, update `PAGE_DEPTH` to the number of LinkedIn pages you want to scrape. Default is 7.
3. On line 31, update `USERNAME_AUTH` to your LinkedIn username.
4. On line 32, update `PASSWORD_AUTH` to your LinkedIn password.
5. On line 34, update `DRIVER_PATH` to the full path of `chromedriver.exe`. On Mac one can find the full path by right clicking on the file, holding option key, and clicking *Copy "chromedriver" as pathname*.

Before running the scraper, make sure the following`.xlsx` files are in your current working directory:
* `Company List.xlsx`
* `sourcing.xlsx`

`Company List.xlsx` should have the word "Company" in A1. For each company you would like to get contacts from, add the Company name exactly as it appears on LinkedIn in column A below Company (one company per row).

`sourcing.xlsx` should be a blank file and will contain the outputs of the scraping.

Finally, in the Sourcing directory, run `python3 emails.py`

Open `sourcing.xlsx`, and you should see the output, which you can then copy over to Google Sheets.

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

Fix: Makes sure you have downloaded `chromedriver` and it is in your Sourcing directory. Open `emails.py` and on line 34, make sure `DRIVER_PATH` contains the full path to the chromedriver.


Scraper stops halfway with this message
```
File "emails.py", line 141, in <module>
    all_filters_button.click()
AttributeError: 'NoneType' object has no attribute 'click'
```
Fix: Quit the current running instance and close the Chrome window. On line 147 in `emails.py`, try increasing the number of seconds in `time.sleep(3)` by a little.
