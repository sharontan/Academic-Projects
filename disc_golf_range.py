"""
Disc Golf Range

Down at the new driving range, there are numerous tees at which golfers can be found practicing their swings. Each golfer will call for a bucket of N balls at a time, then proceed to hit them one by one until empty, at which point he'll call for another bucket. When there are insufficient balls left in the central stash to satisfy a call for a bucket, all practice ceases and the retriever cart takes to the field to gather balls to replenish the supply.

This program implements a properly synchronized simulation for this problem in Python using Semaphores. A separate thread is created for the cart and each golfer. The simulation allows the following items to be easily configurable:

the initial size of the stash
the number of balls per bucket (which determines 
(a) how many balls a golfer can hit before calling for another bucket and (b) when the cart needs to head out to the field) the number of golfer threads

The program assumes endless rounds of golf as long as the cart collects the balls on the field. To terminate: Ctrl-z

"""

from threading import Thread, Semaphore
from time import sleep
import random

frolferArrived = Semaphore(0)
cartArrived = Semaphore(0)

stash = 0
on_field = 0

rng = random.Random()
rng.seed(100)


def Cart():
    global stash
    global on_field
    while True:
        frolferArrived.acquire()
        print ('#' * 50)
        print ("Stash ", stash, " Cart entering field")
        stash += on_field
        print ("Cart done, gathered ", on_field, " discs; Stash = ", stash)
        print ('#' * 50)
        on_field = 0
        cartArrived.release()


def Frolfer(frof, int_discs):
    global stash
    global on_field
    while True:
        print ("Frolfer ", frof, " calling for bucket")
        if stash < int_discs:
            frolferArrived.release()
            cartArrived.acquire()
        stash -= int_discs
        print ("Frolfer ", frof, " got ", int_discs, " discs, Stash = ", stash)
        for i in range(0, int_discs):
            print ("Frolfer ", frof, " threw disc ", i)
            on_field += 1
            sleep(rng.random())


if __name__ == '__main__':
    
    stash = int(input("Enter Initial Size of Stash: "))
    print ("Initial Size of Stash = ", stash)
    int_discs = int(input("Enter Number of Discs Per Bucket: "))
    print ("Number of Discs Per Bucket = ", int_discs)
    num_threads = int(input("Enter Number of Frolfer Threads: "))
    print ("Number of Frolfer Threads = ", num_threads)
    
    for frof in range(0, num_threads):
        tFrolfer = Thread(target=Frolfer, args=(frof, int_discs,))
        tFrolfer.start()
   
    sleep(1)
    tCart = Thread(target=Cart)
    tCart.start()

