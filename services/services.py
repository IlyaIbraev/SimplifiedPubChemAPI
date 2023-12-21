import aiohttp

async def get_properties_by_cid(cid: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/",
        ) as response:
            response_json = await response.json(encoding="windows-1251")
    data = {}
    data["CID"] = cid
    data["Name"] = response_json["Record"]["RecordTitle"]
    data["Image"] = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
    data["Properties"] = {}
    for section in response_json["Record"]["Section"]:
        if section["TOCHeading"] in ("Chemical and Physical Properties"):
            for subsection in section["Section"]:
                if subsection["TOCHeading"] in ("Computed Properties", "Experimental Properties"):
                    for subsubsection in subsection["Section"]:
                        if "Value" in subsubsection:
                            subsubsection_val = "Value"
                        else:
                            subsubsection_val = "Information"
                        data["Properties"][subsubsection["TOCHeading"]] = []
                        for information in subsubsection[subsubsection_val]:
                            try:
                                if "StringWithMarkup" in information["Value"]:
                                    data["Properties"][subsubsection["TOCHeading"]].append(information["Value"]["StringWithMarkup"][0]["String"])
                                else:
                                    data["Properties"][subsubsection["TOCHeading"]].append(information["Value"]["Number"][0])
                            except:
                                pass
    return data

async def get_cid_by_name(nametype: str, name: str) -> tuple[int, int]:

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{nametype}/{name}/cids/json") as response:
            data = await response.json(encoding="Windows-1252")
            status_code = response.status
    
    if status_code == 200:
        cid = data["IdentifierList"]["CID"][0]
        return cid, status_code
    return 0, status_code
    

    