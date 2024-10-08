package main

import (
	"os"
	"output/logger"
  "time"
)

func main() {
	log := logger.NewInfoLogger()

	// 命令行参数：日志类型 日志内容
	switch os.Args[1] {
	case "PAYLOAD":
		log.LogInfo(logger.PAYLOAD, os.Args[2])
	case "INFO":
		log.LogInfo(logger.INFO, os.Args[2])
	case "ERROR":
		log.LogInfo(logger.ERROR, os.Args[2])
	default:
		log.LogInfo(logger.ERROR, "Error Output Arguments.")
	}
  time.Sleep(10 * time.Second)
  
	// Test
	// log.LogInfo(logger.INFO, "testinfo")
	// time.Sleep(5 * time.Millisecond)
}
