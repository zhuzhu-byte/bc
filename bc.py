# sudo apt install python3-pip
# pip3 install pycryptodome
# pip3 install leveldb


#  cat .pip/pip.conf 
# [global]
# index-url = https://pypi.tuna.tsinghua.edu.cn/simple
# [install]
# trusted-host = https://pypi.tuna.tsinghua.edu.cn


# coding=utf-8
from collections import OrderedDict

import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import binascii
import sys
import hashlib
import json
import time
from urllib.parse import urlparse
import threading

lock_block = threading.Lock()
lock_nodes = threading.Lock()
lock_transaction = threading.Lock()

MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 1
MINING_DIFFICULTY = 4

# print(len(sys.argv))
if len(sys.argv) == 2:
    clientenable = int(sys.argv[1])
    if clientenable not in [0, 1, 2, 3]:
        print("worong parameter")
        exit(0)

import leveldb

class LEVELDB:
    def __init__(self, dbname):
        self.db = leveldb.LevelDB(dbname)

    def insert(self, key, value):
        # print("WriteBatch")
        batch = leveldb.WriteBatch()
        batch.Put(bytes(key, encoding = "utf8"), bytes(value, encoding = "utf8"))
        self.db.Write(batch, sync = True)
 
    def insert_fast(self, key, value):
        self.db.Put(bytes(key, encoding = "utf8"), bytes(value, encoding = "utf8"), sync=True)

    def delete(self, key):
        self.db.Delete(bytes(key, encoding = "utf8"))

    def update(self, key, value):
        self.insert(key, value)

    def search_blocknum(self, key):
        try:
            return self.db.Get(bytes(key, encoding = "utf8"))
        except:
            return bytes('0', encoding = "utf8")

    def search(self, key):
        try:
            return self.db.Get(bytes(key, encoding = "utf8"))
        except:
            return bytes('[]', encoding = "utf8")

    def search_balance(self, key):
        try:
            return self.db.Get(bytes(key, encoding = "utf8"))
        except:
            return bytes('0', encoding = "utf8")

    def display(self):
        strtmp = ""
        for key, value in self.db.RangeIter():
            print(key, value)
            strtmp += key.decode()+"  "+value.decode() +"\n"
        return strtmp

    def displayLastBlock(self):
        strtmp = ""
        for key, value in self.db.RangeIter(reverse=True):
            print(key, value)
            strtmp += key.decode()+"  "+value.decode() +"\n"
            break
        return strtmp

    def getLastBlock(self):
        for key, value in self.db.RangeIter(reverse=True):
            print("getLastBlock", value.decode('utf-8'))
            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,key, type(value.decode('utf-8')))
            return value.decode()
        return "[]"

# need to
public_init = "30819f300d06092a864886f70d010101050003818d0030818902818100a00413c24be67da0f07b737ca7d1651362a28879b7f2f0e983f8dc557a706918dd2fa503d254d70c4f010cab67bf8aa406ef4e18b3cbb5b8fa4c2b1344c106382da53a26e69f3bdb6efa955c94faeb0e370878d5ccced3798267687dbe98d23ae443189883aa1ada5b00d992105079b50d6a21e5531bf4884f1768a6b48932a50203010001"

localnode = "192.168.122.60"

if clientenable==0:#192.168.122.60
    public1 = "30819f300d06092a864886f70d010101050003818d0030818902818100cabc1aab5acb6a2832da2979809e0e624ba86a6895d5752a1ac311f678ea9683a92fe082630cacd43eeea5ef39441322f2d664f148e1da360ae70d8b3d4eb43f7eac5f6174c34bdd70ff3b18f1dc9ae3938cb81153895ddaa667d39a1f222e130790cfa86741202821b6b658606abc9ca413bbde0b5872cccc4b72a5029dec890203010001"
    private1 = "3082025d02010002818100cabc1aab5acb6a2832da2979809e0e624ba86a6895d5752a1ac311f678ea9683a92fe082630cacd43eeea5ef39441322f2d664f148e1da360ae70d8b3d4eb43f7eac5f6174c34bdd70ff3b18f1dc9ae3938cb81153895ddaa667d39a1f222e130790cfa86741202821b6b658606abc9ca413bbde0b5872cccc4b72a5029dec8902030100010281801812a0a890ec07378d7d3ff03e5c56392802701b29d27a3a7509cd71daaf014f12297e13416b6580c0d5c1d48f7454c0e13ca1a91066480cc37be6ccee2b50a5e4d8fb0fd3723c8bee78a9c85dde98c08692bdf2023f85dbae7497900bb599b1de47a8900f38ad7c3cbe19789e964a76e2bd1579dfdc51cd33b7567dd5807121024100deb0f832fc9dbe3591e7dab98a80aa6b6ae9d265ef8180cce406fbd1b5d9820fcecf287d13d1324b9c4d0f8a9ff35933f43c86abfeeb7a5191ca3467cb383229024100e90efbdc8f4bbe2a3dd2bdae06cdbcfd65ac035ad82b1380fa91d36c705a1703dc236849ab0ad044efd2c22ff5ac02691a8f339e295a2700457ec806c7c6f361024041411239be946a9c3ff8f4bad1bf0a3117cf147c12469c7b6d862e5c31315f4f4a86a192a52ff3d0fc280899d26cf882a4dae78b96d361b06d4c173722f180a1024100cdb37ff16838be1ba27d83153ac4146ec3725373b7202e12c51638b99960aab7a97146f6de94a8c66fb661d6dacb7b45313ffb9b397c6cb7fc9eae05ee065781024100acfcdd80f3b61ff0d11e6298c0dc36b250e57e49baf26fae6c33b47f4a6293fa9cd7ee78e2a81b661b84096c41e20cc8fb6a57c1e4302e550a606a87559716d4"

if clientenable==1:#192.168.122.61
    localnode = "192.168.122.61"
    public1 = "30819f300d06092a864886f70d010101050003818d0030818902818100a36e6d648968fd4d0e0883fdfd8cef9e65dc9a17c6001823a546130ea591a101340128b013803f7e948e0ebd7f16bc20b65cf68fef0a996a6a40f7b17b42dd4b65fb85cb23057eddb61663bf5182bb5bae424475c6656dc6e921790ea62e1676badce957a793b6fe31200a8be40da88d58e5b31ecbcaa47b1789d28ceed3e4190203010001"
    private1 = "3082025c02010002818100a36e6d648968fd4d0e0883fdfd8cef9e65dc9a17c6001823a546130ea591a101340128b013803f7e948e0ebd7f16bc20b65cf68fef0a996a6a40f7b17b42dd4b65fb85cb23057eddb61663bf5182bb5bae424475c6656dc6e921790ea62e1676badce957a793b6fe31200a8be40da88d58e5b31ecbcaa47b1789d28ceed3e4190203010001028180015fbd96d6392d71fda5765cfb6710734af087d44c61f6694394784e68e05888104ed72fb50c14ff7bbb0477d7f7a9425fc84cb50064ae59d3a8a193bd9ce3c60f95b308f51e217ab069c1ed883d1d2533d4bcb8c6602c1bd67fce3135b83153b30aff1ef4294fcb6c5f5ceedb43af11445353ed5d4c4a1ace074f1576cdaca5024100c69b0fd33d938d772750e2fd3f700838d08754653a85dabb9eff30ca4adf1a6128364fd630efae2abac31c8299963f6a9a2ac3bd363416b6547c8f645b6eb955024100d2a926baa1af353437722fbf11720e2c338e64b10260d53d0a0872dba2690e671cc152faa73ac37f672bf85b5537f8d03d18d20ffd777d6e5d0e1e45ee736fb502406d7ee806aa9843124256d20e957f0ac9680e74752b02c9494fab9a16ad98bb4e7d81141b1ef7c5aa413578ee7806e207bfdf7bf341830e528fd9eca483d453d1024100b601fd7b3c5cb3bc24b79c7719ac9080321f31f2199aee41e99c3918786f0a499e778da910b95dd5829f63da0d7be99689631b83433c6cfbe09c651d8892e60d0240550b1d96146b1ab86f58d61cd48a48030f2f868031c11ceaa72e81b65840d5df088cad13214820ff9567b74521a702a1f9b9553a6d91ad6c9e2e8ab674956562"

if clientenable==2:#192.168.122.62
    localnode = "192.168.122.62"
    public1 = "30819f300d06092a864886f70d010101050003818d0030818902818100ac8a8b4e112cf814b55387d0c9a661278c442ed7e438d50be1f6c67bf761ccdb34d1b83deb4cbeaf372f3595111acf64f622b738a441fb733d8974e7d3f03688551e2eb86eb4abce946176772c85ddb187c47d016a0680341a70e48dcc1871de894621601eeb7b1311de7bf8f7b1b13f5e7e5ef86fa14b12775c55da5c1170c50203010001"
    private1 = "3082025c02010002818100ac8a8b4e112cf814b55387d0c9a661278c442ed7e438d50be1f6c67bf761ccdb34d1b83deb4cbeaf372f3595111acf64f622b738a441fb733d8974e7d3f03688551e2eb86eb4abce946176772c85ddb187c47d016a0680341a70e48dcc1871de894621601eeb7b1311de7bf8f7b1b13f5e7e5ef86fa14b12775c55da5c1170c5020301000102818012ca2fab7bc15aeede644f59146cb30ddc7f9c5e54733ff8404e6085258698099331f78f7ead67e2aaeed036009bdbd411ddebf816233d5fea66aabd885e13820d7c4ddd2cf82b3ca906cd04723960f5a04f403a9ce0ee037f463dd97253e4b17f8ddeacfa74301593ce5a24da1763a73c3b1334eb91b71c9e1daff24a05bded024100ca7b3604b9a87f471ad2685a014ce8844d0dcc0c2d5eba21b725638926c60f97c33853f7e7a667ca45f6168175f985772c37e869f107881241401430acd294a7024100da2573ae55312f0bd2d23ca9e039cfdf4fb39f7e93ba122be175001d5a7c6c0e04f4a6509bf305ce4e706a3aea32c826772225c76436bcdaef543f14c18080b302400ff6bce08c7eb36238c424040c9c32acd3a265d703f0b6fe1781742289130e81a99b944b34515357884289adb54e71ee5e671e04d44302c065b296a4ebcb427b02410084a5df68f39ebbb7d9d343561ce5aa9464d799b59348c301f1cf7e695afb6b8d3ed0314db4f69ae22f6a45fe5b28d3f227e118cddd0f37d97d4c622b51dabce7024026f62858bfade148e9a4a6dd2defc3c76c39a4a4da7adca1a18f366f7aa7e087ffc84eeb6ff06e8190149a95724b7ab8d47ba2c478005f1115290029efaa5906"

if clientenable==3:#192.168.122.63
    localnode = "192.168.122.63"
    public1 = "30819f300d06092a864886f70d010101050003818d0030818902818100b264bf94054517613fbb3243d83933959f1342514961a45b87d87c44b7cfdf79ce6fa9de8e6975921b6d47740ad00114d3c1c29734a0556794451f7ed2660c8eb545f72dc22da2406081aa6913e5850262e98b135f622afdcff7a431c25be48cb2d5b2bf63199b39b0e93c06fa5ecb914abe4193e784ccb6cd7f1f8395d053ad0203010001"
    private1 = "3082025d02010002818100b264bf94054517613fbb3243d83933959f1342514961a45b87d87c44b7cfdf79ce6fa9de8e6975921b6d47740ad00114d3c1c29734a0556794451f7ed2660c8eb545f72dc22da2406081aa6913e5850262e98b135f622afdcff7a431c25be48cb2d5b2bf63199b39b0e93c06fa5ecb914abe4193e784ccb6cd7f1f8395d053ad020301000102818022398874b037236765a7f71a8388e3dfe46b3839aa9ba841e433d11188f7414f57dedde6e4091104952cf7bca8576421b807901adcbe96ebfe8aed623220e06f0d80c07471269af9ec25b7d6dbd14947a1c3f4c72e14604be09a774eb56a4f6f4b810c91abce691f5fa8bca7cbecfe030915556809bd9cb7685b513bfdc89101024100cd3e5f2a5ffa36669649c25a394dbebca2c95bd5cbfbb7d00f0c33b1019d93d2fd52d977d1cdb24423223e61695ece437bda6dcfb177c3b0b8dcb313c0f60701024100de828aec25127081f7779702c058518557513a3a3968efbae55a6d68ded0d6206255f79b7f31b7a901d607ec51717b303b79e55720321ce9204fd41f586598ad024077cc3925f5c1897155b595d0adf3f82a08e6794910784bb110a771a096add073edd327062e1adf3bb03a33a90e24fd461c8bc15ee25a6289cb4d5ee55fd2fb0102410081e3b0971339056649008dadb47c99f1fdbbd402c31aa7bef13ded5a679f7f2fde5792b839f2dae494c6cd4f3d67c262b08582c46e6df28480313981a6c77fed0241008dc286d34f7c4625bcd05c882811fe3e18adda29c74e1ffa0a2f0c5b5f4be9ce912ee1b9d10a1414a20662464468c685cd2a9d111477eefa9325edd184ed14e3"

DB_STATUS=LEVELDB("status")
# DB.insert("123", str(13))
# DB.insert("234", str(11))
# DB.insert("wer", str(12))
  
print("DB_STATUS.display")
DB_STATUS.display()
print("\n\n")
# exit()
DB_BLOCK=LEVELDB("block")
# print("DB_BLOCK.display")
# DB_BLOCK.display()

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        # return OrderedDict({'sender_address': self.sender_address,
        #                     'recipient_address': self.recipient_address,
        #                     'value': self.value})
        return {'sender_address': self.sender_address,
                            'recipient_address': self.recipient_address,
                            'value': self.value}

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


transactionarray = []
transactionarray_receive = []
g_conndict={}
g_connect_2_me=[]

class Blockchain:

    def __init__(self):
        # self.transactions =  Transaction(sender_address=public1, sender_private_key=private1, recipient_address=public1, value=4200000000)
        # self.transactions = [('sender_address', '0'), ('recipient_address', '30819f300d06092a864886f70d010101050003818d0030818902818100a00413c24be67da0f07b737ca7d1651362a28879b7f2f0e983f8dc557a706918dd2fa503d254d70c4f010cab67bf8aa406ef4e18b3cbb5b8fa4c2b1344c106382da53a26e69f3bdb6efa955c94faeb0e370878d5ccced3798267687dbe98d23ae443189883aa1ada5b00d992105079b50d6a21e5531bf4884f1768a6b48932a50203010001'), ('value', 4200000000)]
        aaa = json.loads(DB_BLOCK.search(DB_BLOCK.search_blocknum("blocknum").decode()).decode())
        print("aaa", aaa)
        self.latestblock = aaa
        self.chain = []
        # self.transactions = []
        self.nodes = ["192.168.122.60"]
        self.node_id = public1
        self.pow = 1
        if  self.latestblock == []:
            print("\n")
            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, "create the 1st block")
            self.create_block(0, public_init)
            DB_STATUS.insert(public_init, str(4200000000))
        if clientenable==0:
            self.nodes = []
            self.pow = 1


    def create_block(self, nonce, previous_hash):
        """
        Add a block of transactions to the blockchain
        """
        block = {'block_number': 1,
                'timestamp': "2028-05-28 16:13:00",
                'transactions': "I love the earth travel to moon 1st wallet address :"+public_init,
                'nonce': nonce,
                'previous_hash': previous_hash}

        DB_BLOCK.update("blocknum", str(1))
        DB_BLOCK.update(str(1), json.dumps(block))
        self.chain.append(block)
        self.latestblock = block
        return block

    def add_block(self, nonce, previous_hash, block_number, pos_transaction):
        """
        Add a block of transaction to the blockchain
        """
        global transactionarray
        lock_block.acquire()

        if block_number != self.latestblock['block_number']:
            print("\033[34;40m","\n","\033[0m")
            print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno, "the lastest block is done by othes", block_number,self.latestblock['block_number'],"\033[0m")
            lock_block.release()
            return

        transaction = pos_transaction[0]
        transaction_dict = transaction[0]
        print("\033[34;40m","\n","\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,"add reward to", transaction_dict["sender_address"],"\033[0m")
        amount2 = int(DB_STATUS.search_balance(transaction_dict["recipient_address"]).decode())
        value2 = transaction_dict["value"]
        DB_STATUS.update(transaction_dict["recipient_address"], str(int(amount2 + value2)))

        print("\n\n")
        tmp_transactionarray=[]
        if transactionarray:
            print("\033[34;40m","\n","\033[0m")
            print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno, "transaction synced from other node", transactionarray,"\033[0m")
            lock_transaction.acquire()
            for transaction in transactionarray[:3]:# 3 for test
                transaction_dict = transaction[0]
                amount1 = int(DB_STATUS.search_balance(transaction_dict["sender_address"]))
                amount2 = int(DB_STATUS.search_balance(transaction_dict["recipient_address"]))
                value2 = transaction_dict["value"]
                if amount1 >= value2:
                    DB_STATUS.update(transaction_dict["sender_address"], str(int(amount1 - value2)))
                    DB_STATUS.update(transaction_dict["recipient_address"], str(int(amount2 + value2)))
                    tmp_transactionarray.append(transaction)
            transactionarray = transactionarray[3:]
            lock_transaction.release()
        else:
            print("\033[34;40m","\n","\033[0m")
            print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,"there is no transaction to add","\033[0m")

        tmp_transactionarray=pos_transaction+tmp_transactionarray
        print("\033[34;40m","\n\n","\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,"tmp_transactionarray", len(tmp_transactionarray), tmp_transactionarray,"\033[0m")

        height = block_number + 1
    
        block = {'block_number': height,
                'timestamp': time.time(),
                'transactions': tmp_transactionarray,
                'nonce': nonce,
                'previous_hash': previous_hash}

        self.latestblock = block
        datastr = json.dumps(block)
        for item,server in g_conndict.copy().items():
            # server.set_latestblock(datastr.encode('utf-8'))
            ret = server.set_latestblock(datastr)
            print("sync to" , item, "return value", ret)
        self.chain.append(block)
        DB_BLOCK.update(str(height), datastr)
        DB_BLOCK.update("blocknum", str(height))
        print("\n\n")
        # print(self.chain)
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,block['block_number'],"\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,block['timestamp'],"\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,block['transactions'],"\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,block['nonce'],"\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,block['previous_hash'],"\033[0m")
        lock_block.release()
        return block

    def hash(self, block):
        """
        Create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self):
        """
        Proof of work algorithm
        """
        # print(self.chain[-1])
        # last_block = self.chain[-1]
        last_block = self.latestblock
        print("\033[34;40m","\n")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno, last_block)
        
        last_hash = self.hash(last_block)

        nonce = 0
        while self.valid_proof(last_block, last_hash, nonce) is False:
            nonce += 1

        # print("!!!!!1", last_block, last_hash, nonce)

        return nonce, last_hash, last_block['block_number']

    def check_nonce(self, nonce):
        """
        Proof of work algorithm
        """
        ret = 0
        # print(self.chain[-1])
        last_block = self.latestblock
        last_hash = self.hash(last_block)

        # print("!!!!!2", last_block, last_hash, nonce)
        if self.valid_proof(last_block, last_hash, nonce) == False:
            ret = sys._getframe().f_lineno

        return nonce, last_hash, ret

    def check_syncblock(self, block):
        """
        Proof of work algorithm
        """
        lock_block.acquire()
        if block["block_number"] <= self.latestblock['block_number']:
            print("\n")
            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, block["block_number"],"is little than", self.latestblock['block_number'])
            lock_block.release()
            return sys._getframe().f_lineno

        _,_,ret = self.check_nonce(block['nonce'])
        if(ret):
            print("\n")
            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, "syncnode nonce check failed",ret)
            lock_block.release()
            return  sys._getframe().f_lineno

        i = 0
        for transaction in block["transactions"]:
            # transaction_dict = OrderedDict(transaction[0])
            transaction_dict = transaction[0]
            signdata = transaction[1]
            if i:
                verifyaddress = transaction_dict["sender_address"]
            else:
                verifyaddress = transaction_dict["recipient_address"]
                i=1
            if self.verify_transaction_signature(verifyaddress,signdata, transaction_dict) == True:
                pass
            else:
                print("\n")
                print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, "check signature failed", transaction)
                lock_block.release()
                return sys._getframe().f_lineno

        i = 0
        for transaction in block["transactions"]:
            transaction_dict = transaction[0]
            signdata = transaction[1]
            amount1 = float(DB_STATUS.search_balance(transaction_dict["sender_address"]))
            amount2 = float(DB_STATUS.search_balance(transaction_dict["recipient_address"]))
            value2 = transaction_dict["value"]
            if i:
                if amount1 >= value2:
                    DB_STATUS.update(transaction_dict["sender_address"], str(int(amount1 - value2)))
                    DB_STATUS.update(transaction_dict["recipient_address"], str(int(amount2 + value2)))
                else:
                    print("\n")
                    print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, "someone send wrong transaction", transaction)
                    lock_block.release()
                    return sys._getframe().f_lineno
            else:
                # pow reward
                DB_STATUS.update(transaction_dict["recipient_address"], str(int(amount2 + value2)))
                i = 1

        self.chain.append(block)
        self.latestblock = block
        print("\n")
        print(sys._getframe().f_code.co_name, sys._getframe().f_lineno, "self.latestblock:", self.latestblock)
        DB_BLOCK.update(str(block["block_number"]), json.dumps(block))
        DB_BLOCK.update("blocknum", str(block["block_number"]))

        lock_block.release()
        return 0

    def valid_proof(self, chain, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        """
        Check if a hash value satisfies the mining conditions. This function is used within the proof_of_work function.
        """
        guess = (str(chain)+str(last_hash)+str(nonce)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0'*difficulty


    def new_wallet(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()
        response = {
            'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
            'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        }

        return json.dumps(response), public_key, private_key

    def verify_transaction_signature_debug(self, sender_address, signature, transaction):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (sender_address)
        """
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        strtransaction = str(transaction)
        print("\n\n")
        print("strtransaction", strtransaction)
        print("signature", signature)
        h = SHA.new(strtransaction.encode('utf8'))
        print("h", h)
        data = verifier.verify(h, binascii.unhexlify(signature))
        print("data", data)
        return data

    def verify_transaction_signature(self, sender_address, signature, transaction):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (sender_address)
        """
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))

    def get_fixed_block(self, blocknum):
        data = DB_BLOCK.search(str(blocknum))
        print("get_fixed_block", blocknum,data)
        return data

blockchain = Blockchain()
# _, public1, private1 = blockchain.new_wallet()
print("\n")
print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"blockchain.chain:", blockchain.chain)
# print("new_wallet", blockchain.new_wallet())


class RPCinterface:
    def new_wallet(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()
        response = {
            'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
            'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        }
        return json.dumps(response)

    def get_balance(self, adress):
        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, adress)
        data = DB_STATUS.search_balance(str(adress))
        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,data, type(data))
        return DB_STATUS.search_balance(adress).decode('utf-8')

    # def get_nodes(self, remote_nodes):
    #     # print(remote_nodes,type(remote_nodes))
    #     tmp_nodes = blockchain.nodes
    #     blockchain.nodes += json.loads(remote_nodes)
    #     blockchain.nodes = list(set(blockchain.nodes))
    #     # print(tmp_nodes, remote_nodes, blockchain.nodes)
    #     return json.dumps(tmp_nodes)
    #     # return json.dumps(blockchain.nodes)

    def get_nodes(self, remote_nodes):
        global g_connect_2_me
        # print(remote_nodes,type(remote_nodes))
        tmp_nodes = blockchain.nodes
        remote_nodes = json.loads(remote_nodes)
        blockchain.nodes += remote_nodes
        g_connect_2_me.append(remote_nodes[0])
        g_connect_2_me = list(set(g_connect_2_me))
        blockchain.nodes = list(set(blockchain.nodes))
        # print(tmp_nodes, remote_nodes, blockchain.nodes)
        return json.dumps(tmp_nodes)

    # def get_nodes(self):
    #     return json.dumps(blockchain.nodes)

    def get_latestblock(self):
        return json.dumps(blockchain.latestblock)

    def set_latestblock(self, block):
        return blockchain.check_syncblock(json.loads(block))

    def send_onetransaction(self, onetransaction):
        transaction = json.loads(onetransaction)
        lock_transaction.acquire()
        transactionarray_receive.append(transaction)
        lock_transaction.release()
        return 0
        # transaction = json.loads(onetransaction)
        # transaction_dict = transaction[0]
        # signdata = transaction[1]
        # verifyaddress = transaction_dict["sender_address"]
        # if self.verify_transaction_signature(verifyaddress,signdata, transaction_dict) == True:
        #     with lock_transaction:
        #         transactionarray_receive.append(transaction)
        #     # for item,server in g_conndict.items():
        #     #     ret = server.send_onetransaction(onetransaction)
        #     #     print("sync transaction to" , item, onetransaction, "return value", ret)
        #     return 0
        # else:
        #     return -1

    # def get_blocknum(self):
    #     return DB_BLOCK.search_blocknum("blocknum").decode()
    def get_latest_blocknum(self):
        return blockchain.latestblock['block_number']

    def set_balance(self, toaddress, amount):
        print(toaddress, amount)
        amount = int(amount)
        # if amount > 100:
        #     return 0
        transaction = Transaction(sender_address=public1, sender_private_key=private1, recipient_address=toaddress, value=amount)
        print("sendbalance",transaction.to_dict() )
        lock_transaction.acquire()
        transactionarray.append([transaction.to_dict(),transaction.sign_transaction()])
        lock_transaction.release()
        return amount

    def get_fixed_block(self, blocknum):
        data = DB_BLOCK.search(str(blocknum)).decode('utf-8')
        print("get_fixed_block", blocknum,data,type(data))
        return data
        # return DB_BLOCK.search(str(blocknum)).decode('utf-8')
        # return json.dumps(DB_BLOCK.search(str(blocknum)))

def start_server_rpc():
    from xmlrpc.server import SimpleXMLRPCServer
    obj = RPCinterface()
    server = SimpleXMLRPCServer(("0.0.0.0", 8088))
    server.register_instance(obj)
    print("Listening on port 8088")
    server.serve_forever()


th = threading.Thread(target=start_server_rpc)
th.setDaemon(True)
th.start()


def start_misc():
    while 1:
        lock_transaction.acquire()
        if len(transactionarray_receive):
            for transaction in transactionarray_receive:
                transaction_dict = transaction[0]
                signdata = transaction[1]
                verifyaddress = transaction_dict["sender_address"]
                if blockchain.verify_transaction_signature(verifyaddress,signdata, transaction_dict) == True:
                    transactionarray.append(transaction)
                else:
                    print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,transaction, "check failed")
                    continue
            transactionarray_receive.clear()
        if len(transactionarray) >3:# on block most have 50, for test 3, and the pow 1
            transactionarray.sort(key=lambda data: data[0]['value'], reverse=True)
        lock_transaction.release()
        time.sleep(2)


th = threading.Thread(target=start_misc)
th.setDaemon(True)
th.start()


if clientenable:
    from xmlrpc import client
    def startclient():
        while 1:
            if len(g_conndict) <3:
                i=0
                for item in blockchain.nodes.copy():
                    if i>2:
                        break
                    if item in g_connect_2_me:
                        continue
                    i+=1
                    g_conndict[item] = client.ServerProxy("http://"+item+":8088")
            time.sleep(0.1)
            print("\n\n")
            print("\033[31;42m")
            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"syncing blocks start........",g_conndict)
            for item,server in g_conndict.copy().items():
                print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"try to get blocks from http://"+item+":8088")
                # print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"server",server)
                try:
                    if (len(blockchain.nodes) < 5):
                        localnodelist=[localnode] + blockchain.nodes
                        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,localnodelist)
                        data = server.get_nodes(json.dumps(localnodelist))
                        # data = server.get_nodes(json.dumps(blockchain.nodes))
                        blockchain.nodes += json.loads(data)
                        blockchain.nodes = list(set(blockchain.nodes))
                        if localnode in blockchain.nodes:
                            blockchain.nodes.remove(localnode)
                        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"sync node from",item,"get", data,"and now", blockchain.nodes)
                    blocknumber = server.get_latest_blocknum()
                    diff = blocknumber - blockchain.latestblock['block_number']
                    if diff > 0:
                        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"sync from",item, diff,"blocks from", blockchain.latestblock['block_number'], blocknumber )
                        while diff:
                            # start to sync
                            blocknumber=blockchain.latestblock['block_number']+1
                            print("\n\n")
                            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"#######################start to sync block", blocknumber,"from",item)
                            data = server.get_fixed_block(blocknumber)
                            print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,"get data from",item, "data is:",data,"data type is:",type(data))
                            dataobj = json.loads(data)
                            print("\n\n")
                            ret = blockchain.check_syncblock(dataobj)
                            if (ret):
                                print(sys._getframe().f_code.co_name,sys._getframe().f_lineno, "sync",blocknumber,"from",item,"check failed", ret)
                                break
                            diff -= 1
                    elif diff == 0:
                        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,item, "same blocknumber", blocknumber, "no need to sync")
                    else:
                        print(sys._getframe().f_code.co_name,sys._getframe().f_lineno,item, "not have the latest blocknumber",blocknumber, "than mine",  blockchain.latestblock['block_number'])
                except:
                    if len(blockchain.nodes) > 3:
                        blockchain.nodes.remove(item)
                    server._ServerProxy__transport.close()
                    g_conndict.pop(item)
                    
                # server._ServerProxy__transport.close()
                print("\033[0m")
    th = threading.Thread(target=startclient)
    th.setDaemon(True)
    th.start()

time.sleep(3)

while 1:
    if blockchain.pow == 1:
        print("\n\n")
        print("\033[34;40m","==============================start a new workaround for pow==============================\n\n","\033[0m")
        # DB_STATUS.display()
        nonce,previous_hash,block_number = blockchain.proof_of_work()
        print("\033[34;40m","\n\n","\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,"get the nonce",nonce,"\033[0m")

        transaction = Transaction(sender_address=public1, sender_private_key=private1, recipient_address=public1, value=100)
        print("\033[34;40m","\n\n","\033[0m")
        print("\033[34;40m",sys._getframe().f_code.co_name,sys._getframe().f_lineno,"create the reward transaction",transaction.to_dict(),transaction.sign_transaction(),"\033[0m")
        pos_transaction = [[transaction.to_dict(),transaction.sign_transaction()]]


        blockchain.add_block(nonce, previous_hash, block_number, pos_transaction)
        print("\033[34;40m","\n\n","\033[0m")
        time.sleep(2)
    time.sleep(1)










