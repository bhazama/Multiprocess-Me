#!/usr/bin/env python
import sys
import threading
import requests
from multiprocessing import Process, Queue, current_process

loop = True
domain_list = []
queue_list = []
task_queue = Queue()
done_queue = Queue()
num_workers = 4

# function that creates the menu interface
def print_menu():
    print("="*10 + "MENU" + "="*10)
    print("1. Add a domain name")
    print("2. Reset domain names")
    print("3. Start processing queue")
    print("4. Stop & reset processing queue")
    print("5. Display Logs")
    print("6. Exit")
    print("="*24)
    
#function that checks the queue process for stop string
def check_process(list):
    if list[0] == "STOP":
        print("Stopping queue process...")
        return
    else:
        print("ok!")

def scraper(input,output):
    output.put("{} starting".format(current_process().name))
    for domain in iter(input.get):
        result = requests.get(domain)
        output.put("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))

def main():
    try: 
        global loop
        while loop:
            print_menu()
            choice = input("Enter your choice [1-5]: ")
            choice = int(choice)

            if choice == 1:
                print("*Add a domain name has been selected*")
                domain_name = input("What is the domain name to be added? ")
                domain_list.append(domain_name)
                print(domain_list)
            
            elif choice == 2:
                print("Resetting domain names...")
                del domain_list[:]
                print(domain_list)
               
            elif choice == 3:
                print("*Start processing queue has been selected*")
                #create queues
                
                if len(domain_list) == 0:
                    print("No items to be processed. Add a domain name first")
                elif domain_list[0] == "STOP":
                    print("Stop process has been used. Please reset your domain names")
                else:
                    for name in domain_list:
                        task_queue.put(name)
                        queue_list.append(name)
                        
                        print("="*10 + "CURRENTLY IN QUEUE LIST" + "="*10)
                        print(queue_list)
                        # ADD CODE FOR WEB CRAWLER FUNCTIONALITY HERE
                   
                    for i in range(num_workers):
                        process = Process(target=scraper, args=(task_queue,done_queue))
                        process.start()
                    
                    for message in iter(done_queue.get):
                        print(message)
                        
                    #for domain in queue_list:
                     #   print("CHECK:" + done_queue.get())
                
                del domain_list[:]
            
            elif choice == 4:
                print("*Stop processing queue has been selected*")
                domain_list.insert(0, "STOP")
                check_process(domain_list)
                del queue_list[:]
            
            elif choice == 5:
                print("*Display Logs has been selected*")
                
                
                print("="*5 + "IN QUEUE:" + "="*5)
                for name in queue_list:
                    print(name)
            
            elif choice == 6:
                print("*Exiting...*")
                sys.exit()
            
            else:
                print("Wrong selection. Enter another key to try again")

    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit()






if __name__ == "__main__":
  main()