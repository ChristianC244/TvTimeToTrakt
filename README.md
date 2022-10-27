<!-- Run this in browser console in /history page to remove a page of watched episodes
```js
$(".posters .grid-item").each(function(){
  var $this = $(this);
  historyRemove($this, $this.data("history-id"));
})
``` -->
# Work In Progress

# DESCRIPTION

This Python Script will copy the history from TV Time app to Trakt as the latter is more integrated in different applications.
The process is completely automatic, it will add the movies/episodes using [TVDB](https://thetvdb.com/) ids.

*(Developed with Python 3.9, will probably work with lower versions)*
## What it can do:

+ Transfer TV Shows episodes
+ Transfer Movies (**WIP**)
+ Trasfer Ratings (**WIP**)
+ Add as watchlist the followd Movies/TV Shows (**WIP**)
+ Resume the process if the program gets interrupted

---

# SETUP

## Request your data

You can contact [TV Time support](mailto:support@tvtime.com) and ask for your data, if you live under EU territory they must comply in accordance to GDPR.

## Prepare to Run

+ Download this repository keeping the folder structure
+ The script requires no additional custom python libraries 
+ Move the `csv` files into the `data/` folder
```
TvTimeToTrakt/
├── data/
.   ├── seen_episodes.csv
.   ├── tracking-prod-records.csv
.   ├── ...
    .
    .
    .

```

## Authorize the application

+ Login into your [Trakt](https://trakt.tv) account
+ Go to `Settings` > `Your API Apps` and click `NEW APPLICATION`
1. Give it a `Name` like: "TvTimeToTrakt".
2. Add in `Redirect Url` "urn:ietf:wg:oauth:2.0:oob".
3. Save.
+ By clicking in the application you can see its `client id` and `secret`, you have to copy those fields into the `config.json`

---

# EXECUTE

If you already have put the csv files into `data/` folder, then you can run the program.
```sh
python3 main.py
```
You will have to authorize the app. Once started just follow the instruction prompted on screen (One time only).