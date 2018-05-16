# -*- coding:utf-8 -*-
import MySQLdb
from sys import argv
db = MySQLdb.connect(host="sh-cdb-24esxjys.sql.tencentcdb.com", user="root", passwd="210000Nj", db="test", port=63669, charset="utf8")

table_name = 'zoho_task_data'
file_path = '1524982035276.csv'
headers = []

def printu(s):
    if type(s) is not list:
        print s.decode('utf-8').encode('gbk') 
    else:
        print 'list: ',
        for e in s:
            print e.decode('utf-8').encode('gbk') ,
        print

def is_duplicate(cols, headers, cursor):
    sql = "select * from %s where %s = '%s' " %(table_name, headers[0], cols[0])
    printu("查重")
    print sql.decode('utf-8').encode('gbk') 
    cursor.execute(sql)
    results = cursor.fetchall()
    return len(results) > 0
    
def update(cols, headers, cursor):
    printu("更新")
#UPDATE `test`.`zoho_market_data` SET `价值`='高', `区`='888' WHERE `CUSTOMMODULE9 ID`='zcrm_105530000001792874';
    if len(cols) != len(headers):
        print 'cols:', len(cols), 'headers:', len(headers)
        printu("列数不对")
        printu(cols)
        exit(0)
    ss = []
    for i in range(len(headers)):
        ss.append(headers[i] + '=' + "'" + cols[i] + "'")
    
    sql = "update %s set %s where %s = '%s'" % (table_name, ", ".join(ss), headers[0], cols[0])
    print sql.decode('utf-8').encode('gbk')
    cursor.execute(sql)

def time_cvt(s):
    if "上午" in s:
        s = s.replace("上午", "")
        s = s.strip()
        s = s+":00"
        return s
    elif "下午" in s:
        s = s.replace("下午", "")
        s = s.strip()
        hm = s.split(" ")[1].split(":")
        h = int(hm[0]) + 12
        ts = s.split(" ")[0]+ " " + str(h) + ":" + hm[1]+":00"
        return ts
    return s
        
def get_cols(l):
    idx = 0
    k = False
    cs = l.split(",")
    tc = ""
    cols = []
    for c in cs:
        if not k:
            tc = c
        else:
            tc = tc +","+ c
        if '"' in c:
            k = not k
        if not k:
            cols.append(time_cvt(tc.replace('"', '').replace("'", '')))
    if k:
        return []
    else:
        return cols

#print(time_cvt('2018-04-10 11:14 上午'))
#exit(0)
def load_data():
    argv.append(file_path)
    if len(argv) == 1:
        print "too few arguments"
    else:
        ls = open(argv[1]).readlines()[1:]
        cursor = db.cursor()
        cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        
        headers =['`' + e + '`' for e in ls[0].strip().split(",")]
        insert_head = "insert into " + table_name + "(" + ','.join(headers) + ")"
        #print sql_head.decode('utf-8').encode('gbk')
        
        cnt = 0
        for l in ls[1:]:
            #print l.decode('utf-8').encode('gbk')
            cols = get_cols(l)
            if len(cols) != len(headers):
                print "数据格式错误", cols
                continue
            cnt = cnt + 1
            if not is_duplicate(cols, headers, cursor):  
                printu("插入")
                sql = insert_head + "values(" + ','.join(["''" if len(e) == 0 else '"' + e + '"' for e in cols]) + ")"
                try:
                    printu(sql)
                except Exception, e:
                    print e
                cursor.execute(sql)
            else:
                update(cols, headers, cursor)
            if cnt % 100 == 0:
                db.commit()

if __name__ == "__main__":
    load_data()
    #fill_related()
printu("OKOKOKOK")
db.commit()
db.close()

