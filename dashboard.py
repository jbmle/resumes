import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re


# Préparation et Configuration Initiale
# Titre de la page (WCAG 2.4.2)
st.set_page_config(page_title="Articles et Résumés CNN/Daily Mail", page_icon="📈")

# Fonction de chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('cnn_daily_t5.csv')
    #  Longueur des textes
    df['article_length'] = df['article'].apply(len)
    df['highlights_length'] = df['highlights'].apply(len)
    df['t5_summary_length'] = df['t5_summary'].apply(len)
    return df

def generate_wordcloud(text):
    fig, ax = plt.subplots(figsize=(10, 5))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Désactivation des axes pour le nuage de mots
    # Passer la figure à Streamlit
    st.pyplot(fig)

def calculate_word_frequencies(text_series):
    """Calcul de fréquences des mots, en excluant les mots de 1 lettre."""
    all_text = ' '.join(text_series).lower()
    all_text = re.sub(r'\W', ' ', all_text)  # Remplacement des non-mots par des espaces
    words = all_text.split()
    # Filtre des mots pour enlever les stop words et les mots d'une lettre
    words = [word for word in words if word not in STOPWORDS and len(word) > 1]
    word_counts = Counter(words)
    return word_counts.most_common(10)

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
    **Note:** Vous pouvez zoomer avec votre navigateur pour une meilleure lecture sans perte de contenu et les couleurs ont été choisies pour garantir un contraste suffisant.
""")

# Critère de succès 1.4.1 Utilisation de la couleur 
st.markdown("""
    D'autre part, les couleurs ne sont pas le seul moyen pour comprendre l'information de ces graphiques.
""")

# Instructions sur la manière de naviguer dans le tableau de bord pour les utilisateurs (accessibilité)
st.markdown("""
    **Navigation dans le Dashboard:** Utilisez les widgets sur le côté pour afficher uniquement les diagrammes. Utilisez le menu à 3 points en haut à droite si vous préférez un texte sur toute la largeur de l'écran ou un mode sombre.
""")

# Graphique pour la longueur des textes
st.header("Distribution de la Longueur des Textes")

colors = {
    'article': '#FF5733',  # Rouge
    'highlights': '#33C4FF',  # Bleu
    't5_summary': '#228B22'  # Vert
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


st.markdown("""
    Les distributions sont représentées avec des diagrammes en barres. La longueur des articles varie entre 1000 et 7000 mots. Les résumés d'origine du dataset varient de 100 à 350 caractères avec un pic autour de 150 caractères. Les résumés modélisés avec T5 varient de 100 à 400 caractères avec un pic autour de 250 caractères.
""")

st.header("Fréquence des Mots dans les Textes")

text_type = st.selectbox(
    "Choisissez le type de texte pour visualiser les mots fréquents",
    # options=["article", "highlights", "t5_summary"],
    # format_func=lambda x: x.capitalize()
    list(text_type_aliases.keys()), 
    format_func=lambda x: text_type_aliases[x]
)

# Calcul des fréquences des mots
word_freqs = calculate_word_frequencies(df[text_type])

# graphique
fig, ax = plt.subplots()
words, frequencies = zip(*word_freqs)
ax.bar(words, frequencies, color=colors[text_type])
ax.set_ylabel('Fréquence')
ax.set_title(f'10 mots les plus fréquents dans {text_type_aliases[text_type]}')
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("""
    Les mots les plus fréquents dans les articles sont : said(50 mots), cnn(25 mots), university, people, state, now, fraternity, boren, will, president.
""")
st.markdown("""
    Les mots les plus fréquents dans les résumes d'origine sont : university(5 mots), david, says et page (4 mots), president, boren, fraternity, clarkson, day, student.
""")
st.markdown("""
    Les mots les plus fréquents dans les résumes modélisés avec T5 sont : year (6 mots), university (5 mots), student (4 mots), video, fraternity, students, says, local, museum, one.
""")



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
st.subheader("Entrer un numéro d'article entre 1 et {}".format(len(df)-1), "")


article_number = st.number_input('Entrez le numéro de l\'article', min_value=0, max_value=len(df)-1, value=0)
if article_number:
    st.text_area('Article', df.iloc[article_number]['article'], height=150)
    st.text_area('Résumé d\'origine', df.iloc[article_number]['highlights'], height=100)
    st.text_area('Résumé T5', df.iloc[article_number]['t5_summary'], height=100)




