## HTTPie And Curl

### HTTPie Install

```bash
# 基于 Debian Linux 的构建版，比如 Ubuntu
apt-get install httpie

# 基于 RPM Linux 的构建版
yum install httpie				
```



### http 使用示例

```bash
# METHOD
http GET
http POST
http PUT
http DELETE

# => GET
$ http example.org
# => POST
$ http example.org hello=world  

# => http://localhost:3000
$ http :3000  
# => http://localhost/foo
$ http :/foo  

# headers  :
$ http http://httpie.org  Cookie:foo=bar  User-Agent:bacon/1.0  

# http://httpie.org?search=httpie  == 
$ http http://httpie.org  search==httpie  

# json post  =  =@ 默认使用json格式
$ http --json POST http://httpie.org name=HTTPie language=Python description='CLI HTTP client'
$ http --form POST http://httpie.org name=HTTPie language=Python description='CLI HTTP client'  # 也可以使用form格式
$ http --json POST http://httpie.org essay=@Documents/essay.txt

# json post  := :=@
$ http --json POST http://httpie.org awesome:=true amount:=42 colors:='["red", "green", "blue"]' 
$ http --json POST http://httpie.org package:=@./package.json

# file upload  @ 只能使用form格式
$ http --form POST http://httpie.org cs@~/Documents/CV.pdf

```



### http help

```bash
$ http --help
usage: http [--json] [--form] [--pretty {all,colors,format,none}]
            [--style STYLE] [--print WHAT] [--verbose] [--headers] [--body]
            [--stream] [--output FILE] [--download] [--continue]
            [--session SESSION_NAME_OR_PATH | --session-read-only SESSION_NAME_OR_PATH]
            [--auth USER[:PASS]] [--auth-type {basic,digest}]
            [--proxy PROTOCOL:PROXY_URL] [--follow] [--verify VERIFY]
            [--cert CERT] [--cert-key CERT_KEY] [--timeout SECONDS]
            [--check-status] [--ignore-stdin] [--help] [--version]
            [--traceback] [--debug]
            [METHOD] URL [REQUEST_ITEM [REQUEST_ITEM ...]]

HTTPie - a CLI, cURL-like tool for humans. <http://httpie.org>

Positional Arguments:
  
  These arguments come after any flags and in the order they are listed here.
  Only URL is required.
  

  METHOD
      The HTTP method to be used for the request (GET, POST, PUT, DELETE, ...).
      
      This argument can be omitted in which case HTTPie will use POST if there
      is some data to be sent, otherwise GET:
      
          $ http example.org               # => GET
          $ http example.org hello=world   # => POST
      
  URL
      The scheme defaults to 'http://' if the URL does not include one.
      
      You can also use a shorthand for localhost
      
          $ http :3000                    # => http://localhost:3000
          $ http :/foo                    # => http://localhost/foo
      
  REQUEST_ITEM
      Optional key-value pairs to be included in the request. The separator used
      determines the type:
      
      ':' HTTP headers:
      
          Referer:http://httpie.org  Cookie:foo=bar  User-Agent:bacon/1.0
      
      '==' URL parameters to be appended to the request URI:
      
          search==httpie
      
      '=' Data fields to be serialized into a JSON object (with --json, -j)
          or form data (with --form, -f):
      
          name=HTTPie  language=Python  description='CLI HTTP client'
      
      ':=' Non-string JSON data fields (only with --json, -j):
      
          awesome:=true  amount:=42  colors:='["red", "green", "blue"]'
      
      '@' Form file fields (only with --form, -f):
      
          cs@~/Documents/CV.pdf
      
      '=@' A data field like '=', but takes a file path and embeds its content:
      
           essay=@Documents/essay.txt
      
      ':=@' A raw JSON field like ':=', but takes a file path and embeds its content:
      
          package:=@./package.json
      
      You can use a backslash to escape a colliding separator in the field name:
      
          field-name-with\:colon=value
      

Predefined Content Types:
  --json, -j
      (default) Data items from the command line are serialized as a JSON object.
      The Content-Type and Accept headers are set to application/json
      (if not specified).
      
  --form, -f
      Data items from the command line are serialized as form fields.
      
      The Content-Type is set to application/x-www-form-urlencoded (if not
      specified). The presence of any file fields results in a
      multipart/form-data request.
      

Output Processing:
  --pretty {all,colors,format,none}
      Controls output processing. The value can be "none" to not prettify
      the output (default for redirected output), "all" to apply both colors
      and formatting (default for terminal output), "colors", or "format".
      
  --style STYLE, -s STYLE
      Output coloring style (default is "solarized"). One of:
      
          algol, algol_nu, autumn, borland, bw, colorful, default,
          emacs, friendly, fruity, igor, lovelace, manni, monokai,
          murphy, native, paraiso-dark, paraiso-light, pastie,
          perldoc, rrt, solarized, tango, trac, vim, vs, xcode
      
      For this option to work properly, please make sure that the $TERM
      environment variable is set to "xterm-256color" or similar
      (e.g., via `export TERM=xterm-256color' in your ~/.bashrc).
      

Output Options:
  --print WHAT, -p WHAT
      String specifying what the output should contain:
      
          'H' request headers
          'B' request body
          'h' response headers
          'b' response body
      
      The default behaviour is 'hb' (i.e., the response headers and body
      is printed), if standard output is not redirected. If the output is piped
      to another program or to a file, then only the response body is printed
      by default.
      
  --verbose, -v
      Print the whole request as well as the response. Shortcut for --print=HBbh.
      
  --headers, -h
      Print only the response headers. Shortcut for --print=h.
      
  --body, -b
      Print only the response body. Shortcut for --print=b.
      
  --stream, -S
      Always stream the output by line, i.e., behave like `tail -f'.
      
      Without --stream and with --pretty (either set or implied),
      HTTPie fetches the whole response before it outputs the processed data.
      
      Set this option when you want to continuously display a prettified
      long-lived response, such as one from the Twitter streaming API.
      
      It is useful also without --pretty: It ensures that the output is flushed
      more often and in smaller chunks.
      
  --output FILE, -o FILE
      Save output to FILE. If --download is set, then only the response body is
      saved to the file. Other parts of the HTTP exchange are printed to stderr.
      
  --download, -d
      Do not print the response body to stdout. Rather, download it and store it
      in a file. The filename is guessed unless specified with --output
      [filename]. This action is similar to the default behaviour of wget.
      
  --continue, -c
      Resume an interrupted download. Note that the --output option needs to be
      specified as well.
      

Sessions:
  --session SESSION_NAME_OR_PATH
      Create, or reuse and update a session. Within a session, custom headers,
      auth credential, as well as any cookies sent by the server persist between
      requests.
      
      Session files are stored in:
      
          /home/lanzhiwang/.httpie/sessions/<HOST>/<SESSION_NAME>.json.
      
  --session-read-only SESSION_NAME_OR_PATH
      Create or read a session without updating it form the request/response
      exchange.
      

Authentication:
  --auth USER[:PASS], -a USER[:PASS]
      If only the username is provided (-a username), HTTPie will prompt
      for the password.
      
  --auth-type {basic,digest}
      The authentication mechanism to be used. Defaults to "basic".
      
      "basic": Basic HTTP auth
      "digest": Digest HTTP auth
      

Network:
  --proxy PROTOCOL:PROXY_URL
      String mapping protocol to the URL of the proxy
      (e.g. http:http://foo.bar:3128). You can specify multiple proxies with
      different protocols.
      
  --follow
      Set this flag if full redirects are allowed (e.g. re-POST-ing of data at
      new Location).
      
  --verify VERIFY
      Set to "no" to skip checking the host's SSL certificate. You can also pass
      the path to a CA_BUNDLE file for private certs. You can also set the
      REQUESTS_CA_BUNDLE environment variable. Defaults to "yes".
      
  --cert CERT
      You can specify a local cert to use as client side SSL certificate.
      This file may either contain both private key and certificate or you may
      specify --cert-key separately.
      
  --cert-key CERT_KEY
      The private key to use with SSL. Only needed if --cert is given and the
      certificate file does not contain the private key.
      
  --timeout SECONDS
      The connection timeout of the request in seconds. The default value is
      30 seconds.
      
  --check-status
      By default, HTTPie exits with 0 when no network or other fatal errors
      occur. This flag instructs HTTPie to also check the HTTP status code and
      exit with an error if the status indicates one.
      
      When the server replies with a 4xx (Client Error) or 5xx (Server Error)
      status code, HTTPie exits with 4 or 5 respectively. If the response is a
      3xx (Redirect) and --follow hasn't been set, then the exit status is 3.
      Also an error message is written to stderr if stdout is redirected.
      

Troubleshooting:
  --ignore-stdin
      Do not attempt to read stdin.
      
  --help
      Show this help message and exit.
      
  --version
      Show version and exit.
      
  --traceback
      Prints exception traceback should one occur.
      
  --debug
      Prints exception traceback should one occur, and also other information
      that is useful for debugging HTTPie itself and for reporting bugs.
      

For every --OPTION there is also a --no-OPTION that reverts OPTION
to its default value.

Suggestions and bug reports are greatly appreciated:

    https://github.com/jakubroztocil/httpie/issues


```



[参考](https://keelii.com/2018/09/03/HTTPie/)



### Curl 使用示例

```bash
curl localhost

# Download a single file
curl http://path.to.the/file

# Download a file and specify a new filename
curl http://example.com/file.zip -o new_file.zip

# Download multiple files
curl -O URLOfFirstFile -O URLOfSecondFile

# Download all sequentially numbered files (1-24)
curl http://example.com/pic[1-24].jpg

# Download a file and follow redirects
curl -L http://example.com/file

# Download a file and pass HTTP Authentication
curl -u username:password URL 

# Download a file with a Proxy
curl -x proxysever.server.com:PORT http://addressiwantto.access

# Download a file from FTP
curl -u username:password -O ftp://example.com/pub/file.zip

# Get an FTP directory listing
curl ftp://username:password@example.com

# Resume a previously failed download
curl -C - -o partial_file.zip http://example.com/file.zip

# Fetch only the HTTP headers from a response
curl -I http://example.com

# Fetch your external IP and network info as JSON
curl http://ifconfig.me/all/json

# Limit the rate of a download
curl --limit-rate 1000B -O http://path.to.the/file

# POST to a form
curl -F "name=user" -F "password=test" http://example.com

# POST JSON Data
curl -H "Content-Type: application/json" -X POST -d '{"user":"bob","pass":"123"}' http://example.com

# POST data from the standard in / share data on sprunge.us
curl -F 'sprunge=<-' sprunge.us


```



### curl help

```bash
lanzhiwang@lanzhiwang-desktop:~/work$ curl --help
Usage: curl [options...] <url>
Options: (H) means HTTP/HTTPS only, (F) means FTP only
     --anyauth       Pick "any" authentication method (H)
 -a, --append        Append to target file when uploading (F/SFTP)
     --basic         Use HTTP Basic Authentication (H)
     --cacert FILE   CA certificate to verify peer against (SSL)
     --capath DIR    CA directory to verify peer against (SSL)
 -E, --cert CERT[:PASSWD]  Client certificate file and password (SSL)
     --cert-status   Verify the status of the server certificate (SSL)
     --cert-type TYPE  Certificate file type (DER/PEM/ENG) (SSL)
     --ciphers LIST  SSL ciphers to use (SSL)
     --compressed    Request compressed response (using deflate or gzip)
 -K, --config FILE   Read config from FILE
     --connect-timeout SECONDS  Maximum time allowed for connection
 -C, --continue-at OFFSET  Resumed transfer OFFSET
 -b, --cookie STRING/FILE  Read cookies from STRING/FILE (H)
 -c, --cookie-jar FILE  Write cookies to FILE after operation (H)
     --create-dirs   Create necessary local directory hierarchy
     --crlf          Convert LF to CRLF in upload
     --crlfile FILE  Get a CRL list in PEM format from the given file
 -d, --data DATA     HTTP POST data (H)
     --data-raw DATA  HTTP POST data, '@' allowed (H)
     --data-ascii DATA  HTTP POST ASCII data (H)
     --data-binary DATA  HTTP POST binary data (H)
     --data-urlencode DATA  HTTP POST data url encoded (H)
     --delegation STRING  GSS-API delegation permission
     --digest        Use HTTP Digest Authentication (H)
     --disable-eprt  Inhibit using EPRT or LPRT (F)
     --disable-epsv  Inhibit using EPSV (F)
     --dns-servers   DNS server addrs to use: 1.1.1.1;2.2.2.2
     --dns-interface  Interface to use for DNS requests
     --dns-ipv4-addr  IPv4 address to use for DNS requests, dot notation
     --dns-ipv6-addr  IPv6 address to use for DNS requests, dot notation
 -D, --dump-header FILE  Write the headers to FILE
     --egd-file FILE  EGD socket path for random data (SSL)
     --engine ENGINE  Crypto engine (use "--engine list" for list) (SSL)
     --expect100-timeout SECONDS How long to wait for 100-continue (H)
 -f, --fail          Fail silently (no output at all) on HTTP errors (H)
     --false-start   Enable TLS False Start.
 -F, --form CONTENT  Specify HTTP multipart POST data (H)
     --form-string STRING  Specify HTTP multipart POST data (H)
     --ftp-account DATA  Account data string (F)
     --ftp-alternative-to-user COMMAND  String to replace "USER [name]" (F)
     --ftp-create-dirs  Create the remote dirs if not present (F)
     --ftp-method [MULTICWD/NOCWD/SINGLECWD]  Control CWD usage (F)
     --ftp-pasv      Use PASV/EPSV instead of PORT (F)
 -P, --ftp-port ADR  Use PORT with given address instead of PASV (F)
     --ftp-skip-pasv-ip  Skip the IP address for PASV (F)
     --ftp-pret      Send PRET before PASV (for drftpd) (F)
     --ftp-ssl-ccc   Send CCC after authenticating (F)
     --ftp-ssl-ccc-mode ACTIVE/PASSIVE  Set CCC mode (F)
     --ftp-ssl-control  Require SSL/TLS for FTP login, clear for transfer (F)
 -G, --get           Send the -d data with a HTTP GET (H)
 -g, --globoff       Disable URL sequences and ranges using {} and []
 -H, --header LINE   Pass custom header LINE to server (H)
 -I, --head          Show document info only
 -h, --help          This help text
     --hostpubmd5 MD5  Hex-encoded MD5 string of the host public key. (SSH)
 -0, --http1.0       Use HTTP 1.0 (H)
     --http1.1       Use HTTP 1.1 (H)
     --http2         Use HTTP 2 (H)
     --ignore-content-length  Ignore the HTTP Content-Length header
 -i, --include       Include protocol headers in the output (H/F)
 -k, --insecure      Allow connections to SSL sites without certs (H)
     --interface INTERFACE  Use network INTERFACE (or address)
 -4, --ipv4          Resolve name to IPv4 address
 -6, --ipv6          Resolve name to IPv6 address
 -j, --junk-session-cookies  Ignore session cookies read from file (H)
     --keepalive-time SECONDS  Wait SECONDS between keepalive probes
     --key KEY       Private key file name (SSL/SSH)
     --key-type TYPE  Private key file type (DER/PEM/ENG) (SSL)
     --krb LEVEL     Enable Kerberos with security LEVEL (F)
     --libcurl FILE  Dump libcurl equivalent code of this command line
     --limit-rate RATE  Limit transfer speed to RATE
 -l, --list-only     List only mode (F/POP3)
     --local-port RANGE  Force use of RANGE for local port numbers
 -L, --location      Follow redirects (H)
     --location-trusted  Like '--location', and send auth to other hosts (H)
     --login-options OPTIONS  Server login options (IMAP, POP3, SMTP)
 -M, --manual        Display the full manual
     --mail-from FROM  Mail from this address (SMTP)
     --mail-rcpt TO  Mail to this/these addresses (SMTP)
     --mail-auth AUTH  Originator address of the original email (SMTP)
     --max-filesize BYTES  Maximum file size to download (H/F)
     --max-redirs NUM  Maximum number of redirects allowed (H)
 -m, --max-time SECONDS  Maximum time allowed for the transfer
     --metalink      Process given URLs as metalink XML file
     --negotiate     Use HTTP Negotiate (SPNEGO) authentication (H)
 -n, --netrc         Must read .netrc for user name and password
     --netrc-optional  Use either .netrc or URL; overrides -n
     --netrc-file FILE  Specify FILE for netrc
 -:, --next          Allows the following URL to use a separate set of options
     --no-alpn       Disable the ALPN TLS extension (H)
 -N, --no-buffer     Disable buffering of the output stream
     --no-keepalive  Disable keepalive use on the connection
     --no-npn        Disable the NPN TLS extension (H)
     --no-sessionid  Disable SSL session-ID reusing (SSL)
     --noproxy       List of hosts which do not use proxy
     --ntlm          Use HTTP NTLM authentication (H)
     --oauth2-bearer TOKEN  OAuth 2 Bearer Token (IMAP, POP3, SMTP)
 -o, --output FILE   Write to FILE instead of stdout
     --pass PASS     Pass phrase for the private key (SSL/SSH)
     --path-as-is    Do not squash .. sequences in URL path
     --pinnedpubkey FILE/HASHES Public key to verify peer against (SSL)
     --post301       Do not switch to GET after following a 301 redirect (H)
     --post302       Do not switch to GET after following a 302 redirect (H)
     --post303       Do not switch to GET after following a 303 redirect (H)
 -#, --progress-bar  Display transfer progress as a progress bar
     --proto PROTOCOLS  Enable/disable PROTOCOLS
     --proto-default PROTOCOL  Use PROTOCOL for any URL missing a scheme
     --proto-redir PROTOCOLS   Enable/disable PROTOCOLS on redirect
 -x, --proxy [PROTOCOL://]HOST[:PORT]  Use proxy on given port
     --proxy-anyauth  Pick "any" proxy authentication method (H)
     --proxy-basic   Use Basic authentication on the proxy (H)
     --proxy-digest  Use Digest authentication on the proxy (H)
     --proxy-negotiate  Use HTTP Negotiate (SPNEGO) authentication on the proxy (H)
     --proxy-ntlm    Use NTLM authentication on the proxy (H)
     --proxy-service-name NAME  SPNEGO proxy service name
     --service-name NAME  SPNEGO service name
 -U, --proxy-user USER[:PASSWORD]  Proxy user and password
     --proxy1.0 HOST[:PORT]  Use HTTP/1.0 proxy on given port
 -p, --proxytunnel   Operate through a HTTP proxy tunnel (using CONNECT)
     --pubkey KEY    Public key file name (SSH)
 -Q, --quote CMD     Send command(s) to server before transfer (F/SFTP)
     --random-file FILE  File for reading random data from (SSL)
 -r, --range RANGE   Retrieve only the bytes within RANGE
     --raw           Do HTTP "raw"; no transfer decoding (H)
 -e, --referer       Referer URL (H)
 -J, --remote-header-name  Use the header-provided filename (H)
 -O, --remote-name   Write output to a file named as the remote file
     --remote-name-all  Use the remote file name for all URLs
 -R, --remote-time   Set the remote file's time on the local output
 -X, --request COMMAND  Specify request command to use
     --resolve HOST:PORT:ADDRESS  Force resolve of HOST:PORT to ADDRESS
     --retry NUM   Retry request NUM times if transient problems occur
     --retry-delay SECONDS  Wait SECONDS between retries
     --retry-max-time SECONDS  Retry only within this period
     --sasl-ir       Enable initial response in SASL authentication
 -S, --show-error    Show error. With -s, make curl show errors when they occur
 -s, --silent        Silent mode (don't output anything)
     --socks4 HOST[:PORT]  SOCKS4 proxy on given host + port
     --socks4a HOST[:PORT]  SOCKS4a proxy on given host + port
     --socks5 HOST[:PORT]  SOCKS5 proxy on given host + port
     --socks5-hostname HOST[:PORT]  SOCKS5 proxy, pass host name to proxy
     --socks5-gssapi-service NAME  SOCKS5 proxy service name for GSS-API
     --socks5-gssapi-nec  Compatibility with NEC SOCKS5 server
 -Y, --speed-limit RATE  Stop transfers below RATE for 'speed-time' secs
 -y, --speed-time SECONDS  Trigger 'speed-limit' abort after SECONDS (default: 30)
     --ssl           Try SSL/TLS (FTP, IMAP, POP3, SMTP)
     --ssl-reqd      Require SSL/TLS (FTP, IMAP, POP3, SMTP)
 -2, --sslv2         Use SSLv2 (SSL)
 -3, --sslv3         Use SSLv3 (SSL)
     --ssl-allow-beast  Allow security flaw to improve interop (SSL)
     --ssl-no-revoke    Disable cert revocation checks (WinSSL)
     --stderr FILE   Where to redirect stderr (use "-" for stdout)
     --tcp-nodelay   Use the TCP_NODELAY option
 -t, --telnet-option OPT=VAL  Set telnet option
     --tftp-blksize VALUE  Set TFTP BLKSIZE option (must be >512)
 -z, --time-cond TIME  Transfer based on a time condition
 -1, --tlsv1         Use >= TLSv1 (SSL)
     --tlsv1.0       Use TLSv1.0 (SSL)
     --tlsv1.1       Use TLSv1.1 (SSL)
     --tlsv1.2       Use TLSv1.2 (SSL)
     --trace FILE    Write a debug trace to FILE
     --trace-ascii FILE  Like --trace, but without hex output
     --trace-time    Add time stamps to trace/verbose output
     --tr-encoding   Request compressed transfer encoding (H)
 -T, --upload-file FILE  Transfer FILE to destination
     --url URL       URL to work with
 -B, --use-ascii     Use ASCII/text transfer
 -u, --user USER[:PASSWORD]  Server user and password
     --tlsuser USER  TLS username
     --tlspassword STRING  TLS password
     --tlsauthtype STRING  TLS authentication type (default: SRP)
     --unix-socket FILE    Connect through this Unix domain socket
 -A, --user-agent STRING  Send User-Agent STRING to server (H)
 -v, --verbose       Make the operation more talkative
 -V, --version       Show version number and quit
 -w, --write-out FORMAT  Use output FORMAT after completion
     --xattr         Store metadata in extended file attributes
 -q                  Disable .curlrc (must be first parameter)


```



### wget  使用示例

```bash
# To download a single file
wget http://path.to.the/file

# To download a file and change its name
wget http://path.to.the/file -O newname

# To download a file into a directory
wget -P path/to/directory http://path.to.the/file

# To continue an aborted downloaded
wget -c http://path.to.the/file

# To download multiples files with multiple URLs
wget URL1 URL2

# To parse a file that contains a list of URLs to fetch each one
wget -i url_list.txt

# To mirror a whole page locally
wget -pk http://path.to.the/page.html

# To mirror a whole site locally
wget -mk http://site.tl/

# To download files according to a pattern
wget http://www.myserver.com/files-{1..15}.tar.bz2

# To download all the files in a directory with a specific extension if directory indexing is enabled
wget -r -l1 -A.extension http://myserver.com/directory

# Allows you to download just the headers of responses (-S --spider) and display them on Stdout (-O -).
wget -S --spider -O - http://google.com

# Change the User-Agent to 'User-Agent: toto'
wget -U 'toto' http://google.com

```



wget help

```bash
$ wget --help
GNU Wget 1.17.1, a non-interactive network retriever.
Usage: wget [OPTION]... [URL]...

Mandatory arguments to long options are mandatory for short options too.

Startup:
  -V,  --version                   display the version of Wget and exit
  -h,  --help                      print this help
  -b,  --background                go to background after startup
  -e,  --execute=COMMAND           execute a `.wgetrc'-style command

Logging and input file:
  -o,  --output-file=FILE          log messages to FILE
  -a,  --append-output=FILE        append messages to FILE
  -d,  --debug                     print lots of debugging information
  -q,  --quiet                     quiet (no output)
  -v,  --verbose                   be verbose (this is the default)
  -nv, --no-verbose                turn off verboseness, without being quiet
       --report-speed=TYPE         output bandwidth as TYPE.  TYPE can be bits
  -i,  --input-file=FILE           download URLs found in local or external FILE
  -F,  --force-html                treat input file as HTML
  -B,  --base=URL                  resolves HTML input-file links (-i -F)
                                     relative to URL
       --config=FILE               specify config file to use
       --no-config                 do not read any config file
       --rejected-log=FILE         log reasons for URL rejection to FILE

Download:
  -t,  --tries=NUMBER              set number of retries to NUMBER (0 unlimits)
       --retry-connrefused         retry even if connection is refused
  -O,  --output-document=FILE      write documents to FILE
  -nc, --no-clobber                skip downloads that would download to
                                     existing files (overwriting them)
  -c,  --continue                  resume getting a partially-downloaded file
       --start-pos=OFFSET          start downloading from zero-based position OFFSET
       --progress=TYPE             select progress gauge type
       --show-progress             display the progress bar in any verbosity mode
  -N,  --timestamping              don't re-retrieve files unless newer than
                                     local
       --no-if-modified-since      don't use conditional if-modified-since get
                                     requests in timestamping mode
       --no-use-server-timestamps  don't set the local file's timestamp by
                                     the one on the server
  -S,  --server-response           print server response
       --spider                    don't download anything
  -T,  --timeout=SECONDS           set all timeout values to SECONDS
       --dns-timeout=SECS          set the DNS lookup timeout to SECS
       --connect-timeout=SECS      set the connect timeout to SECS
       --read-timeout=SECS         set the read timeout to SECS
  -w,  --wait=SECONDS              wait SECONDS between retrievals
       --waitretry=SECONDS         wait 1..SECONDS between retries of a retrieval
       --random-wait               wait from 0.5*WAIT...1.5*WAIT secs between retrievals
       --no-proxy                  explicitly turn off proxy
  -Q,  --quota=NUMBER              set retrieval quota to NUMBER
       --bind-address=ADDRESS      bind to ADDRESS (hostname or IP) on local host
       --limit-rate=RATE           limit download rate to RATE
       --no-dns-cache              disable caching DNS lookups
       --restrict-file-names=OS    restrict chars in file names to ones OS allows
       --ignore-case               ignore case when matching files/directories
  -4,  --inet4-only                connect only to IPv4 addresses
  -6,  --inet6-only                connect only to IPv6 addresses
       --prefer-family=FAMILY      connect first to addresses of specified family,
                                     one of IPv6, IPv4, or none
       --user=USER                 set both ftp and http user to USER
       --password=PASS             set both ftp and http password to PASS
       --ask-password              prompt for passwords
       --no-iri                    turn off IRI support
       --local-encoding=ENC        use ENC as the local encoding for IRIs
       --remote-encoding=ENC       use ENC as the default remote encoding
       --unlink                    remove file before clobber

Directories:
  -nd, --no-directories            don't create directories
  -x,  --force-directories         force creation of directories
  -nH, --no-host-directories       don't create host directories
       --protocol-directories      use protocol name in directories
  -P,  --directory-prefix=PREFIX   save files to PREFIX/..
       --cut-dirs=NUMBER           ignore NUMBER remote directory components

HTTP options:
       --http-user=USER            set http user to USER
       --http-password=PASS        set http password to PASS
       --no-cache                  disallow server-cached data
       --default-page=NAME         change the default page name (normally
                                     this is 'index.html'.)
  -E,  --adjust-extension          save HTML/CSS documents with proper extensions
       --ignore-length             ignore 'Content-Length' header field
       --header=STRING             insert STRING among the headers
       --max-redirect              maximum redirections allowed per page
       --proxy-user=USER           set USER as proxy username
       --proxy-password=PASS       set PASS as proxy password
       --referer=URL               include 'Referer: URL' header in HTTP request
       --save-headers              save the HTTP headers to file
  -U,  --user-agent=AGENT          identify as AGENT instead of Wget/VERSION
       --no-http-keep-alive        disable HTTP keep-alive (persistent connections)
       --no-cookies                don't use cookies
       --load-cookies=FILE         load cookies from FILE before session
       --save-cookies=FILE         save cookies to FILE after session
       --keep-session-cookies      load and save session (non-permanent) cookies
       --post-data=STRING          use the POST method; send STRING as the data
       --post-file=FILE            use the POST method; send contents of FILE
       --method=HTTPMethod         use method "HTTPMethod" in the request
       --body-data=STRING          send STRING as data. --method MUST be set
       --body-file=FILE            send contents of FILE. --method MUST be set
       --content-disposition       honor the Content-Disposition header when
                                     choosing local file names (EXPERIMENTAL)
       --content-on-error          output the received content on server errors
       --auth-no-challenge         send Basic HTTP authentication information
                                     without first waiting for the server's
                                     challenge

HTTPS (SSL/TLS) options:
       --secure-protocol=PR        choose secure protocol, one of auto, SSLv2,
                                     SSLv3, TLSv1 and PFS
       --https-only                only follow secure HTTPS links
       --no-check-certificate      don't validate the server's certificate
       --certificate=FILE          client certificate file
       --certificate-type=TYPE     client certificate type, PEM or DER
       --private-key=FILE          private key file
       --private-key-type=TYPE     private key type, PEM or DER
       --ca-certificate=FILE       file with the bundle of CAs
       --ca-directory=DIR          directory where hash list of CAs is stored
       --crl-file=FILE             file with bundle of CRLs
       --random-file=FILE          file with random data for seeding the SSL PRNG
       --egd-file=FILE             file naming the EGD socket with random data

HSTS options:
       --no-hsts                   disable HSTS
       --hsts-file                 path of HSTS database (will override default)

FTP options:
       --ftp-user=USER             set ftp user to USER
       --ftp-password=PASS         set ftp password to PASS
       --no-remove-listing         don't remove '.listing' files
       --no-glob                   turn off FTP file name globbing
       --no-passive-ftp            disable the "passive" transfer mode
       --preserve-permissions      preserve remote file permissions
       --retr-symlinks             when recursing, get linked-to files (not dir)

FTPS options:
       --ftps-implicit                 use implicit FTPS (default port is 990)
       --ftps-resume-ssl               resume the SSL/TLS session started in the control connection when
                                         opening a data connection
       --ftps-clear-data-connection    cipher the control channel only; all the data will be in plaintext
       --ftps-fallback-to-ftp          fall back to FTP if FTPS is not supported in the target server
WARC options:
       --warc-file=FILENAME        save request/response data to a .warc.gz file
       --warc-header=STRING        insert STRING into the warcinfo record
       --warc-max-size=NUMBER      set maximum size of WARC files to NUMBER
       --warc-cdx                  write CDX index files
       --warc-dedup=FILENAME       do not store records listed in this CDX file
       --no-warc-compression       do not compress WARC files with GZIP
       --no-warc-digests           do not calculate SHA1 digests
       --no-warc-keep-log          do not store the log file in a WARC record
       --warc-tempdir=DIRECTORY    location for temporary files created by the
                                     WARC writer

Recursive download:
  -r,  --recursive                 specify recursive download
  -l,  --level=NUMBER              maximum recursion depth (inf or 0 for infinite)
       --delete-after              delete files locally after downloading them
  -k,  --convert-links             make links in downloaded HTML or CSS point to
                                     local files
       --convert-file-only         convert the file part of the URLs only (usually known as the basename)
       --backups=N                 before writing file X, rotate up to N backup files
  -K,  --backup-converted          before converting file X, back up as X.orig
  -m,  --mirror                    shortcut for -N -r -l inf --no-remove-listing
  -p,  --page-requisites           get all images, etc. needed to display HTML page
       --strict-comments           turn on strict (SGML) handling of HTML comments

Recursive accept/reject:
  -A,  --accept=LIST               comma-separated list of accepted extensions
  -R,  --reject=LIST               comma-separated list of rejected extensions
       --accept-regex=REGEX        regex matching accepted URLs
       --reject-regex=REGEX        regex matching rejected URLs
       --regex-type=TYPE           regex type (posix|pcre)
  -D,  --domains=LIST              comma-separated list of accepted domains
       --exclude-domains=LIST      comma-separated list of rejected domains
       --follow-ftp                follow FTP links from HTML documents
       --follow-tags=LIST          comma-separated list of followed HTML tags
       --ignore-tags=LIST          comma-separated list of ignored HTML tags
  -H,  --span-hosts                go to foreign hosts when recursive
  -L,  --relative                  follow relative links only
  -I,  --include-directories=LIST  list of allowed directories
       --trust-server-names        use the name specified by the redirection
                                     URL's last component
  -X,  --exclude-directories=LIST  list of excluded directories
  -np, --no-parent                 don't ascend to the parent directory

Mail bug reports and suggestions to <bug-wget@gnu.org>

```

