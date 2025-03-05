import streamlit as st
from pykml import parser
from geopy.distance import geodesic

# Função para calcular a distância total de uma LineString em metros
def calcular_distancia_linestring(coordinates):
    distancia_total = 0.0
    for i in range(len(coordinates) - 1):
        ponto_atual = coordinates[i]
        proximo_ponto = coordinates[i + 1]
        distancia_total += geodesic(ponto_atual, proximo_ponto).meters
    return distancia_total

# Função para processar recursivamente pastas e subpastas
def processar_elemento(elemento):
    distancia_total = 0.0

    # Processa todas as LineStrings no elemento atual
    for line_string in elemento.findall(".//{http://www.opengis.net/kml/2.2}LineString"):
        coordinates = line_string.coordinates.text.strip().split()
        # Converter coordenadas para (latitude, longitude) e inverter a ordem
        coordinates = [tuple(map(float, coord.split(',')[:2][::-1])) for coord in coordinates]
        distancia_total += calcular_distancia_linestring(coordinates)

    # Processa todas as pastas (Folders) no elemento atual
    for folder in elemento.findall(".//{http://www.opengis.net/kml/2.2}Folder"):
        distancia_total += processar_elemento(folder)

    return distancia_total

# Função para ler o arquivo KML e processar todas as LineStrings
def processar_kml(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        root = parser.parse(arquivo).getroot()

    # Inicia o processamento recursivo a partir do root
    distancia_total = processar_elemento(root)
    return distancia_total

# Configuração do aplicativo Streamlit
st.title("Calculadora de Distância de Arquivos KML")
st.write("Este aplicativo calcula a distância total das LineStrings em um arquivo KML.")

# Upload do arquivo KML
uploaded_file = st.file_uploader("Carregue um arquivo KML", type=["kml"])

if uploaded_file is not None:
    # Salva o arquivo temporariamente para processamento
    with open("temp.kml", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Processa o arquivo KML
    distancia_total = processar_kml("temp.kml")
    
    # Exibe a distância total
    st.success(f"Distância total: {distancia_total:.2f} metros")
