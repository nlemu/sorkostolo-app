# 🍻 Sörfelismerő Verseny App

Ez az alkalmazás egy vakon történő sörfelismerő verseny lebonyolítására készült, amely során a résztvevők 12 különböző sört kóstolnak végig, és minden körben megpróbálják kitalálni, melyik márkát itták.

Az alkalmazás elérhető itt:  
👉 [https://sorkostolo-app.streamlit.app](https://sorkostolo-app.streamlit.app)

---

## 🎯 Cél

A cél egy olyan felület biztosítása, ahol:

- egyszerűen rögzíthetők a résztvevők tippjei,
- a játék végén vizuálisan megjeleníthetők az eredmények,
- lebonyolítható az értékelés (pontozás, statisztikák, bontások),
- figyelembe vehető az, ha valaki "fix tippként" vagy "TOP3" kedvencként jelöl egy sört.

---

## 🗂️ Fájlstruktúra

```plaintext
sorkostolo-app/
├── app.py                  # Eredményportál (nézetek, statisztikák)
├── edit_app.py            # Tippfelvitel vizuálisan
├── requirements.txt       # Szükséges Python csomagok
├── README.md              # Dokumentáció
└── data/
    ├── guesses.csv         # Tippek - melyik résztvevő, melyik körben, milyen sört tippelt (le kell generálni)
    ├── master_beers.csv    # (nem kötelező, sörlista referenciához)
    ├── participants.csv    # Résztvevők neve és csoportja
    └── serving_order.csv   # Csoportonkénti sörsorrend
```


## 🧩 Szükséges adatfájlok

A `data/` mappában a következő fájlokat kell előre létrehozni, mielőtt az app használható:


📄 participants.csv  
A játékosok neveit és csoportjait tartalmazza.
A csoport alapján dől el, hogy ki mikor milyen sört kap.

```
name,group
Anna,A
Béla,B
Csilla,C
Dénes,D
```

📄 serving_order.csv  
Melyik csoport melyik körben milyen sört kapta.

```
group,round,beer
A,1,Soproni
A,2,Dreher
...
D,12,Arany Ászok
```


📄 master_beers.csv (nem kötelező)  
Referencialistaként szolgál a sörök kiválasztásához a tippelés során.

```
beer
Soproni
Dreher
Arany Ászok
Kőbányai
```


## 🛠️ Lokális használat  
1. Klónozd a repót
```
git clone https://github.com/nlemu/sorkostolo-app.git
cd sorkostolo-app
```

2. Telepítsd a szükséges csomagokat
```
pip install -r requirements.txt
```

3. Tippfelvitel
Indítsd el a tippbeviteli felületet:

```
streamlit run edit_app.py
```
- Itt kiválaszthatod a nevet, kört, sört, majd megadhatod a "Fix tipp" és "TOP3" jelölést.
- A mentett adatok a data/guesses.csv fájlba kerülnek.

4. Eredményportál
Ha minden tipp be van írva, indítsd el az eredményportált:
```
streamlit run app.py
```
