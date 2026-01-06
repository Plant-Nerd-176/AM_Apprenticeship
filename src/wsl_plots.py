""" This file contains plotting functions for WSL data visualisation."""

from pathlib import Path
from typing import List, Optional
import pandas as pd
import panel as pn
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from ipywidgets import Dropdown, HTML, VBox, HBox

from config.general_config import REPORTS_OUT

from config.projects.wsl_config import (
    WSL_CLUB_COLOURS,
    WSL_CLUB_BADGES,
    WSL_LOGO_URL,
    SEASON_AVG_COLOUR,
    FALLBACK_COLOUR
    )

# -------------------------------------------------------------------------
# Config
# -------------------------------------------------------------------------
WSL_CHART_CONFIG = {
    'chart_size': dict(
        width=1000,
        height=600
    ),

    'logo_placement': dict(
        xref='paper', yref='paper',
        x=0.0, y=1.23,
        sizex=0.2, sizey=0.2,
        xanchor='left', yanchor='top',
        opacity=1.0,
        layer='above'
    ),

    'dropdown_placement': dict(
        direction='down',
        x=0.5, y=1.12,
        xanchor='center', yanchor='top',
        showactive=True
    )
}

# -------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------
def apply_chart_size(fig):
    fig.update_layout(**WSL_CHART_CONFIG['chart_size'])


def add_logo(fig, source, visible=True):
    fig.add_layout_image({
        **WSL_CHART_CONFIG['logo_placement'],
        'source': source,
        'visible': visible
    })


def add_dropdown(fig, buttons):
    fig.update_layout(
        updatemenus=[{
            **WSL_CHART_CONFIG['dropdown_placement'],
            'buttons': buttons
        }]
    )

def make_scatter_trace(x, y, name, colour, hovertext, hovertemplate, visible=False):
    return go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name=name,
        visible=visible,
        line=dict(color=colour, width=2),
        marker=dict(size=7, line=dict(width=1, color='rgba(0,0,0,0.5)')),
        hovertext=hovertext,
        hovertemplate=hovertemplate,
    )

def make_bar_trace(x, y, name, hovertext, hovertemplate, visible=False):
    return go.Bar(
        x=x,
        y=y,
        name=name,
        marker_color='lightgray',
        visible=visible,
        hovertext=hovertext,
        hovertemplate=hovertemplate,
    )

def save_figure(fig, fig_name):
    save_dir = REPORTS_OUT / 'plots'
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / f'wsl_project_{fig_name}.html'
    print(f'Saving figure to: {file_path}')
    fig.write_html(file_path)

# -------------------------------------------------------------------------
# WLS Plotting Functions
# -------------------------------------------------------------------------
def create_club_capacity_attendance_chart(
    df: pd.DataFrame,
    show_logo: bool = False,
    save_fig: bool = False,
    fig_name: str | None = None
) -> go.Figure:
    """ Create an interactive WSL attendance vs capacity chart.

    This chart shows:
      * Stadium capacity (bars)
      * Match attendance (line)
      * League average attendance (dashed line)
      * Club badge swapping based on dropdown selection
      * WSL logo in the default view

    The dropdown menu allows switching between:
      * Default league-wide view
      * Individual club views (capacity + attendance)

    Args:
        df (pd.DataFrame):
            DataFrame containing WSL data. Must include columns:
            ``Season``, ``Club``, ``Attendance``, ``Capacity``,
            and ``Ground``.

    Returns:
        go.Figure:
            A Plotly figure with interactive dropdown controls and
            automatic badge/logo swapping.
    """

    # Calculate season averages
    season_avg_att = df.groupby('Season', as_index=False)['Attendance'].mean()
    clubs = sorted(df['Club'].unique())

    fig = go.Figure()

    # Add club traces (capacity + attendance)
    for club in clubs:
        club_data = df[df['Club'] == club]
        colour = WSL_CLUB_COLOURS.get(club, FALLBACK_COLOUR)

        # Capacity bar
        fig.add_trace(
            make_bar_trace(
                x=club_data['Season'],
                y=club_data['Capacity'],
                name=f'{club} Capacity',
                hovertext=club_data['Ground'],
                hovertemplate='Season %{x}<br>Capacity %{y}<br>Stadium: %{hovertext}<extra></extra>',
                visible=False
            )
        )

        # Attendance line
        fig.add_trace(
            make_scatter_trace(
                x=club_data['Season'],
                y=club_data['Attendance'],
                name=f'{club} Attendance',
                colour=colour,
                hovertext=club_data['Ground'],
                hovertemplate='Season %{x}<br>Attendance %{y}<br>Stadium: %{hovertext}<extra></extra>',
                visible=False
            )
        )

    # Season average trace
    fig.add_trace(
        make_scatter_trace(
            x=season_avg_att['Season'],
            y=season_avg_att['Attendance'],
            name='Season Average Attendance',
            colour=SEASON_AVG_COLOUR,
            hovertext=None,
            hovertemplate='Season %{x}<br>Average Attendance %{y}<extra></extra>',
            visible=True
        )
    )

    # Add WSL logo (index 0)
    add_logo(fig, WSL_LOGO_URL, visible=show_logo)

    # Add club badges (index 1 → N)
    for club in clubs:
        add_logo(fig, WSL_CLUB_BADGES.get(club), visible=False)

    # Dropdown buttons
    num_traces = len(clubs) * 2
    buttons = []

    # Default view
    buttons.append(
        dict(
            label='-',
            method='update',
            args=[
                {'visible': [False] * num_traces + [True]},
                {'images': [dict(visible=(i == 0)) for i in range(len(clubs) + 1)]},
            ],
        )
    )

    # Club views
    for i, club in enumerate(clubs):
        vis = [False] * num_traces + [True]
        vis[i * 2] = True
        vis[i * 2 + 1] = True

        buttons.append(
            dict(
                label=club,
                method='update',
                args=[
                    {'visible': vis},
                    {'images': [dict(visible=(j == i + 1)) for j in range(len(clubs) + 1)]},
                ],
            )
        )

    # Apply dropdown + layout settings
    add_dropdown(fig, buttons)
    apply_chart_size(fig)

    fig.update_layout(
        barmode='overlay',
        title=dict(
            text='League Average Attendance Across Seasons',
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=22),
        ),
        xaxis_title='Season',
        yaxis_title='Seats',
    )

    # Optional save
    if save_fig:
        if fig_name is None:
            raise ValueError('fig_name must be provided when save_fig=True')
        save_figure(fig, fig_name)
        
    if save_fig:
        print(f'Figure saved to: {REPORTS_OUT / 'plots' / f'wsl_project_{fig_name}.png'}')
    else:
        print('Figure created.')

    return fig


def create_wsl_visual(
    df: pd.DataFrame,
    metric_col: str,
    yaxis_label: str,
    title_prefix: str,
    show_logo: bool = False,
    save_fig: bool = False,
    fig_name: str | None = None
) -> go.Figure:
    """
    Create an interactive WSL line chart with club dropdowns and optional logo/saving.

    Args:
        df (pd.DataFrame): Must include columns: Club, Season, metric_col.
        metric_col (str): Column to plot on Y-axis.
        yaxis_label (str): Y-axis label.
        title_prefix (str): Title prefix (e.g., 'Attendance').
        show_logo (bool): Whether to show WSL logo (default False).
        save_fig (bool): Whether to save the figure (default False).
        fig_name (str): Required if save_fig=True.

    Returns:
        go.Figure
    """

    # Prepare data for plotting
    df_metric = df[['Club', 'Season', metric_col]]
    season_avg = df_metric.groupby('Season', as_index=False)[metric_col].mean()
    clubs = sorted(df_metric['Club'].unique())

    fig = go.Figure()

    # Add club traces
    for club in clubs:
        club_df = df_metric[df_metric['Club'] == club]
        colour = WSL_CLUB_COLOURS.get(club, FALLBACK_COLOUR)

        fig.add_trace(
            make_scatter_trace(
                x=club_df['Season'],
                y=club_df[metric_col],
                name=club,
                colour=colour,
                hovertext=None,
                hovertemplate=f'<b>%{{x}}</b><br>{yaxis_label}: %{{y}}<extra>{club}</extra>',
                visible=False
            )
        )

    # Add season average trace
    fig.add_trace(
        make_scatter_trace(
            x=season_avg['Season'],
            y=season_avg[metric_col],
            name='Season Average',
            colour=SEASON_AVG_COLOUR,
            hovertext=None,
            hovertemplate=f'<b>%{{x}}</b><br>{yaxis_label} (avg): %{{y}}<extra></extra>',
            visible=True
        )
    )

    # Add WSL logo
    add_logo(fig, WSL_LOGO_URL, visible=show_logo)

    # Dropdown buttons
    buttons = []

    # Default view: only season average
    buttons.append(
        dict(
            label='-',
            method='update',
            args=[{'visible': [False] * len(clubs) + [True]}],
        )
    )

    # All clubs + average
    buttons.append(
        dict(
            label='All Clubs',
            method='update',
            args=[{'visible': [True] * len(clubs) + [True]}],
        )
    )

    # Individual clubs
    for i, club in enumerate(clubs):
        vis = [False] * len(clubs) + [True]
        vis[i] = True

        buttons.append(
            dict(
                label=club,
                method='update',
                args=[{'visible': vis}],
            )
        )

    # Apply dropdown + layout
    add_dropdown(fig, buttons)
    apply_chart_size(fig)

    fig.update_layout(
        title=dict(
            text=f'{title_prefix} Across Seasons',
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=22),
        ),
        xaxis_title='Season',
        yaxis_title=yaxis_label,
    )

    # Optional save ---
    if save_fig:
        if fig_name is None:
            raise ValueError('fig_name must be provided when save_fig=True')
        save_figure(fig, fig_name)
        
    if save_fig:
        print(f'Figure saved to: {REPORTS_OUT / 'plots' / f'wsl_project_{fig_name}.png'}')
    else:
        print('Figure created.')

    return fig

#-------------------------------------------------------------------------
# KPI Style Card
#-------------------------------------------------------------------------
def create_kpi_card(
    df: pd.DataFrame,
    metric_col: str,
    label_col: str | None = None,
    season_col: str | None = None,
    club_col: str | None = None,
    title: str = 'KPI',
    overview_aggregation: str = 'mean'
) -> VBox:
    """Create a KPI card widget for WSL dashboards.

    This widget supports multiple views:
      * Overview (all seasons)
      * Best per season
      * Best per season & club
      * All seasons by club

    Text rules:
      * If ``label_col`` exists (e.g., top goal scorer), the card displays:
            '<title>: <label_value> for <club>'
      * Otherwise:
            '<title> for <club>'

    Args:
        df (pd.DataFrame):
            DataFrame containing the metric and grouping columns.
        metric_col (str):
            Column containing the metric to display.
        label_col (str, optional):
            Column containing labels (e.g., player names).
        season_col (str, optional):
            Column containing season values.
        club_col (str, optional):
            Column containing club names.
        title (str):
            Title displayed on the KPI card.
        overview_aggregation (str):
            Aggregation method for overview view. One of:
            ``'mean'`` or ``'max'``.

    Returns:
        VBox:
            ipywidgets VBox containing dropdowns and the KPI card.
    """
    view_options = {
        'Overview (All Seasons)': 'overview',
        'Best Per Season': 'season_best',
        'Best Per Season & Club': 'season_club_best',
        'All Seasons by Club': 'all_seasons_by_club',
    }

    view_dropdown = Dropdown(options=view_options, description='View:')
    season_dropdown = Dropdown(description='Season:')
    club_dropdown = Dropdown(description='Club:')

    if season_col:
        season_dropdown.options = sorted(df[season_col].unique())

    if club_col:
        club_dropdown.options = sorted(df[club_col].unique())

    kpi_card = HTML()

    def render_card(view: str, season=None, club=None) -> None:
        """Render the KPI card based on the selected view."""
        bg_colour = SEASON_AVG_COLOUR
        text = ''
        value = ''
        season_display = ''

        # Overview (all seasons)
        if view == 'overview':
            if overview_aggregation == 'mean':
                value = round(df[metric_col].mean(), 2)
                text = f'Average {title}'
            else:
                value = df[metric_col].max()
                text = f'Top {title}'

        # Best per season
        elif view == 'season_best' and season is not None:
            df_season = df[df[season_col] == season]
            best_idx = df_season[metric_col].idxmax()

            value = df_season.loc[best_idx, metric_col]
            label_value = (
                df_season.loc[best_idx, label_col] if label_col else ''
            )
            club_name = (
                df_season.loc[best_idx, club_col] if club_col else ''
            )
            season_display = season

            # Clean text rule
            if label_value:
                text = f'{title}: {label_value} for {club_name}'
            else:
                text = f'{title} for {club_name}'

            if club_name in WSL_CLUB_COLOURS:
                bg_colour = WSL_CLUB_COLOURS[club_name]

        # Best per season & club
        elif (
            view == 'season_club_best'
            and season is not None
            and club is not None
        ):
            df_sel = df[
                (df[season_col] == season) & (df[club_col] == club)
            ]

            if not df_sel.empty:
                value = df_sel.iloc[0][metric_col]
                label_value = (
                    df_sel.iloc[0][label_col] if label_col else ''
                )
                season_display = season

                if label_value:
                    text = f'{title}: {label_value} for {club}'
                else:
                    text = f'{title} for {club}'

                bg_colour = WSL_CLUB_COLOURS.get(
                    club, SEASON_AVG_COLOUR
                )
            else:
                text = 'No data for this combination'
                value = ''
                season_display = season

        # All seasons by club
        elif view == 'all_seasons_by_club' and club is not None:
            df_club = df[df[club_col] == club]

            if overview_aggregation == 'mean':
                value = round(df_club[metric_col].mean(), 2)
            else:
                idx = df_club[metric_col].idxmax()
                value = df_club.loc[idx, metric_col]
                season_display = df_club.loc[idx, season_col]

            text = f'{title} (All Seasons)'
            bg_colour = WSL_CLUB_COLOURS.get(
                club, SEASON_AVG_COLOUR
            )

        else:
            text = title
            value = ''

        # Render HTML
        kpi_card.value = f"""
        <div style='border-radius:15px; padding:25px; background:{bg_colour};
                    color:white; width:350px; text-align:center;'>
            <h4 style='margin:0; font-size:16px;'>{text}</h4>
            <p style='margin:5px 0 0; font-size:32px;'>{value}</p>
            {f"<p style='margin:0; font-size:14px;'>Season: {season_display}</p>"
              if season_display else ''}
        </div>
        """

    # Callbacks
    def update_kpi(change=None) -> None:
        render_card(
            view=view_dropdown.value,
            season=season_dropdown.value,
            club=club_dropdown.value,
        )

    def on_view_change(change) -> None:
        val = change['new']

        if val == 'overview':
            season_dropdown.layout.display = 'none'
            club_dropdown.layout.display = 'none'

        elif val == 'season_best':
            season_dropdown.layout.display = 'inline-flex'
            club_dropdown.layout.display = 'none'

        elif val == 'season_club_best':
            season_dropdown.layout.display = 'inline-flex'
            club_dropdown.layout.display = 'inline-flex'

        elif val == 'all_seasons_by_club':
            season_dropdown.layout.display = 'none'
            club_dropdown.layout.display = 'inline-flex'

        update_kpi()

    view_dropdown.observe(on_view_change, names='value')
    season_dropdown.observe(update_kpi, names='value')
    club_dropdown.observe(update_kpi, names='value')

    # Initialise
    on_view_change({'new': view_dropdown.value})

    return VBox(
        [view_dropdown, HBox([season_dropdown, club_dropdown]), kpi_card]
    )

#-------------------------------------------------------------------------
# Nationality Plots
#-------------------------------------------------------------------------
def create_nationality_figure(
        df: pd.DataFrame,
        y_col: str,
        hover_cols: Optional[List[str]] = None,
        trace_type: str = 'bar',
        group_col: str = 'group',
        country_col: str = 'Nationality',
        overview_groups: List[str] = ['English','European (excl. Eng)','Non-European'],
        title: str = 'Nationality Figure',
        xaxis_title: str = 'Season',
        yaxis_title: Optional[str] = None,
        barmode: str = 'group',
        height: int = 800,
        width: int = 1000,
        margin: dict = dict(l=80, r=80, t=150, b=50),
        save_fig: bool = False,
        fig_name: str | None = None
    ) -> go.Figure:
    """Create an interactive nationality figure with dropdowns.
    
    This chart displays:
      * Overview group performance across seasons
      * Individual country performance across seasons
      * Dropdowns for selecting countries or viewing overview groups
    Args:
        df (pd.DataFrame): DataFrame containing nationality data.
        y_col (str): Column name for the y-axis values.
        hover_cols (List[str], optional): List of column names to include in hover data.
        trace_type (str): Type of trace ('bar' or 'scatter').
        group_col (str): Column name for grouping overview groups.
        country_col (str): Column name for country names.
        overview_groups (List[str]): List of overview group names.
        title (str): Title of the figure.
        xaxis_title (str): Title for the x-axis.
        yaxis_title (Optional[str]): Title for the y-axis.
        barmode (str): Bar mode ('group', 'stack', etc.).
        height (int): Height of the figure in pixels.
        width (int): Width of the figure in pixels.
        margin (dict): Margin settings for the figure.
    
    Returns:
        go.Figure: A Plotly figure with interactive dropdown menus for country
            selection and view mode.
    """ 

    hover_cols = hover_cols or []

    # Define colours
    colours = {
        'English': '#CE1124',
        'European (excl. Eng)': '#003399',
        'Non-European': 'green'
    }

    fig = go.Figure()
    Trace = go.Bar if trace_type == 'bar' else go.Scatter

    # Overview group traces
    for grp in overview_groups:
        sub = (
            df[df[group_col] == grp]
            .groupby('Season')
            .agg({y_col: 'sum'})
            .reset_index()
        )
        hovertemplate = 'Season: %{x}<br>Value: %{y}'

        kwargs = {}
        if trace_type == 'scatter':
            kwargs['mode'] = 'lines+markers'
            kwargs['line'] = dict(color=colours.get(grp))
        else:
            kwargs['marker'] = dict(color=colours.get(grp))

        fig.add_trace(Trace(
            x=sub['Season'],
            y=sub[y_col],
            name=grp,
            visible=True,
            hovertemplate=hovertemplate,
            **kwargs
        ))

    # Country traces
    country_trace_map = {}
    for nat in sorted(df[country_col].unique()):
        agg_dict = {y_col: 'sum'}
        for col in hover_cols:
            agg_dict[col] = 'mean'

        sub = (
            df[df[country_col] == nat]
            .groupby('Season')
            .agg(agg_dict)
            .reset_index()
        )

        if hover_cols:
            customdata = sub[hover_cols].values
            hovertemplate = (
                'Season: %{x}<br>'
                + '<br>'.join(
                    [f'{col}: %{{customdata[{i}]}}' for i, col in enumerate(hover_cols)]
                )
                + '<br>Value: %{y}'
            )
        else:
            customdata = None
            hovertemplate = 'Season: %{x}<br>Value: %{y}'

        kwargs = {}
        if trace_type == 'scatter':
            kwargs['mode'] = 'lines+markers'

        trace_idx = len(fig.data)
        fig.add_trace(Trace(
            x=sub['Season'],
            y=sub[y_col],
            name=nat,
            visible=False,
            customdata=customdata,
            hovertemplate=hovertemplate,
            **kwargs
        ))
        country_trace_map[nat] = [trace_idx]

    # Dropdowns
    overview_indices = [
        i for i, trace in enumerate(fig.data)
        if trace.name in overview_groups
    ]

    overview_button = dict(
        buttons=[dict(
            label='Overview (Groups)',
            method='update',
            args=[{'visible': [i in overview_indices for i in range(len(fig.data))]}, {}]
        )],
        direction='down',
        showactive=True,
        x=1.00,
        xanchor='left',
        y=1.10,
        yanchor='top'
    )

    country_buttons = []
    for nat in sorted(country_trace_map.keys()):
        vis = [False] * len(fig.data)
        for idx in country_trace_map[nat]:
            vis[idx] = True
        country_buttons.append(dict(
            label=nat,
            method='update',
            args=[{'visible': vis}, {}]
        ))

    country_dropdown = dict(
        buttons=country_buttons,
        direction='down',
        showactive=True,
        x=1.20,
        xanchor='left',
        y=1.10,
        yanchor='top'
    )

    # Layout
    fig.update_layout(
        updatemenus=[overview_button, country_dropdown],
        title=title,
        title_x=0.5,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title or y_col,
        barmode=barmode,
        height=height,
        width=width,
        margin=margin,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.05,
            xanchor='center',
            x=0.5
        )
    )

    # Optional save ---
    if save_fig:
        if fig_name is None:
            raise ValueError('fig_name must be provided when save_fig=True')
        save_figure(fig, fig_name)
        
    if save_fig:
        print(f'Figure saved to: {REPORTS_OUT / 'plots' / f'wsl_project_{fig_name}.png'}')
    else:
        print('Figure created.')

    return fig


def create_distribution_visual(
    df: pd.DataFrame,
    save_fig: bool = False,
    fig_name: str | None = None
) -> go.Figure:
    """Create a WSL player vs minutes distribution figure.
    
    This chart displays the percentage distribution of players and minutes
    across seasons for different nationality groups.
    
    Args:
        df (pd.DataFrame): DataFrame containing nationality distribution data.
        save_fig (bool): Whether to save the figure as an HTML file.
        fig_name (str, optional): Name of the file to save the figure as.
        
    Returns:
        go.Figure: A Plotly figure showing player vs minutes distribution.
    """

    df = df.copy()

    # Calculate percentages relative to season totals ---
    df['percentage_player_distribution'] = (
        df['Num_Players'] / df.groupby('Season')['Num_Players'].transform('sum')
    )
    df['percentage_mins_distribution'] = (
        df['Minutes_Played'] / df.groupby('Season')['Minutes_Played'].transform('sum')
    )

    # Aggregate by season + group ---
    df_grouped = (
        df.groupby(['Season', 'group'], as_index=False)[
            ['percentage_player_distribution', 'percentage_mins_distribution']
        ].sum()
    )

    # Convert to percentages and round to 2 dp ---
    df_grouped['percentage_player_distribution'] = (
        df_grouped['percentage_player_distribution'] * 100
    ).round(2)
    df_grouped['percentage_mins_distribution'] = (
        df_grouped['percentage_mins_distribution'] * 100
    ).round(2)

    # Ensure season is numeric and sorted ---
    df_grouped['Season'] = pd.to_numeric(df_grouped['Season'])
    df_grouped = df_grouped.sort_values(['group', 'Season'])

    # Define colors ---
    colours = {
        'English': '#CE1124',
        'European (excl. Eng)': '#003399',
        'Non-European': 'green'
    }

    fig = go.Figure()

    # Solid lines: % Players ---
    for grp in df_grouped['group'].unique():
        g = df_grouped[df_grouped['group'] == grp]
        fig.add_trace(go.Scatter(
            x=g['Season'],
            y=g['percentage_player_distribution'],
            mode='lines+markers',
            name=f'{grp} % Players',
            line=dict(color=colours.get(grp, 'gray'), width=3, dash='solid'),
            hovertemplate='%{y:.2f}% Players<br>%{x}<br>' + grp + '<extra></extra>'
        ))

    # Dotted lines: % Minutes ---
    for grp in df_grouped['group'].unique():
        g = df_grouped[df_grouped['group'] == grp]
        fig.add_trace(go.Scatter(
            x=g['Season'],
            y=g['percentage_mins_distribution'],
            mode='lines+markers',
            name=f'{grp} % Minutes',
            line=dict(color=colours.get(grp, 'gray'), width=3, dash='dot'),
            hovertemplate='%{y:.2f}% Minutes<br>%{x}<br>' + grp + '<extra></extra>'
        ))

    # Layout ---
    fig.update_layout(
        title='Player vs Minutes Distribution (%) by Season',
        xaxis_title='Season',
        yaxis_title='Percentage (%)',
        yaxis=dict(range=[0, 100]),
        xaxis=dict(type='linear', dtick=1),
        template='plotly_white',
        legend_title='Metric',
        height=650
    )

    # Optional save ---
    if save_fig:
        if fig_name is None:
            raise ValueError('fig_name must be provided when save_fig=True')
        save_figure(fig, fig_name)
        
    if save_fig:
        print(f'Figure saved to: {REPORTS_OUT / 'plots' / f'wsl_project_{fig_name}.png'}')
    else:
        print('Figure created.')

    return fig

#-------------------------------------------------------------------------
# Focasting Plots
#-------------------------------------------------------------------------  
def create_attendance_capacity_forecast_chart(
    df: pd.DataFrame,
    show_logo: bool = False,
    save_fig: bool = False,
    fig_name: str | None = None
) -> go.Figure:
    """ Create an interactive WSL attendance forecast chart.
    This chart shows:
      * Average attendance vs predicted attendance (lines)
      * Average capacity (bars)
      * League average metrics
      
      Args:
        df (pd.DataFrame): Forecasting DataFrame with required columns.
        show_logo (bool): Whether to show WSL logo (default False).
        save_fig (bool): Whether to save the figure (default False).
        fig_name (str): Required if save_fig=True.
        
    Returns:
        go.Figure
        
    """
    # 0. Clean Club column (fix TypeError when sorting)
    df = df[df['Club'].notna()].copy()
    df['Club'] = df['Club'].astype(str)

    # 1. Identify league regulars (>=3 seasons BEFORE 2024)
    historical_counts = (
        df[df['Season'] < 2024]
        .groupby('Club')
        .size()
        .to_dict()
    )

    # 2. Prepare df for aggregation 
    df_for_group = df.copy()

    # Don't fill attendance/capacity with 0
    safe_fill_cols = [
        'Points', 'Goal_Difference', 'Goals_For', 'Goals_Against',
        'Top_Scorer_Goals', 'pct_players_eng', 'pct_minutes_eng'
    ]
    df_for_group[safe_fill_cols] = df_for_group[safe_fill_cols].fillna(0)

    # 3. Aggregate data
    league_avg = (
        df_for_group.groupby('Season', as_index=False)
          .agg({
              'Attendance': 'mean',
              'Predicted_Attendance': 'mean',
              'pct_players_eng': 'mean',
              'pct_minutes_eng': 'mean'
          })
          .rename(columns={
              'Attendance': 'AvgAttendance',
              'Predicted_Attendance': 'AvgPredicted',
              'pct_players_eng': 'AvgPctEngPlayers',
              'pct_minutes_eng': 'AvgPctEngMinutes'
          })
    )

    # Add max metrics per season
    league_avg['MaxAttendance'] = df_for_group.groupby('Season')['Attendance'].max().values
    league_avg['MaxPoints'] = df_for_group.groupby('Season')['Points'].max().values
    league_avg['MaxTopScorerGoals'] = df_for_group.groupby('Season')['Top_Scorer_Goals'].max().values

    club_avg = (
        df_for_group.groupby(['Club', 'Season'], as_index=False)
          .agg({
              'Attendance': 'mean',
              'Predicted_Attendance': 'mean',
              'Capacity': 'mean',
              'Points': 'mean',
              'Goal_Difference': 'mean',
              'Goals_For': 'mean',
              'Goals_Against': 'mean',
              'Top_Scorer_Goals': 'mean',
              'pct_players_eng': 'mean',
              'pct_minutes_eng': 'mean'
          })
          .rename(columns={
              'Attendance': 'AvgAttendance',
              'Predicted_Attendance': 'AvgPredicted'
          })
    )

    # 4. Clubs list 
    clubs = sorted(df['Club'].unique())
    fig = go.Figure()

    # 5. League average traces
    league_customdata = np.stack([
        league_avg['AvgAttendance'],         # 0
        league_avg['AvgPredicted'],          # 1
        league_avg['AvgPctEngPlayers'],      # 2
        league_avg['AvgPctEngMinutes'],      # 3
        league_avg['MaxAttendance'],         # 4
        league_avg['MaxPoints'],             # 5
        league_avg['MaxTopScorerGoals']      # 6
    ], axis=-1)

    league_hover = (
        'Season %{x}<br>'
        'Avg Actual %{y:.2f}<br>'
        'Max Points %{customdata[5]:d}<br>'
        'Max Top Scorer Goals %{customdata[6]:d}<br>'
        'Pct Eng Players %{customdata[2]:.2f}<br>'
        'Pct Eng Minutes %{customdata[3]:.2f}<extra></extra>'
    )

    # Stop league actual line at last real season
    league_actual_y = league_avg['AvgAttendance'].copy()
    last_real_idx = league_actual_y.last_valid_index()
    if last_real_idx is not None:
        league_actual_y.loc[last_real_idx+1:] = None

    # Actual league average
    fig.add_trace(go.Scatter(
        x=league_avg['Season'],
        y=league_actual_y,
        name='League Avg Attendance',
        mode='lines+markers',
        marker=dict(color=SEASON_AVG_COLOUR),
        customdata=league_customdata,
        hovertemplate=league_hover,
        visible=True
    ))

    # Predicted league average (dotted)
    fig.add_trace(go.Scatter(
        x=league_avg['Season'],
        y=league_avg['AvgPredicted'],
        name='League Avg Predicted',
        mode='lines+markers',
        line=dict(color=SEASON_AVG_COLOUR, dash='dot'),
        customdata=league_customdata,
        hovertemplate=league_hover.replace('Avg Actual', 'Avg Predicted'),
        visible=True
    ))

    # 6. Club-specific traces
    for club in clubs:
        cdf = club_avg[club_avg['Club'] == club]

        is_regular = historical_counts.get(club, 0) >= 3
        status_text = 'League Regular' if is_regular else 'Not a League Regular'

        # Build customdata array
        customdata = np.stack([
            cdf['Points'],            # 0
            cdf['Goal_Difference'],   # 1
            cdf['Goals_For'],         # 2
            cdf['Goals_Against'],     # 3
            cdf['Top_Scorer_Goals'],  # 4
            cdf['pct_players_eng'],   # 5
            cdf['pct_minutes_eng'],   # 6
            np.full(len(cdf), status_text)  # 7
        ], axis=-1)

        team_hover = (
            'Season %{x}<br>'
            f'Club: {club}<br>'
            'Actual %{y:.2f}<br>'
            'Points: %{customdata[0]:d}<br>'
            'Goals For: %{customdata[2]:d}<br>'
            'Goals Against: %{customdata[3]:d}<br>'
            'Top Scorer Goals: %{customdata[4]:d}<br>'
            'Status: %{customdata[7]}<extra></extra>'
        )

        # Capacity bars stop when real attendance ends

        capacity_y = cdf['Capacity'].copy()
        last_real_idx = cdf['AvgAttendance'].last_valid_index()
        if last_real_idx is not None:
            capacity_y.loc[last_real_idx+1:] = None

        fig.add_trace(go.Bar(
            x=cdf['Season'],
            y=capacity_y,
            name=f'{club} Capacity',
            marker=dict(color=FALLBACK_COLOUR),
            hovertemplate='Season %{x}<br>Capacity %{y:d}<extra></extra>',
            visible=False
        ))

        # Stop actual line when real data ends
        actual_y = cdf['AvgAttendance'].copy()
        last_real_idx = actual_y.last_valid_index()
        if last_real_idx is not None:
            actual_y.loc[last_real_idx+1:] = None

        fig.add_trace(go.Scatter(
            x=cdf['Season'],
            y=actual_y,
            name=f'{club} Actual Avg',
            mode='lines+markers',
            marker=dict(color=WSL_CLUB_COLOURS.get(club, FALLBACK_COLOUR)),
            customdata=customdata,
            hovertemplate=team_hover,
            visible=False
        ))

        # Predicted attendance (only for regular clubs)
        if is_regular:
            fig.add_trace(go.Scatter(
                x=cdf['Season'],
                y=cdf['AvgPredicted'],
                name=f'{club} Predicted Avg',
                mode='lines+markers',
                marker=dict(color='orange'),
                customdata=customdata,
                hovertemplate=team_hover.replace('Actual', 'Predicted'),
                visible=False
            ))
        else:
            # Dummy trace to preserve dropdown indexing
            fig.add_trace(go.Scatter(
                x=[],
                y=[],
                name=f'{club} Predicted Avg',
                visible=False
            ))

    # 7. Dropdown logic
    num_club_traces = 3 * len(clubs)

    buttons = []

    default_vis = [True, True] + [False] * num_club_traces
    buttons.append(dict(label='League Average', method='update', args=[{'visible': default_vis}]))

    for i, club in enumerate(clubs):
        vis = [False, False] + [False] * num_club_traces
        start = 2 + i * 3
        vis[start] = True      # capacity
        vis[start + 1] = True  # actual
        vis[start + 2] = True  # predicted or dummy

        buttons.append(dict(label=club, method='update', args=[{'visible': vis}]))

    add_dropdown(fig, buttons)

    # 8. Layout
    apply_chart_size(fig)

    fig.update_layout(
        title=dict(
            text='WSL Attendance Forecast: Actual vs Predicted (with Capacity)',
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=22),
        ),
        xaxis_title='Season',
        yaxis_title='Attendance / Capacity',
        barmode='overlay',
        template='plotly_white'
    )

    fig.update_yaxes(tickformat='.2f')

    if show_logo:
        add_logo(fig, WSL_LOGO_URL)

    if save_fig:
        if fig_name is None:
            raise ValueError('fig_name must be provided when save_fig=True')
        save_figure(fig, fig_name)

    return fig
