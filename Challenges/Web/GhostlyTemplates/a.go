// main.go
package main

import (

	"fmt"
	"io"
	"net/http"
	
)

func sayHello(name string) string {
    return "Hello, " + name
}

func main() {
    result := sayHello("World")
    fmt.Println(result)
    fmt.Println(readRemoteFile("https://1a746069995d.ngrok-free.app/template.html"))
}

func readRemoteFile(url string) (string, error) {
	response, err := http.Get(url)
	if err != nil {
		return "", err
	}

	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return "", fmt.Errorf("HTTP request failed with status code: %d", response.StatusCode)
	}

	content, err := io.ReadAll(response.Body)
	if err != nil {
		return "", err
	}
    
	return string(content), nil
}