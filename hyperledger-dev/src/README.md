# Contract and Application Instructions

In this folder you will find both our Go smart contract, as well as our Node application script. For this exercise, we will be replacing the default contract and application script of the 'Basic' Hyperledger Fabric sample. This will use the test-network, allowing us to focus on the smart contract development and testing.

These scripts have to be moved to specific locations, so run the following commands to move them appropriately (Note: \<username\> should be the same username you used when creating the directory for the Hyperledger Installation):

```bash
mv app.js $HOME/go/src/github.com/<username>/fabric-samples/asset-transfer-basic/application-javascript/.

mv smartcontract.go $HOME/go/src/github.com/<username>/fabric-samples/asset-transfer-basic/chaincode-go/chaincode/.
```

Note that we are over writing the current app.js and smartcontract.go files which exist in this sample.

Once you have moved these files to their respective locations, follow the instructions in our utils/ folder to start the exercise!
