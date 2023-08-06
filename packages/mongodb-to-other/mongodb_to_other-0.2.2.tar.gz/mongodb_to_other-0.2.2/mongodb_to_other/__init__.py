import pymongo
import xlwt
import json

import pymysql
def mongodb_to_xls(db_name,set_name,xls_path,port=27017,ip="127.0.0.1",name=None,password=None):
    #初始化变量
    key_list=[]
    l,i=-1,0
    #初始化输入参数
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('json',cell_overwrite_ok=True)
    #初始化数据库
    #myclient = pymongo.MongoClient(f'mongodb://{ip}:{port}/')
    if name==None and password==None:
        myclient = pymongo.MongoClient(host= ip, port=port)
    else:
        myclient==pymongo.MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = myclient[db_name] #testdb可按需求改动
    coll = db.get_collection(set_name)
    #开始写入
    for i in coll.find():
        for x in i.items(): 
            db_item={x[0]:x[1]}
            #的出一个数据库项
            for key,value in db_item.items():
                key_list.clear()
                key_list.extend((key, value))
                #位置设置
                i,l=1,l+1
                #写入
                #i 列，l 行
                for y in range(len(key_list)):
                    if isinstance(key_list[y],list):
                        z=y
                        for u in key_list[y]:
                            sheet.write(l,z,str(u))
                            z+=1
                    else:
                        sheet.write(l,y,str(key_list[y]))
    book.save(xls_path)

#示例
#mongodb_to_xls("testdb","userdb","D:\\test12345678.xls")
def mongodb_to_json(db_name,set_name,json_path,port=27017,ip="127.0.0.1",name=None,password=None):
    if name==None and password==None:
        client = pymongo.MongoClient(host= ip, port=port)
    else:
        client==pymongo.MongoClient(f'mongodb://{name}:{password}@{ip}:{port}/?authSource=info_data')
    db = client[db_name]
    coll = db.get_collection(set_name)
    coll=list(coll.find())
    l=len(coll)
    with open(json_path,"w+",encoding="utf-8") as f:
        f.write("[")
    n=0
    for i in coll:
        n+=1   
        with open(json_path,"a+",encoding="utf-8") as f:
            del i["_id"]
            f.write("   ")
            if coll.index(i)==l-1:
                json.dump(i, f,ensure_ascii=False)
            else:
                json.dump(i, f,ensure_ascii=False)
                f.write(",")
            f.write("\n")
            f.close
    with open(json_path,"a+",encoding="utf-8") as f:
        f.write("]")

# def mongodb_to_mysql(m_db_name,m_set_name,s_dbname,s_name,s_password,s_ip="127.0.0.1",m_port=27017,m_ip="127.0.0.1",m_name=None,m_password=None):
#     #mongo——Init
#     if m_name==None and m_password==None:
#         client = pymongo.MongoClient(host= m_ip, port=m_port)
#     else:
#         client==pymongo.MongoClient(f'mongodb://{m_name}:{m_password}@{m_ip}:{m_port}/?authSource=info_data')
#     db = client[m_db_name]
#     coll = db.get_collection(m_set_name)
#     coll=list(coll.find())
#     #sql——Init
#     key_=[]
#     db = pymysql.connect(host=s_ip,
#                      user=s_name,
#                      password=s_password,
#                      database=s_dbname)
#     cursor = db.cursor()
    
#     key_s=''
#     for i in coll:
#         #获取所有key
#         key_s=""
#         key_s_s=''
#         key_=[]
#         key=i.keys()
#         print(key)
#         key_s_=[]
#         for  x  in key:
#             key_s_.append(f"{x} VARCHAR(255)")

#         for z in key:
            
#             key_s+=f",{z}"
#         # key_s=key_s[1:]
      
           

#         for u in key_s_:
            
#                 key_s_s+=f",{u}"
#         # key_s_s=key_s_s[1:]
#         sql=f"CREATE TABLE {str(i['_id'])}  (id VARCHAR(255) PRIMARY KEY {key_s_s})"
#         print(sql)
#         cursor.execute(sql)
#         #获取所有value
#         value_s=''
#         value_=[]
#         value=i.values()
#         # for  x in value:
#         #     value_.append(f"{x} VARCHAR(255)")
#         for m in value:
          
#             value_s+=f",'{str(m)}'"
#         # value_s=value_s[1:]
        
#         #写入数据
#         sql = f""" INSERT INTO {str(i['_id'])}(id {key_s}) VALUES ({str(time.time())} {value_s})"""
#         print(sql)
#         try:
#             # 执行sql语句
#             cursor.execute(sql)
#             # 提交到数据库执行
#             db.commit()
#         except:
#             # 如果发生错误则回滚
#             db.rollback()
#     db.close()


    

def mongodb_to_mysql(m_db_name,m_set_name,s_dbname,s_name,s_password,s_ip="127.0.0.1",m_port=27017,m_ip="127.0.0.1",m_name=None,m_password=None):
    #mongo——Init
    if m_name==None and m_password==None:
        client = pymongo.MongoClient(host= m_ip, port=m_port)
    else:
        client==pymongo.MongoClient(f'mongodb://{m_name}:{m_password}@{m_ip}:{m_port}/?authSource=info_data')
    db = client[m_db_name]
    coll = db.get_collection(m_set_name)
    coll=list(coll.find())
    #sql——Init
    key_=[]
    db = pymysql.connect(host=s_ip,
                     user=s_name,
                     password=s_password,
                     database=s_dbname)
    cursor = db.cursor()

    # key_s=''
    key_=[]
    # key_s=""
    key_s_s=''
    # key_=[]

    key_s_=[]
    for i in coll:
        k= i.keys()
        for i in k:
            key_.append(i)
    res_list=[]
    for i in key_:
        if i not in res_list:
            res_list.append(i)
    
    for u in res_list:
         key_s_.append(f"{u} VARCHAR(255)")
    print(key_s_)
    for u in key_s_:
            
        key_s_s+=f",{u}"
    key_s_s=key_s_s[1:]
    print(key_s_s)
    sql=f"CREATE TABLE {m_set_name}  ({key_s_s})"
    print(sql)
    cursor.execute(sql)
    for i in coll:
        #获取所有key
        key_s=""
        key_s_s=''
        key_=[]
        key=i.keys()
        print(key)
        key_s_=[]
     

        for z in key:
            
            key_s+=f",{z}"
        key_s=key_s[1:]
      
           


        #获取所有value
        value_s=''
        value_=[]
        value=i.values()
      
        for m in value:
          
            value_s+=f",'{str(m)}'"
        value_s=value_s[1:]
        
        #写入数据
        sql = f""" INSERT INTO {m_set_name} ( {key_s}) VALUES ( {value_s})"""
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
    db.close()


# mongodb_to_mysql("testdb","pricedb","testdb","root","Laozhang123456")