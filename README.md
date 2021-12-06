# ohjelmistotekniikka
Coursework for course Ohjelmistotekniikka

The game is a chess game where users can make their own chess pieces to play with.

Current state of code is pretty messy, trying to prototype will refactor later

[Arkkitehtuuri](https://github.com/ToxPuro/ohjelmistotekniikka/tree/main/documentation/arkkitehtuuri.md)
[Tuntikirjanpito](https://github.com/ToxPuro/ohjelmistotekniikka/tree/main/documentation/tuntikirjanpito.md)
[Määrittelydokumentti](https://github.com/ToxPuro/ohjelmistotekniikka/tree/main/documentation/maarittelydokumentti.md)

Download dependencies with poetry install

Start the application with poetry invoke start

Test with poetry run invoke test

Generate coverage report with poetry run invoke coverage-report

Check codestyle with poetry run invoke lint

## Käyttöohjeet

Paina "Play" ensimmäisessä menussa, jos haluat pelata perinteistä shakkia.

Jos haluat muokata peliä paina "Settings"

Näet aluksi kaksi nappulaa: "Play" ja "Menu". 

Painamalla "Play" pääset pelaamaan valituilla asetuksilla ja säännöillä

Painamalla "Menu" saat asetus-menun auki.

Kun lisäät liikkeitä on olemassa kaksi erilaista liike-luokkaa: liukumis- ja hyppäämislikkeet.

Liukumisliikkeissä nappula voi liukua mihin tahansa ruutuun liukumisen matkalla kunhan matkalla ei ole estävää nappulaa

Hyppäämisliikeet voivat hypätä ruutuun kunhan se on vain vapaa

Automaattisesti on valittu hyppäämisliikkeet, voit vaihtaa tämän painamalla "Jumper" kohdasta.

Nyt pitäisi näkyä "Slider". Painamalla uudestaan pääset takaisin "Jumper"

Hyppäämisliikkeitä on helppo lisätä: valitse ruudut joihin laudalla oleva nappula voi hypätä sen paikalta.

Tämän jälkeen paina "Save".

Liukumisliikkeitä lisätään seuraavasti, valitse yhtenäiset ruudut joista ensimmäinen on nappulan vieressä. 

Ohjelma muodostaa valituista nappuloista liukumisliikkeen kun painat nappulaa.

Jos ei ole selvää missä järjestyksessä ruudut on tarkoitus liukua sovellus suosii järjestystä: alas, ylös, oikea, vasen ja viistot

Ohjelma tallentaa usein liikkeet, mutta ne voidaan aina manuaalisesti tallentaa painamalla "Save"

Jos haluat jakaa tai tallentaa luomuksesi tietokantaan paina "Upload" ja anna nappulalle nimi

Näitä julkaistuja nappuloita voit ladata painamalla "Download" ja valitsemalla ladattavan nappulan nimen

Kaikki liike muutokset tehdään aina laudalla olevaan nappulaan. Jos haluta muokata muita nappuloita paina "Next piece"

Painamalla "Customize" voit muokata missä järjestyksessä nappulat ovat laudalla, huomaa että laudalla täytyy olla tasan yksi kuningas.

Painamalla "Movement" voit aloittaa muokkamaan hyökkäämiisliikkeitä.

Nyt pitäisi näkyä "Attack". Hyökkäämisliikkeitä lisätään samalla logiikalla kuin liikkumisliikkeitä.

Erona hyökkäyksissä on, että hyppäämishyökkäykset voivat hypätä ruutuun vain jos niissä on vastustajan nappula.

Samaten liukumishyökkäykset voivat mennä ruutuun vain jos niissä on vastustajan nappula, ja ruudut sen takana eivät ole saatavilla

Jos haluat kopioida liikkumiset hyökkäyksiin paina "Copy" kun "Movement" on valittuna.

Jos haluat kopioida hyökkäykset liikkumisiin paina "Copy" kun "Attack" on valittuna.

Painamalla "Reset" voit aloittaa asetuksien muokkaamisen alusta

Painamalla "Hide" saat menun piilotettua

Painamalla "Dimension" voit muokata kuinka suuri lauta on. Laudan koon tulee olla 2:n moninkerta.

Nyt olet valmis pelaamaan omaa hullunkurista shakkia!