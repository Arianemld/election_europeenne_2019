import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px


#st.balloons()
st.write(st.__version__)

#lien google pour le fichier xls
sheet_url = "https://docs.google.com/spreadsheets/d/11r5ihSDfzZ0kgieQZwUHq73gQRAodCmB061up1n2d9s/export?format=xlsx"
df1 = pd.read_excel(sheet_url)
st.write(st.__version__)


page = st.sidebar.selectbox("Sélectionnez une page", ["Introduction", "Exploration des données", "Analyse des taux de participation", "Répartition des voix par parti", "Uber data"])
image_url = "https://media.licdn.com/dms/image/v2/C560BAQHDVCW9BFYrbQ/company-logo_200_200/company-logo_200_200/0/1641975959299/efrei_logo?e=1735776000&v=beta&t=zhHwwLIe4ZmyMUdOv7ELIuIh_rfVhASiQ-hrL-sPwBY"

if page == "Introduction":
    st.title("Introduction")
    st.markdown(
        "Actuellement en première année de master en ingénierie des données, il nous a été demandé de réaliser un projet de visualisation de données. Pour ce projet, j'ai choisi de travailler sur le jeu de données « Élections européennes 2019 » disponible sur le site data.gouv.fr. Ce jeu de données a particulièrement retenu mon attention en raison de l'importance des élections européennes pour l'analyse des dynamiques politiques et sociales à travers les régions. J'ai également pensé qu'il me permettrait de jouer avec la localisation des données, en explorant les tendances géographiques des votes. Grâce à Streamlit, j'ai pu créer plusieurs visualisations interactives, que j'interpréterai dans les sections suivantes.")
    st.markdown(
        "La visualisation des données est un outil essentiel dans l'analyse de l'information, car elle rend les données complexes plus accessibles et compréhensibles. En transformant des chiffres bruts en graphiques et cartes interactifs, elle facilite l'identification de tendances, d'anomalies et de corrélations, parfois invisibles dans les tableaux de données classiques. Grâce à ces représentations visuelles, nous pouvons non seulement explorer les données de manière plus intuitive, mais aussi communiquer les résultats de manière claire et percutante. Cela permet de prendre des décisions plus éclairées et de présenter des analyses approfondies à un large public, qu'il s'agisse d'experts ou de non-initiés.")

    ###################Sidebar#########################
    st.sidebar.header("Ariane Mailanandam")
    st.sidebar.image(image_url, use_column_width=True)
    email = st.sidebar.write("**📧** : ariane.mailanandam@efrei.net")
    location = st.sidebar.write("📍: Ile-de-France")

    linkedin_url = "https://www.linkedin.com/in/ariane-mailanandam-data-science/"  # Remplace par ton lien LinkedIn
    st.sidebar.markdown(f"""
        <div style="border: 2px solid #0e76a8; padding: 10px; text-align: center; border-radius: 10px; margin-bottom: 20px;">
            <a href="{linkedin_url}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width:40px; height:40px;">
            </a>
            <p><a href="{linkedin_url}" target="_blank" style="text-decoration:none; color:#0e76a8;">My LinkedIn profil</a></p>
        </div>
    """, unsafe_allow_html=True)

    # CV button with the same size and style as LinkedIn
    cv_url = "https://drive.google.com/uc?export=download&id=1Gs6fYP05lfgBcjIbgc-3IlZjItscDApT"  # Remplace ID_DU_FICHIER par ton propre ID Google Drive
    st.sidebar.markdown(f"""
        <div style="border: 2px solid #0e76a8; padding: 10px; text-align: center; border-radius: 10px;">
            <a href="{cv_url}" download>
                <button style="padding:10px; border-radius:5px; background-color:#0e76a8; border:none; color: white; width: 100%;">
                    📄 Télécharger mon CV
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

elif page =="Exploration des données":
    ####################Présentation de la bdd#########################
    st.subheader("Présentation de la base de donnée")
    # st.title("Département:")

    st.markdown("Avant suppression des colonnes : ")
    st.write(df1)
    st.subheader("Nettoyage des données :")
    st.markdown("De nombreuses colonnes n'ont pas été identifiées. J'ai donc procédé à une analyse détaillée de chacune d'entre elles afin d'en extraire les colonnes contenant le nombre de voix obtenues par chaque parti dans un département spécifique lors des élections européennes.")

    # On garde les colonnes qui me parait plus pertinant
    df1.rename(columns={'Code du département': 'code_dep',
                        'Libellé du département': 'lib_dep',
                        'Inscrits': 'inscrits',
                        'Abstentions': 'abstentions',
                        'Votants': 'votants',
                        'Blancs': 'blancs',
                        'Nuls': 'nuls',
                        'Exprimés': 'exprimes',
                        'Voix': 'LFI',
                        'Unnamed: 48': 'LREM',
                        'Unnamed: 97': 'PP',
                        'Unnamed: 174': 'RN',
                        'Unnamed: 216': 'LR',
                        'Unnamed: 223': 'EEV'

                        }, inplace=True)

    df1 = df1[['code_dep', 'lib_dep', 'inscrits', 'abstentions',
               'votants', 'blancs', 'nuls', 'exprimes',
               'LFI', 'PP', 'EEV', 'LREM', 'LR', 'RN']]

    st.markdown("Voici le résultat après suppression des colonnes inutiles : ")
    st.write(df1)

    st.subheader("Statistiques :")
    # Total inscrit
    total_inscrits = df1["inscrits"].sum()
    st.subheader("Total enregistré en France")
    st.write(f"Le nombre total d'inscriptions sur l'ensemble du territoire français est de : {total_inscrits}")

    totaux = {
        'Inscrits': df1['inscrits'].sum(),
        'Votants': df1['votants'].sum(),
        'Abstentions': df1['abstentions'].sum(),
        'Blancs': df1['blancs'].sum(),
        'Nuls': df1['nuls'].sum(),
        'Exprimés': df1['exprimes'].sum()
    }

    # Convertir en DataFrame pour faciliter la visualisation

    totaux_df = pd.DataFrame(list(totaux.items()), columns=['Catégorie', 'Total'])
    st.subheader("Totaux des électeurs inscrits, des électeurs qui se sont abstenus, etc.")
    fig = px.bar(totaux_df, x='Catégorie', y='Total')
    st.plotly_chart(fig)

    # Votant et non votant
    total_inscrits = df1['inscrits'].sum()
    total_votants = df1['votants'].sum()
    total_non_votants = total_inscrits - total_votants

    # Créer un graphique en barres interactif pour afficher les votants et non-votants
    fig = go.Figure(data=[go.Bar(
        x=['Votants', 'Non-Votants'],
        y=[total_votants, total_non_votants],
        text=[f'{(total_votants / total_inscrits) * 100:.1f}%', f'{(total_non_votants / total_inscrits) * 100:.1f}%'],
        textposition='auto',
        hoverinfo='x+y+text',
        marker_color=['green', 'red']
    )])

    fig.update_layout(
        title="Total des votants et des non-votants en France",
        xaxis_title="Catégorie",
        yaxis_title="Nombre total",
        yaxis=dict(showgrid=True),
        width=800,
        height=600
    )
    st.plotly_chart(fig)

   #Camembert
    totaux = {
        'Votants': df1['votants'].sum(),
        'Abstentions': df1['abstentions'].sum(),
        'Blancs': df1['blancs'].sum(),
        'Nuls': df1['nuls'].sum(),
        'Exprimés': df1['exprimes'].sum()
    }

    labels = list(totaux.keys())
    sizes = list(totaux.values())
    colors = ['#2ca02c', '#ff7f0e', '#d62728', '#9467bd', '#8c564b']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title("Répartition des votants, des abstentions, des bulletins blancs, des bulletins nuls et des suffrages exprimés")
    st.pyplot(fig)


    #statistiques
    statistiques_generales = df1[['inscrits', 'votants', 'abstentions', 'blancs', 'nuls', 'exprimes']].describe()
    st.subheader("Statistiques descriptives générales")
    st.write(statistiques_generales)
    st.markdown("Le tableau vous donne un bon aperçu de la répartition des inscrits, des votants, des abstentions, des votes blancs, des votes nuls et des suffrages exprimés dans les 107 départements de votre jeu de données. Il indique la moyenne des données, la médiane, les écarts-types ainsi que les valeurs minimales et maximales pour chacun de ces indicateurs.")



elif page == "Analyse des taux de participation":
    st.title("Analyse des taux de participation")

    st.title("Département:")

    #On garde les colonnes qui me parait plus pertinant
    df1.rename(columns={'Code du département': 'code_dep',
                             'Libellé du département': 'lib_dep',
                             'Inscrits': 'inscrits',
                             'Abstentions': 'abstentions',
                             'Votants': 'votants',
                             'Blancs': 'blancs',
                             'Nuls': 'nuls',
                             'Exprimés': 'exprimes',
                             'Voix': 'LFI',
                             'Unnamed: 48': 'LREM',
                             'Unnamed: 97': 'PP',
                             'Unnamed: 174': 'RN',
                             'Unnamed: 216': 'LR',
                             'Unnamed: 223': 'EEV'

                             }, inplace=True)

    df1 = df1[['code_dep', 'lib_dep', 'inscrits', 'abstentions',
                         'votants', 'blancs', 'nuls', 'exprimes',
                         'LFI', 'PP', 'EEV', 'LREM', 'LR', 'RN']]


    #type de Vote pour chaque département
    vote = df1[['lib_dep', 'abstentions', 'votants', 'blancs']]

    df_melted = vote.melt(id_vars=['lib_dep'], value_vars=['abstentions', 'votants', 'blancs'],
                         var_name='Type de vote', value_name='Nombre')

    fig = px.bar(
        df_melted,
        x='lib_dep',
        y='Nombre',
        color='Type de vote',
        title='Répartition des abstentions, votants et votes blancs par département',
        labels={'lib_dep': 'Département', 'Nombre': 'Nombre de personnes'},
        barmode='stack',
        text='Nombre'
    )
    fig.update_layout(xaxis_tickangle=-45)

    fig.update_layout(
        xaxis_tickangle=-45,
        width=1200,
        height=700
    )
    st.plotly_chart(fig)

    #Département qui ont le plus voté et le moins
    df1['taux_participation'] = (df1['votants'] / df1['inscrits']) * 100

    dep_max_participation = df1.loc[df1['taux_participation'].idxmax()]
    dep_min_participation = df1.loc[df1['taux_participation'].idxmin()]

    st.subheader("Département avec le plus fort taux de participation")
    st.write(
        f"Département : {dep_max_participation['lib_dep']} - Taux de participation : {dep_max_participation['taux_participation']:.2f}%")

    dep_name = dep_max_participation['lib_dep']
    votants = dep_max_participation['votants']
    abstentions = dep_max_participation['abstentions']
    blancs = dep_max_participation['blancs']

    fig = go.Figure(data=[go.Bar(
        x=['Votants', 'Abstentions', 'Blancs'],
        y=[votants, abstentions, blancs],
        text=[votants, abstentions, blancs],
        textposition='auto',
        marker_color=['green', 'red', 'blue']
    )])

    fig.update_layout(
        title=f"Répartition des votes dans le département {dep_name} (taux de participation : {dep_max_participation['taux_participation']:.2f}%)",
        xaxis_title="Type de vote",
        yaxis_title="Nombre total",
        yaxis=dict(showgrid=True),
        width=800,
        height=600
    )

    st.plotly_chart(fig)

    st.subheader("Département avec le plus faible taux de participation")
    st.write(
        f"Département : {dep_min_participation['lib_dep']} - Taux de participation : {dep_min_participation['taux_participation']:.2f}%")

    #Graphe pour le min
    dep_name_min = dep_min_participation['lib_dep']
    votants_min = dep_min_participation['votants']
    abstentions_min = dep_min_participation['abstentions']
    blancs_min = dep_min_participation['blancs']

    fig_min = go.Figure(data=[go.Bar(
        x=['Votants', 'Abstentions', 'Blancs'],
        y=[votants_min, abstentions_min, blancs_min],
        text=[votants_min, abstentions_min, blancs_min],
        textposition='auto',
        marker_color=['green', 'red', 'blue']
    )])

    fig_min.update_layout(
        title=f"Répartition des votes dans le département {dep_name_min} (taux de participation : {dep_min_participation['taux_participation']:.2f}%)",
        xaxis_title="Type de vote",
        yaxis_title="Nombre total",
        yaxis=dict(showgrid=True),
        width=800,
        height=600
    )

    st.plotly_chart(fig_min)

    #Heatmap

    departement_coords = {
        "Ain": [46.2044, 5.2257],
        "Aisne": [49.5686, 3.3609],
        "Allier": [46.3416, 3.1985],
        "Alpes-de-Haute-Provence": [44.0666, 6.2314],
        "Hautes-Alpes": [44.5630, 6.2519],
        "Alpes-Maritimes": [43.9367, 7.2620],
        "Ardèche": [44.7951, 4.3702],
        "Ardennes": [49.7613, 4.7074],
        "Ariège": [43.0323, 1.5555],
        "Aube": [48.3284, 4.0794],
        "Aude": [43.1575, 2.3997],
        "Aveyron": [44.2778, 2.5297],
        "Bouches-du-Rhône": [43.4477, 5.4000],
        "Calvados": [49.0802, -0.3806],
        "Cantal": [45.0150, 2.5200],
        "Charente": [45.6913, 0.1590],
        "Charente-Maritime": [45.8750, -0.9513],
        "Cher": [47.0652, 2.3962],
        "Corrèze": [45.2736, 1.7888],
        "Corse-du-Sud": [41.5917, 8.9961],
        "Haute-Corse": [42.2097, 9.1813],
        "Côte-d'Or": [47.3167, 4.8283],
        "Côtes-d'Armor": [48.5146, -2.8871],
        "Creuse": [46.0735, 1.9984],
        "Dordogne": [45.1839, 0.7186],
        "Doubs": [47.2366, 6.0227],
        "Drôme": [44.7322, 4.8902],
        "Eure": [49.0379, 1.2110],
        "Eure-et-Loir": [48.4483, 1.4723],
        "Finistère": [48.2321, -4.2217],
        "Gard": [43.9174, 4.4200],
        "Haute-Garonne": [43.6047, 1.4442],
        "Gers": [43.6736, 0.5872],
        "Gironde": [44.8378, -0.5792],
        "Hérault": [43.6119, 3.8772],
        "Ille-et-Vilaine": [48.1173, -1.6778],
        "Indre": [46.6969, 1.4686],
        "Indre-et-Loire": [47.3936, 0.6897],
        "Isère": [45.1885, 5.7245],
        "Jura": [46.6754, 5.5744],
        "Landes": [43.9493, -0.5992],
        "Loir-et-Cher": [47.5895, 1.3361],
        "Loire": [45.4315, 4.3922],
        "Haute-Loire": [45.0428, 3.8844],
        "Loire-Atlantique": [47.2186, -1.5546],
        "Loiret": [47.9029, 1.9092],
        "Lot": [44.4475, 1.4403],
        "Lot-et-Garonne": [44.3517, 0.6381],
        "Lozère": [44.5196, 3.4998],
        "Maine-et-Loire": [47.4749, -0.5562],
        "Manche": [48.8323, -1.5275],
        "Marne": [49.0440, 4.0246],
        "Haute-Marne": [48.1110, 5.3302],
        "Mayenne": [48.3023, -0.6168],
        "Meurthe-et-Moselle": [48.6921, 6.1844],
        "Meuse": [48.9976, 5.3697],
        "Morbihan": [47.8004, -2.7771],
        "Moselle": [49.1193, 6.1757],
        "Nièvre": [47.0514, 3.6567],
        "Nord": [50.6292, 3.0573],
        "Oise": [49.4162, 2.8261],
        "Orne": [48.6196, 0.1113],
        "Pas-de-Calais": [50.4252, 2.8312],
        "Puy-de-Dôme": [45.7772, 3.0826],
        "Pyrénées-Atlantiques": [43.2951, -0.3708],
        "Hautes-Pyrénées": [43.0987, 0.1677],
        "Pyrénées-Orientales": [42.6988, 2.8954],
        "Bas-Rhin": [48.5846, 7.7507],
        "Haut-Rhin": [47.7486, 7.3398],
        "Rhône": [45.7640, 4.8357],
        "Haute-Saône": [47.6239, 6.1535],
        "Saône-et-Loire": [46.7556, 4.8535],
        "Sarthe": [48.0077, 0.1996],
        "Savoie": [45.5646, 5.9178],
        "Haute-Savoie": [45.8992, 6.1294],
        "Paris": [48.8566, 2.3522],
        "Seine-Maritime": [49.4432, 1.0993],
        "Seine-et-Marne": [48.6082, 2.6021],
        "Yvelines": [48.7802, 1.9876],
        "Deux-Sèvres": [46.3230, -0.4545],
        "Somme": [49.9219, 2.3007],
        "Tarn": [43.8939, 2.1499],
        "Tarn-et-Garonne": [44.0068, 1.3555],
        "Var": [43.4667, 6.2211],
        "Vaucluse": [44.0563, 5.0501],
        "Vendée": [46.6705, -1.4269],
        "Vienne": [46.5802, 0.3404],
        "Haute-Vienne": [45.8350, 1.2624],
        "Vosges": [48.2156, 6.4238],
        "Yonne": [47.7973, 3.5674],
        "Territoire de Belfort": [47.6383, 6.8628],
        "Essonne": [48.6314, 2.2379],
        "Hauts-de-Seine": [48.8607, 2.2435],
        "Seine-Saint-Denis": [48.9356, 2.3535],
        "Val-de-Marne": [48.7920, 2.4712],
        "Val-d'Oise": [49.0514, 2.1160],
        "Guadeloupe": [16.9950, -62.0671],
        "Martinique": [14.6415, -61.0242],
        "Guyane": [4.9372, -52.3262],
        "La Réunion": [-21.1151, 55.5364],
        "Mayotte": [-12.8275, 45.1662]
    }

    top5_votants = df1.nlargest(20, 'votants')
    bottom5_votants = df1.nsmallest(20, 'votants')

    # Créer la carte centrée sur la France
    map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter les départements avec le plus de votants à la carte
    for index, row in top5_votants.iterrows():
        departement_name = row['lib_dep']
        if departement_name in departement_coords:
            lat, lon = departement_coords[departement_name]
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                popup=f"Top votants - {departement_name}: {row['votants']} votants",
                color="blue",
                fill=True,
                fill_color="blue"
            ).add_to(map)

    # Ajouter les départements avec le moins de votants à la carte
    for index, row in bottom5_votants.iterrows():
        departement_name = row['lib_dep']
        if departement_name in departement_coords:
            lat, lon = departement_coords[departement_name]
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                popup=f"Moins votants - {departement_name}: {row['votants']} votants",
                color="red",
                fill=True,
                fill_color="red"
            ).add_to(map)

    # Ajouter une légende à la carte
    legend_html = '''
    <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 150px; height: 90px; 
         background-color: white; border:2px solid grey; z-index:9999; font-size:14px;">
         &nbsp;<b>Légende</b><br>
         &nbsp;<i class="fa fa-circle" style="color:blue"></i>&nbsp;Top votants<br>
         &nbsp;<i class="fa fa-circle" style="color:red"></i>&nbsp;Moins votants
    </div>
    '''

    map.get_root().html.add_child(folium.Element(legend_html))

    # Afficher la carte dans Streamlit
    st.title("Répartition des Départements avec le Plus et le Moins de Votants")
    st_folium(map, width=700, height=500)




elif page == "Répartition des voix par parti":


    # On garde les colonnes qui me parait plus pertinant
    df1.rename(columns={'Code du département': 'code_dep',
                        'Libellé du département': 'lib_dep',
                        'Inscrits': 'inscrits',
                        'Abstentions': 'abstentions',
                        'Votants': 'votants',
                        'Blancs': 'blancs',
                        'Nuls': 'nuls',
                        'Exprimés': 'exprimes',
                        'Voix': 'LFI',
                        'Unnamed: 48': 'LREM',
                        'Unnamed: 97': 'PP',
                        'Unnamed: 174': 'RN',
                        'Unnamed: 216': 'LR',
                        'Unnamed: 223': 'EEV'

                        }, inplace=True)

    df1 = df1[['code_dep', 'lib_dep', 'inscrits', 'abstentions',
               'votants', 'blancs', 'nuls', 'exprimes',
               'LFI', 'PP', 'EEV', 'LREM', 'LR', 'RN']]

    departement_coords = {
        "Ain": [46.2044, 5.2257],
        "Aisne": [49.5686, 3.3609],
        "Allier": [46.3416, 3.1985],
        "Alpes-de-Haute-Provence": [44.0666, 6.2314],
        "Hautes-Alpes": [44.5630, 6.2519],
        "Alpes-Maritimes": [43.9367, 7.2620],
        "Ardèche": [44.7951, 4.3702],
        "Ardennes": [49.7613, 4.7074],
        "Ariège": [43.0323, 1.5555],
        "Aube": [48.3284, 4.0794],
        "Aude": [43.1575, 2.3997],
        "Aveyron": [44.2778, 2.5297],
        "Bouches-du-Rhône": [43.4477, 5.4000],
        "Calvados": [49.0802, -0.3806],
        "Cantal": [45.0150, 2.5200],
        "Charente": [45.6913, 0.1590],
        "Charente-Maritime": [45.8750, -0.9513],
        "Cher": [47.0652, 2.3962],
        "Corrèze": [45.2736, 1.7888],
        "Corse-du-Sud": [41.5917, 8.9961],
        "Haute-Corse": [42.2097, 9.1813],
        "Côte-d'Or": [47.3167, 4.8283],
        "Côtes-d'Armor": [48.5146, -2.8871],
        "Creuse": [46.0735, 1.9984],
        "Dordogne": [45.1839, 0.7186],
        "Doubs": [47.2366, 6.0227],
        "Drôme": [44.7322, 4.8902],
        "Eure": [49.0379, 1.2110],
        "Eure-et-Loir": [48.4483, 1.4723],
        "Finistère": [48.2321, -4.2217],
        "Gard": [43.9174, 4.4200],
        "Haute-Garonne": [43.6047, 1.4442],
        "Gers": [43.6736, 0.5872],
        "Gironde": [44.8378, -0.5792],
        "Hérault": [43.6119, 3.8772],
        "Ille-et-Vilaine": [48.1173, -1.6778],
        "Indre": [46.6969, 1.4686],
        "Indre-et-Loire": [47.3936, 0.6897],
        "Isère": [45.1885, 5.7245],
        "Jura": [46.6754, 5.5744],
        "Landes": [43.9493, -0.5992],
        "Loir-et-Cher": [47.5895, 1.3361],
        "Loire": [45.4315, 4.3922],
        "Haute-Loire": [45.0428, 3.8844],
        "Loire-Atlantique": [47.2186, -1.5546],
        "Loiret": [47.9029, 1.9092],
        "Lot": [44.4475, 1.4403],
        "Lot-et-Garonne": [44.3517, 0.6381],
        "Lozère": [44.5196, 3.4998],
        "Maine-et-Loire": [47.4749, -0.5562],
        "Manche": [48.8323, -1.5275],
        "Marne": [49.0440, 4.0246],
        "Haute-Marne": [48.1110, 5.3302],
        "Mayenne": [48.3023, -0.6168],
        "Meurthe-et-Moselle": [48.6921, 6.1844],
        "Meuse": [48.9976, 5.3697],
        "Morbihan": [47.8004, -2.7771],
        "Moselle": [49.1193, 6.1757],
        "Nièvre": [47.0514, 3.6567],
        "Nord": [50.6292, 3.0573],
        "Oise": [49.4162, 2.8261],
        "Orne": [48.6196, 0.1113],
        "Pas-de-Calais": [50.4252, 2.8312],
        "Puy-de-Dôme": [45.7772, 3.0826],
        "Pyrénées-Atlantiques": [43.2951, -0.3708],
        "Hautes-Pyrénées": [43.0987, 0.1677],
        "Pyrénées-Orientales": [42.6988, 2.8954],
        "Bas-Rhin": [48.5846, 7.7507],
        "Haut-Rhin": [47.7486, 7.3398],
        "Rhône": [45.7640, 4.8357],
        "Haute-Saône": [47.6239, 6.1535],
        "Saône-et-Loire": [46.7556, 4.8535],
        "Sarthe": [48.0077, 0.1996],
        "Savoie": [45.5646, 5.9178],
        "Haute-Savoie": [45.8992, 6.1294],
        "Paris": [48.8566, 2.3522],
        "Seine-Maritime": [49.4432, 1.0993],
        "Seine-et-Marne": [48.6082, 2.6021],
        "Yvelines": [48.7802, 1.9876],
        "Deux-Sèvres": [46.3230, -0.4545],
        "Somme": [49.9219, 2.3007],
        "Tarn": [43.8939, 2.1499],
        "Tarn-et-Garonne": [44.0068, 1.3555],
        "Var": [43.4667, 6.2211],
        "Vaucluse": [44.0563, 5.0501],
        "Vendée": [46.6705, -1.4269],
        "Vienne": [46.5802, 0.3404],
        "Haute-Vienne": [45.8350, 1.2624],
        "Vosges": [48.2156, 6.4238],
        "Yonne": [47.7973, 3.5674],
        "Territoire de Belfort": [47.6383, 6.8628],
        "Essonne": [48.6314, 2.2379],
        "Hauts-de-Seine": [48.8607, 2.2435],
        "Seine-Saint-Denis": [48.9356, 2.3535],
        "Val-de-Marne": [48.7920, 2.4712],
        "Val-d'Oise": [49.0514, 2.1160],
        "Guadeloupe": [16.9950, -62.0671],
        "Martinique": [14.6415, -61.0242],
        "Guyane": [4.9372, -52.3262],
        "La Réunion": [-21.1151, 55.5364],
        "Mayotte": [-12.8275, 45.1662]
    }


    parti = df1[['LFI', 'PP', 'EEV', 'LREM', 'LR', 'RN']]
    total_voix_par_parti = parti.sum()

    fig = px.pie(
        names=total_voix_par_parti.index,
        values=total_voix_par_parti.values,
        title="Répartition des voix par parti politique",
        labels={'names': 'Partis politiques', 'values': 'Nombre de voix'}
    )
    st.plotly_chart(fig)


    #Départements qui ont le plus et moins partcipé

    df1['taux_participation'] = (df1['votants'] / df1['inscrits']) * 100

    # Trier les départements par taux de participation
    df_sorted_participation = df1.sort_values('taux_participation', ascending=False)

    # Graphique pour les départements avec les taux de participation les plus hauts et les plus bas
    st.subheader("Départements avec les plus hauts et les plus bas taux de participation")

    # Graphique des 10 départements avec le plus haut taux de participation
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted_participation.head(10).plot(kind='bar', x='lib_dep', y='taux_participation', ax=ax, color='green')
    plt.title("Top 10 départements - Taux de participation")
    plt.ylabel("Taux de participation (%)")
    plt.xlabel("Département")
    st.pyplot(fig)

    # Graphique des 10 départements avec le plus bas taux de participation
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted_participation.tail(10).plot(kind='bar', x='lib_dep', y='taux_participation', ax=ax, color='red')
    plt.title("Bottom 10 départements - Taux de participation")
    plt.ylabel("Taux de participation (%)")
    plt.xlabel("Département")
    st.pyplot(fig)

    # Heatmap 2
    st.title("Carte des Partis Vainqueurs par Département")
    df1['parti_vainqueur'] = df1[['LFI', 'RN', 'LREM', 'LR', 'EEV']].idxmax(axis=1)

    # Assigner des couleurs aux partis
    parti_couleurs = {
        'LFI': 'blue',
        'RN': 'red',
        'LREM': 'yellow',
        'LR': 'green',
        'EEV': 'darkgreen'
    }

    # Créer la carte centrée sur la France
    map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter des markers pour chaque département avec la couleur correspondant au parti vainqueur
    for index, row in df1.iterrows():
        departement_name = row['lib_dep']
        parti_vainqueur = row['parti_vainqueur']
        couleur = parti_couleurs.get(parti_vainqueur, 'gray')  # Utiliser 'gray' si le parti n'est pas trouvé

        if departement_name in departement_coords:
            lat, lon = departement_coords[departement_name]
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                popup=f"{departement_name} - {parti_vainqueur}",
                color=couleur,
                fill=True,
                fill_color=couleur
            ).add_to(map)

    # Ajouter une légende personnalisée pour les couleurs des partis
    legend_html = '''
        <div style="position: fixed; 
             bottom: 50px; left: 50px; width: 150px; height: 150px; 
             background-color: white; z-index:9999; font-size:14px;
             border:2px solid grey; padding: 10px;">
             <b>Légende des partis</b><br>
             <i style="background: blue; width: 10px; height: 10px; display: inline-block;"></i> LFI<br>
             <i style="background: red; width: 10px; height: 10px; display: inline-block;"></i> RN<br>
             <i style="background: yellow; width: 10px; height: 10px; display: inline-block;"></i> LREM<br>
             <i style="background: green; width: 10px; height: 10px; display: inline-block;"></i> LR<br>
             <i style="background: darkgreen; width: 10px; height: 10px; display: inline-block;"></i> EEV<br>
        </div>
        '''
    map.get_root().html.add_child(folium.Element(legend_html))

    # Afficher la carte dans Streamlit
    st_folium(map, width=700, height=500)


    #Vainqueur des élections européennes 2019
    import matplotlib.pyplot as plt
    import streamlit as st

    # Totaux des voix pour chaque parti
    voix_totales = {
        'LFI': df1['LFI'].sum(),
        'RN': df1['RN'].sum(),
        'LREM': df1['LREM'].sum(),
        'LR': df1['LR'].sum(),
        'EEV': df1['EEV'].sum()
    }

    # Extraire les noms des partis et les totaux
    partis = list(voix_totales.keys())
    totaux_voix = list(voix_totales.values())

    # Créer un bar chart pour afficher les totaux des voix par parti
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(partis, totaux_voix, color=['blue', 'red', 'yellow', 'green', 'darkgreen'])

    # Ajouter des labels et un titre
    ax.set_xlabel("Partis")
    ax.set_ylabel("Total des voix")
    ax.set_title("Totaux des voix pour chaque parti aux élections européennes 2019")

    # Afficher les valeurs directement au-dessus de chaque barre
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:,}', ha='center', va='bottom')

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)


elif page == "Uber data":
    st.subheader("UBER DATA :")

    # Lien Google Sheets
    uber_sheet_url = "https://docs.google.com/spreadsheets/d/1WlQrDTQNHIKAomJhMnKdEWHXQUIhM_f1oyht_jqH93g/export?format=xlsx"

    # Chargement des données depuis Google Sheets avec pandas
    df2 = pd.read_excel(uber_sheet_url)

    # Conversion des dates
    df2['Date/Time'] = pd.to_datetime(df2['Date/Time'])
    st.write(df2)

    # Fonctions pour extraire des informations des dates
    def get_dom(dt):
        return dt.day

    def get_weekday(dt):
        return dt.weekday()

    def get_hour(dt):
        return dt.hour

    df2['day'] = df2['Date/Time'].map(get_dom)
    df2['weekday'] = df2['Date/Time'].map(get_weekday)
    df2['hour'] = df2['Date/Time'].map(get_hour)

    st.write(df2.head())

    # Histogramme des jours du mois
    st.write("Histogramme : Fréquence par jour du mois")
    fig, ax = plt.subplots()
    df2['day'].hist(bins=30, rwidth=0.8, range=(0.5, 30.5), ax=ax)
    ax.set_xlabel('Jours du mois')
    ax.set_title("Fréquence par jour du mois - Uber Avril 2014")
    st.pyplot(fig)

    # Compter les lignes par jour
    def count_rows(rows):
        return len(rows)

    by_date = df2.groupby('day').apply(count_rows)

    # Graphique en barre des fréquences par jour du mois
    st.write("Graphique en barre : Fréquence par jour du mois")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(1, 31), by_date.sort_values())
    ax.set_xticks(range(1, 31))
    ax.set_xticklabels(by_date.sort_values().index)
    ax.set_xlabel('Jours du mois')
    ax.set_ylabel('Fréquence')
    ax.set_title('Fréquence par jour du mois - Uber Avril 2014')
    st.pyplot(fig)

    # Histogramme des heures de la journée
    st.write("Histogramme : Fréquence par heure de la journée")
    fig, ax = plt.subplots()
    df2['hour'].hist(bins=24, range=(-0.5, 23.5), ax=ax)
    ax.set_xlabel('Heure de la journée')
    ax.set_ylabel('Fréquence')
    ax.set_title('Fréquence par heure - Uber Avril 2014')
    st.pyplot(fig)

    # Histogramme des jours de la semaine
    st.write("Histogramme : Fréquence par jour de la semaine")
    fig, ax = plt.subplots()
    df2['weekday'].hist(bins=7, rwidth=0.8, range=(-0.5, 6.5), ax=ax)
    ax.set_xlabel('Jour de la semaine')
    ax.set_ylabel('Fréquence')
    ax.set_title('Fréquence par jour de la semaine - Uber Avril 2014')
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'])
    st.pyplot(fig)

    # Heatmap des fréquences par jour et heure
    st.write("Heatmap : Fréquence par heure et jour de la semaine")
    df3 = df2.groupby(['weekday', 'hour']).apply(count_rows).unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df3, linewidths=.5, ax=ax)
    ax.set_yticklabels(['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'], rotation=0)
    ax.set_title('Heatmap par heure et jour de la semaine - Uber Avril 2014')
    st.pyplot(fig)

    # Histogrammes pour la latitude et la longitude
    st.write("Histogramme : Distribution des latitudes")
    fig, ax = plt.subplots()
    df2['Lat'].hist(bins=100, range=(40.5, 41), color='r', alpha=0.5, ax=ax)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Fréquence')
    ax.set_title('Distribution des latitudes - Uber Avril 2014')
    st.pyplot(fig)

    st.write("Histogramme : Distribution des longitudes")
    fig, ax = plt.subplots()
    df2['Lon'].hist(bins=100, range=(-74.1, -73.9), color='g', alpha=0.5, ax=ax)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Fréquence')
    ax.set_title('Distribution des longitudes - Uber Avril 2014')
    st.pyplot(fig)

    # Scatter plot des latitudes et longitudes
    st.write("Scatter plot : Distribution des latitudes et longitudes")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(df2['Lat'], df2['Lon'], s=0.8, alpha=0.4)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_ylim(-74.1, -73.8)
    ax.set_xlim(40.7, 40.9)
    ax.set_title('Scatter plot - Uber Avril 2014')
    st.pyplot(fig)












