const registrar = artifacts.require("registration");

module.exports = async function(deployer) {
	await deployer.deploy(registrar)
};