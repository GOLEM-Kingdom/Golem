pip install -r 'root/requirements.txt'

import streamlit as st
import urllib.parse
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import googlemaps
from wordcloud import WordCloud

df_KH = pd.read_csv('result.csv')
df_rating = pd.read_csv('2_Reviews.csv')


new_row = pd.DataFrame({'ID':['9999999'],'Restaurant':['Chọn nhà hàng để phân tích']})

df_KH = pd.concat([df_KH,new_row], ignore_index=True)
default_index = df_KH.index[df_KH.Restaurant == 'Chọn nhà hàng để phân tích'][0]

def findcomment(id):
  max_row_index = df_rating[df_rating['IDRestaurant'] == id]['Rating'].idxmax()
  comment_maxrank = df_rating.loc[max_row_index]['Comment']
  max_rank = df_rating.loc[max_row_index]['Rating']

  min_row_index = df_rating[df_rating['IDRestaurant'] == id]['Rating'].idxmin()
  comment_minrank = df_rating.loc[min_row_index]['Comment']
  min_rank = df_rating.loc[min_row_index]['Rating']

  return comment_minrank, comment_maxrank, min_rank, max_rank


selected = st.sidebar.selectbox("Chọn nhà hàng để phân tích", df_KH['Restaurant'], index = int(default_index))
rest_selected = df_KH[df_KH.Restaurant == selected]
if selected == 'Chọn nhà hàng để phân tích':
    st.title("WELLCOME TO")
    st.title("RESTAURANT ANALYSIS!!!!!!!")
    st.subheader('Chào bạn, mình là Remy nhà phê bình ẩm thực, mình sẽ giúp bạn quyết định có nên đặt món ở nhà hàng đó không!')
    st.markdown("![Alt Text](https://64.media.tumblr.com/2374e4a72a250144f743db1170dacd6e/b941d54a3f515403-18/s540x810/2709a9f4d51a278ae9eaf33a6834b251b307a4d7.gifv)")
else:
    st.title(selected)
    st.write('Địa chỉ: ',rest_selected['Address'].iloc[0])
    
    API_KEY = 'AIzaSyBgTyUDMiqNoi0oNEeyqe9uXzLCKXKoE7Q'
    map_client = googlemaps.Client(API_KEY)

    work_place_address = rest_selected['Address'].iloc[0]
    response = map_client.geocode(work_place_address)

    lat_ = response[0]['geometry']['location']['lat']
    lng_ = response[0]['geometry']['location']['lng']

    df_map = pd.DataFrame({'lat':[lat_],'lon':[lng_]})

    st.write('Location: ',lat_,lng_)
    st.map(df_map,size=20,zoom=16)
    
    st.write('Thời gian mở cửa: ',rest_selected['Time'].iloc[0])
    st.write('\n Giá tiền: ',rest_selected['Price'].iloc[0])
    st.write('\n Phân phối của xếp hạng nhà hàng \n')

    chart1 = df_rating[df_rating['IDRestaurant'] == rest_selected['ID'].iloc[0]]['Rating']

    fig = plt.figure(figsize=(8, 4))
    sn.histplot(chart1, kde=True, bins=10, color='skyblue', edgecolor='black')
    plt.title('Histogram')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    st.pyplot(fig)
    
    cmt_min,cmt_max, min_rank, max_rank = findcomment(rest_selected['ID'].iloc[0])
    st.write('\nReview có điểm rank cao nhất: \n',max_rank,'\n', cmt_max)
    st.write('\nReview có điểm rank thấp nhất: \n',min_rank,'\n', cmt_min)

    nhom = df_KH[df_KH['ID'] == rest_selected['ID'].iloc[0]]['cluster'].iloc[0]
    st.write('\nNhóm nhà hàng được phân loại: ',nhom)
    

    cmt_process = df_KH[df_KH['ID'] == rest_selected['ID'].iloc[0]]['Comment_processed'].iloc[0]
    wc_like=WordCloud(
            background_color='black',
            max_words=500)
    wc_like.generate(cmt_process)

    st.write('\nNội dung chính trong các comment trong review: \n')
    fig = plt.figure(figsize=(12,12))
    plt.imshow(wc_like,interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)

    if nhom == 'Chất lượng tốt':
        st.write('\n\nĐây là một nhà hàng tốt, bạn hãy đến ăn thử!')
        st.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExY29uYXpob3IzM25nYTg4em9scTJ3ZHV2N3Rrbm9nenVxcmtjMTgwOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/97ZWlB7ENlalq/giphy.gif)")
    elif nhom == 'Chất lượng trung bình':
        st.write('\n\nĐây là một nhà hàng trung bình, bạn có thể thử nếu thích!')
        st.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHp2MXV3N29lcDJyZjh3aXNhN3Z0YjdzbWUzZWF5NGVvY2ZvNjB3bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QX6anVBPOfabwB7rSQ/giphy.gif)")
    else:
        st.write('\n\nĐây là một nhà hàng tệ, bạn không nên thử')
        st.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmI2dGw1OTZxdzZ1eTBmbzF1Ynl1dTRqdHplY3FldHR5Yzh6ejhuYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VfSYx0y0jAQBlaLrMb/giphy.gif)")
