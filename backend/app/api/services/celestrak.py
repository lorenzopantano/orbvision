from enum import Enum
from typing import List, Optional, Dict
import httpx
import asyncio


# -----------------------------
# Enums for Queries
# -----------------------------
class GPQuery(str, Enum):
    CATNR = "CATNR"        # Catalog Number
    INTDES = "INTDES"      # International Designator
    GROUP = "GROUP"        # Standard groups of satellites
    NAME = "NAME"          # Satellite name search
    SPECIAL = "SPECIAL"    # Special datasets


class GPGroup(str, Enum):
    """Standard groups from Celestrak"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    STATIONS = "STATIONS"
    GPS_OPS = "GPS-OPS"
    GALILEO = "GALILEO"
    GLONASS = "GLONASS-OPS"
    IRIDIUM = "IRIDIUM"
    STARLINK = "STARLINK"
    BEIDOU = "BEIDOU"
    INTELSAT = "INTELSAT"
    GEO = "GEO"


class GPSpecial(str, Enum):
    """Special datasets"""
    GPZ = "GPZ"                 # GEO Protected Zone
    GPZ_PLUS = "GPZ-PLUS"       # GPZ Plus
    DECAYING = "DECAYING"       # Potential Decays


class GPFormat(str, Enum):
    """Supported output formats"""
    TLE = "TLE"
    THREE_LE = "3LE"
    TWO_LE = "2LE"
    XML = "XML"
    KVN = "KVN"
    JSON = "JSON"
    JSON_PRETTY = "JSON-PRETTY"
    CSV = "CSV"


# -----------------------------
# Optional Flags
# -----------------------------
class GPFlag(str, Enum):
    BSTAR = "BSTAR"
    SHOW_OPS = "SHOW-OPS"
    OLDEST = "OLDEST"
    DOCKED = "DOCKED"
    MOVERS = "MOVERS"


# -----------------------------
# Celestrak Base URLs
# -----------------------------
BASE_GP_URL = "https://celestrak.org/NORAD/elements/gp.php"
BASE_GP_FIRST_URL = "https://celestrak.org/NORAD/elements/gp-first.php"
BASE_TABLE_URL = "https://celestrak.org/NORAD/elements/table.php"


# -----------------------------
# Generic Fetcher
# -----------------------------
async def fetch_gp_data(
    query_type: GPQuery,
    value: str,
    format: GPFormat = GPFormat.TLE,
    flags: Optional[List[GPFlag]] = None,
    custom_url: Optional[str] = None
) -> List[str]:
    """
    Fetch Celestrak GP data for any query type with optional flags.

    Args:
        query_type (GPQuery): Type of query (CATNR, INTDES, GROUP, NAME, SPECIAL)
        value (str): Query value (e.g., satellite name, catalog number)
        format (GPFormat): Output format (default: TLE)
        flags (Optional[List[GPFlag]]): Optional flags (SHOW-OPS, BSTAR, etc.)
        custom_url (Optional[str]): For alternative endpoints (gp-first, table)

    Returns:
        List[str]: Raw data lines from Celestrak
    """
    url = custom_url if custom_url else BASE_GP_URL

    params: Dict[str, str] = {query_type.value: value, "FORMAT": format.value}

    if flags:
        for flag in flags:
            params[flag.value] = ""  # Flags are present without value

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text.splitlines()


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    async def main():
        # Example 1: Fetch active satellites in TLE format
        active_tle = await fetch_gp_data(
            query_type=GPQuery.GROUP,
            value=GPGroup.ACTIVE.value
        )
        print("Active satellites (first 6 lines):")
        print("\n".join(active_tle[:6]))

        # Example 2: Fetch ISS by catalog number in KVN format
        iss_kvn = await fetch_gp_data(
            query_type=GPQuery.CATNR,
            value="25544",
            format=GPFormat.KVN
        )
        print("\nISS KVN data:")
        print("\n".join(iss_kvn[:6]))

        # Example 3: Fetch GEO Protected Zone in CSV with flags
        gpz_csv = await fetch_gp_data(
            query_type=GPQuery.SPECIAL,
            value=GPSpecial.GPZ.value,
            format=GPFormat.CSV,
            flags=[GPFlag.SHOW_OPS]
        )
        print("\nGEO Protected Zone CSV (first 6 lines):")
        print("\n".join(gpz_csv[:6]))

    asyncio.run(main())