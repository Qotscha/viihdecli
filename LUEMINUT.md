# ViihdeCLI
Komentorivityökalu Elisa Viihteen tallenteiden hallintaan, katseluun ja lataukseen.
## Vaatimukset
* Windows-käyttöjärjestelmä
* [Python](https://www.python.org/) 3.8 tai uudempi
* [FFmpeg](https://www.ffmpeg.org/) tallenteiden lataukseen
## Asennus
Käytä pip-paketinhallintajärjestelmää asentaaksesi tai päivittääksesi ohjelman ja sen suorittamiseen tarvittavat kirjastot [keyring](https://pypi.org/project/keyring/) ja [requests](https://pypi.org/project/requests/) sekä tallenteiden lataukseen tarvittavan työkalun [ViihdexDL](https://pypi.org/project/viihdexdl/).
```
pip install -U viihdecli
```
## Käyttö
Käynnistä sovellus komennolla `viihdecli`. Ensimmäisellä käyttökerralla sovellus kysyy käyttäjätunnusta ja salasanaa, jotka on myös mahdollista tallentaa. Käyttäjätunnus tallennetaan tiedostoon settings.ini, joka luodaan sovelluksen ensimmäisellä käyttökerralla kansioon `%APPDATA%\viihdecli`. Salasana tallentuu keyring-kirjastoa käyttäen Windowsin tunnistetietojen hallintaan. Kirjautumisen jälkeen valitaan ohjelman käyttötila syöttämällä haluttua tilaa vastaava kirjain.
### \[d\] Poista kirjautumistiedot
Poistaa asetustiedostoon tallennetun käyttäjätunnuksen ja kyseiseen käyttäjätunnukseen liittyvän salasanan Windowsin tunnistetietojen hallinnasta.
### \[p\] Liitä
Ohjelma lataa FFmpeg:tä käyttäen ViihdexDL:n avulla tallenteen, jonka [elisaviihde.fi](https://elisaviihde.fi)-sivustolta kopioidun URLin käyttäjä syöttää. Tallenteen URLin (tallenteen id 123) tulee olla jotakin seuraavaa muotoa:
* https://elisaviihde.fi/tallenne/katso/123
* https://elisaviihde.fi/tallenteet/katso/123
* https://elisaviihde.fi/ohjelmaopas/ohjelma/123

Myös yhden kansion kaikki tallenteet on mahdollista ladata. Tällöin URLin tulee olla muotoa https://elisaviihde.fi/tallenteet/kansio/123/sivu/1 tai pääkansion osalta https://elisaviihde.fi/tallenteet/sivu/1.
### \[f\] Kansiot
Ohjelma listaa Elisa Viihteen tallennekansiot. Voit siirtyä valitsemaasi kansioon syöttämällä kansion numeron (sarake #). Komennolla `h` saa ruudulle alla näkyvän listauksen muista komennoista.
```
Komento             Selite
ENTER               Hyväksy/Palaa/Poistu
h                   Näytä tämä listaus
q                   Näytä jäljellä oleva tallennustila
#                   Siirry kansioon # (numero)
/                   Siirry pääkansioon
..                  Siirry yläkansioon
.                   Listaa kansiot
n NIMI              Luo uusi kansio NIMI
del                 Poista nykyinen kansio
del #               Poista kansio #
l                   Listaa nykyisen kansion tallenteet
r                   Päivitä kansiot
dl                  Lataa nykyisen kansion tallenteet
q                   Näytä jäljellä oleva tallennustila
fs NIMI             Lisää nykyinen kansio pikavalinnaksi NIMI
lf                  Listaa kansioiden pikavalinnat
ld                  Näydä nykyinen latauskansio ja pikavalinnat
df POLKU            Aseta latauskansioksi POLKU
ds NIMI             Aseta pikavalinta NIMI latauskansioksi
dp NIMI             Lisää nykyinen latauskansio pikavalinnaksi NIMI
dp NIMI | POLKU     Lisää latauskansio POLKU pikavalinnaksi NIMI
rc                  Päivitä asetukset tiedostoista settings.ini ja columns.ini
o                   Avaa settings.ini Muistiossa
oc                  Avaa columns.ini Muistiossa
```
Kun kansion tallenteet listataan, hallitaan tallenteita seuraavassa luvussa kuvatulla tavalla.
### \[a\] Kaikki tallenteet
Tässä käyttötilassa kaikkia Elisa Viihteen tallenteita voidaan käsitellä yhtensä kokonaisuutena riippumatta niiden kansioista. Näkymää voi mukauttaa asetustiedostoa `%APPDATA%\viihdecli` käyttäen. Kyseisen tiedoston, jota käsitellään tarkemmin alempana, saa avattua komennolla `oc` Muistiossa. Muistiossa. Komennolla `h` saa listauksen käytettävissä olevista komennoista.
```
Komento             Selite
ENTER               Hyväksy/Palaa/Poistu
h                   Näytä tämä listaus
q                   Näytä jäljellä oleva tallennustila
l                   Listaa suodatetut tallenteet
sw                  Näytä tallenteiden listaukseen tarvittava terminaalin leveys
pd                  Näytä/piilota tallenteiden kuvaukset
sh                  Näytä lajitteluavaimet
s %                 Järjestä tallenteet nousevasti avaimen % mukaisesti (ks. LUEMINUT)
sd %                Järjestä tallenteet laskevasti avaimen % mukaisesti (ks. LUEMINUT)
r                   Päivitä tallenteet ja kansiot
f                   Listaa käytössä olevat suotimet
fh                  Listaa mahdolliset suotimet
.                   Poista kaikki suotimet
..                  Poista viimeisin suodin
. X                 Poista suodin numero X
+ NIMI              Lisää viimeisin suodin pikavalinnaksi NIMI
+ NIMI | X          Lisää suodin numero X pikavalinnaksi NIMI
+ NIMI | KOMENTO    Lisää KOMENTO pikavalinnaksi NIMI
, NIMI              Käytä pikavalinnan NIMI suodinta
ff                  Listaa suodinten pikavalinnat
cd #                Näytä tallennetta # edeltävät ja seuraavat tallenteet
rem ##              Suodata pois tallenteet ##
ex                  Suodata pois valittavassa kansiossa sijaitsevat tallenteet
ex #                Suodata pois tallenteen # kansiossa sijaitsevat tallenteet
ex > NIMI           Suodata pois kansiossa, jonka pikavalinta on NIMI, sijaitsevat tallenteet
rd                  Etsi duplikaatit (sama nimi ja kuvaus)
rd X                Etsi duplikaatit, hakumoodi X (ks. LUEMINUT)
p #                 Toista tallenne # (numero)
d #                 Näytä tallenteen # kuvaus
i #                 Näytä tallenteen # tiedot
u #                 Näytä tallenteen # URL
dl ##               Lataa tallenteet ##
del ##              Siirrä tallenteet ## roskakorikansioon
rm ##               Poista tallenteet ## Elisa Viihteen roskakoriin
m ##                Siirrä tallenteet ## valittavaan kansioon
m ## > NIMI         Siirrä tallenteet ## kansioon, jonka pikavalinta on NIMI
m ## _ #            Siirrä tallenteet ## kansioon, jossa tallenne # sijaitsee
q                   Näytä jäljellä oleva tallennustila
fs NIMI             Lisää valittava kansio pikavalinnaksi NIMI
fs NIMI | #         Lisää tallenteen # sisältävä kansio pikavalinnaksi NIMI
lf                  Listaa kansioiden pikavalinnat
ld                  Näydä nykyinen latauskansio ja pikavalinnat
df POLKU            Aseta latauskansioksi POLKU
ds NIMI             Aseta pikavalinta NIMI latauskansioksi
dp NIMI             Lisää nykyinen latauskansio pikavalinnaksi NIMI
dp NIMI | POLKU     Lisää latauskansio POLKU pikavalinnaksi NIMI
rc                  Päivitä asetukset tiedostoista settings.ini ja columns.ini
o                   Avaa settings.ini Muistiossa
oc                  Avaa columns.ini Muistiossa
```
#### Tallenteisiin viittaaminen
Tallenteisiin viitataan sarakkeessa # tai -# näkyvällä numerolla. Komentolistauksessa esiintyvä ## tarkoittaa tallennejoukkoa. Alla olevat esimerkit havannollistavat useisiin tallenteisiin viittaamista.
```
##          Tallenteet
1           1
3+          3 ja 4
3+++        3, 4, 5 ja 6
5-          4 ja 5
5---        2, 3, 4 ja 5
5-+-        3, 4, 5 ja 6
1 2         1 ja 2
1:3         1, 2 ja 3
1:2:7       1, 3, 5 ja 7
4:3:11      4, 7 ja 10
3:          3, 4, 5, 6...
:3          0, 1, 2 ja 3
3:2:        3, 5, 7, 9...
:3:11       0, 3, 6 ja 9
3:1         3, 2 ja 1
7:2:1       7, 5, 3 ja 1
11:3:4      11, 8 ja 5
11:-3:      11, 8, 5 ja 2
```
Jos viimeisen listatun tallenteen numero on 15, niin tallenteisiin viittaaminen toimii alla olevien esimerkkien mukaisesti.
```
##          Tallenteet
-1          15
-5+-+       10, 11, 12 ja 13
-5 -6       11 ja 10
2 -13       2 ja 3
-15:2:-9    1, 3, 5 ja 7
4:3:-5      4, 7 ja 10
-12:3:11    4, 7 ja 10
-5:         11, 12, 13, 14 ja 15
:-10        0, 1, 2, 3, 4, 5 ja 6
-7:2:       9, 11, 13 ja 15
:3:-7       0, 3, 6 ja 9
-5:-3:      11, 8, 5 ja 2
:-3:-15     15, 12, 9, 6 ja 3
:-3:2       15, 12, 9, 6 ja 3
```
Huutomerkillä järjestyksen, jolla sinänsä ei ole vaikutusta kuin tallenteita ladattaessa, voi kääntää päinvastaiseksi:
```
##          Tallenteet
!1:3        3, 2 ja 1
!4:3:11     10, 7 ja 3
!7:2:1      1, 3, 5 ja 7
!-5:        15, 14, 13, 12 ja 11
!:-3:2      3, 6, 9, 12 ja 15
```
Yllä olevien esimerkkien ilmauksia voi yhdistellä vapaasti. Esimerkiksi `8 1:2:7 0 !-5:` viittaa tallenteisiin 8, 1, 3, 5, 7, 0, 15, 14, 13, 12 ja 11.

Kaikkiin suodatettuihin tallenteisiin viitataan kirjaimella a ja kaikkiin duplikaatteihin kirjaimella d.
#### Tallenteiden järjestäminen
Tallenteet on mahdollista järjestää joko nousevasti (s) tai laskevasti (sd) alkamisajan (s), päättymisajan (e), nimen (n), keston (d), kanavan (n) tai IMDB-arvosanan (i) mukaan. Esimerkkejä:
```
Komento   Selite
s s       Järjestä nousevasti alkamisajan mukaan
sd d      Järjestä laskevasti keston mukaan
```
#### Tallenteiden suodattaminen
Tallenteita on mahdollista suodattaa eri tavoilla. Suodattaminen tapahtuu komennoilla:
```
Komento                       Selite
n TEKSTI                      Tallenteen nimi sisältää tekstin
de TEKSTI                     Tallenteen kuvaus sisältää tekstin
c TEKSTI                      Tallenteen kanavanimi sisältää tekstin
dur X tai HH:MM               Tallenteen pituus vähintään X min tai HH tuntia, MM minuuttia
b YYYY-MM-DD tai DD.MM.YYYY   Tallennus alkoi ennen päivämäärää
be YYYY-MM-DD tai DD.MM.YYYY  Tallennus päättyi ennen päivämäärää
w VIIKONPÄIVÄN LYHENNE        Tallennus alkoi viikonpäivänä
t HH:MM                       Tallennus alkoi ennen kellonaikaa
a SUKUNIMI, ETUNIMI           Näyttelijä esintyy tallenteella
di SUKUNIMI, ETUNIMI          Tallenne on ohjaajan ohjaama
im X.Y                        Tallenteen IMDB-pisteet vähintään X.Y
st TEKSTI                     Tallenteen showtype (metadatassa) sisältää tekstin
g TEKSTI                      Jokin tallenteen genreistä (metadatassa) sisältää tekstin
ser TEKSTI                    Sarjan nimi sisältää tekstin
en TEKSTI                     Sarjan jakson nimi sisältää tekstin
se XX                         Sarjan kausi XX
ep XX                         Sarjan jakso XX
```
Huutomerkki suodatuskomennon alussa tarkoittaa negaatiota. Esimerkiksi siis `!dur 30`  suodattaa näkyviin vain tallenteet, joiden pituus on alle 30 minuuttia, ja `!b 2023-07-01` tallenteet, joiden lähetys alkoi aikaisintaan 1.7.2023.

Tallenteen nimen, kuvauksen, kanavan, viikonpäivän, näyttelijän, ohjaajan, showtypen, genren, jakson ja sarjan nimen sekä tuotantokauden ja jakson haussa voi käyttää tai-operaattoria |. Esim. `c nelonen | jim | hero`.

Viikonpäivien lyhenteet riippuvat järjestelmän kielestä. Suomenkielisissä järjestelmissä käytössä ovat ma, ti, ke, to, pe, la ja su.

Näyttelijän tai ohjaajan mukaan suodattaessa voi käyttää myös pelkkää etu- tai sukunimeä. Lisäksi nimen lopussa on mahdollista käyttää jokerimerkkiä *. Esimerkkejä:
```
a stal*, syl*
a , arnold
a van damme
```
Tallenteita suodattaessa on syytä huomioida, että Viihteen metadatassa voi olla puutteita.
##### Esimerkki suodattimien käytöstä.
Suodatetaan näkyviin kaikki elokuvat, joissa esiintyy Ansa (Ikonen), Regina Linnanheimo tai (Tuulikki) Paananen, jotka on ohjannut (T.J.) Särkkä ja joissa esiintyy joku Rinne, muttei kuitenkaan Jalmari Rinne. Tämän jälkeen listataan suodattimet:
```
a , ansa | linnanheimo, regina | paananen
di särkkä
n rinne
!n rinne, jalmari
f
```
Suodatinlistaus näyttää seuraavalta:
```
Aktiiviset suotimet:
0    Näyttelijä: , ANSA | LINNANHEIMO, REGINA | PAANANEN
1    Ohjaaja: SÄRKKÄ
2    Näyttelijä: RINNE
3    EI: Näyttelijä: RINNE, JALMARI
```
Toteamme, ettei Rinteen mukanaolo ole välttämätöntä, joten poistamme suodattimen. Lisäksi haluamme, että IMDB-arvosana on vähintään 5.2 ja lisäksi haluamme, että elokuvan kesto on alle 100 minuuttia. Taas katsomme aktiiviset suodattimet.
```
. 2
im 5.2
!dur 100
f
```
Nyt suodatinlistaus näyttää seuraavalta:
```
Aktiiviset suotimet:
0    Näyttelijä: , ANSA | LINNANHEIMO, REGINA | PAANANEN
1    Ohjaaja: SÄRKKÄ
2    EI: Näyttelijä: RINNE, JALMARI
3    IMDB-pisteet vähintään 5.2
4    Kesto alle 100 minuuttia
```
Muutammekin mielemme ja toteamme, että yli 100-minuuttisetkin kelpaavat, joten poistamme viimeisimmän suodattimen. Lisäksi jostakin kumman syystä haluamme, että tallenne on lähetetty tiistaina tai torstaina ennen kello neljäätoista.
```
..
w ti | to
t 14:00
f
```
Suodatinlistaus näyttää seuraavalta:
```
Aktiiviset suotimet:
0    Näyttelijä: , ANSA | LINNANHEIMO, REGINA | PAANANEN
1    Ohjaaja: SÄRKKÄ
2    EI: Näyttelijä: RINNE, JALMARI
3    IMDB-pisteet vähintään 5.2
4    Viikonpäivät: TI | TO
5    Tallennusaika ennen 14:00
```
Tämän jälkeen voimmekin sitten vaikkapa katsoa haluamamme tallenteen.
#### Duplikaattien poisto
Duplikaattien haku tapahtuu kulloinkin suodatettuna olevasta joukosta. Se, mikä ehdot täyttävistä tallenteista lasketaan duplikaatiksi ja mikä "alkuperäiseksi", riippuu tallenteiden järjestyksestä. Ensimmäisenä listauksessa oleva on originaali. Jos siis esim. haluaa säilyttää viimeisimpänä tallennetun, on syytä ennen duplikaattien hakua järjestää tallenteet laskevasti alkamisajan mukaan.

Duplikaattien haussa on useita eri toimintatiloja:

```
Moodi   Ehdot
1       nimi JA kuvaus JA metadataId
2       nimi JA kuvaus [oletus]
3       kuvaus JA (nimi TAI metadataId)
4       metadataId JA (nimi TAI kuvaus)
5       metadataId
6       nimi JA (kuvaus TAI metadataId)
7       (nimi JA kuvaus) TAI metadataId
```
Lisäksi on mahdollista käyttää haluttua yhdistelmää ehdoista nimi (n), kuvaus (d), metadataId (m) ja ero pituudessa korkeintaan X minuuttia (.X). Esimerkkejä:
```
Komento      Selite
rd n d       nimi JA kuvaus
rd n         nimi
rd n .10 d   nimi JA ero kestossa enintään 10 minuuttia JA kuvaus
```
Duplikaattien haun jälkeen on mahdollista poistaa kaikki löydetyt duplikaatit. Jos tätä ei tee, voi duplikaatteja suodattaa yllä kuvatuilla tavoilla ja halutessaan poistaa osan niistä.
### \[r\] Roskakori
Tässä käyttötilassa Elisa Viihteen roskakorissa olevia tallenteida voidaan käsitellä edellisessä luvussa kuvatulla tavalla. Roskakorissa olevia tallenteida ei kuitenkaan voida katsella tai ladata, vaan ne tulee ensin palauttaa.

Roskakorissa olevan tallenteen kansio on se Elisa Viihteen kansio, jossa tallenne sijaitsi ennen poistamista. Jos tallenne palautetaan, se palautuu kyseiseen kansioon. Jos roskakorin tallenteen siirtää toiseen kansioon, tallenne pysyy edelleen roskakorissa, mutta kansio, johon se palautuu vaihtuu.
### \[c\] Avaa asetustiedosto Muistiossa
Asetustiedosto settings.ini avataan Muistiossa.
### \[q\] Sulje ohjelma
## Asetustiedosto settings.ini
Sovelluksen asetukset määritetään tiedostossa `%APPDATA%\viihdecli\settings.ini`. Kyseinen tiedosto luodaan kun sovellus käynnistetään ensimmäisen kerran. Tiedosto näyttää seuraavalta:
```
[Login information]
service name = Elisa Viihde API
username = 
auto login = false

[General settings]
print help at start = true
move prompt min = 1
print at start = true
print all = true
sorting key = startTime
sorting dir = asc
recycle duplicates = false

[Download settings]
player = "C:\Program Files\MPC-HC\mpc-hc64.exe"
platform = ios
download folder = 
folder structure = false
season episode filename = false
audio languages = fin, dut
subtitle languages = fi, nl
default audio = fin, dut
default subtitle = fin, dut
visual impaired = dut
hearing impaired = dut
maximum bandwidth = 0
file extension = mkv
external subtitles = true
ffmpeg options = -v error -stats
ffmpeg video codec = copy
ffmpeg audio codec = copy
save description = true
prompt overwrite = true

[Folder shortcuts]
home = 0

[Download folders]
esimerkki = C:\Lataukset
```
### [Login information]
Tässä osiossa hallitaan kirjautumisasetuksia.
```
Asetus              Selite
service name        Palvelun nimi Windowsin tunnistetietojen hallinnassa
username            Käyttäjätunnus
auto login          Kirjaudu automaattisesti
```
### [General settings]
Tässä osiossa hallitaan sovelluksen toimintaan liittyviä asetuksia.
```
Asetus                 Selite
print help at start    Näytä komentolistaus alussa
move prompt min        Kysy vahvistusta, kun vähintään tämä määrä tallenteita yritetään siirtää tai poistaa kerralla
print at start         Listaa tallenteet alussa
print all              Listaa kaikki (ei suodattimia) tallenteet päivityksen tai järjestämisen jälkeen
sorting key            Tallenteiden oletusjärjestysavain
sorting dir            Tallenteiden oletusjärjestyssuunta
recycle duplicates     Siirrä duplikaatit kysyttäessä Elisa Viihteen roskakoriin roskakorikansion sijaan
```
### [Download settings]
Tässä osiossa hallitaan tallenteiden lataukseen liittyviä asetuksia.
```
Asetus                      Selite
player                      Sovellus, jota käytetään tallenteiden toistoon
platform                    Vaikuttaa siihen, missä muodossa tallenne on ladattavissa
download folder             Latauskansio
folder structure            Säilytä Viihteen kansiorakenne ladattaessa
season episode filename     Tiedostonimi muodossa Sarjan nimi SXXEYY, jos kyseessä sarja
audio languages             Ladattavat ääniraidat (jos tyhjä, ladataan kaikki)
subtitle languages          Ladattavat tekstitysraidat (jos tyhjä, ladataan kaikki)
default audio               Oletukseksi merkittävä ääniraita
default subtitle            Oletukseksi merkittävä tekstitysraita
visual impaired             Ääniraita, joka merkitään 'visual impaired' -lipulla
hearing impaired            Tekstitysraita, joka merkitään 'hearing impaired' -lipulla
maximum bandwidth           Ladattavan tallenteen maksimibittivirrannopeus (0 = aina korkein)
file extension              Tiedostomuoto
external subtitles          Teksitykset ladataan erillisiin .srt-tiedostoihin
ffmpeg options              FFmpeg:n yleiset asetukset
ffmpeg video codec          FFmpeg:n videokoodekkiasetukset
ffmpeg audio codec          FFmpeg:n audiokoodekkiasetukset
save description            Tallenna tallenteen kuvaus tekstitiedostoon
prompt overwrite            Jos tallenne on jo ladattu, kysy ylikirjoitetaanko
```
### [Folder shortcuts]
Listaus kansioiden pikavalinnoista, joita voi hyödyntää tallenteita siirtäessä.
### [Download folders]
Listaus latauskansioiden pikavalinnoista.
## Asetustiedosto columns.ini
Tallennenäkymää saa mukautettua tiedostoa `%APPDATA%\viihdecli\columns.ini` käyttäen. Näkymä on oletuksena asetettu 120 merkkiä leveään terminaali-ikkunaan mahtuvaksi. Roskakorille (Recycle bin) on eri asetukset kuin muille tallenteille (Recordings).
```
Asetus          Selite
spacing         sarakkeiden väli
negative        -#
start day       viikonpäivä, jona tallenne alkoi
start date      tallenteen alkamispäivä
start time      tallenteen alkamiskellonaika
end day         viikonpäivä, jona tallenne päättyi
end date        tallenteen päättymispäivä
end time        tallenteen päättymiskellonaika
channel         kanava
duration        kesto
name            tallenteen nimi
folder          tallenteen kansio
show imdb       näytä IMDB-arvosana
show live       näytä merkintä, jos tallenne ei ole päättynyt
```
Tallenteen kanavalle, nimelle ja kansiolle määritellään sarakkeen leveys (0 piilottaa sarakkeen paitsi nimisarake on aina vähintään 20 merkkiä leveä). Muut sarakkeet ovat joko näkyvissä (true) tai eivät ole (false). Roskakorin (Recycle bin) osalta saa tallenteen aloitus- ja lopetusajan kaltaisesti määritettyä tallenteen lopullisen poistumisen ajankohdan (removal) näkymisen.
## Lisenssi
Sovellus on julkaistu MIT-lisenssillä (ks. tiedosto LICENSE).