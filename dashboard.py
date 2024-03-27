import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Préparation et Configuration Initiale
# Titre de la page (WCAG 2.4.2)
st.set_page_config(page_title="Résumé des Analyses CNN", page_icon="📈")

# Fonction de chargement des données
@st.cache_data
def load_data():
    return pd.read_csv('cnn_daily_t5.csv')

def generate_boxplot(df):
    # Créer une figure et des axes pour Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    length_data = {
        'Article': df['article'].apply(len),
        'Résumé': df['highlights'].apply(len),
        'Résumé T5': df['t5_summary'].apply(len)
    }
    length_df = pd.DataFrame(length_data)
    sns.boxplot(data=length_df, ax=ax)
    ax.set_title('Comparaison de la longueur des textes')
    ax.set_ylabel('Nombre de caractères')
    ax.set_xlabel('Textes')
    # Passer la figure à Streamlit
    st.pyplot(fig)

def generate_wordcloud(text):
    # Créer une figure pour le nuage de mots
    fig, ax = plt.subplots(figsize=(10, 5))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Désactiver les axes pour le nuage de mots
    # Passer la figure à Streamlit
    st.pyplot(fig)


# 2. Chargement des Données
df = load_data()

# Titre du tableau de bord
st.title("Dashboard d'analyse des résumés CNN")

# Description pour le contenu non textuel (WCAG 1.1.1)
st.markdown("""
    Ce dashboard présente des analyses sur les résumés d'articles du dataset CNN. Les graphiques ci-dessous permettent d'explorer les caractéristiques des résumés générés par différents modèles.
""")

# Ajouter une note sur le contraste des couleurs et le redimensionnement du texte (WCAG 1.4.3, 1.4.4)
st.markdown("""
    **Note:** Vous pouvez zoomer dans les graphiques pour une meilleure lecture, et les couleurs ont été choisies pour garantir un contraste suffisant.
""")

# Instructions sur la manière de naviguer dans le tableau de bord pour les utilisateurs (accessibilité)
st.markdown("""
    **Navigation dans le Dashboard:** Utilisez les widgets sur le côté pour filtrer les résultats et interagir avec les graphiques.
""")

# 3. Création de Widgets d'Interaction Utilisateur
st.header("Longueur des Résumés")
generate_boxplot(df)  # Affiche directement le graphique de longueur des résumés

st.header("Nuage de Mots des Résumés")
summary_type = st.radio("Choisissez le type de résumé :", ('article', 'highlights', 't5_summary'))
if st.button('Générer le nuage de mots'):
    all_text = ' '.join(df[summary_type])
    generate_wordcloud(all_text)



    # Initialisation des états de session pour conserver les textes
if 'article_text' not in st.session_state:
    st.session_state.article_text = ""
if 'summary_text' not in st.session_state:
    st.session_state.summary_text = ""

# Titre de la nouvelle section
st.header("Explorer un Article Spécifique")

# Champ de texte pour l'entrée de l'utilisateur
user_input = st.text_input("Entrez un numéro de ligne entre 1 et {}".format(len(df)), "")

# Fonction pour mettre à jour le texte de l'article
def show_article():
    line_number = int(user_input) - 1
    st.session_state.article_text = df.loc[line_number, 'article']

# Fonction pour mettre à jour le texte du résumé T5
def show_summary():
    line_number = int(user_input) - 1
    st.session_state.summary_text = df.loc[line_number, 't5_summary']

# Vérification de la validité de l'entrée de l'utilisateur et affichage des boutons
if user_input.isdigit():
    line_number = int(user_input) - 1
    if 0 <= line_number < len(df):
        # Boutons pour afficher les textes sans annuler l'autre
        if st.button('Afficher Article'):
            show_article()
        if st.button('Afficher Résumé T5'):
            show_summary()
    else:
        st.error("Le numéro de ligne doit être entre 1 et {}.".format(len(df)))
else:
    st.error("Veuillez entrer un nombre valide.")

# Zones de texte pour afficher l'article et le résumé
st.text_area("Article", st.session_state.article_text, height=200)
st.text_area("Résumé T5", st.session_state.summary_text, height=200)




