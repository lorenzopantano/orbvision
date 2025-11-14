from typing import List
from pydantic import BaseModel, Field


class GPTLEResponse(BaseModel):
    """
    Represents a parsed TLE suitable for orbit projection and visualization.

    Each field corresponds to elements extracted from a standard 3-line TLE.
    """
    query_type: str = Field(..., description="Type of GP query: CATNR, INTDES, GROUP, NAME, SPECIAL. Used to identify the query category for orbit projection.")
    value: str = Field(..., description="Query value used to fetch this TLE. Essential for referencing the specific satellite data.")
    format: str = Field(..., description="Format of the original TLE data. Important for parsing and interpreting the orbit parameters correctly.")
    raw_data: List[str] = Field(..., description="Raw TLE lines as received from Celestrak. Provides the original data used to derive orbit parameters.")
    catalog_number: int = Field(..., description="NORAD catalog number, unique identifier for the satellite. Used to uniquely identify and track the satellite in orbit projections.")
    satellite_name: str = Field(..., description="Name of the satellite. Useful for labeling and identification in orbit visualization.")
    epoch: str = Field(..., description="Epoch of the TLE (YYDDD.FFFFFF), used for accurate position propagation. Marks the exact time for which the orbital elements are valid.")
    inclination: float = Field(..., description="Orbital inclination in degrees; affects latitude coverage. Determines the tilt of the satellite's orbit relative to Earth's equator.")
    raan: float = Field(..., description="Right Ascension of Ascending Node in degrees; orbit orientation relative to equator. Defines the horizontal orientation of the orbit.")
    eccentricity: float = Field(..., description="Orbital eccentricity; defines orbit shape (0=circular, 0-1=elliptical). Influences the orbit's shape and satellite's distance from Earth.")
    argument_of_perigee: float = Field(..., description="Argument of perigee in degrees; orientation of orbit ellipse within orbital plane. Specifies the location of the orbit's closest approach to Earth.")
    mean_anomaly: float = Field(..., description="Mean anomaly in degrees; satellite's position along orbit at epoch. Indicates the satellite's position in its orbit at the epoch time.")
    mean_motion: float = Field(..., description="Mean motion in revolutions per day; determines orbital period. Used to calculate how fast the satellite orbits the Earth.")
