from fastapi import APIRouter, Query
from typing import List, Optional
from app.api.services.celestrak import fetch_gp_data, GPQuery, GPFormat, GPFlag
from app.api.services.parser import Parser

router = APIRouter()


# -----------------------------
# Predefined endpoints
# -----------------------------
@router.get("/iss")
async def get_iss_tle():
    """Fetch TLE data for the ISS (catalog number 25544)"""
    gp = await fetch_gp_data(query_type=GPQuery.CATNR, value="25544", format=GPFormat.TLE)
    gp = Parser.parse_tle(gp)
    return gp


@router.get("/active")
async def get_active_satellites():
    """Fetch TLEs for all active satellites"""
    element = await fetch_gp_data(query_type=GPQuery.GROUP, value="ACTIVE", format=GPFormat.TLE)
    return {"tle_data": element}

# -----------------------------
# Generic endpoint
# -----------------------------
@router.get("/")
async def get(
    query_type: GPQuery = Query(..., description="Type of query: CATNR, INTDES, GROUP, NAME, SPECIAL"),
    value: str = Query(..., description="Value corresponding to the query type"),
    format: GPFormat = Query(GPFormat.TLE, description="Format of the returned data"),
    flags: Optional[str] = Query(None, description="Comma-separated list of flags (e.g., SHOW-OPS,BSTAR)")
):
    """
    Generic endpoint for fetching GP data from Celestrak.
    Example:
    /tle/generic?query_type=GROUP&value=ACTIVE&format=TLE&flags=SHOW-OPS,BSTAR
    """
    flag_list: Optional[List[GPFlag]] = None
    if flags:
        flag_list = [GPFlag(f.strip()) for f in flags.split(",")]

    element = await fetch_gp_data(query_type=query_type, value=value, format=format, flags=flag_list)
    return {"tle_data": element}