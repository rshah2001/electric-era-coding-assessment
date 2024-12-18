from typing import Dict, List, Set, Tuple
import sys
from dataclasses import dataclass


@dataclass
class AvailabilityReport:
    charger_id: int
    start_time: int
    end_time: int
    is_up: bool


class StationUptimeCalculator:
    def __init__(self):
        self.station_to_chargers: Dict[int, Set[int]] = {}
        self.charger_reports: Dict[int, List[AvailabilityReport]] = {}

    def parse_input_file(self, filepath: str) -> bool:
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()

            sections = content.split('[')
            if len(sections) != 3:  # Including empty first split
                return False

            # Parse Stations section
            stations_section = sections[1].split('\n')[1:-1]  # Skip header and empty line
            for line in stations_section:
                if not line.strip():
                    continue
                station_data = list(map(int, line.split()))
                if len(station_data) < 1:
                    return False
                station_id = station_data[0]
                charger_ids = set(station_data[1:])
                self.station_to_chargers[station_id] = charger_ids

            # Parse Charger Availability Reports section
            reports_section = sections[2].split('\n')[1:]  # Skip header
            for line in reports_section:
                if not line.strip():
                    continue
                charger_id, start_time, end_time, up_str = line.split()
                report = AvailabilityReport(
                    int(charger_id),
                    int(start_time),
                    int(end_time),
                    up_str.lower() == "true"
                )
                if report.start_time > report.end_time:
                    return False

                if report.charger_id not in self.charger_reports:
                    self.charger_reports[report.charger_id] = []
                self.charger_reports[report.charger_id].append(report)

            return True
        except Exception:
            return False

    def calculate_charger_uptime(self, reports: List[AvailabilityReport]) -> Tuple[int, int]:
        """Returns (uptime_duration, total_duration)"""
        if not reports:
            return (0, 0)

        # Sort reports by start time
        reports.sort(key=lambda x: x.start_time)

        # Find total time range
        start_time = min(report.start_time for report in reports)
        end_time = max(report.end_time for report in reports)
        total_duration = end_time - start_time

        # Calculate uptime
        uptime = 0
        current_time = start_time

        for report in reports:
            # Account for gaps between reports (counted as downtime)
            if report.start_time > current_time:
                current_time = report.start_time

            if report.is_up:
                uptime += report.end_time - current_time

            current_time = max(current_time, report.end_time)

        return (uptime, total_duration)

    def calculate_station_uptime(self) -> Dict[int, int]:
        result = {}

        for station_id, charger_ids in self.station_to_chargers.items():
            # Get all reports for all chargers at this station
            station_reports = []
            for charger_id in charger_ids:
                if charger_id in self.charger_reports:
                    station_reports.extend(self.charger_reports[charger_id])

            if not station_reports:
                result[station_id] = 0
                continue

            # Find total time range for the station
            start_time = min(report.start_time for report in station_reports)
            end_time = max(report.end_time for report in station_reports)
            total_duration = end_time - start_time

            # For each point in time, we need only one charger to be up
            timeline = []
            for report in station_reports:
                timeline.append((report.start_time, 1 if report.is_up else 0))
                timeline.append((report.end_time, -1 if report.is_up else 0))

            timeline.sort()

            current_up_chargers = 0
            current_time = start_time
            uptime = 0

            for time, delta in timeline:
                if current_up_chargers > 0:
                    uptime += time - current_time
                current_time = time
                current_up_chargers += delta

            # Calculate percentage and round down
            if total_duration == 0:
                result[station_id] = 0
            else:
                result[station_id] = int((uptime * 100) / total_duration)

        return result


def main():
    if len(sys.argv) != 2:
        print("ERROR")
        return

    calculator = StationUptimeCalculator()
    if not calculator.parse_input_file(sys.argv[1]):
        print("ERROR")
        return

    # Calculate and output results
    results = calculator.calculate_station_uptime()
    for station_id in sorted(results.keys()):
        print(f"{station_id} {results[station_id]}")


if __name__ == "__main__":
    main()