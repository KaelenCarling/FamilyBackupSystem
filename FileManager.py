import os
import sqlite3
import datetime
from configparser import ConfigParser
from glob import glob

__SQLName = 'test'

config = ConfigParser()


def fileSniff(directory):
    # recursively walks through the directory given
    for fileDirectory in os.walk(directory):
        # uses glob to find files which match the criteria. if you delete the *.* it will find files without
        # types (mainly directories)
        for file in glob(os.path.join(fileDirectory[0], '*.*')):
            insertFile(file)


def createSQL():
    # connects to the SQL server. if it doesn't exist it creates one
    database = sqlite3.connect('{}.sqlite'.format(__SQLName))

    # creates a cursor to interact with the database
    curse = database.cursor()
    curse.execute('CREATE TABLE FileDirectories (name VARCHAR, type VARCHAR, lastModified DATETIME)')

    # commits changes and then closes
    database.commit()
    database.close()


def insertFile(file):
    # generates the formatted date when this file is read in from the current time
    formattedDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    name = file

    # stores the file extension without the dot
    type = os.path.splitext(file)[1][1:]

    # connects to the server and instantiates a cursor
    database = sqlite3.connect('{}.sqlite'.format(__SQLName))
    curse = database.cursor()

    # generates the query for the insertion and then executes it
    query = 'INSERT INTO FileDirectories (name, type, lastModified) VALUES (?,?,?)'
    curse.execute(query, (name, type, formattedDate))

    # commits the change and closes the database
    database.commit()
    database.close()

def startUpCheck():

    createConfig()
    addConfigLine('main', 'directory0', 'C:\\Users\\kaele\\Documents\\TestBackup')

    '''
    config.read('backup_config.ini')
    config.add_section('main')
    
    #set directory
    config.set('main', 'directory0', 'C:\\Users\\kaele\\Documents\\TestBackup')
    
    with open('backup_config.ini', 'w') as outLine:
        config.write(outLine)
    '''
# todo: implement main method that will manage table creation and be for use in another python program

def createConfig():
    config.read('backup_config.ini')
    config.add_section('main')

    with open('backup_config.ini', 'w') as outLine:
        config.write(outLine)

def addConfigLine(section, key, value):
    config.read('backup_config.ini')
    config.set(section, key, value)

    with open('backup_config.ini', 'w') as outLine:
        config.write(outLine)

def main():
    #createSQL()
    startUpCheck()
    config.read('backup_config.ini')
    config.get('main', 'directory0')
    #fileSniff(config.get('main', 'directory0'))

if __name__ == "__main__":
    main()


