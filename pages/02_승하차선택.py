import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os

# 데이터 로드
csv_file_path = '2024년 05월  교통카드 통계자료.csv'

# 파일 존재 여부 확인
if not os.path.exists(csv_file_path):
    st.error(f"파일을 찾을 수 없습니다: {csv_file_path}")
else:
    try:
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

        def plot_data(station_data_1, station_data_2, station_name_1, station_name_2, time_periods, graph_type, data_type):
            if data_type == '승차':
                data_1 = station_data_1[columns_to_convert[::2]].sum().values
                data_2 = station_data_2[columns_to_convert[::2]].sum().values
            else:  # '하차'
                data_1 = station_data_1[columns_to_convert[1::2]].sum().values
                data_2 = station_data_2[columns_to_convert[1::2]].sum().values

            # 데이터 길이 맞추기
            min_length = min(len(data_1), len(data_2), len(time_periods))
            data_1 = data_1[:min_length]
            data_2 = data_2[:min_length]
            time_periods = time_periods[:min_length]

            fig, ax = plt.subplots(figsize=(12, 8))
            x = range(len(time_periods))

            if graph_type == '막대 그래프':
                width = 0.35
                ax.bar([p - width/2 for p in x], data_1, width, label=f'{station_name_1} {data_type}', color='skyblue')
                ax.bar([p + width/2 for p in x], data_2, width, label=f'{station_name_2} {data_type}', color='salmon')
            else:  # '꺾은선 그래프'
                ax.plot(x, data_1, label=f'{station_name_1} {data_type}', color='blue', marker='o')
                ax.plot(x, data_2, label=f'{station_name_2} {data_type}', color='red', marker='o')

            ax.set_xlabel('시간대', fontsize=14)
            ax.set_ylabel('인원수', fontsize=14)
            ax.set_title(f'두 역 시간대별 {data_type} 인원 비교', fontsize=16)
            ax.set_xticks(x)
            ax.set_xticklabels(time_periods, rotation=90, fontsize=12)
            ax.legend()
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            for i in range(len(time_periods)):
                if graph_type == '막대 그래프':
                    ax.text(i - width/2, data_1[i] + 5, str(data_1[i]), ha='center', fontsize=10, color='blue')
                    ax.text(i + width/2, data_2[i] + 5, str(data_2[i]), ha='center', fontsize=10, color='red')
                else:  # '꺾은선 그래프'
                    ax.text(i, data_1[i] + 5, str(data_1[i]), ha='center', fontsize=10, color='blue')
                    ax.text(i, data_2[i] + 5, str(data_2[i]), ha='center', fontsize=10, color='red')

            st.pyplot(fig)

        # 두 역 비교
        st.header('두 역 비교')

        selected_line_1 = st.selectbox('호선 1을 선택하세요', line_options, key='line1')
        station_options_1 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_1]['지하철역'].unique()
        selected_station_1 = st.selectbox('역 1을 선택하세요', station_options_1, key='station1')

        selected_line_2 = st.selectbox('호선 2를 선택하세요', line_options, key='line2')
        station_options_2 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_2]['지하철역'].unique()
        selected_station_2 = st.selectbox('역 2를 선택하세요', station_options_2, key='station2')

        graph_type = st.selectbox('그래프 종류를 선택하세요', ['막대 그래프', '꺾은선 그래프'])
        data_type = st.selectbox('데이터 종류를 선택하세요', ['승차', '하차'])

        station_data_1 = get_station_data(selected_line_1, selected_station_1)
        station_data_2 = get_station_data(selected_line_2, selected_station_2)

        time_periods = [col.split('~')[0] for col in columns_to_convert[::2]]
        plot_data(station_data_1, station_data_2, selected_station_1, selected_station_2, time_periods, graph_type, data_type)

    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
