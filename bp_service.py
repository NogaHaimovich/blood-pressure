import statistics
import logging
from typing import Dict, List, Union
from models import BloodPressure
from schemas import BloodPressureCreate, MonthlyUserReport
from storage import storage

logger = logging.getLogger(__name__)

class BloodPressureService:
    @staticmethod
    def _calculate_metric( values: List[int], func, name: str) -> float:
        if not values:
            logger.debug(f"Empty values list provided for {name} calculation")
            return 0.0
        result = func(values)
        logger.debug(f"Calculated {name}: {result} for {len(values)} values")
        return result

    def _calculate_user_stats(self, records: List[BloodPressure]) -> Dict[str, Union[int, float]]:
        logger.debug(f"Calculating statistics for {len(records)} records")

        systolic_values = [r.systolic for r in records]
        diastolic_values = [r.diastolic for r in records]
        pulse_pressures = [s - d for s, d in zip(systolic_values, diastolic_values)]

        stats = {
            "average_systolic": self._calculate_metric(systolic_values, statistics.mean, "mean"),
            "average_diastolic": self._calculate_metric(diastolic_values, statistics.mean, "mean"),
            "systolic_std": self._calculate_metric(systolic_values, statistics.pstdev, "std_dev"),
            "diastolic_std": self._calculate_metric(diastolic_values, statistics.pstdev, "std_dev"),
            "pulse_pressure_avg": self._calculate_metric(pulse_pressures, statistics.mean, "mean"),

            "high_readings_count": sum(1 for r in records if r.systolic > 140 or r.diastolic > 90),
            "low_readings_count": sum(1 for r in records if r.systolic < 100 or r.diastolic < 60),
        }

        logger.info(f"Calculated stats: avg_systolic={stats['average_systolic']:.1f}, "
                   f"high_readings={stats['high_readings_count']}, "
                   f"low_readings={stats['low_readings_count']}")
        return stats


    @staticmethod
    def add_bp_record(user_id: int, bp_create: BloodPressureCreate) -> BloodPressure:
        logger.info(f"Adding BP record for user {user_id}: {bp_create.systolic}/{bp_create.diastolic}")

        reading = BloodPressure(
            user_id=user_id,
            systolic=bp_create.systolic,
            diastolic=bp_create.diastolic,
            timestamp=bp_create.timestamp
        )

        try:
            storage.add_record(reading)
            logger.info(f"Successfully added BP record for user {user_id}")
            return reading
        except Exception as e:
            logger.error(f"Failed to add BP record for user {user_id}: {str(e)}")
            raise

    def calc_data_for_month_report(self, month: int, year: int) -> List[MonthlyUserReport]:
        logger.info(f"Generating monthly report for {year}-{month:02d}")

        logger.info(f"Retrieving records for {year}-{month:02d}")
        all_records = storage.get_records_for_month(month, year)

        if not all_records:
            logger.warning(f"No records found for {year}-{month:02d}")
            return []

        reports = []
        for user_id, records in all_records.items():
            logger.debug(f"Processing {len(records)} records for user {user_id}")
            stats = self._calculate_user_stats(records)
            report = MonthlyUserReport(
                user_id=user_id,
                measurements_count=len(records),
                **stats
            )
            reports.append(report)

        logger.info(f"Generated monthly report with {len(reports)} user reports")
        return reports