package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"net/http"
	"strings"
)

const (
	// 为了举例的目的，暂时先写死，实际编码中不要写死
	Realm    = "myrealm"
	QOP      = "auth"
	Nonce    = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
	Opaque   = "5ccc069c403ebaf9f0171e9517f40e41"
	User     = "user1"
	Password = "mypassword"
)

func computeMD5Hash(text string) string {
	hasher := md5.New()
	io.WriteString(hasher, text)
	return fmt.Sprintf("%x", hasher.Sum(nil))
}

func parseAuthorizationHeader(header string) (username, realm, nonce, uri, qop, nc, cnonce, response string) {
	fields := strings.Split(header[6:], ", ")
	parts := make(map[string]string)
	for _, field := range fields {
		pair := strings.SplitN(field, "=", 2)
		if len(pair) == 2 {
			fmt.Println(strings.TrimSpace(pair[0]))
			parts[strings.TrimSpace(pair[0])] = strings.Trim(pair[1], `"`)
		}
	}
	return parts["username"], parts["realm"], parts["nonce"], parts["uri"], parts["qop"], parts["nc"], parts["cnonce"], parts["response"]
}

func checkAuth(r *http.Request) bool {
	authHeader := r.Header.Get("Authorization")
	if authHeader == "" {
		return false
	}
	username, realm, nonce, uri, qop, nc, cnonce, response := parseAuthorizationHeader(authHeader)
	// HA1 = MD5(username:realm:password)
	HA1 := computeMD5Hash(fmt.Sprintf("%s:%s:%s", username, realm, Password))
	// HA2 = MD5(method:digestURI)
	HA2 := computeMD5Hash(fmt.Sprintf("%s:%s", r.Method, uri))
	// response = MD5(HA1:nonce:nonceCount:cnonce:qop:HA2)
	validResponse := computeMD5Hash(fmt.Sprintf("%s:%s:%s:%s:%s:%s", HA1, nonce, nc, cnonce, qop, HA2))
	return response == validResponse
}

func protectedHandler(w http.ResponseWriter, r *http.Request) {
	if checkAuth(r) {
		w.Write([]byte("You're in the protected area"))
	} else {
		w.Header().Set("WWW-Authenticate", fmt.Sprintf(`Digest realm="%s", qop="%s", nonce="%s", opaque="%s"`, Realm, QOP, Nonce, Opaque))
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("401 Unauthorized\n"))
	}
}

func main() {
	http.HandleFunc("/protected", protectedHandler)
	http.ListenAndServe(":8080", nil)
}
