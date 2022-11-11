#importing modules required for the program
#uncomment line 3 to see memory profile
#from memory_profiler import profile
from threading import Thread
from time import perf_counter
from rx import Observable
from rx import create

#initialize a list of dictionaries with menu items
items = [
        {'name': 'Milk Tea', 'price': 4.00},
        {'name': 'Thai Tea', 'price': 4.50},
        {'name': 'Jasmine Tea', 'price': 3.00},
        {'name': 'Oolong Tea', 'price': 3.50},
        {'name': 'Green Tea', 'price': 3.00},
        {'name': 'Black Tea', 'price': 3.00}
    ]

#implementing MVC model
#model
class QuoteModel:
    #initialize constructor with items ordered by user
    def __init__(self, order_items):
        self.order_items = order_items
    
    #return items ordered by user
    def get_item(self):
        return order_items;
     
    #add the item with the index on to the order_items list (list ordered by user)
    def addToList(self, order_items, index): 
        try:
            order_items.append(items[index])
            self.order_items = order_items 
        except IndexError as err: 
            order_items = 'Not found!' 
        return order_items
    
    # set order_items to order_items passed in
    def set_items(self, order_items):
        self.order_items = order_items
 
 #view
class QuoteTerminalView:
    #pring items ordered by user
    def show(self, item): 
        for vals in item:
            print(vals)
            
    #print items on the menu
    def show_items(self):
        count = 0;
        print('\t Menu')
        for vals in items:  
            res = ", ".join("{}: {}".format(*i) for i in vals.items())
            count += 1;            
            print(count, res)
 
    def selected_items(self, item): 
        return item 
 
class QuoteTerminalController:
    #initialize order_items, model object, view object
    def __init__(self):
        order_items = []
        self.model = QuoteModel(order_items) 
        self.view = QuoteTerminalView()
 
    def run(self):
        #initialize order_items or customer order list
        order_items = []
        #initializing index
        index = -1
        #initialize user selection with y to start the while loop
        selection = 'y';
        while selection == 'y':
            #get user input on what drink they would like to order
            choice = int(input('Select the number of the item you want to order: '))
            # if selection is one, set index to zero
            if choice == 1:
                index = 0
            elif choice == 2:
                index = 1
            elif choice == 3:
                index = 2
            elif choice == 4:
                index = 3
            elif choice == 5:
                index = 4
            elif choice == 6:
                index = 5
            else:
                print('Invalid choice')
            if index >= 0 and index < 6:
                #call model items addToList function while passing in the customer order list and the index user selected, this is set to item
                item = self.model.addToList(order_items, index)
                #ask user if they want to continue inputting in more items, press any key to stop while loop
            selection = input(str('Do you want to add another item? Select y to order another item. Press any other key if you are done ordering. ')).lower() 
            
        #call show method of the view object to display the items in customer order list
        self.view.show(item)
        #make a list of filenames
        filenames = [
        'customer.txt',
        'salesrecord.txt',
        ]
        # create threads
        threads = [Thread(target=writeToFile, args=(filename, order_items))
            for filename in filenames]

        # start the threads
        for thread in threads:
            thread.start()

        # wait for the threads to complete
        for thread in threads:
            thread.join()
 
#checking to see if price is greater than 3.99 which the price for milk items
def buy_teas(observer, scheduler):
  for item in items:
    if(item['price'] > 3.99):
      observer.on_next(item['name'])
    elif(item['price'] <= 0):
      observer.on_error(item['name'])
  observer.on_completed()

#writing the customer order list to a file
def writeToFile(filename, order_items):
    print(f'Processing the file {filename}')
    #creating order list for customer copy
    if filename == 'customer.txt':
        with open(filename, 'w') as f:
            total = 0
            for vals in order_items:  
                res = ", ".join("{}: {}".format(*i) for i in vals.items())
                f.write(res)
                f.write('\n')
                total = total + vals['price']
            strTotal = '\n$ ' + str(total)
            f.write(strTotal)
            f.write("\n")
    else:
        #creating order list for sales record
        with open(filename, 'a') as f:
            total = 0
            for vals in order_items:  
                res = ", ".join("{}: {}".format(*i) for i in vals.items())
                f.write(res)
                total = total + vals['price']                               
                f.write("\n")
            strTotal = '\n$ ' + str(total) + ('\n')
            f.write(strTotal)
 
#uncomment line 145 to see memory profiler
#@profile
def main():
    #initialize customer order list
    order_items = []
    #declare view object
    view = QuoteTerminalView()
    #showing menu items to the user
    view.show_items()
    
    #displaying which menu items have milk
    source = create(buy_teas)

    source.subscribe(on_next=lambda value: print("Specialty Items - Following Drink Contains Diary Products: {0}".format(value)),
                on_completed=lambda: print(" "),
                on_error=lambda e: print(e))
    
    #initializing controller object
    controller = QuoteTerminalController()
    #calling run method in the controller object to perform all other operations with data
    controller.run()
    
 
if __name__ == '__main__': 
    main()
