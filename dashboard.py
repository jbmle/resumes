import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# Préparation et Configuration Initiale
# Titre de la page (WCAG 2.4.2)
st.set_page_config(page_title="Articles et Résumés CNN/Daily Mail", page_icon="📈")

# Fonction de chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('cnn_daily_t5.csv')
    # Calculer la longueur des textes
    df['article_length'] = df['article'].apply(len)
    df['highlights_length'] = df['highlights'].apply(len)
    df['t5_summary_length'] = df['t5_summary'].apply(len)
    return df

def generate_wordcloud(text):
    # Créer une figure pour le nuage de mots
    fig, ax = plt.subplots(figsize=(10, 5))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Désactiver les axes pour le nuage de mots
    # Passer la figure à Streamlit
    st.pyplot(fig)


# Chargement des Données
df = load_data()

# Titre du tableau de bord
st.title("Dashboard d'Analyse de la Génération de Résumés avec T5 du Dataset CNN/Daily Mail")

# Description pour le contenu non textuel (WCAG 1.1.1)
st.markdown("""
    Ce dashboard présente des analyses sur les articles et résumés du dataset CNN/Daily Mail. Les graphiques ci-dessous permettent d'explorer les caractéristiques des articles, des résumés d'origine et des résumés générés par T5.
""")

# Ajouter une note sur le contraste des couleurs et le redimensionnement du texte (WCAG 1.4.3, 1.4.4)
st.markdown("""
    **Note:** Vous pouvez zoomer dans les graphiques pour une meilleure lecture, et les couleurs ont été choisies pour garantir un contraste suffisant.
""")

# Instructions sur la manière de naviguer dans le tableau de bord pour les utilisateurs (accessibilité)
st.markdown("""
    **Navigation dans le Dashboard:** Utilisez les widgets sur le côté pour filtrer les résultats et interagir avec les graphiques.
""")

# Graphique pour la longueur des textes
st.header("Distribution de la Longueur des Textes")

colors = {
    'article': '#FF5733',  # Rouge
    'highlights': '#33C4FF',  # Bleu
    't5_summary': '#75FF33'  # Vert
}

text_type_aliases = {
    'article': 'Article',
    'highlights': 'Résumé d\'origine',
    't5_summary': 'Résumé T5'
}

# type_texte = st.selectbox('Choisissez le type de texte', ['article', 'highlights', 't5_summary'])
type_texte = st.selectbox('Choisissez le type de texte', list(text_type_aliases.keys()), format_func=lambda x: text_type_aliases[x])

if type_texte:
    fig, ax = plt.subplots()
    sns.histplot(df[f'{type_texte}_length'], bins=30, ax=ax, color=colors[type_texte])
    ax.set_xlabel('Longueur')
    ax.set_ylabel('Nombre de textes')
    ax.set_title(f'Distribution de la longueur des {text_type_aliases[type_texte]}')  # Utiliser l'alias
    st.pyplot(fig)


st.header("Nuage de Mots des Textes")
summary_type = st.radio(
    "Choisissez le type de résumé :",
    list(text_type_aliases.keys()),  # Les clés sont les valeurs techniques
    format_func=lambda x: text_type_aliases[x]  # Les alias pour l'affichage
)
if st.button('Générer le nuage de mots'):
    all_text = ' '.join(df[summary_type])
    generate_wordcloud(all_text)

# Exploration des articles et des résumés
st.header("Explorer un Article Spécifique et ses Résumés")
st.subheader("Entrer un numéro d'article entre 1 et {}".format(len(df)), "")


article_number = st.number_input('Entrez le numéro de l\'article', min_value=0, max_value=len(df)-1, value=0)
if article_number:
    st.text_area('Article', df.iloc[article_number]['article'], height=150)
    st.text_area('Résumé d\'origine', df.iloc[article_number]['highlights'], height=100)
    st.text_area('Résumé T5', df.iloc[article_number]['t5_summary'], height=100)




