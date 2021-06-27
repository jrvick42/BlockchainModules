#!/bin/bash

cd test-network

# Ensure the network is turned off
./network.sh down

# Enable the network
./network.sh up createChannel -c mychannel -ca

# Deploy the Golang chaincode
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go/ -ccl go
