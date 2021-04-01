from run import cursor, conn
import json
import urllib.parse
import pyodbc
import datetime
from http import HTTPStatus


#song entry
def insertSong(input_data):
    name = input_data['name']
    duration = input_data['duration']
    uploadtime = input_data['uploadtime']

    CurrentDate = datetime.datetime.now()
    uploadtime = datetime.datetime.strptime(uploadtime, "%d-%m-%Y %H:%M")

    if uploadtime < CurrentDate:
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        try:
            SQLCommand = ("INSERT INTO song(name, duration, uploadtime) VALUES (?,?,?)")  
            Values = [name, duration, uploadtime]
                
            cursor.execute(SQLCommand,Values)
            conn.commit()
            return ("{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.description))
        except pyodbc.Error as ex:
            return ("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description))

#podcast entry
def insertPodcast(input_data):
    name = input_data['name']
    duration = input_data['duration']
    uploadtime = input_data['uploadtime']
    host = input_data['host']

    CurrentDate = datetime.datetime.now()
    uploadtime = datetime.datetime.strptime(uploadtime, "%d-%m-%Y %H:%M")

    if uploadtime < CurrentDate:
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        part_list=[]
        if len (input_data['participants'])<10:
            for user in input_data['participants']:
                if len(user)<100:
                    part_list.append(user)

            try:
                SQLCommand = ("INSERT INTO podcast(name, duration, uploadtime, host, Participants) VALUES (?,?,?,?,?)")  
                Values = [name, duration, uploadtime, host, str(part_list)]
                    
                cursor.execute(SQLCommand,Values)
                conn.commit()
                conn.close()
                return (HTTPStatus.OK.value)
            except pyodbc.Error as ex:
                return (str(ex)) 

        else:
            return ("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))

#audiobook entry
def insertAudioBook(input_data):
    name = input_data['title']
    duration = input_data['duration']
    author = input_data['authortitle']
    narrator = input_data['narrator']
    uploadtime = input_data['uploadtime']

    CurrentDate = datetime.datetime.now()
    uploadtime = datetime.datetime.strptime(uploadtime, "%d-%m-%Y %H:%M")


    if uploadtime < CurrentDate:
        return ("date cannot be parsed")
    else:
        try:
            SQLCommand = ("INSERT INTO audiobook(title, duration, authortitle, narrator, uploadtime) VALUES (?,?,?,?,?)")  
            Values = [name, duration, author, narrator, uploadtime]
                
            cursor.execute(SQLCommand,Values)
            conn.commit()
            conn.close()
            return (HTTPStatus.OK.value)
        except pyodbc.Error as ex:
            return ("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description))


#update podcast
def updatePodcast(input_data, id):
    name = input_data['name']
    duration = input_data['duration']
    uploadtime = input_data['uploadtime']
    host = input_data['host']

    CurrentDate = datetime.datetime.now()
    uploadtime = datetime.datetime.strptime(uploadtime, "%d-%m-%Y %H:%M")

    if uploadtime < CurrentDate:
        return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        part_list=[]
        if len (input_data['participants'])<10:
            for user in input_data['participants']:
                if len(user)>100:
                     return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
                else:
                    part_list.append(user)
            try:
                SQLCommand = ("UPDATE podcast SET name=?, duration=?, uploadtime=?, host=?, Participants=? where id =?")  
                Values = [name, duration, uploadtime, host, str(part_list), id]
                    
                cursor.execute(SQLCommand,Values)
                conn.commit()
                conn.close()
                return (("{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.description)))
            except pyodbc.Error as ex:
                return (("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description)))
        else:
             return json.dumps("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))


#update song
def updateSong(input_data,id):
    name = input_data['name']
    duration = input_data['duration']
    uploadtime = input_data['uploadtime']

    CurrentDate = datetime.datetime.now()
    uploadtime = datetime.datetime.strptime(uploadtime, "%d-%m-%Y %H:%M")

    if uploadtime < CurrentDate:
        return ("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        try:
            SQLCommand = ("UPDATE song SET name=?, duration=?, uploadtime=? where id =?")
            Values = [name, duration, uploadtime, id]        
            cursor.execute(SQLCommand,Values)
            conn.commit()
            conn.close()
            return ("{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.description))
        except pyodbc.Error as ex:
            return (("{} {}".\
                format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description)))


#audiobook update
def updateAudioBook(input_data,id):
    name = input_data['title']
    duration = input_data['duration']
    author = input_data['authortitle']
    narrator = input_data['narrator']
    uploadtime = input_data['uploadtime']

    CurrentDate = datetime.datetime.now()
    uploadtime = datetime.datetime.strptime(uploadtime, "%d-%m-%Y %H:%M")


    if uploadtime < CurrentDate:
        return ("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
    else:
        try:
            SQLCommand = ("UPDATE audiobook SET title=?, duration=?, authortitle=?, narrator=?, uploadtime=? where id =?")  
            Values = [name, duration, author, narrator, uploadtime, id]
                
            cursor.execute(SQLCommand,Values)
            conn.commit()
            conn.close()
            return (("{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.description)))
        except pyodbc.Error as ex:
            return (("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description)))

# fetch data
# get data by type
def  get_databytype(input_type):
    table_name = ''
    json_data=[]

    try:
        if input_type == 'audiobook':
            table_name = 'audiobook'
        elif input_type == 'song':
            table_name = 'song'
        elif input_type == 'podcast':
            table_name = 'podcast'
        else:
            return 0
            
        cursor.execute("SELECT * FROM {0}".format(table_name))
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchall()
        
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        return (json_data)
    except pyodbc.Error as ex:
        return (("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description)))

#get data by type and id
def get_databyid(input_type, id):
    json_data=[]
    try:
        if input_type == 'audiobook':
            table_name = 'audiobook'
        elif input_type == 'song':
            table_name = 'song'
        elif input_type == 'podcast':
            table_name = 'podcast'
        else:
            return 0

        cursor.execute("SELECT * FROM {0} WHERE id = {1}".format(table_name, id))
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchall()
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        return (json_data)
        # json_data=[dict(zip(row_headers,rv))]
        # return (json_data)
    except pyodbc.Error as ex:
        return (("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description)))

#delete file
def del_file(input_type, id):
    try:
        cursor=conn.cursor()
        cursor.execute("DELETE from {0} WHERE id = {1}".format(input_type, id))
        conn.commit()
        conn.close()
        if (cursor.rowcount==0):
            return("{} {}".format(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.description))
        else:
            return(("{} {}".format(HTTPStatus.OK.value, HTTPStatus.OK.description)))
    except pyodbc.Error as ex:
        return (("{} {}".format(HTTPStatus.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR.description)))