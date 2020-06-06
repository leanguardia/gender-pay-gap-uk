import pandas as pd
import numpy as np

def drop_sic_codes_na(df):
    """ Removes all rows with missing SicCodes
    """
    return df.dropna(subset=['SicCodes']).reset_index(drop=True)

def clean_sic_codes(df):
    """ Cleans lists of SicCodes
    """
    df = _codes_to(df, str)
    df.SicCodes = df.SicCodes.apply(_strip_and_split)
    return df

def add_sections(df):
    """ Maps five digit SicCodes to single character Sections and stores them in SicSections
    """
    codes_to_section = _build_code_to_section_dict()
    sic_sections = df.SicCodes.apply(_map_codes_to_section, args=(codes_to_section,))
    df['SicSections'] = sic_sections
    return df

def explode_sections(df):
    """ Creates a row for each of the industry sections a company belongs.
        Additionaly, the section description is added in a new column
    """
    df = df.explode('SicSections')
    section_to_desc = _build_section_to_desc_dict()
    df['SectDesc'] = df.SicSections.map(section_to_desc)
    return df

# def split_sectors(df):
#     """Splitting Industry Sections"""
#     df = df.copy()
#     df = drop_sic_codes_na(df)
#     df = _codes_to(df, str)
#     df = clean_sic_codes(df)
#     sections = _get_sections()
#     dummies = _generate_dummies(df, sections)
#     df = df.join(dummies)
#     return df

def _get_sections():
    return pd.unique(_load_codes().Section)

def _get_section_descriptions():
    return pd.Series(_load_codes().SectionDesc.unique()).apply(_first_sentence)

def _codes_to(df, typ):
    df.SicCodes = df.SicCodes.astype(typ)
    return df

def _map_codes_to_section(codes, codes_to_section):
    return np.unique(
        [codes_to_section[int(code)] for code in codes if int(code) in codes_to_section]
    )

def _generate_dummies(df, sections):
    dummies = _build_empty_dummies(df, sections)
    code_to_section = _build_code_to_section_dict()
    for i, sic_codes in enumerate(df.SicCodes):
        sections = [code_to_section[int(code)] for code in sic_codes]
        indices = np.unique(dummies.columns.get_indexer(sections))
        dummies.iloc[i, indices] = 1
    return dummies.add_prefix('Sect')

def _build_empty_dummies(df, sections):
    zeroes = np.zeros((df.shape[0], len(sections)))
    return pd.DataFrame(zeroes, columns=sections, index=df.index)

def _build_code_to_section_dict():
    codes = _load_codes()
    code_to_section = {}
    for i, sic_code in enumerate(codes.SicCodes):
        row = codes.iloc[i]
        code_to_section[row.SicCodes] = row.Section
    # code_to_section[1] = "Unknown" # Uncomment to encode invalid value (1)
    return code_to_section

def _build_section_to_desc_dict():
    return dict(zip(_get_sections(), _get_section_descriptions()))

def _strip_and_split(codes):
    return codes.replace('\r\n','').split(',')

def _first_sentence(description):
    return description.split(';')[0]

def _load_codes():
    codes = pd.read_csv('data/sic_codes.csv')
    codes.rename(columns={
            "sic_code": "SicCodes",
            "section": "Section",
            "section_description": "SectionDesc"
        }, inplace=True)
    codes.drop(['sic_version'], axis='columns', inplace=True)
    codes = _codes_to(codes, int)
    return codes

def main():
    df = pd.read_csv('data/UK-Gender-Pay-Gap-Data-2018-2019.csv')
    df = drop_sic_codes_na(df)
    df = clean_sic_codes(df)
    return df

if __name__ == "__main__":
    df = main()
