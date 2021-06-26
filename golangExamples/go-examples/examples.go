package main

import (
	"errors"
	"fmt"
)

// Add two integers and display the results
func addIntegers() {
	var a int = 10
	var b int = 5
	var c int = a + b
	fmt.Printf("Sum of %d and %d: %d\n", a, b, c)
}

// Add two floats and display the results
func addFloats() {
	var a float64 = 10.0
	var b float64 = 5.5
	var c float64 = a + b
	fmt.Printf("Sum of %f and %f: %f\n", a, b, c)
}

// If/Else Conditional
func ifelse(v bool) {
	if v == true {
		fmt.Printf("Your parameter was 'true'\n")
	} else if v == false {
		fmt.Printf("Your parameter was 'false'\n")
	}
}

func forLoop(iters int) {
	fmt.Printf("For Loop Begin\n")
	for i := 0; i <= iters; i++ {
		fmt.Printf("  Iteration %d\n", i)
	}
	fmt.Printf("For Loop End\n")
}

// 1 and 2 dimensional arrays
func arrays() {
	var arr [5]int
	fmt.Println("arr: ", arr)

	arr[0] = 1
	fmt.Println("arr: ", arr)

	fmt.Printf("arr length: %d\n", len(arr))

	var matrix [3][3]int
	count := 0
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			matrix[i][j] = count
			count++
		}
	}
	fmt.Println("Matrix:", matrix)

}

// Working with maps (key:value datatype)
func maps() {
	// we can make an empty map
	mymap := make(map[string]int)
	fmt.Println("MyMap: ", mymap)

	mymap["element1"] = 1
	fmt.Println("MyMap: ", mymap)

	mymap["element2"] = 2
	mymap["element3"] = 3
	mymap["element4"] = 4
	mymap["element5"] = 5

	element := mymap["element4"]
	fmt.Printf("Element 4 : %d\n", element)
}

func structs() {
	type account struct {
		owner   string
		balance float64
	}

	admin_acct := account{"Admin", 19.99}
	fmt.Println("admin_acct Struct  : ", admin_acct)
	fmt.Println("admin_acct.owner   : ", admin_acct.owner)
	fmt.Println("admin_acct.balance : ", admin_acct.balance)

}

// Returning Errors
func errorHandling(v bool) (int, error) {
	if v == true {
		return -1, errors.New("You asked for this 'error'")
	} else {
		return -1, errors.New("You didnt ask for it but here's an 'error' anyway")
	}
}

func main() {
	addIntegers()
	addFloats()

	const v bool = true
	ifelse(v)

	const i int = 5
	forLoop(i)

	arrays()

	maps()

	structs()

	ret, err := errorHandling(true)
	fmt.Printf("Return Value  : %d\n", ret)
	fmt.Println("Error Message :", err)

}
