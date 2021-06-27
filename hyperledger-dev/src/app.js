/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Gateway, Wallets } = require('fabric-network');
const FabricCAServices = require('fabric-ca-client');
const path = require('path');
const { buildCAClient, registerAndEnrollUser, enrollAdmin } = require('../../test-application/javascript/CAUtil.js');
const { buildCCPOrg1, buildWallet } = require('../../test-application/javascript/AppUtil.js');

const channelName = 'mychannel';
const chaincodeName = 'basic';
const mspOrg1 = 'Org1MSP';
const walletPath = path.join(__dirname, 'wallet');
const org1UserId = 'appUser';

var new_accts = [
	{"first_name": "Jane", "last_name":"Doe", "acct_id": "0x9999", "balance":"50.00","registered": "false"},
	{"first_name": "Ihave", "last_name":"Nomoney", "acct_id": "0x1111", "balance":"5.00","registered": "false"}
];

function prettyJSONString(inputString) {
	return JSON.stringify(JSON.parse(inputString), null, 2);
}
async function main() {
	try {
		const ccp = buildCCPOrg1();
		const caClient = buildCAClient(FabricCAServices, ccp, 'ca.org1.example.com');
		const wallet = await buildWallet(Wallets, walletPath);
		await enrollAdmin(caClient, wallet, mspOrg1);
		await registerAndEnrollUser(caClient, wallet, mspOrg1, org1UserId, 'org1.department1');
		const gateway = new Gateway();

		try {
			await gateway.connect(ccp, {
				wallet,
				identity: org1UserId,
				discovery: { enabled: true, asLocalhost: true }
			});

			// Get our network and our contract
			const network = await gateway.getNetwork(channelName);
			const contract = network.getContract(chaincodeName);

			// InitLedger
			console.log('\n**********  InitLedger  **********');
			await contract.submitTransaction('InitLedger');

			// GetAllAccount
			console.log('\n**********  GetAllAccounts  **********');
			let result = await contract.evaluateTransaction('GetAllAccounts');
			console.log(`${prettyJSONString(result.toString())}`);

			// CreateAccount
			console.log('\n**********  CreateAccount JaneDoe **********');
			result = await contract.submitTransaction('CreateAccount', new_accts[0]["first_name"], new_accts[0]["last_name"], new_accts[0]["acct_id"], new_accts[0]["balance"], new_accts[0]["registered"]);
			if (`${result}` !== '') {
				console.log(`${prettyJSONString(result.toString())}`);
			}

			// Check that new account exists
			console.log('\n**********  AccountExists  **********');
			result = await contract.evaluateTransaction('AccountExists', '0x9999');
			if (result.toString() == 'true') {
				console.log(`The account was created successfully`)
			}			

			// CreateAccount IhaveNom
			console.log('\n**********  CreateAccount IhaveNomoney **********');
			result = await contract.submitTransaction('CreateAccount', new_accts[1]["first_name"], new_accts[1]["last_name"], new_accts[1]["acct_id"], new_accts[1]["balance"], new_accts[1]["registered"]);
			if (`${result}` !== '') {
				console.log(`${prettyJSONString(result.toString())}`);
			}

			// GetAllAccounts
			console.log('\n**********  GetAllAccounts  **********');
			result = await contract.evaluateTransaction('GetAllAccounts');
			console.log(`${prettyJSONString(result.toString())}`);
			
			// Register the Jane Doe account
			console.log('\n**********  RegisterAccount  **********');
			await contract.submitTransaction('RegisterAccount', new_accts[0]["first_name"], new_accts[0]["last_name"], new_accts[0]["acct_id"], new_accts[0]["balance"], new_accts[0]["registered"]);
			console.log(`Account successfully registered`)

			// ReadAccount to show changes and update our local account information
			console.log('\n**********  ReadAccount  **********');
			console.log(`Account after registration`)
			result = await contract.evaluateTransaction('ReadAccount', new_accts[0]["acct_id"]);
			new_accts[0] = JSON.parse(result.toString())
			console.log(`${prettyJSONString(result.toString())}`);
			
			// Register an already registered user
			try {
				console.log('\n**********  RegisterAccount  <Register for the 2nd time> **********');
				await contract.submitTransaction('RegisterAccount', new_accts[0]["first_name"], new_accts[0]["last_name"], new_accts[0]["acct_id"], new_accts[0]["balance"], new_accts[0]["registered"]);
				console.log(`Account successfully registered`)
			} catch (error) {
				console.log(error.toString())
			}
			
			// Register a user with insufficient funds
			try {
				console.log('\n**********  RegisterAccount  <Register with insufficient funds> **********');
				await contract.submitTransaction('RegisterAccount', new_accts[1]["first_name"], new_accts[1]["last_name"], new_accts[1]["acct_id"], new_accts[1]["balance"], new_accts[1]["registered"]);
				console.log(`Account successfully registered`)
			} catch (error) {
				console.log(error.toString())
			}

			// GetAllAccounts
			console.log('\n**********  GetAllAccounts  **********');
			result = await contract.evaluateTransaction('GetAllAccounts');
			console.log(`${prettyJSONString(result.toString())}`);

		} finally {
			gateway.disconnect();
		}
	} catch (error) {
		console.error(`******** FAILED to run the application: ${error}`);
	}
}

main();
