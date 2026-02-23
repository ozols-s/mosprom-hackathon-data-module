# Функции для создания графиков
def create_pie_chart(df_year, year):
    """Создает круговую диаграмму для конкретного года"""
    CHINA = 'China'
    
    # Подготовка данных
    d = df_year.copy()
    d['primaryValue'] = pd.to_numeric(d['primaryValue'], errors="coerce").fillna(0)
    
    # Маски
    mask_china = d['reporterDesc'].str.contains(CHINA, na=False)
    mask_friend = d['isFriendly'] == 1
    
    # Суммы по категориям
    val_china = float(d.loc[mask_china, 'primaryValue'].sum())
    val_friend_other = float(d.loc[mask_friend & ~mask_china, 'primaryValue'].sum())
    val_unfriendly = float(d.loc[~mask_friend, 'primaryValue'].sum())
    
    # Создание графика
    labels = ["Китай", "Другие дружественные", "Недружественные"]
    values = [val_china, val_friend_other, val_unfriendly]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent+value',
        textfont_size=14,
        marker_line=dict(color='white', width=2)
    )])
    
    fig.update_layout(
        title=dict(
            text=f"Структура импорта по стоимости, {year}",
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        font=dict(size=12),
        showlegend=True,
        height=450,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig

def create_total_pie_chart(df1, df2, df3):
    """Создает общую круговую диаграмму за все годы"""
    CHINA = 'China'
    
    # Объединяем все данные
    df_total = pd.concat([df1, df2, df3], ignore_index=True)
    df_total['primaryValue'] = pd.to_numeric(df_total['primaryValue'], errors="coerce").fillna(0)
    
    # Маски
    mask_china = df_total['reporterDesc'].str.contains(CHINA, na=False)
    mask_friend = df_total['isFriendly'] == 1
    
    # Суммы по категориям
    val_china = float(df_total.loc[mask_china, 'primaryValue'].sum())
    val_friend_other = float(df_total.loc[mask_friend & ~mask_china, 'primaryValue'].sum())
    val_unfriendly = float(df_total.loc[~mask_friend, 'primaryValue'].sum())
    
    # Создание графика
    labels = ["Китай", "Другие дружественные", "Недружественные"]
    values = [val_china, val_friend_other, val_unfriendly]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent+value',
        textfont_size=16,
        marker_line=dict(color='white', width=3)
    )])
    
    fig.update_layout(
        title=dict(
            text="Общая структура импорта за 3 года",
            font=dict(size=18, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        font=dict(size=14),
        showlegend=True,
        height=550,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        )
    )
    
    return fig

def create_trend_chart(years, values, title, emoji):
    """Создает график тренда"""
    fig = go.Figure()
    
    # Определяем цвет в зависимости от типа графика
    if "импорт" in title.lower():
        color = '#1f77b4'
        gradient_color = 'rgba(31, 119, 180, 0.2)'
    elif "недружественных" in title.lower():
        color = '#FF6B6B'
        gradient_color = 'rgba(255, 107, 107, 0.2)'
    elif "китая" in title.lower():
        color = '#4ECDC4'
        gradient_color = 'rgba(78, 205, 196, 0.2)'
    else:
        color = '#45B7D1'
        gradient_color = 'rgba(69, 183, 209, 0.2)'
    
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines+markers',
        name=title,
        line=dict(color=color, width=4, shape='spline'),
        marker=dict(
            size=12, 
            color=color,
            line=dict(color='white', width=2)
        ),
        fill='tonexty',
        fillcolor=gradient_color,
        hovertemplate=f'<b>{emoji} {title}</b><br>Год: %{{x}}<br>Значение: %{{y}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"{emoji} {title}",
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Год", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title=dict(text=title, font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        font=dict(size=12),
        height=450,
        hovermode='x unified',
        showlegend=False
    )
    
    # Добавляем аннотации с значениями
    for i, (year, value) in enumerate(zip(years, values)):
        fig.add_annotation(
            x=year,
            y=value,
            text=f"<b>{value:.1f}</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor=color,
            ax=0,
            ay=-40,
            font=dict(size=12, color=color),
            bgcolor='white',
            bordercolor=color,
            borderwidth=1
        )
    
    return fig

def create_production_chart(years, production_data, consumption_data, title, category):
    """Создает график производства и потребления"""
    fig = go.Figure()
    
    # График производства
    fig.add_trace(go.Scatter(
        x=years,
        y=production_data,
        mode='lines+markers',
        name='Производство',
        line=dict(color='#2E8B57', width=4, shape='spline'),
        marker=dict(size=12, color='#2E8B57', line=dict(color='white', width=2)),
        fill='tonexty',
        fillcolor='rgba(46, 139, 87, 0.2)',
        hovertemplate=f'<b> Производство</b><br>Год: %{{x}}<br>Значение: %{{y}}<extra></extra>'
    ))
    
    # График потребления
    fig.add_trace(go.Scatter(
        x=years,
        y=consumption_data,
        mode='lines+markers',
        name='Потребление',
        line=dict(color='#FF6B6B', width=4, shape='spline'),
        marker=dict(size=12, color='#FF6B6B', line=dict(color='white', width=2)),
        fill='tonexty',
        fillcolor='rgba(255, 107, 107, 0.2)',
        hovertemplate=f'<b>🛒 Потребление</b><br>Год: %{{x}}<br>Значение: %{{y}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f" {title} - {category}",
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Год", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title=dict(text="Объем", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        font=dict(size=12),
        height=450,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_self_sufficiency_chart(years, self_sufficiency_data, title, category):
    """Создает график самообеспеченности"""
    fig = go.Figure()
    
    # Линия самообеспеченности
    fig.add_trace(go.Scatter(
        x=years,
        y=self_sufficiency_data,
        mode='lines+markers',
        name='Самообеспеченность',
        line=dict(color='#4ECDC4', width=4, shape='spline'),
        marker=dict(size=12, color='#4ECDC4', line=dict(color='white', width=2)),
        fill='tonexty',
        fillcolor='rgba(78, 205, 196, 0.2)',
        hovertemplate=f'<b> Самообеспеченность</b><br>Год: %{{x}}<br>Значение: %{{y:.2f}}<extra></extra>'
    ))
    
    # Линия 100% самообеспеченности
    fig.add_hline(y=1.0, line_dash="dash", line_color="red", 
                  annotation_text="100% самообеспеченность", 
                  annotation_position="bottom right")
    
    fig.update_layout(
        title=dict(
            text=f" {title} - {category}",
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Год", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title=dict(text="Коэффициент самообеспеченности", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)',
            range=[0, max(1.2, max(self_sufficiency_data) * 1.1)]
        ),
        font=dict(size=12),
        height=450,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def create_import_dependency_chart(years, import_dependency_data, title, category):
    """Создает график зависимости от импорта"""
    fig = go.Figure()
    
    # График зависимости от импорта
    fig.add_trace(go.Scatter(
        x=years,
        y=import_dependency_data,
        mode='lines+markers',
        name='Зависимость от импорта',
        line=dict(color='#FF8C00', width=4, shape='spline'),
        marker=dict(size=12, color='#FF8C00', line=dict(color='white', width=2)),
        fill='tonexty',
        fillcolor='rgba(255, 140, 0, 0.2)',
        hovertemplate=f'<b> Зависимость от импорта</b><br>Год: %{{x}}<br>Значение: %{{y:.2f}}<extra></extra>'
    ))
    
    # Линия 30% зависимости (критический порог)
    fig.add_hline(y=0.3, line_dash="dash", line_color="red", 
                  annotation_text="Критический порог 30%", 
                  annotation_position="bottom right")
    
    fig.update_layout(
        title=dict(
            text=f" {title} - {category}",
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Год", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title=dict(text="Коэффициент зависимости", font=dict(size=14, color='#2c3e50')),
            tickfont=dict(size=12),
            gridcolor='rgba(128,128,128,0.2)',
            range=[0, max(0.5, max(import_dependency_data) * 1.1)]
        ),
        font=dict(size=12),
        height=450,
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def create_metrics_radar_chart(metrics_data, category):
    """Создает радарную диаграмму метрик"""
    fig = go.Figure()
    
    # Подготавливаем данные для радара
    metrics = ['self_sufficiency', 'production_share', 'competitiveness_index', 'self_sufficiency_index']
    values = []
    labels = ['Самообеспеченность', 'Доля производства', 'Конкурентоспособность', 'Индекс самообеспеченности']
    
    for metric in metrics:
        if metric in metrics_data and metrics_data[metric] is not None:
            # Нормализуем значения для радара (0-1)
            if metric == 'competitiveness_index':
                # Для индекса конкурентоспособности используем логарифмическую шкалу
                value = min(1.0, np.log10(metrics_data[metric] + 1) / 3)
            else:
                value = min(1.0, metrics_data[metric])
            values.append(value)
        else:
            values.append(0)
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=category,
        line_color='#1f77b4',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=dict(
            text=f" Радар метрик - {category}",
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        height=500
    )
    
    return fig
