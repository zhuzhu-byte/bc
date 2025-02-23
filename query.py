from xmlrpc import client
import sys

server = client.ServerProxy("http://127.0.0.1:8088")
#server = client.ServerProxy("http://192.168.122.60:8088")

while 1:
    try:
        print("\n")
        print("new_wallet , get_latest_blocknum , get_balance , set_balance , get_latestblock , get_fixed_block , get_nodes")
        line = input('Prompt> ')
        words = line.split()
        len1 = len(words)
        if len1 == 1:
            if words[0] == "new_wallet":
                print(server.new_wallet())
            elif words[0] == "get_latest_blocknum":
                print(server.get_latest_blocknum())
            elif words[0] == "get_nodes":
                print(server.get_nodes())
            elif words[0] == "get_block":
                print(server.get_block())
            elif words[0] == "get_latestblock":
                print(server.get_latestblock())
            elif words[0] == "get_blocknum":
                print(server.get_blocknum())
        elif len1 == 2:
            if words[0] == "get_balance" :
                print(server.get_balance(words[1]))
            elif words[0] == "get_fixed_block" :
                print(server.get_fixed_block(words[1]))
        elif len1 == 3:
            if words[0] == "set_balance" :
                print(server.set_balance(words[1], words[2]))
    except:
        print("failed to connect")
        exit()
