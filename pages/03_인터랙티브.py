import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 데이터 로드
csv_file_path = '2024년 05월  교통카드 통계자료.csv'
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

        def plot_single_station_data(station_data, station_name, time_periods, graph_type):
            boardings = station_data[columns_to_convert[::2]].sum().values
            alightings = station_data[columns_to_convert[1::2]].sum().values

            # 데이터 길이 맞추기
            min_length = min(len(boardings), len(alightings), len(time_periods))
            boardings = boardings[:min_length]
            alightings = alightings[:min_length]
            time_periods = time_periods[:min_length]

            x = list(range(len(time_periods)))

            if graph_type == '막대 그래프':
                fig = go.Figure(data=[
                    go.Bar(name='승차', x=time_periods, y=boardings, marker_color='skyblue'),
                    go.Bar(name='하차', x=time_periods, y=alightings, marker_color='salmon')
                ])
            else:  # '꺾은선 그래프'
                fig = go.Figure(data=[
                    go.Scatter(name='승차', x=time_periods, y=boardings, mode='lines+markers', marker=dict(color='blue')),
                    go.Scatter(name='하차', x=time_periods, y=alightings, mode='lines+markers', marker=dict(color='red'))
                ])

            fig.update_layout(
                title=f'{station_name} 시간대별 승하차 인원수',
                xaxis_title='시간대',
                yaxis_title='인원수',
                legend_title='구분',
                xaxis=dict(tickmode='array', tickvals=x, ticktext=time_periods),
                barmode='group'
            )

            fig.update_traces(
                hoverlabel=dict(
                    font_size=16  # 글씨 크기 설정
                )
            )

            st.plotly_chart(fig)

        def plot_comparison_data(station_data_1, station_data_2, station_name_1, station_name_2, time_periods, graph_type, data_type):
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

            x = list(range(len(time_periods)))

            if graph_type == '막대 그래프':
                fig = go.Figure(data=[
                    go.Bar(name=f'{station_name_1} {data_type}', x=time_periods, y=data_1, marker_color='skyblue'),
                    go.Bar(name=f'{station_name_2} {data_type}', x=time_periods, y=data_2, marker_color='salmon')
                ])
            else:  # '꺾은선 그래프'
                fig = go.Figure(data=[
                    go.Scatter(name=f'{station_name_1} {data_type}', x=time_periods, y=data_1, mode='lines+markers', marker=dict(color='blue')),
                    go.Scatter(name=f'{station_name_2} {data_type}', x=time_periods, y=data_2, mode='lines+markers', marker=dict(color='red'))
                ])

            fig.update_layout(
                title=f'두 역 시간대별 {data_type} 인원 비교',
                xaxis_title='시간대',
                yaxis_title='인원수',
                legend_title='역',
                xaxis=dict(tickmode='array', tickvals=x, ticktext=time_periods),
                barmode='group'
            )

            fig.update_traces(
                hoverlabel=dict(
                    font_size=16  # 글씨 크기 설정
                )
            )

            st.plotly_chart(fig)

        # 호선과 역 선택
        line_options = subway_data_cleaned['호선명'].unique()
        selected_line = st.selectbox('호선을 선택하세요', line_options)
        station_options = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line]['지하철역'].unique()
        selected_station = st.selectbox('역을 선택하세요', station_options)

        # 그래프 타입 선택
        graph_type = st.selectbox('그래프 종류를 선택하세요', ['막대 그래프', '꺾은선 그래프'])

        # 선택한 역의 데이터 필터링 및 그래프 생성
        station_data = get_station_data(selected_line, selected_station)
        time_periods = [col.split('~')[0] for col in columns_to_convert[::2]]
        plot_single_station_data(station_data, selected_station, time_periods, graph_type)

        # 두 역 비교
        st.header('두 역 비교')

        selected_line_1 = st.selectbox('호선 1을 선택하세요', line_options, key='line1')
        station_options_1 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_1]['지하철역'].unique()
        selected_station_1 = st.selectbox('역 1을 선택하세요', station_options_1, key='station1')

        selected_line_2 = st.selectbox('호선 2를 선택하세요', line_options, key='line2')
        station_options_2 = subway_data_cleaned[subway_data_cleaned['호선명'] == selected_line_2]['지하철역'].unique()
        selected_station_2 = st.selectbox('역 2를 선택하세요', station_options_2, key='station2')

        # 그래프 타입 선택
        graph_type = st.selectbox('비교 그래프 종류를 선택하세요', ['막대 그래프', '꺾은선 그래프'], key='comparison_graph_type')
        data_type = st.selectbox('데이터 종류를 선택하세요', ['승차', '하차'], key='data_type')

        station_data_1 = get_station_data(selected_line_1, selected_station_1)
        station_data_2 = get_station_data(selected_line_2, selected_station_2)

        time_periods = [col.split('~')[0] for col in columns_to_convert[::2]]
        plot_comparison_data(station_data_1, station_data_2, selected_station_1, selected_station_2, time_periods, graph_type, data_type)

    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
