from typing import Optional, List

from fastapi_camelcase import CamelModel


class CityAlias(CamelModel):
    id: Optional[str]
    country_iso3: Optional[str]
    province_code: Optional[str]
    official_name_en: Optional[str]
    official_name_fr: Optional[str]
    clli_code: Optional[str]
    st_vec_req: Optional[str]
    serv_addr_edits: Optional[str]
    legacy_txt: Optional[str]
    leca_cd: Optional[str]
    alias: Optional[List[str]] = []
