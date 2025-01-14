import streamlit as st
import pandas as pd


@st.cache_data
def get_df():
    df=pd.read_csv('https://raw.githubusercontent.com/Thibaud-TR/Movie_advice/refs/heads/master/db_reco.csv')
    df['genre'] = df['genre'].apply(lambda x : eval(x) if len(x)>3 else 0)
    df = df.drop(df[df['genre'] == 0].index , axis=0)
    return df

df = get_df()

# Style changes
st.markdown("""<style>
            *{color:#B0B0B0;}
            h1{text-align:center;}
            .e1f1d6gn0 {margin: auto auto ;}
            .stMarkdown p{font-size:25px;}
            </style>""", unsafe_allow_html=True)


# Sidebar creation
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Accueil", "Films du moment", "Recommandations", "Liens utiles"])

if page != 'Recommandations':
    st.session_state['selected_index'] = None

st.markdown("""<style>
            label {height : 35px;}
            </style>""", unsafe_allow_html=True)


# Page : Accueil - START
if page == "Accueil":
    st.title("👋 Bienvenue sur Toucan Movie! 🦜")
    st.write("")
    col1,col2,col3 = st.columns([1,5,1])
    with col2 :
        st.image("https://i.ibb.co/Dttjw3S/45cef378-7cf0-453d-a658-9df8e84a19a3.png", width=500    )
    st.write("")
    st.write("*Chez Toucan Movie, on vous promet des films a vous clouer le bec et des histoires qui ne manqueront pas de faire vibrer vos plumes !*")

    st.markdown("""<style>
            *{color:#B0B0B0;}
            h1{text-align:center;font-size:35px;}
            .stMarkdown > div > p {font-size:20px;text-align:center;}
            </style>""", unsafe_allow_html=True)

# Page : Accueil - END


# Page : Films du moment - START
if page == "Films du moment":
    st.title('🎥 Les films du moment ! 🎬')
    st.write('---')

    st.markdown("""<style>
        *{color:#B0B0B0;}
        .stSelectbox p{font-size:25px ; color:#5F9EA0}
        h1{text-align:center;}
        .e2wxzia0{margin: auto auto ;}
        .stMarkdown p{font-size:25px;}
        </style>""", unsafe_allow_html=True)
    
    col1,col2,col3 = st.columns([1,9,1])

    with col2 :

        language = st.selectbox('Affiner par langue originale',['Tous'] + ['Français', 'Anglais'], )
        st.text(' ')
        genre = st.selectbox('Affiner par genre', ['Tous'] + sorted(list(df['genre'].explode().unique())[:-1]))

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
            st.image('https://image.tmdb.org/t/p/original'+list(df['poster_path'])[i], width=200)
        with col2:
            st.markdown(list(df['title'])[i])
            st.text("🎭  " + " - ".join(list(df['genre'].iloc[i])) + " | 📆 " + str(df['release_date'].iloc[i]))
            st.text(list(df['overview'])[i])
            st.text("✅ " + str(round(df['vote_average'].iloc[i],1)) + " / 10")
        st.write('---')
# Page : Films du moment - END

def click_button(index_film):
    st.session_state['selected_index'] = int(index_film)

# Page : Recommandations - START
if "selected_index" not in st.session_state:
    st.session_state["selected_index"] = None

if page == "Recommandations":
    st.title("🚀 Recommandation de films 🎬")
    st.write('---')

    st.markdown("""<style>
        *{color:#B0B0B0;}
        .stSelectbox p{font-size:25px ; color:#5F9EA0}
        </style>""", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,12,2])
    with col2 :
        selected_movie = st.selectbox('Choisir un film pour la recommandation', df['title'], index= st.session_state['selected_index'], placeholder='Choisir un film')
    with col3 :    
        if selected_movie != None :
            st.image('https://image.tmdb.org/t/p/original'+df[df['title'] == selected_movie]['poster_path'].iloc[0], width=120)
    st.write('---')

    if selected_movie != None :
        selected_id = int(df[df['title'] == selected_movie]['id'].iloc[0])
        for i in range(3) :
            id = int(df[df['id'] == selected_id][f'reco_{i+1}'])
            serie = df[df['id'] == id]
            col1, col2 = st.columns([2,4])
            with col1:
                st.image('https://image.tmdb.org/t/p/original'+serie['poster_path'].iloc[0], width=200)
            with col2:
                st.markdown(serie['title'].iloc[0])
                st.text("🎭  " + " - ".join(serie['genre'].iloc[0]) + " | 📆 " + str(serie['release_date'].iloc[0]))
                st.text(serie['overview'].iloc[0])
                st.text("✅ " + str(round(serie['vote_average'].iloc[0],1)) + " / 10")
                st.button("Recommandations de ce film",key=f"button_{i}", on_click=click_button, args=[serie.index[0]])              
            st.write('---')

# Page : Recommandations - END

# Page : Liens Utiles - START
if page == "Liens utiles":
    st.title("😎 Liens utiles ✌")
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
