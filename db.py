import mysql.connector

class Database:
    def __init__(self):
        try:
            self.con =  mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password",
                database="TodoCLI",
                auth_plugin='mysql_native_password')  
            self.mycur  = self.con.cursor()
            self.mycur.execute("Create table if not exists todoitems (id int NOT NULL AUTO_INCREMENT primary key,title VARCHAR(500),created_at varchar(50),completed_at varchar(50) default NULL,status varchar(50) DEFAULT 'INCOMPLETE')")    
        except:
            print(f"THERE IS SOME PROBLEM WITH DATABASE SET UP PLEASE CHECK IF ALL THE FIELDS ARE CORRECT")


    def insert(self,title,current_time):
        query = f"insert into todoitems (title,created_at) values ('{title}' , '{current_time}');"
        self.mycur.execute(query)
        self.con.commit()
        print("inserted")
   
    def getlist(self,date):
        if date:
            self.mycur.execute("select * from todoitems")
            mylist=self.mycur.fetchall()
            return mylist
        else:
            self.mycur.execute("select id,title,status from todoitems")
            mylist=self.mycur.fetchall()
            return mylist    

    def updateListTitle(self,task_id,new_title):
        self.mycur.execute(f"update todoitems set title='{new_title}' where id = {task_id}")
        self.con.commit()
        print("Title updated")

    def updateListStatus(self,task_id,status,current_time):
        if(status=="COMPLETE"):
            self.mycur.execute(f"update todoitems set status='{status}', completed_at='{current_time}' where id = {task_id}")
        else:
            self.mycur.execute(f"update todoitems set status='{status}', completed_at=NULL where id = {task_id}")
        self.con.commit()
        print("Status updated")
            
    def deleteItem(self,task_id):
        self.mycur.execute(f"select * from todoitems")
        total = self.mycur.fetchall()
        for i in total:
            if(i[0] == task_id):
                self.mycur.execute(f"delete from todoitems where id = {task_id}")
                self.con.commit()
                print(f"Deleted item with task_id {task_id}")
                break
        else:
            print(f"No item with task id = {task_id} is present please enter a valid task id \nTo check taskids of todos use command <python3 todo.py --list>")    

    def searchText(self,text):
        self.mycur.execute(f"select * from todoitems where title LIKE '%{text}%'")
        search_result = self.mycur.fetchall()
        return search_result

    def completedItems(self):
        self.mycur.execute(f"select * from todoitems where status = 'COMPLETE' ")
        result  = self.mycur.fetchall()
        return result

    def incompleteItems(self):
        self.mycur.execute(f"select * from todoitems where status = '{'INCOMPLETE'}'") 
        result = self.mycur.fetchall()
        return result  

    def alignedItems(self):
        pass
