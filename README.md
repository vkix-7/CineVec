# Movie-Recommender-application
Movie Recommendation System is a Python Application  with Collaborative Filtering and Vector Search Using MongoDB database, HuggingFace embeded Models , and Python Streamlit Library 
<b><br>Movie Recommendation System with Collaborative Filtering and Vector Search:</b><br>
This project presents a movie recommendation system that combines both collaborative filtering and vector search techniques to recommend movies to users.<br>
The core dataset includes 11,506 American movies released between 1970 and 2023, along with ratings from 11,675 users.<br>
To address the cold-start problem, the system employs vector embeddings generated using the Sentence Transformer model. These embeddings capture semantic information beyond explicit ratings, allowing similarity comparisons even for unseen movies or users.<br>
Additionally, the project explores hybrid filtering (under development), combining collaborative filtering with content-based filtering to potentially improve recommendation accuracy.<br>
The vector search component uses Chroma DB, an open-source vector database, to store and retrieve movie and user embeddings1.<br>
<b>Movie Recommendation System using KNN and Text Vectorization:</b>
This movie recommender system recommends five movies based on a given movie input.<br>
It utilizes a K-Nearest Neighbors (KNN) model that operates on concept text vectorization.<br>
The model leverages Hugging Face embeddings to create vector representations for movies, enabling efficient similarity comparisons and personalized recommendations2.<br>
Feel free to explore either of these approaches based on your project requirements! 😊🎥<br>
