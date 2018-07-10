import pymysql
from pymysql import connect,cursors
from pymysql.err import  OperationalError
import sys,time

class DataBase():
    def __init__(self,mysql_name):    
        try:
            self.conn = connect(host='localhost',
                             port=3306,
                                user='root',
                                password='123456',
                                db='GitSpace',
                                charset='utf8',
                                cursorclass = cursors.DictCursor)
        except OperationalError as e:
            print(e)

    def insert_inspection_list(self,table_name):
        for i in range(1,20):
            myid = i
            createdate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            contenturl = 'none'
            articletitle = 'title none'
            label = 19
            senderid = 1

            sql = 'insert into index_article (articleID,createDate,contentURL,articleTitle,label,sender_id) \
            #        values (%d,'%s','%s','%s',%d,%d);' % (myid, createdate, contenturl, articletitle, label, senderid)
                    values(myid + ",'" + createdate + "','" + contenturl + "','" + articletitle + "'," + label + "," + senderid + "';")
            print(sql)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    tb = DataBase('')
    tb.insert_inspection_list('inspection_list')
