DL="curl -#O"

fetch_ripe_db()
{
    ${DL} ftp://ftp.ripe.net/ripe/dbase/ripe.db.gz
}

fetch_apnic_db()
{
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.as-block.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.as-set.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.aut-num.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.domain.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.filter-set.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.inet-rtr.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.inet6num.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.inetnum.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.irt.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.key-cert.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.limerick.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.mntner.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.organisation.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.peering-set.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.role.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.route-set.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.route.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.route6.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.rtr-set.gz

    ${DL} ftp://ftp.apnic.net/apnic/dbase/data/jpnic.db.gz # Japan
    ${DL} ftp://ftp.apnic.net/apnic/dbase/data/krnic.db.gz # Korea
    ${DL} ftp://ftp.apnic.net/apnic/dbase/data/twnic.db.gz # Taiwan
    ${DL} ftp://irr-mirror.idnic.net/idnic.db.gz # Indonesia
    ${DL} ftp://ftp.nic.ad.jp/jpirr/jpirr.db.gz # Japan
}

fetch_afrinic_db()
{
    ${DL} ftp://ftp.afrinic.net/pub/dbase/afrinic.db.gz
}

fetch_arin_db()
{
    ${DL} ftp://ftp.arin.net/pub/rr/arin.db.gz
}

fetch_lacnic_db()
{
    curl -# ftp://ftp.lacnic.net/lacnic/irr/lacnic.db.gz -o lacnic.db.irr.gz

    ${DL} ftp://ftp.lacnic.net/lacnic/dbase/lacnic.db.gz

#   ${DL} ftp://ftp.bgp.net.br/host.db.gz
#   ${DL} ftp://ftp.bgp.net.br/level3.db.gz
#   ${DL} ftp://ftp.bgp.net.br/nttcom.db.gz
#   ${DL} ftp://ftp.bgp.net.br/radb.db.gz
#   ${DL} ftp://ftp.bgp.net.br/reach.db.gz
    ${DL} ftp://ftp.bgp.net.br/tc.db.gz # Brazil
#   ${DL} ftp://ftp.bgp.net.br/wcgdb.db.gz
}

fetch_others_db()
{
    ${DL} ftp://ftp.altdb.net/pub/altdb/altdb.db.gz
#   ${DL} ftp://whois.in.bell.ca/bell/bell.db.gz # access forbidden now
    ${DL} ftp://irr.bboi.net/bboi.db.gz
    ${DL} https://whois.canarie.ca/dbase/canarie.db.gz
    ${DL} ftp://rr.Level3.net/level3.db.gz
    ${DL} ftp://rr.Level3.net/wcgdb.db.gz
    ${DL} ftp://ftp.nestegg.net/irr/nestegg.db.gz
    ${DL} ftp://rr1.ntt.net/nttcomRR/nttcom.db.gz
    ${DL} ftp://ftp.panix.com/pub/rrdb/panix.db.gz

#   ${DL} ftp://ftp.radb.net/radb/dbase/altdb.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/arin.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/bboi.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/bell.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/canarie.db.gz
    ${DL} ftp://ftp.radb.net/radb/dbase/host.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/jpirr.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/level3.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/nestegg.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/nttcom.db.gz
    ${DL} ftp://ftp.radb.net/radb/dbase/openface.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/panix.db.gz
    ${DL} ftp://ftp.radb.net/radb/dbase/radb.db.gz
    ${DL} ftp://ftp.radb.net/radb/dbase/reach.db.gz
    ${DL} ftp://ftp.radb.net/radb/dbase/rgnet.db.gz
#   ${DL} ftp://ftp.radb.net/radb/dbase/tc.db.gz
}

fetch_ripe_db
fetch_apnic_db
fetch_afrinic_db
fetch_arin_db
fetch_lacnic_db
fetch_others_db
