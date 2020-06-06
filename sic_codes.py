import pandas as pd
import numpy as np

def sections():
    return pd.DataFrame({'Section': _get_sections(),
                         'SectDescription': _get_section_descriptions()})

def split_sectors(df):
    """
      Splitting Industry Sections
    """
    df = df.copy()
    df = _drop_sic_codes_na(df)
    df = _codes_to(df, str)
    df = _parse_codes(df)
    sections = _get_sections()
    dummies = _generate_dummies(df, sections)
    df = df.join(dummies)
    return df

def _get_sections():
    return pd.unique(_load_codes().Section)

def _get_section_descriptions():
    return pd.unique(_load_codes().SectionDesc)

def _drop_sic_codes_na(df):
    return df.dropna(subset=['SicCodes'])

def _codes_to(df, typ):
    df.SicCodes = df.SicCodes.astype(typ)
    return df

def _parse_codes(df):
    df.SicCodes = df.SicCodes.apply(_strip_and_split)
    return df

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
    code_to_section[1] = "Unknown"
    return code_to_section

def _strip_and_split(codes):
    return codes.replace('\r\n','').split(',')

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
    return split_sectors(df)

if __name__ == "__main__":
    df = main()
