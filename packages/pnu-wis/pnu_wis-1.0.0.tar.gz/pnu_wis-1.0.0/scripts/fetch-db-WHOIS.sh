DL="curl -sO"

fetch_ripe_db()
{
    ${DL} ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.domain.gz
    ${DL} ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inet6num.gz
    ${DL} ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz
    ${DL} ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.organisation.gz
}

fetch_apnic_db()
{
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.domain.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.inet6num.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.inetnum.gz
    ${DL} ftp://ftp.apnic.net/public/apnic/whois/apnic.db.organisation.gz

    ${DL} ftp://ftp.apnic.net/apnic/dbase/data/jpnic.db.gz # Japan NIR
    ${DL} ftp://ftp.apnic.net/apnic/dbase/data/krnic.db.gz # Korea NIR
    ${DL} ftp://ftp.apnic.net/apnic/dbase/data/twnic.db.gz # Taiwan NIR

    echo "Nothing for APNIC/IDNIC"
    echo "Nothing for APNIC/CNNIC"
    echo "Nothing for APNIC/VNNIC"
    echo "Nothing for APNIC/IRINN"
}

fetch_afrinic_db()
{
    ${DL} ftp://ftp.afrinic.net/pub/dbase/afrinic.db.gz
}

fetch_arin_db()
{
    echo "Nothing for ARIN"
}

fetch_lacnic_db()
{
    # The following database is not really searchable
    # It contains only city names

    ${DL} ftp://ftp.lacnic.net/lacnic/dbase/lacnic.db.gz
    echo "Nothing meaningful for LACNIC"
}

fetch_others_db()
{
    ${DL} https://whois.canarie.ca/dbase/canarie.db.gz
}

fetch_ripe_db
fetch_apnic_db
fetch_afrinic_db
fetch_arin_db
fetch_lacnic_db
fetch_others_db
