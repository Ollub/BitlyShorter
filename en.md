# Bitly url shorterer

**BitlyShorter helps to create bitlinks and to get bitlinks info from the terminal.**

### How to install

At first you need to get api_key at bit.ly. [how to get token](https://support.bitly.com/hc/en-us/articles/230647907-How-do-I-find-my-OAuth-access-token-)
You need to create .env file at application directory and provide your api_key: API_KEY=[your_api_key]

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
### How to use BitlyShorter

To create short link provide ling as argument when starting your program in terminal:
```
$ python bitly.py -l http://google.com
```

To get bitlinks click info provide bitlink as argument:
```
$ python bitly.py -l bit.ly/2HDkUn0
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).