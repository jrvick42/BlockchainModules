# Golang Examples

## Prerequisites
You need only ensure that Golang in properly installed on your machine.
The following steps detail this process for an Ubuntu 20.10 Virtual Machine:
1. Download the appropriate Golang tar using curl
    ```bash
    curl -O https://storage.googleapis.com/golang/go1.16.5.linux-amd64.tar.gz
    ```
    Note here that 1.16.5 is the latest stable version at the time of writing, but you
    can replace this with any other available version should you need to
1. Extract the contents of the downloaded file into a new directory (go/)
    ```bash
    tar -xvf go1.16.5.linux-amd64.tar.gz go/
    ```
1. Move this new directory to the /usr/local directory
    ```bash
    sudo mv go /usr/local
    ```
1. Add the location of the golang binary to your path
    Append the following line to the end of your ~/.profile file:
    "export PATH=$PATH:/usr/local/go/bin"
    Now to enact this change, run the command:
    ```bash
    source ~/.profile
    ```

## Verify Installation
At this piont Golang should be installed and operational.
You can check this by running this command in your terminal now:
```bash
go version
```
This should simply display the currently installed version of Golang

If this command is successful, then you are good to go!