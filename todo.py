from db import Database
from argparse import ArgumentParser 
from datetime import date,datetime

# showTodoList method can be changed to noshowTODOList

class TodoList():
    def __init__(self):
        self.db=Database()


    def showTodolist(self,dte):
        if dte:
            mylist=self.db.getlist(dte)
            for i in mylist:
                print(i)
        else:
            mylist=self.db.getlist(dte)
            for i in mylist:
                print(i)       

    def completedTodos(self):
        result=self.db.completedItems()
        if(len(result)>0):
            for row in result:
                print(row)
        else:
            print("You have not completed any task")        

    def incompleteTodos(self):
        result=self.db.incompleteItems()
        if(len(result)>0):
            for row in result:
                print(row)
        else:
            print("Congratulations!! you have completed all your tasks")        


    def insertTodo(self,title,dte):
        mylist = self.db.getlist(dte)
        for dbtitle in mylist:
            if title in dbtitle[1]:
                print("Item already in the todolist")
                break 
        else:
            today = date.today()
            day = today.strftime("%d %B")
            now = datetime.now()
            current_time = now.strftime("%H:%M %p")
            current_datetime = day+" "+current_time
            self.db.insert(title,current_datetime)

    def updateTodoTitle(self,task_id,new_title):
        self.db.updateListTitle(task_id,new_title)

    def updateTodoStatus(self,task_id,status):
        today = date.today()
        day = today.strftime("%d %B")
        now = datetime.now()
        current_time = now.strftime("%H:%M %p")
        current_datetime = day+" "+current_time
        self.db.updateListStatus(task_id,status,current_datetime)    

    def deleteTodo(self,task_id):
        self.db.deleteItem(task_id)   

    def searchTodo(self,text):
        search_result=self.db.searchText(text)
        if(len(search_result)>0):
            for todo in search_result:
                print(todo)
        else:
            print("no such Item is present in the list")             

def main():
    parser = ArgumentParser(description="Welcome To the to Do list CLI app")

    #<--------------------------------LIST COMMAND------------------>

    parser.add_argument('-l','--list',action='store_true',help="print the list")
    parser.add_argument('-da','--date' ,action='store_true' ,help="print list with date")

    subparser = parser.add_subparsers(help="prints list items with status complete or incomplete")

    #<-------------LIST COMPLETE COMMAND---------------------------------------------->
    parser_complete = subparser.add_parser('complete',help="print complete list")
    parser_complete.add_argument('complete', action='store_true' ,help="print complete list")

    #<---------------------LIST INCOMPLETE  COMMAND--------------->
    parser_incomplete = subparser.add_parser('incomplete',help="print incomplete list")
    parser_incomplete.add_argument('incomplete',action='store_true',help="print incomplete list",default=False)



    # <------------------------CREATE COMMAND--------------------------------->

    parser.add_argument('-c','--create',help="Enter todo title to add to the database",metavar="<title>")




    #<----------------------------------EDIT COMMAND------------------------------->

    parser.add_argument('-et','--edit-title',nargs=2,
        metavar=('<task-id>','<updated-title>'),help='Edit the title with new title')
    parser.add_argument('-es','--edit-status',nargs=2,
        metavar=('<task-id>','<updated-status>'),help='Edit the status of the todoitem')    


    # <--------------------------------DELETE COMMAND--------------------------------->

    parser.add_argument('-d','--delete',help="Delete a todoitem",metavar="<task-id>")

    #<------------------------------------- SEARCH------------------------------>

    parser.add_argument('-s','--search', help="search for particular item in todolist" ,metavar="<search-item>" )

    args=parser.parse_args()
    todo = TodoList()

    if args.list and "complete" not in args and "incomplete" not in args: 
        if args.date:
            todo.showTodolist(args.date)
        else:
            todo.showTodolist(args.date)    


    elif args.create:
        print(args.create)
        todo.insertTodo(args.create,args.date)

    elif args.edit_title:
        try:
            task_id=int(args.edit_title[0])
            new_title=args.edit_title[1]
        except ValueError:
            print("Enter valid input \nfirst input should be taskid<int> and second is updated todoitem title \nyou can also refer to help section or enter command 'python3 todo.py to get all the available commands'")    
        else:
            todo.updateTodoTitle(task_id,new_title)

    elif args.edit_status:
        try:
            task_id=int(args.edit_status[0])
            status=args.edit_status[1].upper()
            if(status not in ["COMPLETE","INCOMPLETE"]):
                raise ValueError
        except ValueError:
            print("Enter valid input \nfirst input should be taskid<int> and second is status which can be either Complete or incomplete \nyou can also refer to help section or enter command 'python3 todo.py to get all the available commands'")    
        else:
            todo.updateTodoStatus(task_id,status)
     
    elif args.delete:
        task_id = args.delete
        try:
            task_id = int(task_id)
            todo.deleteTodo(task_id)
        except ValueError:
            print("Delete only takes integer as an argument")


    elif args.search:
        text = args.search
        todo.searchTodo(text)    
    
    elif "complete" in args and args.list:
        todo.completedTodos()
        
    elif "incomplete" in args and args.list:
        todo.incompleteTodos()

    else:
        print("USAGE guide \npython todo.py --list -da(for date)\npython todo.py --list incomplete\npython todo.py --list complete\npython todo.py --create <title>\npython todo.py --edit-title <task-id> <updated-title>\npython todo.py --edit-status <task-id> <updated-status>\npython todo.py --delete <task-id>\npython todo.py --search <search-item>")   
    

if __name__ == "__main__":
    main()

    
