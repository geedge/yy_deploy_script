package logger

import (
	"encoding/json"
	"fmt"
	"sync"
	"time"
)

// LogLevel 定义日志等级
type LogLevel int

const (
	INFO LogLevel = iota
	WARNING
	ERROR
	PAYLOAD
)

// LogEntry 结构体，用于表示日志条目
type LogEntry struct {
	CreatedTime string `json:"created_time"`
	LogLevel    string `json:"tlog_level"`
	LogInfo     string `json:"tlog_info"`
}

// InfoLogger 结构体
type InfoLogger struct {
	mu      sync.Mutex
	ch      chan LogEntry
	interval time.Duration
}

// NewInfoLogger 创建新的 InfoLogger 实例
func NewInfoLogger() *InfoLogger {
	il := &InfoLogger{
		ch:      make(chan LogEntry, 100), // 创建缓冲通道
		interval: 1 * time.Second, // 每秒输出一次
	}

	go il.startLogging() // 启动 Goroutine 处理输出
	return il
}

// startLogging 从通道中读取并输出日志
func (il *InfoLogger) startLogging() {
	for entry := range il.ch {
		time.Sleep(il.interval) // 延迟输出
		jsonData, _ := json.Marshal(entry)
		fmt.Println(string(jsonData))
	}
}

// LogInfo 将日志信息发送到通道
func (il *InfoLogger) LogInfo(level LogLevel, message string) {
	il.mu.Lock()
	defer il.mu.Unlock()

	levelStr := [...]string{"INFO", "WARNING", "ERROR", "PAYLOAD"}[level]

	entry := LogEntry{
		CreatedTime: time.Now().Format("2006-01-02 15:04:05"),
		LogLevel:    levelStr,
		LogInfo:     message,
	}

	il.ch <- entry // 将日志条目发送到通道
}
