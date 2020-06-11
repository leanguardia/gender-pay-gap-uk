## Gender Pay Gap in the UK
Data analysis of gender pay gap public reports from UK companies. This data is public and
available in the government's Gender pay gap service
[website](gender-pay-gap.service.gov.uk/). 

### Dependencies
- Python 3
- Jupyter Notebook
- Pandas
- Numpy
- Matplotlib
- Seaborn

### Files
- `UK-Gender-Pay-Gap.ipynb` Notebook containing the main analysis. It includes general descriptions, external
  references, the data transformation procedures, context narratives and the plotting scripts.
- `sic_codes.py` Module that handles SIC codes. It helps extending and transforming the original
  dataset with the companies' economic activities.
- `data/UK-Gender-Pay-Gap.csv` Dataset containing company pay gap reports of year 2018-2019.
- `data/sic_codes.csv` Datset with Standard Indutrial Classification codes for sectors and sections.

### Analysis Results

**1 - How balanced are pay quartiles by gender?**
In general, a big proportion of the highiest salaries in the workforce is assigned to men.

**2 - Which economic activities have the largest pay gap?**
Several employers with the largest pay gaps are involved in education and economic activities
such as construction, technical jobs, science and finances.

**3 - Which economic activities have the largest pay gap?**
Lower and  top pay quartiles of a company are key indicators to predict its pay gap. In
contrast, the size of the company does not seem to influence it.

### Acknowledgements
The "Data Science" nanodegree at Udacity. The "Applied Data Science" MSc unit
at University of Bristol. My group for the final project; Thor, Shivangi, Sharath, Steve and
Monica. Finally, Wes McKinney for writing "Python for Data Analysis".
