$TTL    604800
@       IN      SOA     ns1.pythia.com. root.pythia.com. (
                  3       ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; name servers - NS records
     IN      NS      ns1.pythia.com.

; name servers - A records
ns1.pythia.com.          IN      A      172.23.0.2

host1.pythia.com.        IN      A      172.20.0.2
host2.pythia.com.        IN      A      172.20.0.4