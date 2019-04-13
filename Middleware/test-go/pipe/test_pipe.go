package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"syscall"
	"time"
)

var pipeFile = "pipe.log"

func main() {
	os.Remove(pipeFile)
	err := syscall.Mkfifo(pipeFile, 0666)
	if err != nil {
		log.Fatal("Make named pipe file error:", err)
	}
	go scheduleWrite()
	fmt.Println("open a named pipe file for read.")
	file, err := os.OpenFile(pipeFile, os.O_CREATE, os.ModeNamedPipe)
	if err != nil {
		log.Fatal("Open named pipe file error:", err)
	}

	reader := bufio.NewReader(file)

	for {
		line, err := reader.ReadBytes('\n')
		if err == nil {
			fmt.Print("load string:" + string(line))
		}
	}
}

func scheduleWrite() {
	fmt.Println("start schedule writing.")
	f, err := os.OpenFile(pipeFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0777)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	i := 0
	for {
		fmt.Println("write string to named pipe file.")
		f.WriteString(fmt.Sprintf("test write times:%d\n", i))
		i++
		time.Sleep(time.Second)
	}
}

/* Test result */
/*================================
go run pipe.go
open a named pipe file for read.
start schedule writing.
write string to named pipe file.
load string:test write times:0
write string to named pipe file.
load string:test write times:1
write string to named pipe file.
load string:test write times:2
=================================*/
