# C-lightning Plugin

### c-lightning node setup
#### Download c-lightning repository
```shell
git clone https://github.com/ElementsProject/lightning
```
#### Installation instructions for Ubuntu:
```shell
sudo apt-get install -y software-properties-common
sudo add-apt-repository -u ppa:bitcoin/bitcoin
sudo add-apt-repository -u ppa:lightningnetwork/ppa
sudo apt-get install bitcoind lightningd
```
#### Setup regtest with two lighting nodes, more details in script
```shell
source contrib/startup_regtest.sh
```
#### Start two local nodes with bitcoind, all running on regtest
```shell
start_ln
```
#### Generate client's address
```shell
address=$(l1-cli newaddr| jq -r '.address')
```
#### Mine 101 blocks and payout to the client's address
```shell
bt-cli generatetoaddress 101 $address
```
#### Create transaction between two lightning nodes using RPC methods plugins added to lightningd
```shell
./main.py
```
