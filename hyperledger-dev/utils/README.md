# Running the Exercise

In this folder you will see two helper scripts. Each of which is intended to ease the process of starting the exercise, especially during development when you may be doing so many times in a row.

### runNetwork.sh
This script handles the creation and deployment of our network and chaincode.

### runApp.sh
This script starts our application which will interact with the newly operational network and blockchain.

## Starting the Exercise
Before you begin, these scripts need to be moved into the fabric-samples directory. Using the same \<username\> from earlier, run the following command:

```bash
cp run* $HOME/go/src/github.com/<username>/fabric-samples/
```

Now navigate to this fabric-samples directory and you should now see the scripts in place. Great! We can now run the exercise!

First start the network:
```bash
./runNetwork.sh
```
This will take a minute, there is a lot going on behind the scenes! The entire network is being generated. Peers, Organizations, channels, and everything else discussed in the write up are all being instantiated. After a few moments, the network should be up and running, and the chaincode should be deoployed and ready to go!

Now, we can run the application to test out our smart contract. Open up another tab in this directory and run the command:
```bash
./runApp.sh
```
 This won't take nearly as long to run, but look through the output and you will see that we have initialized a ledger, written to, and read from the blockchain! If all goes according to plan, you should also see some errors which have been thrown on purpose!

 ## Restarting the Exercise
 If you need to re-run the experiment after making any changes to either the application or the smart contract, just run runNetwork.sh and runApp.sh again (in that order), and the whole process will restart!
