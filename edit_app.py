import streamlit as st
import pandas as pd
import os

# Útvonalak
data_dir = "data"
guesses_path = os.path.join(data_dir, "guesses.csv")
participants_path = os.path.join(data_dir, "participants.csv")
master_beers_path = os.path.join(data_dir, "master_beers.csv")

# Adatok betöltése
participants = pd.read_csv(participants_path)
beers = pd.read_csv(master_beers_path)["beer"].tolist()

# Létrehozzuk a guesses.csv-t, ha még nem létezik
if not os.path.exists(guesses_path):
    pd.DataFrame(columns=["name", "round", "guessed_beer", "used_fix", "top3", "pre_guess", "post_guess"]).to_csv(guesses_path, index=False)

guesses = pd.read_csv(guesses_path)

# --- UI ---
st.set_page_config(page_title="Tippelés rögzítése", page_icon="📝", layout="wide")
st.title("📝 Tippelések rögzítése")

name = st.selectbox("Név", participants["name"].unique())

st.markdown("### Tippelések")
with st.form("tip_form"):
    round_data = []
    for round_num in range(1, 13):
        cols = st.columns([1, 3, 1, 1])
        cols[0].markdown(f"**{round_num}. kör**")
        beer = cols[1].selectbox("Tippelt sör", beers, key=f"beer_{round_num}")
        fix = cols[2].checkbox("Fix tipp", key=f"fix_{round_num}")
        top3 = cols[3].checkbox("Top 3", key=f"top3_{round_num}")
        round_data.append({"round": round_num, "guessed_beer": beer, "used_fix": fix, "top3": top3})

    st.markdown("### Eltalálások becslése")
    col1, col2 = st.columns(2)
    pre = col1.number_input("Előzetes becslés (hányat fogsz eltalálni?)", min_value=0, max_value=12, key="pre")
    post = col2.number_input("Utólagos becslés (hányat találtál el?)", min_value=0, max_value=12, key="post")

    submitted = st.form_submit_button("Tipp mentése")
    if submitted:
        # töröljük a korábbi bejegyzéseket ugyanettől az embertől
        guesses = guesses[guesses.name != name]
        new_rows = pd.DataFrame([{
            "name": name,
            "round": d["round"],
            "guessed_beer": d["guessed_beer"],
            "used_fix": d["used_fix"],
            "top3": d["top3"],
            "pre_guess": pre,
            "post_guess": post
        } for d in round_data])

        guesses = pd.concat([guesses, new_rows], ignore_index=True)
        guesses.to_csv(guesses_path, index=False)
        st.success("Tippelés mentve!")

st.markdown("---")
st.dataframe(guesses.sort_values(by=["name", "round"]))
