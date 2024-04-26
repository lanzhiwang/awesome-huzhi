package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"net/http"
)

const (
	Username = "user1"
	Password = "mypassword"
	Realm    = "myrealm"
	Nonce    = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
	NC       = "00000001"
	CNonce   = "0a4f113b"
	QOP      = "auth"
	URI      = "/protected"
	Method   = "GET"
)

func computeMD5Hash(text string) string {
	hasher := md5.New()
	io.WriteString(hasher, text)
	return fmt.Sprintf("%x", hasher.Sum(nil))
}

func createDigestAuthorizationHeader() string {
	// HA1 = MD5(username:realm:password)
	HA1 := computeMD5Hash(fmt.Sprintf("%s:%s:%s", Username, Realm, Password))
	// HA2 = MD5(method:URI)
	HA2 := computeMD5Hash(fmt.Sprintf("%s:%s", Method, URI))
	// response = MD5(HA1:nonce:NC:cnonce:qop:HA2)
	response := computeMD5Hash(fmt.Sprintf("%s:%s:%s:%s:%s:%s", HA1, Nonce, NC, CNonce, QOP, HA2))

	return fmt.Sprintf(`Digest username="%s", realm="%s", nonce="%s", uri="%s", qop=%s, nc=%s, cnonce="%s", response="%s", opaque=""`,
		Username, Realm, Nonce, URI, QOP, NC, CNonce, response)
}

func main() {
	client := &http.Client{}

	req, err := http.NewRequest(Method, "http://localhost:8080"+URI, nil)
	if err != nil {
		panic(err)
	}

	fmt.Println(createDigestAuthorizationHeader())

	req.Header.Set("Authorization", createDigestAuthorizationHeader())

	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		fmt.Println("Successfully authenticated.")
	} else {
		fmt.Println("Failed to authenticate.")
	}
}
