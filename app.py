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

# 호선과 역 선택
line_options = subway_data_cleaned['호선명'].unique()
selected_line = st.selectbox('호선을 선택하세요', line_options)
station_options = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line]['지하철역'].unique()
selected_station = st.selectbox('역을 선택하세요', station_options)

# 선택한 역의 데이터 필터링
station_data = subway_data_cleaned[(subway_data_cleaned['호선명'] == selected_line) & (subway_data_cleaned['지하철역'] == selected_station)]

# 시간대별 그래프 생성
time_periods = [col.split('~')[0] for col in columns_to_convert[::2]]
boardings = station_data[columns_to_convert[::2]].sum().values
alightings = station_data[columns_to_convert[1::2]].sum().values

# 데이터 길이 일치 확인 및 처리
if len(alightings) < len(time_periods):
    alightings = list(alightings) + [0] * (len(time_periods) - len(alightings))

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(time_periods, boardings, label='승차', marker='o')
ax.plot(time_periods, alightings, label='하차', marker='o')
ax.set_xlabel('시간대')
ax.set_ylabel('인원수')
ax.set_title(f'{selected_station} 시간대별 승하차 인원수')
ax.legend()

st.pyplot(fig)

# 두 역 비교
st.header('두 역 비교')
selected_line_1 = st.selectbox('호선 1을 선택하세요', line_options, key='line1')
station_options_1 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_1]['지하철역'].unique()
selected_station_1 = st.selectbox('역 1을 선택하세요', station_options_1, key='station1')

selected_line_2 = st.selectbox('호선 2를 선택하세요', line_options, key='line2')
station_options_2 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_2]['지하철역'].unique()
selected_station_2 = st.selectbox('역 2를 선택하세요', station_options_2, key='station2')

station_data_1 = subway_data_cleaned[(subway_data_cleaned['호선명'] == selected_line_1) & (subway_data_cleaned['지하철역'] == selected_station_1)]
station_data_2 = subway_data_cleaned[(subway_data_cleaned['호선명'] == selected_line_2) & (subway_data_cleaned['지하철역'] == selected_station_2)]

boardings_1 = station_data_1[columns_to_convert[::2]].sum().values
alightings_1 = station_data_1[columns_to_convert[1::2]].sum().values
boardings_2 = station_data_2[columns_to_convert[::2]].sum().values
alightings_2 = station_data_2[columns_to_convert[1::2]].sum().values

# 데이터 길이 일치 확인 및 처리
if len(alightings_1) < len(time_periods):
    alightings_1 = list(alightings_1) + [0] * (len(time_periods) - len(alightings_1))
if len(alightings_2) < len(time_periods):
    alightings_2 = list(alightings_2) + [0] * (len(time_periods) - len(alightings_2))

fig, ax = plt.subplots()
ax.plot(time_periods, boardings_1, label=f'{selected_station_1} 승차', marker='o')
ax.plot(time_periods, alightings_1, label=f'{selected_station_1} 하차', marker='o')
ax.plot(time_periods, boardings_2, label=f'{selected_station_2} 승차', marker='o')
ax.plot(time_periods, alightings_2, label=f'{selected_station_2} 하차', marker='o')
ax.set_xlabel('시간대')
ax.set_ylabel('인원수')
ax.set_title('두 역 시간대별 승하차 인원수 비교')
ax.legend()

st.pyplot(fig)
