import streamlit as st
import pandas as pd
import os

# Útvonalak
data_dir = "data"
guesses_path = os.path.join(data_dir, "guesses.csv")
participants_path = os.path.join(data_dir, "participants.csv")
serving_order_path = os.path.join(data_dir, "serving_order.csv")

# Adatok betöltése
participants = pd.read_csv(participants_path)
guesses = pd.read_csv(guesses_path)
serving_order = pd.read_csv(serving_order_path)

# Segédfüggvény a pontszámításra
def get_correct_beer(name, round_num):
    group = participants.loc[participants["name"] == name, "group"].values[0]
    beer = serving_order[(serving_order["group"] == group) & (serving_order["round"] == round_num)]["beer"].values[0]
    return beer

def calculate_score(row):
    correct_beer = get_correct_beer(row["name"], row["round"])
    base = 1 if row["guessed_beer"] == correct_beer else 0
    fix_bonus = 1 if row["used_fix"] and base == 1 else -3 if row["used_fix"] else 0
    return base + fix_bonus

# Alkalmazás
st.set_page_config("Sörkóstoló Eredményportál", page_icon="🍺", layout="wide")
st.title("🍺 Sörkóstoló Eredményportál")

# Pontszámítás
guesses["score"] = guesses.apply(calculate_score, axis=1)

# Főmenü
menu = st.sidebar.radio("Navigáció", ["🏆 Ranglista", "👤 Résztvevő", "🍻 Sörönként"])

# 1) Ranglista
if menu == "🏆 Ranglista":
    st.header("🏆 Ranglista")
    summary = guesses.groupby("name")["score"].sum().reset_index()
    summary = summary.merge(participants, on="name")
    summary = summary.sort_values(by="score", ascending=False).reset_index(drop=True)
    summary.index += 1
    st.dataframe(summary.rename(columns={"score": "Pontszám", "group": "Csoport"}))

# 2) Résztvevő nézet
elif menu == "👤 Résztvevő":
    st.header("👤 Résztvevő bontás")
    selected_name = st.selectbox("Válassz résztvevőt:", participants["name"].unique())
    subset = guesses[guesses["name"] == selected_name].sort_values("round")
    subset["Valós"] = subset["round"].apply(lambda x: get_correct_beer(selected_name, x))
    subset = subset[["round", "Valós", "guessed_beer", "used_fix", "top3"]]
    subset.columns = ["Kör", "Valós", "Tipp", "Fix tipp", "TOP3"]

    def bool_to_icon(val):
        return "✅" if val else ""

    subset["Fix tipp"] = subset["Fix tipp"].apply(bool_to_icon)
    subset["TOP3"] = subset["TOP3"].apply(bool_to_icon)

    st.dataframe(subset.set_index("Kör"))

# 3) Sörönkénti bontás
elif menu == "🍻 Sörönként":
    st.header("🍻 Sörönkénti bontás")
    beer_options = serving_order["beer"].unique().tolist()
    selected_beer = st.selectbox("Válassz sört:", sorted(beer_options))

    correct_rows = []
    for _, row in participants.iterrows():
        name = row["name"]
        group = row["group"]
        served = serving_order[(serving_order["group"] == group) & (serving_order["beer"] == selected_beer)]
        for _, served_row in served.iterrows():
            round_num = served_row["round"]
            guess_row = guesses[(guesses["name"] == name) & (guesses["round"] == round_num)]
            if not guess_row.empty:
                guess = guess_row.iloc[0]["guessed_beer"]
                correct = guess == selected_beer
                fix = guess_row.iloc[0]["used_fix"]
                top3 = guess_row.iloc[0]["top3"]
                correct_rows.append({
                    "name": name,
                    "guess": guess,
                    "correct": correct,
                    "fix": fix,
                    "top3": top3
                })

    df = pd.DataFrame(correct_rows)
    if df.empty:
        st.warning("Ehhez a sörhöz nincs még adat.")
    else:
        hit = df[df.correct == True]
        miss = df[df.correct == False]

        st.markdown("### Kik találták el és kik vétettek")
        st.markdown(f"✅ **Eltalálta:** {', '.join(hit['name'])} ({len(hit)})")
        st.markdown(f"❌ **Nem találta el:** {', '.join(miss['name'])} ({len(miss)})")

        st.markdown(f"### Ki mit tippelt a(z) {selected_beer} sörre")
        df_table = df[["name", "guess", "fix"]].copy()
        df_table.columns = ["Név", "Tipp", "Fix tipp"]
        df_table["Fix tipp"] = df_table["Fix tipp"].apply(lambda x: "✅" if x else "")
        st.dataframe(df_table)

        st.markdown(f"### Melyik sört hányszor tippelték a(z) {selected_beer} helyett")
        mistake_counts = df[df.correct == False].groupby("guess").size().reset_index(name="Darab")
        mistake_counts.columns = ["Tippelt sör", "Darab"]
        st.dataframe(mistake_counts)

        st.markdown(f"### Ennyien mondták a(z) {selected_beer} sörre, hogy benne van a TOP3-ukban: {df['top3'].sum()}")
        st.markdown(f"### Nekik volt TOP3 a(z) {selected_beer} sör")
        top3_df = df[df.top3 == True][["name", "guess"]].copy()
        top3_df.columns = ["Név", "Ilyen sörnek hitte"]
        st.dataframe(top3_df)