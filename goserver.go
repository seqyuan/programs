package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
)

func main() {
	flag.Parse()
	pwd, _ := os.Getwd()

	port := 8090
	path := pwd
	switch len(flag.Args()) {
	case 0:
		fmt.Println("usage:\n\tgoserver <port> <path>\n\t          port default:8090, path default:$pwd\n\tgoserver 8090 ./\n\tgoserver 8090")
	case 1:
		port, _ = strconv.Atoi(os.Args[1])
	case 2:
		port, _ = strconv.Atoi(os.Args[1])
		path, _ = filepath.Abs(os.Args[2])
	}

	http.ListenAndServe(fmt.Sprintf(":%v", port), http.FileServer(http.Dir(path)))
}
