# Internal reporting tool for logs analysis of newspaper website

This program connects to the database named news, uses single SQL query (PostgreSQL) to analyze the log data, and prints out the answer to each the following questions:

1. What are the most popular three articles of all time? Or, which articles have been accessed the most? This information is presented as a sorted list with the most popular article at the top together with the number of views.

2. Who are the most popular article authors of all time? Or, which authors get the most page views? This information is presented as a sorted list with the most popular author at the top together with the number of views.

3. On which days did more than 1% of requests lead to errors? Errors here refer to requests whose HTTP status codes start with 4 or 5. This information is presented as a sorted list with the most day at the top together with the error percentage.

# How to run?

Save the Python script **logs_analysis.py** attached in the submission in a folder where you have the database named news. From your shell (and folder having the Python script and SQL database), run:

    python logs_analysis.py

The answers in formatted plain text will be printed on your shell and also saved as answers.text in the folder.

The Python script **logs_analysis.py** is released under the MIT License.
