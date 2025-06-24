# 🍺 Sörfelismerő Verseny App

Az alkalmazás elérhető itt:

👉 https://sorkostolo-app.streamlit.app

Ez az alkalmazás egy vakon történő sörfelismerő verseny lebonyolítására készült, amely során a résztvevők 12 különböző sört kóstolnak végig, és minden körben megpróbálják kitalálni, melyik márkát itták.

## 🎯 Cél

A cél egy olyan felület biztosítása, ahol:
- egyszerűen rögzíthetők a résztvevők tippjei,
- a játék végén vizuálisan megjeleníthetők az eredmények,
- lebonyolítható az értékelés (pontozás, statisztikák, bontások).

---

## 📋 Verseny menete

- **Feladat:** 12 körben söröket kóstolni és minden körben megtippelni a sör típusát
- **Sörök:** Ismert márkák (pl. Dreher, Soproni, Arany Ászok, stb.)
- **Extra:** Minden körben lehet "Fix tipp"-et jelölni (+1/-3 pont), valamint megjelölni, ha az adott sör benne van a "TOP3 legfinomabb" között

---

## 📁 Fájlszerkezet

```
sorkostolo-app/
├── app.py # Eredményportál (nézetek, statisztikák)
├── edit_app.py # Tippfelvitel vizuálisan
├── data/
│ ├── guesses.csv # Tippelések adatai
│ ├── master_beers.csv # (nem kötelező, referencialistához)
│ ├── participants.csv # Résztvevők neve és csoportja
│ └── serving_order.csv # Sörkiosztási sorrend
```

---


---

## 🛠 Lokális használat

### 1. Klónozd a repót

git clone https://github.com/nlemu/sorkostolo-app.git
cd sorkostolo-app


### 2. Telepítsd a szükséges csomagokat
pip install streamlit pandas


### 3. Tippfelvitel
Indítsd el a tippbeviteli felületet:

streamlit run edit_app.py

Itt kiválaszthatod a nevet, kört, sört, majd megadhatod a "Fix tipp" és "TOP3" jelölést. A mentett adatok a data/guesses.csv fájlba kerülnek.


### 4. Eredményportál
Ha minden tipp be van írva, indítsd el az eredményportált:

streamlit run app.py
