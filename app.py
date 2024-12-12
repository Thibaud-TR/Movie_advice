import streamlit as st
import pandas as pd

df=pd.read_csv('https://raw.githubusercontent.com/Thibaud-TR/Movie_advice/refs/heads/master/bdd_tmdb.csv')
df['genre'] = df['genre'].apply(lambda x :eval(x))

# Style changes
st.markdown("""<style>
            *{color:#B0B0B0;}
            .st-emotion-cache-ysk9xe p{font-size:25px ; color:#5F9EA0}
            h1{text-align:center;}
            .e1f1d6gn0 {margin: auto auto ;}
            .st-emotion-cache-1y5f4eg p{font-size:25px;}
            </style>""", unsafe_allow_html=True)


# Sidebar creation
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Accueil", "Films du moment", "Système de recommandation", "Liens utiles", "Remerciements", "Contact"])

st.markdown("""<style>
            label {height : 35px;}
            </style>""", unsafe_allow_html=True)


# Page : Accueil - START
if page == "Accueil":
    st.title("👋 Bienvenue sur CinéClap !")
    st.write("")
    st.image(
        "https://media1.tenor.com/m/7ARSlPMxupoAAAAd/laughing-garfield.gif",
        caption="En acceptant les CGV de site, vous agréez expressément à souscrire à notre service Cinélist à 490€ HT / mois",
        use_container_width=True
    )
# Page : Accueil - END


# Page : Films du moment - START
if page == "Films du moment":
    st.title('🎥 Les films du moment ! 🎬')
    st.markdown("""<style>
                *{color:#B0B0B0;}
                .st-emotion-cache-ysk9xe p{font-size:25px ; color:#5F9EA0}
                h1{text-align:center;}
                .e1f1d6gn0 {margin: auto auto ;}
                .st-emotion-cache-1y5f4eg p{font-size:25px;}
                </style>""", unsafe_allow_html=True)

    st.write('---')
    col1,col2,col3 = st.columns([1,9,1])
    with col2 :
        language = st.radio('Affiner par langue originale',['Tous'] + ['Français', 'Anglais'], )
        st.text(' ')
        genre = st.selectbox('Affiner par genre', ['Tous'] + sorted(list(df['genre'].explode().unique())))

    if language == 'Français' :
        df = df[df['original_language'] == 'fr']
    if language == 'Anglais' :
        df = df[df['original_language'] == 'en']
    if genre != 'Tous' :
        df = df[df["genre"].apply(lambda liste: genre in liste)]

    st.write('---')

    for i in range(4) :
        col1, col2 = st.columns([2,3])
        with col1:
            st.image('https://image.tmdb.org/t/p/original'+list(df['poster_path'])[i],width=200)
        with col2:
            st.markdown(list(df['title'])[i])
            st.text(list(df['overview'])[i])
        st.write('---')
# Page : Films du moment - END


# Page : Liens Utiles - START
if page == "Liens utiles":
    st.title("🚩 Liens utiles 😎")
    st.write("---")
    st.write("Ces sites internets peuvent vous aider à trouver des informations sur vos films préférés :")

    links = [
        ("TMDB", "https://www.themoviedb.org/?language=fr", "https://upload.wikimedia.org/wikipedia/commons/6/6e/Tmdb-312x276-logo.png"),
        ("Rotten Tomatoes", "https://www.rottentomatoes.com/", "https://upload.wikimedia.org/wikipedia/commons/6/6f/Rotten_Tomatoes_logo.svg"),
        ("Allociné", "https://www.allocine.fr/", "https://www.logotheque-vectorielle.fr/wp-content/uploads/2022/10/logo-vectoriel-allocine.jpg"),
        ("Sens Critique", "https://www.senscritique.com/", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/SensCritique_logo.svg/640px-SensCritique_logo.svg.png"),
    ]

    for name, url, image in links:
        col1, col2, col3 = st.columns([1, 2, 5])
        with col2:
            st.image(image, width=120,)
            st.write("")
        with col3:
            st.markdown(f"[Accéder à {name}]({url})", unsafe_allow_html=True)

    # Specific layout
    st.markdown("""<style>
            .stHorizontalBlock {height : 100px}
            .st-emotion-cache-0 div{margin: auto 0}
            .st-emotion-cache-1y5f4eg p{font-size:22px;}
            </style>""", unsafe_allow_html=True)
# Page : Liens Utiles - END