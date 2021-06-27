package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

// Account Struct and Attributes
type Account struct {
	First_name string  `json:"first_name"`
	Last_name  string  `json:"last_name"`
	Acct_id    string  `json:"acct_id"`
	Balance    float64 `json:"balance"`
	Registered bool    `json:"registered"`
}

// InitLedger : Start the ledger with the specified data
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	assets := []Account{
		{First_name: "John", Last_name: "Doe", Acct_id: "0x1234", Balance: 100.00, Registered: false},
	}

	for _, acct_data := range assets {
		acct_data_json, err := json.Marshal(acct_data)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(acct_data.Acct_id, acct_data_json)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %v", err)
		}
	}

	return nil
}

// CreateAccount : Creates a new account and writes to world state
func (s *SmartContract) CreateAccount(ctx contractapi.TransactionContextInterface, fname string, lname string, id string, balance float64, registered bool) error {
	exists, err := s.AccountExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

	asset := Account{
		First_name: fname,
		Last_name:  lname,
		Acct_id:    id,
		Balance:    balance,
		Registered: registered,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// ReadAccount : Returns account from world state with specified id
func (s *SmartContract) ReadAccount(ctx contractapi.TransactionContextInterface, id string) (*Account, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Account
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// RegisterAccount : Checks that the user is capable of registration and updates the account accordingly
func (s *SmartContract) RegisterAccount(ctx contractapi.TransactionContextInterface, fname string, lname string, id string, balance float64, registered bool) error {
	exists, err := s.AccountExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	if registered == true {
		return fmt.Errorf("The account is already registered. No need to register again...")
	}

	if balance < 10.00 {
		return fmt.Errorf("the account does not have sufficient funds to register\nRequired: 10.00\nBalance: %f", balance)
	}

	// overwriting original asset with new asset
	acct := Account{
		First_name: fname,
		Last_name:  lname,
		Acct_id:    id,
		Balance:    balance - 10.00,
		Registered: true,
	}
	acctJSON, err := json.Marshal(acct)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, acctJSON)
}

// AccountExists : Returns whether the account is in the world state or not
func (s *SmartContract) AccountExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// GetAllAccounts : Returns all accounts in world state
func (s *SmartContract) GetAllAccounts(ctx contractapi.TransactionContextInterface) ([]*Account, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Account
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Account
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}
