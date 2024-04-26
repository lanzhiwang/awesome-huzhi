package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
)

func ComputeHmac256(message string, secret string) string {
	key := []byte(secret)
	h := hmac.New(sha256.New, key)
	h.Write([]byte(message))
	return hex.EncodeToString(h.Sum(nil))
}

func VerifyHmac256(message, receivedHmac, secret string) bool {
	expectedHmac := ComputeHmac256(message, secret)
	return hmac.Equal([]byte(receivedHmac), []byte(expectedHmac))
}

func main() {
	secret := "luduoxin'blog"
	message := "Hello, HMAC!"

	// Sender computes HMAC
	hmac := ComputeHmac256(message, secret)
	fmt.Printf("Generated HMAC: %s\n", hmac)

	// Receiver verifies HMAC
	isValid := VerifyHmac256(message, hmac, secret)
	fmt.Printf("HMAC is valid: %v\n", isValid)
}
