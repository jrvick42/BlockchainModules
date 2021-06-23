import registration from '../abis/registration.json'
import React, { Component } from 'react';
import Web3 from 'web3';
import './App.css';

class App extends Component {

  async componentWillMount() {
    await this.loadBlockchainData(this.props.dispatch)
  }

  async loadBlockchainData(dispatch) {

    //check if MetaMask exists
    if (typeof window.ethereum !== 'undefined'){
      const web3 = new Web3(window.ethereum);
      const netId = await web3.eth.net.getId();
      const accounts = await web3.eth.getAccounts();
      console.log(accounts)
      console.log(netId)

      if (typeof accounts[0] !== 'undefined') {
        this.setState({account: accounts[0], web3: web3});
      }
      else {
        window.alert("Please log into MetaMask");
      }

      try {
        const addr = registration.networks[netId].address;
        const contract = new web3.eth.Contract(registration.abi, addr);
        console.log(addr);
        this.setState({contract: contract});
      }
      catch (e) {
        console.log('Error', e);
        window.alert("Contracts could not be deployed");
      }
      
    }
    else {
      window.alert("Please install MetaMask");
    }
  }

  // Functions to handle calls to the smart contract
  async register() {
    console.log("Register function has been triggered");
    const amount = 10e18;
    const msg = await this.state.contract.methods.payRegistration().send({value: amount.toString(), from: this.state.account})
    console.log(msg)

    document.getElementById("paybutton").disabled = true;
    document.getElementById("payDisplay").innerHTML = "Thanks for registering!"
  }

  async getAccountAddress() {
    const this_acct = this.state.account;
    document.getElementById("addrDisplay").innerHTML = this_acct;
  }

  constructor(props) {
    super(props)
    this.state = {
      web3: 'undefined',
      account: '',
      contract: null
    }
  }

  render() {
    return (
      <div>
        <div className="container-fluid mt-5 text-center">
        <br></br>
          <h1>Dapp Dev Registration Page</h1>
          <br></br>
          <div className="row">
            <main role="main" className="col-lg-12 d-flex text-center">
              <div className="content mr-auto ml-auto">
              <div>
                  <br></br>
                  Verify your Account
                  <br></br>
                  <form onSubmit={(e) => {
                    e.preventDefault()
                    this.getAccountAddress()
                    }}>
                    <button type="submit" className="btn btn-primary">Verify Account</button>
                  </form>
                  <br></br>
                  <h3 id="addrDisplay"></h3>
                </div>
                <br></br>
                <div>
                  <br></br>
                  Click to pay registration fee!
                  <br></br>
                  <form onSubmit={(e) => {
                    e.preventDefault()
                    this.register()
                    }}>
                    <button id="paybutton" type="submit" className="btn btn-primary">Pay Now</button>
                  </form>
                  <br></br>
                  <h3 id="payDisplay"></h3>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>
    );
  }
}

export default App;