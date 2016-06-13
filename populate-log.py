import requests
import random
from multiprocessing import Process
import time

url="http://localhost:80/index.php"

def request(i, url):
	
	lista = ["a=b&c=d", "x=y&a=z&error=1", "urucubaca=teste&bugou=false", "OO=GTtg&bA=1", "T1=hj&ul=1"]

	requests.get(url + "?" + random.choice(lista))
	print "Done request " + i

for i in range(1, 10000):
	print "Start request " + str(i)
	Process(target=request, args=(str(i), url, )).start()
	time.sleep(1)

