# CourseDownloader

## Compatibility

Mac OS with Intel or M1 Processor or Windows 10 & 7

[Brave Browser](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiln5DzwrHzAhUL-qQKHZwdDIIQFnoECAcQAQ&url=https%3A%2F%2Fbrave.com%2F&usg=AOvVaw2CfcgN6wLi3270uJRtAJ62) or
[Chrome Browser](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiUzKuAw7HzAhXS66QKHW_GB7cQFnoECA4QAQ&url=https%3A%2F%2Fwww.google.com%2Fintl%2Fit_it%2Fchrome%2F&usg=AOvVaw2mSArY3brRVd2oEF94R97T)

## Installation

First of all you need to install Python on your computer from [here](https://www.python.org/downloads/), then move the "main.py" file to a folder called how you want. At this point you must install the requirement package by using the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
python3 -m pip install selenium
```
If you have troubles with this part, you can follow this [tutorial](https://packaging.python.org/tutorials/installing-packages/).
\
\
\
Afterwards you can start your program by digiting this command:

```bash
cd folderChosenByYou # <-- The name is chosen by you!
py main.py
```
Now you will see on the terminal view the same text:

```bash
You have installed this program successfully, now follow this steps:
```
Then you will need to insert the **email** and **password** of your FutureLearn's account and next insert the **url** of  your course (you need to be already registered to it by selecting the free plan).
\
\
\
⚠️ The format of the course's link is as like this: \
[https://www.futurelearn.com/courses/norwegian/15/todo/119848](https://www.futurelearn.com/courses/norwegian/15/todo/119848)

\
⚠️ If the program can't find your Browser's path, you can eventualy modify manually at the **79 line**.


## Contributing
Pull requests are welcome. 
\
For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Copyright

[CourseDownloader](https://github.com/MyTeraIT/CourseDownloader) © 2021 by [TeraIT](https://github.com/MyTeraIT) is licensed under [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)
