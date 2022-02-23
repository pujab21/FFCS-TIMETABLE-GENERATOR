class database():
    def __init__(self):
        import mysql.connector as sql
        import json
        try:
            self.mydb = sql.connect(host = 'localhost',user = 'root',passwd = 'mysql',database = 'COMDB')
            self.cur = self.mydb.cursor(buffered = True)
        except:
            self.mydb = sql.connect(host = 'localhost',user = 'root',passwd = 'mysql')
            self.cur = self.mydb.cursor()
            self.cur.execute('CREATE DATABASE IF NOT EXISTS COMDB')
            self.cur.execute('USE COMDB')
            self.setup()     
            
    def setup(self):        
        self.cur.execute('CREATE TABLE IF NOT EXISTS users(userId INTEGER AUTO_INCREMENT PRIMARY KEY,username TEXT,password TEXT,email TEXT,firstName TEXT,lastName TEXT,address TEXT,city TEXT,state TEXT,country TEXT, phone BIGINT )')
        self.cur.execute('CREATE TABLE COURSELIST(USERID INT, PRIMARY KEY(USERID),COURSES JSON,CREDITS FLOAT(4,1),FOREIGN KEY(USERID) REFERENCES USERS(USERID));')

    def newuser(self,username,pwd,email,fname,lname,address,city,state,phone,country):
        q = "INSERT into USERS(username,password,email,firstname,lastname,address,city,state,country,phone) values('{}','{}','{}','{}','{}','{}','{}','{}','{}',{})".format(username,pwd,email,fname,lname,address,city,state,country,phone)
        self.cur.execute(q)
        self.cur.execute('select userid from users where username = "{}" '.format(username))
        userid = self.cur.fetchone()
        userid = userid[0]
        self.cur.execute("INSERT INTO courselist values({},'{}',0)".format(userid,list()))
        self.mydb.commit()

    def updatecourselist(self,userid,creds,courselist = []):
        curs.execute("UPDATE COURSELIST SET courses = '{}',credits = {} where userid = {}".format(json.dumps(courselist),creds,userid))
        db.mydb.commit()
        return True
        
            
    def drop(self):
        self.cur.execute('DROP TABLE COURSELIST')
        self.cur.execute('DROP TABLE USERS')
        
        
    def delete(self):
        for i in ['WISHLIST','ORDERS','CART_DETAILS','CART','PRODUCTS','USERS']:
             self.cur.execute('delete from {}'.format(i))
        self.mydb.commit()           
        
'''db = database()
db.drop()
db.setup()
db.newuser('priya101','iampriya','123@gmail.com','Priya','Ferguson','hehehe','London','London',9273941488,'ENGLAND')
db.newuser('tes','1','tes2@gmail.com','Tess','Hanks','13 sunflower apartements','Chennai','TN',9102837465,'INDIA')
db.newuser('a','a','aaaa2@gmail.com','Tessa','Hanks','13 sunflower apartements','Chennai','TN',9102837465,'INDIA')
'''


