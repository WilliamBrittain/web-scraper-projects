# Web Scraper Projects
Welcome to my repository for web scraper projects! This is where I store all my various web scraping scripts and projects. Whether it's scraping data from websites, extracting information, or automating tasks, you'll find a variety of web scraper projects here.

Feel free to explore the projects, contribute, or use the scripts for your own purposes. If you have any suggestions, improvements, or new ideas for web scraping projects, don't hesitate to get involved!
______________________________________

## Project: Pokemon Go PVE Fast Moves
This Python script is designed to scrape Pokemon Go PVE (Player versus Environment) fast moves data from gamepress.gg and insert this data into a MySQL database.

### Prerequisites:
Python 3.12.2 installed on your system
MySQL 8.0.33 installed and running
Required Python packages installed. You can install them using the following command:
```shell script
pip3 install -r requirements.txt
```

### Usage:
Clone this repository or download the script file poke_fast_moves.py.
Install dependencies using the provided requirements file.
Run the script:
```shell script
python3 poke_fast_moves.py
```
Enter the required database connection information when prompted (host, user, password).
The script will scrape data from gamepress.gg/pokemongo/pve-fast-moves, clean it, and insert it into the MySQL database.

### Notes:
Ensure that your MySQL server is running and accessible.
Adjust timeout value in the script if needed for the website scraping process.
Make sure you have appropriate permissions to create databases and tables in MySQL.
______________________________________

## Disclaimer
The web scraper projects stored in this repository are provided as-is, and their usage is at your own risk. Before running any scripts, it is strongly recommended to review and understand the code to ensure it aligns with your requirements and expectations.
