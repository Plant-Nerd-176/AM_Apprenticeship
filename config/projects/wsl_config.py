""" Configuration settings for Women's Super League (WSL) project."""

from config.general_config import REPO_ROOT

# Project directory paths
PROJECT_FOLDER = REPO_ROOT / 'notebooks' / 'wsl_project'


# -------------------------------------------------------------------------
# Data Mappings
# -------------------------------------------------------------------------
SEASON_COL_MAP = {
    'Rk': 'Rank',
    'Squad': 'Club',
    'MP': 'Matches',
    'W': 'Wins',
    'D': 'Draws',
    'L': 'Losses',
    'GF': 'Goals_For',
    'GA': 'Goals_Against',
    'GD': 'Goal_Difference',
    'Pts': 'Points',
    'xG': 'Expected_Goals',
    'xGA': 'Expected_Goals_Allowed',
    'xGD': 'Expected_Goals_Difference',
    'xGD/90': 'Expected_Goals_Difference_Per_90_Mins',
    'Pts/MP': 'Points_Per_Match',
    'Attendance': 'Attendance',
    'Top Team Scorer': 'Top_Scorer',
    'Goalkeeper': 'Goalkeeper'
}

NATIONALITY_COL_MAP = {
    'Rk': 'Rank',
    'Nation': 'Nationality',
    '# Players': 'Num_Players',
    'Min': 'Minutes_Played',
    'List': 'List_of_Players'
}

CLUB_NAME_MAP = {
    'Tottenham_Hotspur': 'Tottenham',
    'West_Ham_United': 'West_Ham',
    'Manchester_United': 'Manchester_United',
    'Brighton_&_Hove_Albion': 'Brighton'
}

EURO_COUNTRIES = [
    'England',
    'Wales',
    'Scotland',
    'Republic_of_Ireland',
    'Netherlands',
    'Germany',
    'Sweden',
    'Northern_Ireland',
    'Belgium'
    'Norway',
    'Denmark',
    'Switzerland',
    'Austria',
    'Finland',
    'France',
    'Iceland',
    'Portugal',
    'Poland',
    'Spain',
    'Czech_Republic',
    'Greece',
    'Italy',
    'Russia',
    'Slovenia',
    'Serbia',
    'Hungary'
    ]

#-------------------------------------------------------------------------
# Column Groups
#-------------------------------------------------------------------------
WSL_DROP_COLUMNS = [
    'Notes',
    'Goalkeeper',
    'Expected_Goals',
    'Expected_Goals_Allowed',
    'Expected_Goals_Difference',
    'Expected_Goals_Difference_Per_90_Mins'
    'Top_Scorer',
    ]

NATIONALITY_DROP_COLUMNS = [
    'List_of_Players',
    'euro_flag',
    ]

#-------------------------------------------------------------------------
# Visualisation settings
#-------------------------------------------------------------------------
# Colour schemes
WSL_CLUB_COLOURS = {
    'Arsenal': '#db0007', 
    'Aston_Villa': '#670e36', 
    'Birmingham_City': '#095cd2', 
    'Brighton': '#095cd2', 
    'Bristol_City': '#E21A23',
    'Chelsea': '#034694', 
    'Crystal_Palace': '#1B458F', 
    'Everton': '#274488', 
    'Leicester_City': '#0053a0', 
    'Liverpool': '#d00027', 
    'Manchester_City': '#97c1e7', 
    'Manchester_United': '#DA291C',
    'Reading': '#004494',
    'Sunderland': '#eb172b',
    'Tottenham': '#132257',
    'West_Ham': '#7c2c3b', 
    'Yeovil_Town': '#348a6e'}

SEASON_AVG_COLOUR = '#3d195b'
FALLBACK_COLOUR = '#7f7f7f'

# Logo paths
WSL_LOGO_URL = 'https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/WSL_Football.png/250px-WSL_Football.png'

WSL_CLUB_BADGES = {
    'Arsenal': 'https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/960px-Arsenal_FC.svg.png', 
    'Aston_Villa': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Aston_Villa_FC_new_crest.svg/960px-Aston_Villa_FC_new_crest.svg.png', 
    'Birmingham_City': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/68/Birmingham_City_FC_logo.svg/960px-Birmingham_City_FC_logo.svg.png',
    'Brighton': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/960px-Brighton_%26_Hove_Albion_logo.svg.png', 
    'Bristol_City': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Bristol_City_crest.svg/960px-Bristol_City_crest.svg.png',
    'Chelsea': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/960px-Chelsea_FC.svg.png', 
    'Crystal_Palace': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/960px-Crystal_Palace_FC_logo_%282022%29.svg.png', 
    'Everton': 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/Everton_FC_logo.svg/960px-Everton_FC_logo.svg.png', 
    'Leicester_City': 'https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Leicester_City_crest.svg/960px-Leicester_City_crest.svg.png', 
    'Liverpool': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/960px-Liverpool_FC.svg.png', 
    'Manchester_City': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/960px-Manchester_City_FC_badge.svg.png', 
    'Manchester_United': 'https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/960px-Manchester_United_FC_crest.svg.png',
    'Reading': 'https://upload.wikimedia.org/wikipedia/en/thumb/1/11/Reading_FC.svg/960px-Reading_FC.svg.png',
    'Sunderland': 'https://upload.wikimedia.org/wikipedia/en/thumb/7/77/Logo_Sunderland.svg/1280px-Logo_Sunderland.svg.png',
    'Tottenham': 'https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/500px-Tottenham_Hotspur.svg.png',
    'West_Ham': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/960px-West_Ham_United_FC_logo.svg.png', 
    'Yeovil_Town': 'https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/Yeovil_Town_FC_crest.svg/960px-Yeovil_Town_FC_crest.svg.png'
    }
