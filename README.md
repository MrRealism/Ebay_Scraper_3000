# Ebay Scraper 3000
This program scrapes ebay finding the most recent deals and sends them to your own personal discord server! I only have it working for in linux (tested in mint and piOS) and using firefox.
the dependencies are as followed:
- Python3
- firefox
- python3-selenium
- python3-requests
- geckoDriver

## Installation
```
#install python and update
sudo apt update && sudo apt install python3 -y

#install firefox
sudo apt install firefox -y

#install python dependencies
sudo apt install python3-requests python3-selenium -y

#install geckodriver
GECKO_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name"' | cut -d '"' -f 4)
wget "https://github.com/mozilla/geckodriver/releases/download/$GECKO_VERSION/geckodriver-$GECKO_VERSION-linux64.tar.gz"
tar -xvzf geckodriver-*-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver-*-linux64.tar.gz

#check installations
firefox --version
geckodriver --version
python3 --version
```
## setup
1. I recomend using cron and running both the best offer search and buy now, because they tend to catch new items that the other may not have, but you can choose to run one or another
2. set up personal discord server (does not matter what kind), go to server settings, integrations, and then add webhook, copy that url and use it in the code
3. Edit the files and replace: webhook_url, search_query, and max_price to your prefrences
4. set up cron with the following code(you can add more searches or adjust the time as you see fit)(also you can set the log location to any location, it will create the file itself)(one last thing, i have it set to run on the top of the hour and 5 mins past the top of the hour):
```
0 * * * * /usr/bin/python3 /path/to/ebay/scanners/ebay-scanner.py >> /path/to/log/ebay.log 2>&1
5 * * * * /usr/bin/python3 /path/to/ebay/scanners/ebay-scanner_buy-now.py >> /path/to/log/ebay_buy-now.log2>&1
```
5. you can add in the message feild a "@everyone" if you want to get pinged every time


## Known bugs
- will not run on non-gui linux instances
- randomly show related byt not exact searches, ex. shows sega genesis when searching for snes
- no support for auctions
