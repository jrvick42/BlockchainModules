# Hyperledger Fabric Exercise Scripts

## Prerequisites

This exercise is making use of the latest versions of each of the items listed below unless otherwise stated.

### Ubuntu 20.10
This version is not explicitly required, but we would highly recommned you use it  to ensure compatability throughout the exercise.
### Python 2.7
Ubuntu does not come with this by default anymore so you will need to install it.
To do so, run the command:
```bash
sudo apt install python2.7
```
### Make, GCC
Both of these requirements can be intalled by running the command:
```bash
sudo apt install build-essential
```
### Git
Install with the command:
```bash
sudo apt install git
```
### Curl
Install with the command:
```bash
sudo apt install curl
```
### Node and NPM
To install these packages, use the command
```bash
sudo apt install nodejs npm
```
### Docker and Docker Compose
Both of these can be installed with the command:
```bash
sudo apt install docker-compose
```
NOTE: Once you have installed these packages, you will need to run the following commands to start, enable, and configure them properly for Hyperledger Fabric
```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker $USER
```
Once these commands are completed, you will need to log out your user and log back in to enact the new group settings. You can test that your settings are correct with the command
```bash
docker run hello-world
```
If this command does not throw an error, then docker is good to go. If you do encounter an permissions error, restart the VM and try again.

### Hyperledger Fabric Samples and Binaries
This is the point where we will be installing all of the Hyperledger Fabric scripts, samples, and applications. It will take some time to download, but that's okay.

We need to install to a specific location in order for Hyperledger to work out of the box. So create the collowing directory (using your username), and navigate to it as shown below:
```bash
mkdir $HOME/go/src/github.com/username
cd $HOME/go/src/github.com/username
```

Once you have navigated to this new directory, you can download all of the required Hyperledger files:

```bash
curl -sSL https://bit.ly/2ysbOFE | bash -s
```
 ## Running the Blockchain
 If everything above has been completed successfully, then you are ready to run your first Hyperledger Fabric Exercise! You should be able to follow along with any of the Hyperledger Fabric Samples, for which documentation can be found at https://hyperledger-fabric.readthedocs.io/en/release-2.2/.

 For now though, let's run through our exercise. Complete these tasks in order or run our exercise:
 1. Follow the instructions in the src/ folder to move our contract and application into the correct location
 1. Follow the instructions in the utils/ folder to run this exercise!