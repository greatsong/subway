import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 로드
csv_file_path = '2024년 05월  교통카드 통계자료.csv'
subway_data = pd.read_csv(csv_file_path)

# 데이터 전처리
subway_data_cleaned = subway_data.drop(0).reset_index(drop=True)

# Function to convert columns to integers and handle non-numeric values
def clean_numeric_column(column):
    return column.str.replace(',', '').apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

# Convert numerical columns to integers after removing commas
columns_to_convert = subway_data_cleaned.columns[4:]
for column in columns_to_convert:
    subway_data_cleaned[column] = clean_numeric_column(subway_data_cleaned[column])

# 전체 시간대에 대해 승하차 인원이 가장 많은 역 찾기
subway_data_cleaned['총 승차'] = subway_data_cleaned[columns_to_convert[::2]].sum(axis=1)
subway_data_cleaned['총 하차'] = subway_data_cleaned[columns_to_convert[1::2]].sum(axis=1)
subway_data_cleaned['총 승하차'] = subway_data_cleaned['총 승차'] + subway_data_cleaned['총 하차']
busiest_station = subway_data_cleaned.loc[subway_data_cleaned['총 승하차'].idxmax()]

# 시간대별 그래프 생성
time_periods = [col.split('~')[0][:2] for col in columns_to_convert[::2]]  # 시간대 2자리로 축약
boardings = busiest_station[columns_to_convert[::2]].values
alightings = busiest_station[columns_to_convert[1::2]].values

# 데이터 길이 일치 확인 및 처리
if len(alightings) < len(time_periods):
    alightings = list(alightings) + [0] * (len(time_periods) - len(alightings))

# 가장 바쁜 역 이름
busiest_station_name = busiest_station['지하철역']

# 시간대와 승하차 데이터 길이 확인
st.write(f'Time Periods Length: {len(time_periods)}')
st.write(f'Boardings Length: {len(boardings)}')
st.write(f'Alightings Length: {len(alightings)}')

# 막대 그래프 그리기
fig, ax = plt.subplots()
width = 0.35  # 막대의 너비
x = range(len(time_periods))

ax.bar(x, boardings, width, label='승차')
ax.bar([p + width for p in x], alightings, width, label='하차')

ax.set_xlabel('시간대')
ax.set_ylabel('인원수')
ax.set_title(f'{busiest_station_name} 시간대별 승하차 인원수')
ax.set_xticks([p + width/2 for p in x])
ax.set_xticklabels(time_periods, rotation=90)
ax.legend()

st.pyplot(fig)
