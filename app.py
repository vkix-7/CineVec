# Import libraries
import streamlit as st
from dotenv import find_dotenv, dotenv_values
from urllib.request import urlopen
import os, sys
sys.path.insert(0, '../')
# from llama_index.embeddings import HuggingFaceEmbedding
# Uncomment the line above and comment the line below if you face an import error
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import requests

# Add helper client
from AtlasClient import AtlasClient

# Define variables

DB_NAME = 'sample_mflix'
COLLECTION_NAME = 'embedded_movies'
MODEL_MAPPINGS = {
    'BAAI/bge-small-en-v1.5' : {'embedding_attr' : 'plot_embedding_bge_small', 'index_name' : 'idx_plot_embedding_bge_small'},
    'sentence-transformers/all-mpnet-base-v2' : {'embedding_attr' : 'plot_embedding_mpnet_base_v2', 'index_name' : 'idx_plot_embedding_mpnet_base_v2'},
    'sentence-transformers/all-MiniLM-L6-v2' : {'embedding_attr' : 'plot_embedding_minilm_l6_v2', 'index_name' : 'idx_plot_embedding_minilm_l6_v2'},
}
# Initialization function
def initialize():
    config = dotenv_values(find_dotenv())

    ATLAS_URI = config.get('ATLAS_URI')
    print(f"ATLAS_URI detected is: {ATLAS_URI}")

    if not ATLAS_URI:
        raise Exception ("'ATLAS_URI' is not set. Please set it in .env before continuing...")

    ip = urlopen('https://api.ipify.org').read()
    print (f"My public IP is '{ip}.  Make sure this IP is allowed to connect to cloud Atlas")

    os.environ['LLAMA_INDEX_CACHE_DIR'] = os.path.join(os.path.abspath('../'), 'cache')

    st.session_state.atlas_client = AtlasClient(ATLAS_URI, DB_NAME)
    print ('Atlas client succesfully initialized!')

# Query function
def run_vector_query (query, model_name):
    output_container = st.empty()
    
    model_mapping = MODEL_MAPPINGS.get(model_name)
    embedding_attr = model_mapping['embedding_attr']
    index_name = model_mapping ['index_name']

    with output_container.container():
        st.write (f'Running query for: {query}')

        # Generate embeddings for the given query
        embed_model = HuggingFaceEmbedding(model_name = model_name)
        query_embeddings = embed_model.get_text_embedding(query)
        st.write (f"Generated embeddings for the given query: {query_embeddings [:5]}...")

        movies = st.session_state.atlas_client.vector_search(collection_name = COLLECTION_NAME, 
                                    index_name = index_name, 
                                    attr_name = embedding_attr, 
                                    embedding_vector = query_embeddings, 
                                    limit = 5)

        st.write (f"Found {len (movies)} movies")
        for idx, movie in enumerate (movies):
            md_str =  (f"""
                        - Movie {idx+1}
                        - Title: {movie["title"]}
                        - Year: {movie["year"]}
                        - Plot: {movie["plot"]}
                        """)
            st.markdown(md_str)

# Configuring the display
# Initiatize only once
if 'atlas_client' not in st.session_state:
    initialize()

# Streamlit App
st.title("Movie Recommender System using Hugging Face embedding model. ")

# Poster placeholder
st.image("banner-image.png", use_column_width=True)

# User Input: Search Query
user_query = st.text_input("What do you feel like watching today?:")

# User Input: Model Selection
selected_model = st.selectbox("Choose an embedding model:", list(MODEL_MAPPINGS.keys()))

# Button to trigger the recommendation
if st.button("Recommend Movies"):
    output_container = st.container()
    search_result = run_vector_query(user_query, selected_model)