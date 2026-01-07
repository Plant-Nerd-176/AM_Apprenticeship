""" This file contains functions for building the WSL dashboard."""

import panel as pn
from config.general_config import REPORTS_OUT
from config.projects.wsl_config import (
    WSL_LOGO_URL,
    WSL_CLUB_BADGES,
    SEASON_AVG_COLOUR,
)

#-------------------------------------------------------------------------
# Dashboard Functions
#-------------------------------------------------------------------------
def center(content, width=1200, pad=150):
    """Return a centered row containing the provided content.

    This helper wraps content in a horizontally centered layout by placing
    left and right spacers around a fixed-width column.

    Args:
        content (panel.layout.Panel): The Panel object(s) to center.
        width (int, optional): Width of the central content container.
            Defaults to 1200.
        pad (int, optional): Left and right padding (spacer width).
            Defaults to 150.

    Returns:
        pn.Row: A Panel Row with centered content.
    """
    
    return pn.Row(
        pn.Spacer(width=pad),
        pn.Column(content, width=width),
        pn.Spacer(width=pad),
        sizing_mode='stretch_width',
    )

def build_page_layout(page_name, content):
    """Construct the layout for a given dashboard page.

    Args:
        page_name (str): Short structural name of the page, used for tab labels.
        content (dict): Dictionary of Panel components for the page.
            Must include keys like 'A', 'B', 'C', etc.
            May include a 'title' key for a long descriptive page title.

    Returns:
        pn.Column: Assembled Panel layout.
    """
    long_title = content.get('title', page_name)

    if page_name == 'Attendance':
        return pn.Column(
            pn.pane.Markdown(f'## {long_title}'),
            center(
                pn.Row(
                    pn.Column(content.get('A'), sizing_mode='stretch_width'),
                    pn.Column(content.get('B'), sizing_mode='stretch_width'),
                    sizing_mode='stretch_width',
                ),
                width=1200,
                pad=50,
            ),
            center(
                pn.Row(
                    pn.Column(content.get('C'), sizing_mode='stretch_width'),
                    sizing_mode='stretch_width',
                ),
                width=1200,
            ),
        )
        
    if page_name == 'Points':
        return pn.Column(
        pn.pane.Markdown(f'## {long_title}'),

        center(
            pn.Row(
                pn.Column(content.get('A'), sizing_mode='stretch_width'),
                sizing_mode='stretch_width',
            ),
            width=1200,
        ),

        center(
            pn.Row(
                pn.Column(content.get('B'), sizing_mode='stretch_width'),
                pn.Column(
                    content.get('C'),
                    sizing_mode='stretch_width',
                    margin=(0, 20, 0, 0),  
                ),
                sizing_mode='stretch_width',
            ),
            width=1200,
        ),

        center(
            pn.Row(
                pn.Column(
                    content.get('D'),
                    sizing_mode='stretch_width',
                ),
                pn.Column(
                    content.get('E'),
                    sizing_mode='stretch_width',
                ),
                sizing_mode='stretch_width',
            ),
            width=1200,
        ),
    )


    if page_name == 'Goals':
        return pn.Column(
            pn.pane.Markdown(f'## {long_title}'),
            center(
                pn.Row(
                    pn.Column(content.get('A'), sizing_mode='stretch_width'),
                    pn.Column(content.get('B'), sizing_mode='stretch_width'),
                    sizing_mode='stretch_width',
                ),
                width=1200,
                pad=50,
            ),
            center(
                pn.Row(
                    pn.Column(content.get('C'), sizing_mode='stretch_width'),
                    sizing_mode='stretch_width',
                ),
                width=1200,
            ),
        )

    if page_name == 'Nationality':
        return pn.Column(
        pn.pane.Markdown(f'## {long_title}'),

        center(
            pn.Row(
                pn.Column(content.get('A'), sizing_mode='fixed'),
                sizing_mode='stretch_width',
            ),
            width=1200,
        ),

        center(
            pn.Row(
                pn.Column(content.get('B'), sizing_mode='fixed'),
                pn.Column(content.get('C'), sizing_mode='fixed', width=1200, height=900),
                sizing_mode='stretch_width',
            ),
            width=1200,
        ),
    )

    raise ValueError(f'Unknown page name: {page_name}')


def build_tabs(pages_dict, config):
    """Create a Panel Tabs object with icons from config."""
    icons = config.get('icons', {})
    tab_items = []

    for page_name in pages_dict:
        # Build a string label, not a Panel object
        if page_name in icons:
            icon = icons[page_name]
            label = f'{icon} {page_name}'
        else:
            label = page_name

        tab_items.append(
            (label, build_page_layout(page_name, pages_dict[page_name]))
        )

    return pn.Tabs(*tab_items, sizing_mode='stretch_width')


def build_dashboard(
    pages_dict,
    title,
    save_fig: bool = False,
    fig_name: str | None = None
):
    """Assemble the full dashboard template using WSL config settings.

    Args:
        pages_dict (dict): Page definitions passed to `build_tabs()`.
        title (str): Dashboard title displayed in the header.
        save_fig (bool): If True, save the dashboard as an HTML file.
        fig_name (str): Required if save_fig=True.

    Returns:
        pn.template.FastListTemplate: A complete dashboard template.
    """
    tabs = build_tabs(pages_dict, config={'icons': WSL_CLUB_BADGES})

    template = pn.template.FastListTemplate(
        title=title,
        logo=WSL_LOGO_URL,
        header_background=SEASON_AVG_COLOUR,
        main=[tabs],
        sidebar=[],
        collapsed_sidebar=True,
    )

    # Optional save (HTML only)
    if save_fig:
        if fig_name is None:
            raise ValueError('fig_name must be provided when save_fig=True')

        save_dir = REPORTS_OUT
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / f'wsl_project_{fig_name}.html'
        template.save(file_path, embed=True)
        print(f'Dashboard saved to: {file_path}')

    return template
