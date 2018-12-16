#!/usr/bin/env python
import sys
import threading
import requests
from multiprocessing import Process, Queue, current_process
import time
from bs4 import BeautifulSoup
import csv

loop = True
domain_list = []
task_queue = Queue()
done_queue = Queue()
num_workers = 3
filename = "output.txt"
link_list = []

# function that creates the menu interface
def print_menu():
    print("="*10 + "MENU" + "="*10)
    print("1. Add a domain name")
    print("2. Set output file")
    print("3. Reset domain names")
    print("4. Start processing queue")
    print("5. Stop processing queue")
    print("6. Display Logs")
    print("7. Exit")
    print("="*24)

def scraper(input,output):
    output.put("{} starting".format(current_process().name))
    file = open(filename, "a")
    for domain in iter(input.get, "STOP"):
        slash_domain = domain + "/"
        result = requests.get(domain)
        soup = BeautifulSoup(result.text, "html.parser")
        file.write("\nSOURCE URL: " + domain +"\n")
        for link in soup.find_all("link"):
            url_link = link.get("href")
            
            if domain == url_link or slash_domain == url_link:
                pass
                print("PASS")
            elif url_link not in link_list:
                link_list.append(url_link)
                output.put(current_process().name + ": " + url_link)
                file.write("-"+url_link +"\n")
            else:
                pass
        
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
                domain_name = "www.{}".format(domain_name)
                domain_list.append(domain_name)
            
            elif choice == 2:
                global filename
                filename = input("Enter output filename: ")

            elif choice == 3:
                print("\nResetting domain names...\n")
                del domain_list[:]
               
            elif choice == 4:
                print("\nQueue now processing...\n")
                
                if len(domain_list) == 0:
                    print("No items to be processed. Add a domain name first")
               
                else:
                    for name in domain_list:
                        name = "https://{}".format(name)
                        task_queue.put(name)
                        
                    # ADD CODE FOR WEB CRAWLER FUNCTIONALITY HERE
                   
                    for i in range(num_workers):
                        process = Process(target=scraper, args=(task_queue,done_queue))
                        process.start()
                    
                    del domain_list[:]
                   
            
            elif choice == 5:
                print(process.is_alive())
                for i in range(num_workers):
                    process.terminate()
                print(process.is_alive())
            
            elif choice == 6:
                print("="*13 + "\n DISPLAY LOG\n" + "="*13)
                
                for message in iter(done_queue.get, "STOP"):
                    try:
                        print(message)
                        time.sleep(2)
                    except KeyboardInterrupt:
                        break

            elif choice == 7:
                print("*Exiting...*")
                sys.exit()
            
            else:
                print("Wrong selection. Enter another key to try again")

    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit()


if __name__ == "__main__":
  main()