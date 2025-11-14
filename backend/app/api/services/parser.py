from typing import List
from app.api.models.gp import GPTLEResponse


class Parser:
    """
    Parser utility class for Celestrak GP responses.
    Currently supports TLE parsing.
    Extend this class to support JSON, CSV, XML in the future.
    """

    @staticmethod
    def parse_tle(raw_lines: List[str]) -> List[GPTLEResponse]:
        """
        Parses raw TLE lines into structured GPCatalogResponse objects suitable for Three.js orbit projection.

        Args:
            raw_lines (List[str]): Raw lines from Celestrak TLE response.
                                   Assumes standard 3-line TLE format:
                                   Line 0: Satellite name
                                   Line 1: TLE line 1
                                   Line 2: TLE line 2

        Returns:
            List[GPCatalogResponse]: List of parsed TLEs as Pydantic models
        """
        parsed_tles = []
        for i in range(0, len(raw_lines), 3):
            try:
                name = raw_lines[i].strip()
                line1 = raw_lines[i + 1].strip()
                line2 = raw_lines[i + 2].strip()

                # Line 1
                catalog_number = int(line1[2:7])
                epoch = line1[18:32].strip()

                # Line 2
                inclination = float(line2[8:16].strip())
                raan = float(line2[17:25].strip())
                eccentricity = float("0." + line2[26:33].strip())
                argument_of_perigee = float(line2[34:42].strip())
                mean_anomaly = float(line2[43:51].strip())
                mean_motion = float(line2[52:63].strip())

                tle_model = GPTLEResponse(
                    query_type="CATNR",
                    value=str(catalog_number),
                    format="TLE",
                    raw_data=[name, line1, line2],
                    catalog_number=catalog_number,
                    satellite_name=name,
                    epoch=epoch,
                    inclination=inclination,
                    raan=raan,
                    eccentricity=eccentricity,
                    argument_of_perigee=argument_of_perigee,
                    mean_anomaly=mean_anomaly,
                    mean_motion=mean_motion
                )

                parsed_tles.append(tle_model)

            except (IndexError, ValueError):
                # Skip incomplete or malformed TLE entries
                continue

        return parsed_tles