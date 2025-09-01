import pickle
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

def fetch_image(id):
    image_csv = pd.read_csv('images.csv')
    if id in image_csv['id'].values:
        url = image_csv.loc[image_csv['id'] == id,'link'].values[0]
        data = requests.get(url)
        if data.status_code == 200:
            image_data = BytesIO(data.content)
            return Image.open(image_data)
    return None

def recommended(style):
     index = styles[styles['productDisplayName'] == style].index[0]
#     if not index_series.empty:
     # index = index_series[0]
     distance = sorted(list(enumerate(simalrity[index])), reverse=True, key=lambda x:x[1])
     recommended_style = []
     recommended_image = []
     for i in distance[0:20]:
          style_name = styles.iloc[i[0]].productDisplayName
          style_id = styles.iloc[i[0]].id
          recommended_style.append(styles.iloc[i[0]].productDisplayName)
          recommended_image.append(fetch_image(style_id))
          # st.write((styles.iloc[i[0]].productDisplayName))
     return recommended_style,recommended_image
    
st.header("Fashion Style Recommendation System")
styles = pickle.load(open('pickleData/style_list.pkl','rb'))
simalrity = pickle.load(open('pickleData/similarity.pkl','rb')) 

style_list = styles['productDisplayName'].values
selection_style = st.selectbox("Select your Fashion",style_list)

if st.button('Show recommendation'):
     recommended_style,recommended_image  = recommended(selection_style)

     # col1,col2,col3,col4,col5 = st.columns(5)
     # with col1:
     #     st.text(recommended_style[0])
     #     st.image(recommended_image[0])
     # with col2:
     #     st.text(recommended_style[1])
     #     st.image(recommended_image[1])
     # with col3:
     #     st.text(recommended_style[2])
     #     st.image(recommended_image[2])
     # with col4:
     #     st.text(recommended_style[3])
     #     st.image(recommended_image[3])
     # with col5:
     #     st.text(recommended_style[4])
     #     st.image(recommended_image[4])

     num_recommendation = len(recommended_style)
     num_col = 5
     num_rows = -(-num_recommendation // num_col)
     for row in range(num_rows):
          cols = st.columns(num_col)
          for col in range(num_col):
               index = row * num_col + col
               if index < num_recommendation:
                    with cols[col]:
                         st.text(recommended_style[index])
                         st.image(recommended_image[index])

