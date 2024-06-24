import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 로드
csv_file_path = '2024년 05월  교통카드 통계자료.csv'
subway_data = pd.read_csv(csv_file_path)

# 데이터 전처리
def preprocess_data(data):
    data_cleaned = data.drop(0).reset_index(drop=True)
    return data_cleaned

def clean_numeric_column(column):
    return column.str.replace(',', '').apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

subway_data_cleaned = preprocess_data(subway_data)
columns_to_convert = subway_data_cleaned.columns[4:]

for column in columns_to_convert:
    subway_data_cleaned[column] = clean_numeric_column(subway_data_cleaned[column])

def get_station_data(line, station):
    return subway_data_cleaned[(subway_data_cleaned['호선명'] == line) & (subway_data_cleaned['지하철역'] == station)]

def plot_station_data(station_data, station_name, title):
    time_periods = [col.split('~')[0] for col in columns_to_convert[::2]]
    boardings = station_data[columns_to_convert[::2]].sum().values
    alightings = station_data[columns_to_convert[1::2]].sum().values

    # 데이터 길이 일치 확인 및 처리
    if len(alightings) < len(time_periods):
        alightings = list(alightings) + [0] * (len(time_periods) - len(alightings))

    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35  # 막대의 너비
    x = range(len(time_periods))

    ax.bar(x, boardings, width, label='승차', color='skyblue')
    ax.bar([p + width for p in x], alightings, width, label='하차', color='salmon')

    ax.set_xlabel('시간대', fontsize=14)
    ax.set_ylabel('인원수', fontsize=14)
    ax.set_title(title, fontsize=16)
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(time_periods, rotation=90, fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for i in range(len(boardings)):
        ax.text(i, boardings[i] + 5, str(boardings[i]), ha='center', fontsize=10)
        ax.text(i + width, alightings[i] + 5, str(alightings[i]), ha='center', fontsize=10)

    st.pyplot(fig)

# 호선과 역 선택
line_options = subway_data_cleaned['호선명'].unique()
selected_line = st.selectbox('호선을 선택하세요', line_options)
station_options = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line]['지하철역'].unique()
selected_station = st.selectbox('역을 선택하세요', station_options)

# 선택한 역의 데이터 필터링 및 그래프 생성
station_data = get_station_data(selected_line, selected_station)
plot_station_data(station_data, selected_station, f'{selected_station} 시간대별 승하차 인원수')

# 두 역 비교
st.header('두 역 비교')

def plot_comparison(station_data_1, station_data_2, station_name_1, station_name_2, time_periods):
    boardings_1 = station_data_1[columns_to_convert[::2]].sum().values
    alightings_1 = station_data_1[columns_to_convert[1::2]].sum().values
    boardings_2 = station_data_2[columns_to_convert[::2]].sum().values
    alightings_2 = station_data_2[columns_to_convert[1::2]].sum().values

    # 데이터 길이 일치 확인 및 처리
    if len(alightings_1) < len(time_periods):
        alightings_1 = list(alightings_1) + [0] * (len(time_periods) - len(alightings_1))
    if len(alightings_2) < len(time_periods):
        alightings_2 = list(alightings_2) + [0] * (len(time_periods) - len(alightings_2))

    fig, ax = plt.subplots(figsize=(12, 8))
    width = 0.2  # 막대의 너비
    x = range(len(time_periods))

    ax.bar([p - width for p in x], boardings_1, width, label=f'{station_name_1} 승차', color='skyblue')
    ax.bar(x, alightings_1, width, label=f'{station_name_1} 하차', color='lightgreen')
    ax.bar([p + width for p in x], boardings_2, width, label=f'{station_name_2} 승차', color='salmon')
    ax.bar([p + 2 * width for p in x], alightings_2, width, label=f'{station_name_2} 하차', color='orange')

    ax.set_xlabel('시간대', fontsize=14)
    ax.set_ylabel('인원수', fontsize=14)
    ax.set_title('두 역 시간대별 승하차 인원수 비교', fontsize=16)
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(time_periods, rotation=90, fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for i in range(len(boardings_1)):
        ax.text(i - width, boardings_1[i] + 5, str(boardings_1[i]), ha='center', fontsize=10)
        ax.text(i, alightings_1[i] + 5, str(alightings_1[i]), ha='center', fontsize=10)
        ax.text(i + width, boardings_2[i] + 5, str(boardings_2[i]), ha='center', fontsize=10)
        ax.text(i + 2 * width, alightings_2[i] + 5, str(alightings_2[i]), ha='center', fontsize=10)

    st.pyplot(fig)

selected_line_1 = st.selectbox('호선 1을 선택하세요', line_options, key='line1')
station_options_1 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_1]['지하철역'].unique()
selected_station_1 = st.selectbox('역 1을 선택하세요', station_options_1, key='station1')

selected_line_2 = st.selectbox('호선 2를 선택하세요', line_options, key='line2')
station_options_2 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_2]['지하철역'].unique()
selected_station_2 = st.selectbox('역 2를 선택하세요', station_options_2, key='station2')

station_data_1 = get_station_data(selected_line_1, selected_station_1)
station_data_2 = get_station_data(selected_line_2, selected_station_2)

time_periods = [col.split('~')[0] for col in columns_to_convert[::2]]
plot_comparison(station_data_1, station_data_2, selected_station_1, selected_station_2, time_periods)
