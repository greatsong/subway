import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

st.markdown(
    """
    <h1 style='font-size:20px;'>수도권 교통 카드 데이터 분석 프로젝트(by 서울고 교사 석리송)</h1>
    """, 
    unsafe_allow_html=True
)

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

# 시간대별 그래프 생성
time_periods = [col.split('~')[0][:2] for col in columns_to_convert[::2]]  # 시간대 2자리로 축약

# 시간대별 승차 인원 최다 역 찾기
boarding_max_indices = subway_data_cleaned[columns_to_convert[::2]].idxmax()
boarding_max_stations = subway_data_cleaned.loc[boarding_max_indices]
boarding_max_counts = subway_data_cleaned[columns_to_convert[::2]].max().values
boarding_max_station_names = boarding_max_stations['지하철역'].values

# 시간대별 하차 인원 최다 역 찾기
alighting_max_indices = subway_data_cleaned[columns_to_convert[1::2]].idxmax()
alighting_max_stations = subway_data_cleaned.loc[alighting_max_indices]
alighting_max_counts = subway_data_cleaned[columns_to_convert[1::2]].max().values
alighting_max_station_names = alighting_max_stations['지하철역'].values

# 데이터 길이 일치 확인 및 처리
if len(alighting_max_counts) < len(time_periods):
    alighting_max_counts = list(alighting_max_counts) + [0] * (len(time_periods) - len(alighting_max_counts))
if len(alighting_max_station_names) < len(time_periods):
    alighting_max_station_names = list(alighting_max_station_names) + [""] * (len(time_periods) - len(alighting_max_station_names))

# 시간대별 승차 인원 최다 역 그래프 그리기
fig, ax = plt.subplots()
width = 0.35  # 막대의 너비
x = range(len(time_periods))

ax.bar(x, boarding_max_counts, width, label='승차 인원 최다 역')
ax.set_xlabel('시간대')
ax.set_ylabel('인원수')
ax.set_title('시간대별 승차 인원 최다 역')
ax.set_xticks([p for p in x])
ax.set_xticklabels(time_periods, rotation=90)
ax.legend()

# 역 이름을 아래 방향으로 표시
for i, v in enumerate(boarding_max_counts):
    ax.text(i, v + 100, str(boarding_max_station_names[i]), ha='center', rotation=90)

st.pyplot(fig)

# 시간대별 하차 인원 최다 역 그래프 그리기
fig, ax = plt.subplots()
width = 0.35  # 막대의 너비
x = range(len(time_periods))

ax.bar(x, alighting_max_counts, width, label='하차 인원 최다 역')
ax.set_xlabel('시간대')
ax.set_ylabel('인원수')
ax.set_title('시간대별 하차 인원 최다 역')
ax.set_xticks([p for p in x])
ax.set_xticklabels(time_periods, rotation=90)
ax.legend()

# 역 이름을 아래 방향으로 표시
for i, v in enumerate(alighting_max_counts):
    ax.text(i, v + 100, str(alighting_max_station_names[i]), ha='center', rotation=90)

st.pyplot(fig)
