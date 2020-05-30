import os
from sqlite3 import OperationalError
import sqlite3
import datetime
from configparser import ConfigParser, DuplicateSectionError
from glob import glob

__SQLName = 'test'

config = ConfigParser()


def fileSniff(directory):
    # recursively walks through the directory given
    for fileDirectory in os.walk(directory):
        # uses glob to find files which match the criteria. if you delete the *.* it will find files without
        # types (mainly directories)
        for file in glob(os.path.join(fileDirectory[0], '*.*')):
            if isNotInDatabase(file):
                insertFile(file)


def createSQL():
    # connects to the SQL server. if it doesn't exist it creates one
    database = sqlite3.connect('{}.sqlite'.format(__SQLName))

    # creates a cursor to interact with the database
    curse = database.cursor()
    curse.execute(
        'CREATE TABLE FileDirectories (name VARCHAR, type VARCHAR, lastModified DATETIME, lastChecked DATETIME)')

    # commits changes and then closes
    database.commit()
    database.close()


def isNotInDatabase(file):
    # connects to the database and sets up the cursor
    database = sqlite3.connect('{}.sqlite'.format(__SQLName))
    curse = database.cursor()

    # generates the query for the insertion and then executes it
    query = 'SELECT * FROM FileDirectories WHERE name=?'
    curse.execute(query, (file,))

    # fetches the row that matches the description
    row = curse.fetchone()
    database.commit()
    database.close()

    # if the select query didn't return anything return true
    if row is None:
        return True
    else:
        return False


def insertFile(file):
    # generates the formatted date when this file is read in from the current time
    lastCheckedFMT = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # gets last modified date and converts it to DATETIME
    lastModifiedFMT = datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')

    # stores the file extension without the dot
    type = os.path.splitext(file)[1][1:]

    # connects to the server and instantiates a cursor
    database = sqlite3.connect('{}.sqlite'.format(__SQLName))
    curse = database.cursor()

    # generates the query for the insertion and then executes it
    query = 'INSERT INTO FileDirectories (name, type, lastModified, LastChecked) VALUES (?,?,?,?)'
    curse.execute(query, (file, type, lastModifiedFMT, lastCheckedFMT))

    # commits the change and closes the database
    database.commit()
    database.close()


def createConfig():
    config.read('backup_config.ini')
    config.add_section('main')

    config.write(open('backup_config.ini', 'w'))


def addConfigLine(section, key, value):
    # sets config to read from and sets the parameters
    config.read('backup_config.ini')
    config.set(section, key, value)

    # writes changes out to config
    with open('backup_config.ini', 'w') as outLine:
        config.write(outLine)


def startUpCheck():
    # creates a config in none exists
    try:
        createConfig()
    except DuplicateSectionError:
        pass
    try:
        createSQL()
        addConfigLine('main', 'sqlite3_server', __SQLName + '.sqlite')
    except OperationalError:
        addConfigLine('main', 'sqlite3_server', __SQLName + '.sqlite')

    # add directory
    addConfigLine('main', 'directory0', 'C:\\Users\\kaele\\Documents\\TestBackup')


def main():
    # creates sqlite server if none exists and the config file for setting informations
    startUpCheck()
    fileSniff(config.get('main', 'directory0'))


if __name__ == "__main__":
    main()
