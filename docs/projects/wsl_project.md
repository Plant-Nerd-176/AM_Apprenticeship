# Exploring the impact of the Lionesses’ success on the Women’s Super League (WSL)
The WSL is the highest tier of professional women’s football in England, established in 2010. The 2018/19 season marked the first recognised fully professional season. Since its creation the women’s game has grown exponentially, with TV broadcasting deals featuring 57 live games per season, the creation of ‘FA Player’, a dedicated app for live streams, highlights and features from WSL. 

Moreover, the league has continued to expand, for the 2026/27 season the league will be expanded to 14 teams from 12.

Echoing this domestic growth, the Lionesses have achieved notable success in recent years. Wining the UEFA’s European Championship in 2022 (as hosts) and again in 2025, and finishing the 2023 World Cup as runners-up.

However, it’s unclear whether this national success has translated into the domestic league. According to WSL Football (n.d), the WSL saw an all-time high attendance rise in September 2022 following the first euro win. Whereas Humphreys (2025), reports that the WSL has “yet to see boom in attendances from Lionesses’ glory run”, they do acknowledge that the initial win saw interest pique, but that attendance has stagnated in recent years. 

### Aims and Objectives
This project explores whether the Lionesses’ successes have contributed to measurable growth within the WSL. Focusing on the following key area:

- Attendance and stadium capacity
- League performance/competitiveness (points, goal difference, etc.)
- Nationality diversity

### Data

- FBRef.com – primary source for seasonal league and nationality data
- Wikipedia – background context and stadium information
- FIFA official rankings – standardised measure of national team performance

> * All raw data can be viewed under the following (folder))[path_to_raw_data]
> * All processed data can be viewed under following (folder))[path_to_processed_data]

## Analysis & Results

### Data Cleaning
In order to analyse the data, generate insight and forecast what future seasons might look like the data had to be cleaned.

> Code relating to data cleaning and preprocessing can be viewed in the following [Jupyter Notebook](path_to_notebook1 'Notebook Name').

### EDA
Once the data was cleaned it was ready for exploratory data analysis, where a number of visualations and an interactive dashboard was created.

> Code relating to data visualisations can be viewed in the following [Jupyter Notebook](path_to_notebook2 'Notebook Name').

From this EDA we can observe the following:

- Key Attendance Highlights (2017/18–2024/25)
    - **Overall average attendance:** 3,909  
    - **Highest season averages:**
        - **2017/18:** 3,818 - Manchester City  
        - **2018/19:** 2,040 - Chelsea  
        - **2019/20:** 6,204 - Tottenham  
        - **2020/21:** COVID‑19 impacted  
        - **2021/22:** 3,567 - Manchester United  
        - **2022/23:** 19,245 - Arsenal  
        - **2023/24:** 29,999 - Arsenal  
        - **2024/25:** 28,808 - Arsenal  

    [Attendance Plot Figure]()

- Key Point Highlights:

    |           | Winners     | Highest Points         | Highest Points per Match |
    |-----------|-------------|------------------------|--------------------------|
    | 2017/18   | Chelsea     | 44 - Chelsea           | 2.44 - Chelsea           |
    | 2018/19   | Arsenal     | 54 - Arsenal           | 2.70 - Arsenal           |
    | 2019/20*  | Chelsea     | 40 - Manchester City   | 2.60 - Chelsea           |
    | 2020/21   | Chelsea     | 57 - Chelsea           | 2.59 - Chelsea           |
    | 2021/22   | Chelsea     | 56 - Chelsea           | 2.55 - Chelsea           |
    | 2022/23   | Chelsea     | 58 - Chelsea           | 2.64 - Chelsea           |
    | 2023/24   | Chelsea     | 55 - Chelsea           | 2.50 - Chelsea           |
    | 2024/25   | Chelsea     | 60 - Chelsea           | 2.73 - Chelsea           |
 
    * Due to the COVID-19 pandemic, the season ended early and the league was decided on a points-per-game basis 

- Key Goal Highlights
    - **Highest single‑season goal tally:** 22
    - **Top scorers by season:**
        - **2017/18:** 15 - Ellen White (English) for Birmingham City
        - **2018/19:** 22 - Vivianne Miedema (Dutch) for Arsenal
        - **2019/20:** 16 - Vivianne Miedema (Dutch) for Arsenal
        - **2020/21:** 21 - Sam Kerr (Australian) for Chelsea
        - **2021/22:** 20 - Sam Kerr (Australian) for Chelsea
        - **2022/23:** 22 - Rachel Daly (English) for Aston Villa
        - **2023/24:** 21 - Khadija Shaw (Jamaican) for Manchester City
        - **2024/25:** 12 - Alessia Russo (England) for Arsenal

- Nationality Representation Highlights
    - **English players** consistently form the largest group, though their share has declined slightly over time.
    - **European (non-English)** and **Non-European** players have increased in both presence and playing time.
    - The rise in international minutes suggests growing reliance on overseas talent, especially in attacking and midfield roles.
    - The league’s globalisation reflects broader investment and visibility in women’s football.

    [Nationality Distribution Plot Figure]()


### Forecasting

The next stage of the analysis was predictive modelling and forecasting.
> All code relating to the modelling element of this project can be viewed in the following [Jupyter Notebook](path_to_notebook3 'Notebook Name').

Predictive modelling focused on attendance as the target variable, using features such as performance indicators, stadium capacity, nationality composition, FIFA ranking, and Euro-win flags.

- Train-test split: Pre-2022 seasons for training; post-2022 for testing.
- Model performance:
    - Training: R² = 0.69, predictions within 10–15% variance.
    - Testing: R² = -0.21, indicating poor generalisation due to small dataset (<100 rows).

[Attendance Plot Figure]()

## Conclusions

Key Findings:
- Attendance: Initial spikes in attendance followed Euro wins, but growth seems to be plateauing
- League Performance:
    - Points have stayed in the high 50s (66-point max) and the gap between the top three has been narrow, making the title race competitive rather than a one-club dominance.
    - Top scorers hitting 20+ goals is exceptional given the usual low-to-mid teens average; the dip in 2024 suggests a more competitive season rather than declining quality.

In terms of nationality, the proportion of English players has decreased, while the number of European and non-European players has steadily increased.

The findings indicate that the WSL has been growing and maturing.

While the model captures historical trends relatively accurately, there’s reduced forecasting performance, this can be attributed to the limited dataset (<100 rows). Expanding the dataset to include attendance figures for every home game across all clubs would likely significantly improve predictive capability, resulting in a dataset of over 1,000 rows. Or exploring alternative models to better hand this type and size of data. Moreover, as the league continues to grow more seasonal could be added to this model to help improve the predictive capabilities.

Attendance and performance are influence but several external factors that cannot be represented by historical data alone, for example injuries to key players, managerial changes, fixture scheduling. In addition to broader element such as ticket pricing, the cost-of-living crisis, and travel costs.

While these findings contribute to understanding the drivers of growth in women’s football, football remains an inherently unpredictable, a factor that arguably underpins its popularity with fans.

## Reference 
Humphreys, J.P. (2025) WSL yet to see boom in attendances from Lionesses’ glory run, The Observer. Available at: https://observer.co.uk/news/sport/article/wsl-yet-to-see-boom-in-attendances-from-lionesses-glory-run.

WSL Football (no date) Official site of Barclays WSL, Barclays WSL2 & Subway League Cup, WSL Football. Available at: https://www.wslfootball.com/history.
