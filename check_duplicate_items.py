# -*- coding:utf-8 -*-
import MySQLdb
from sys import argv
db = MySQLdb.connect(host="sh-cdb-24esxjys.sql.tencentcdb.com", user="root", passwd="210000Nj", db="test", port=63669, charset="utf8")

table_name = 'zoho_market_data'
file_path = 'zoho_market.csv'
headers = []

def printu(s):
    if type(s) is not list:
        print s.decode('utf-8').encode('gbk') 
    else:
        print 'list: ',
        for e in s:
            print e.decode('utf-8').encode('gbk') ,
        print
    
def u2s(s):
    return s.encode('unicode-escape').decode('string_escape')
    
def get_numbers(s):
    cns = s.replace("，",",").replace("、",",").replace("；",",").replace(";",",").replace("\n",",").replace("/",",").replace(" ",",").replace('"', '').replace('\t', '')
    return cns.split(",")
    
def search_contact_number_make_tag(cursor, numbers, pid):
    if len(numbers) < 6:
        return 
    cursor.execute("select `CUSTOMMODULE9 ID` from zoho_market_data where `联系电话` like '%%%s%%'"%(numbers))
    print pid, ":  ",
    for id in cursor.fetchall():
        id = u2s(id[0])
        print id,
        if id != pid:
            cursor.execute("select `联系电话` from zoho_market_data where `CUSTOMMODULE9 ID` = "+id)
            contact = get_numbers(u2s(cursor.fetchall()[0][0]))
            if numbers in contact:
                cursor.execute("update zoho_market_data set `重复数据`="+numbers+" where `CUSTOMMODULE9 ID`='"+id+"'")
            db.commit()
    print 

#重复的、有问题的返回True，没问题的返回FALSE
def search_contact_number(cursor, numbers):
    if len(numbers) < 6:
        return False
    sql = "select `CUSTOMMODULE9 ID` from zoho_market_data where `联系电话` like '%%%s%%'"%(numbers)
#    print sql
    cursor.execute(sql)
#    print "search_contact_number", numbers
    for id in cursor.fetchall():
        id = u2s(id[0])
        cursor.execute("select `联系电话` from zoho_market_data where `CUSTOMMODULE9 ID` = '"+id+"'")
        contact = get_numbers(u2s(cursor.fetchall()[0][0]))
#        print "contact", contact
        for e in contact:
            if numbers in e:
                return True
    return False

if __name__ == "__main__":
    if len(argv) == 2:
        ls = open(argv[1]).readlines()
        for l in ls:
            print "%s\t%s"%(l.strip(), True in [search_contact_number(db.cursor(), e) for e in get_numbers(l)] or 
            True in [search_contact_number(db.cursor(), e[:4] + '-' + e[4:]) for e in get_numbers(l) if e.startswith('0') and '-' not in e and len(e) >= 6])
    else:
        cursor = db.cursor()
        cursor.execute("select `CUSTOMMODULE9 ID` from zoho_market_data")
        ids = cursor.fetchall()
        cnt = 0
        for id in ids:
            sql = "select `联系电话` from zoho_market_data where `CUSTOMMODULE9 ID` = '" + id[0].encode('unicode-escape').decode('string_escape') + "'"
            cnt += 1
            print cnt,
            cursor.execute(sql)
            contact = cursor.fetchall()
            if len(contact) == 1:
                cns = contact[0][0].encode('unicode-escape').decode('string_escape')
                cns = cns.replace("，",",").replace("、",",").replace("；",",").replace(";",",").replace("\n",",").replace("/",",").replace(" ",",").replace("-",",")
                cns = cns.split(",")
                for num in cns:
                    search_contact_number_make_tag(cursor, num, u2s(id[0]))
            else:
                printu("该ID未找到 联系电话")

db.commit()
db.close()

