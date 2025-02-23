1. os , software requrement

ubuntu 20
python3
vscode
virtual machine manage
qemu
qcow2 100G

2. python

 sudo apt install python3-pip
 pip3 install pycryptodome
 pip3 install leveldb

3. 4 vms nat communication between each other

192.168.122.60
192.168.122.61
192.168.122.62
192.168.122.63


4. rm block/ status -rf ;reset ; python3 bc.py 0 to 60 to start 60 node
use python3 bc.py 0, the last parameter means
0 is for 192.168.122.60 works as server first start
to mine some blocks.

and 1 is for 192.168.122.61
and 2 is for 192.168.122.62
and 3 is for 192.168.122.63
use 0 1 2 3 to assign different public key and private key


5. put the develop rsa.pub to 4 vm nodes

after change code , use scp -r ../bc ubuntu@192.168.122.6*

6. use sha to get the hash of receive address , sender address and send value,
 rsa private key to sign the digest.

7. use sha to get the hash of receive address , sender address and send value,
 use rsa pulic key to verify the sinature.

8.  rpc thread for local or remote managemant, server thread is used for others to
pull blocks, client(sync thread) to pull node to the latest
block . pow thread.

9.
python3 query.py

new_wallet , get_latest_blocknum , get_balance , set_balance , get_latestblock , get_fixed_block , get_nodes
Prompt> new_wallet
{"private_key": "3082025c02010002818100e20d8883582f1bb9238f0aa2034ca5b27737bdb60250f4e019b6969f37404a8684b3d826d57261429fb4b429ed03857e6eb90db7d969c9ee2decf54c0bd0abad62ab5881ae9200015bf321642e39b00cf9f8250373088ee425c41e06a4f1dcb6646bf71e21de7df2eeabfd8c194b9fcc045762604a87994522c41adca9e2dd0502030100010281800b604ca54b86a76459abefb2e2969f64cc0779467e77038929a772376b5e3d6c92a36db6854469d7a2ab9896343adaa3826aa6b6eb669db11d0ce6a00a9cd8498675a0c035dc71797bb3ccb93a3d9ecf0e230cffc567f9a88cf0cae4af4468782d9844b8f827b9fa8bd6ac3e646d32f3a118dedd1e63705660c892d36e93502b024100e9265d27a6949f0f70ea00354d9a411f3eeac43b710217764fa03c1e6d3c9270cb0f0bcc068a9fa47d16652339c1917908004c4d83d4dbaedba06b189873f9e7024100f8351bcf15b0c4c8115b807f3a8b0aa4f449b757146d7cd5a190c81d10489456e73166f2fb3add5de41eb095381bb79c7ffb57ff9c5057534f2d3cf796bccc3302405ada2a3ec338f2ea8f737ff5457230a23e60396b7853fa548e1ec08e92bea1c9f636bcc01a64766520a15373f093af5e5c71d149fb6f3cd3dc9d9c5e0f3a524d024100bfe206daa45120ffee7347b69422b39aec8424a9bc501c66e75d8f66f094bba1276048cf65ab8f412bbf121279eaeb9aa052462884c6938c0334dce22775538302404e5eaeb9d5bc05787cad183b0e256cdaf22f6ea3b8d8e256dcbf044467aeeaa3a7b87ab43e5e81b05d779168c2587d954add34273fad0b6b73a3849ab5b6e86c", "public_key": "30819f300d06092a864886f70d010101050003818d0030818902818100e20d8883582f1bb9238f0aa2034ca5b27737bdb60250f4e019b6969f37404a8684b3d826d57261429fb4b429ed03857e6eb90db7d969c9ee2decf54c0bd0abad62ab5881ae9200015bf321642e39b00cf9f8250373088ee425c41e06a4f1dcb6646bf71e21de7df2eeabfd8c194b9fcc045762604a87994522c41adca9e2dd050203010001"}


new_wallet , get_latest_blocknum , get_balance , set_balance , get_latestblock , get_fixed_block , get_nodes
Prompt> get_latest_blocknum
17

