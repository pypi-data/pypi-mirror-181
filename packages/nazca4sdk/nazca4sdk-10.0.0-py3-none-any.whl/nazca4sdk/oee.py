"""The OEE module allows you to calculate Overall Equipment Effectiveness
    The following functions are available:
    get_oee_simple() -> function to calculate OEE where availability,
    performance and quality are available
        Args:
            availability: float
            performance: float
            quality: float
        Return:
            OEE value: float
    get_oee_complex() -> function to calculate OEE where A, B, C, D, E, F params are available
        Args:
            A = Total available time: float
            B = Run time: float
            C = Production capacity: float
            D = Actual production: float
            E = Production output (same as actual production): float
            F = Actual good products (i.e. product output minus scraps): float
        Returns:
            OEE value: float
    get_availability() -> function to calculate Avaiability
    where run time and total time are available
        Args:
            run_time: float
            total_time: float
        Returns:
            Avaiability value: float
    get_performance() -> function to calculate Performance
    where actual production and production capacity are available
        Args:
            actual_production: float
            production_capacity: float
        Returns:
            Performance value: float
    get_quality() -> function to calculate Quality
    where actual products and production output are available
        Args:
            actual_products: float
            production_output: float
        Returns:
            Quality value: float"""

from pydantic import ValidationError
from nazca4sdk.businesslevel.oee_calculations import Oee

def get_oee_simple(availability: float, performance: float, quality: float):
    """The Overall Equipment Effectiveness (OEE)

    The Overall Equipment Effectiveness (OEE) is a proven way to monitor
    and improve process efficiency.
    it is considered as a diagnostic tool since it does not provide a solution to a given problem.
    OEE is a key process indicator that measures effectiveness and deviations
    from effective machine performance.

    OEE is calculated as:
        OEE = Availability x Performance x Quality
    Args:
        availability: float
        performance; float
        quality: float

    Return:
        OEE value: float

    Example:
        get_oee_simple(availability: 50, performance: 30, quality: 60)
    """
    try:
        oee = Oee()
        data = {"availability": availability,
                "performance": performance,
                "quality": quality
                }
        result = oee.calculate_oee_simple(data)/100
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_oee_complex(a: float, b: float, c: float, d: float, e: float, f: float):
    """The Overall Equipment Effectiveness (OEE)

    The Overall Equipment Effectiveness (OEE) is a proven way to monitor
    and improve process efficiency.
    it is considered as a diagnostic tool since it does not provide a solution to a given problem.
    OEE is a key process indicator that measures effectiveness and deviations
    from effective machine performance.

    Args:
    OEE depends on parameters as follows:
        A = Total available time
        B = Run time
        C = Production capacity
        D = Actual production
        E = Production output (same as actual production)
        F = Actual good products (i.e. product output minus scraps)
    where,
    A and B define Availability,
    C and D define Performance,
    E and F define Quality

    OEE is calculated as:

    OEE = (B/A) x (D/C) x (F/E)

    Returns:
        OEE value: float

    Example:
        get_oee_complex(A: 50, B: 40, C: 60, D: 20, E: 100, F: 10)
    """
    try:
        oee = Oee()
        data = {"A": a,
                "B": b,
                "C": c,
                "D": d,
                "E": e,
                "F": f
                }
        result = oee.calculate_oee_complete(data)*100
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_availability(run_time: float, total_time: float):
    """Availability

        Takes into account availability/time loss, which includes all events
        related to unplanned stops.
        (e.g. equipment failures, material shortages) and planned stops (e.g. changeover times).
        Availability measures the proportion of time a machine or cell runs
        from the total theoretical available time.
        Calculated as:
            Availability = Run time/Total available time
        Args:
            ::input -> dictionary with oee parameters::
            run_time, Run time in hours
            total_time, Total run time in hours

        Returns:
            availability value: float

        Example:
            get_availability(run_time: 30, total_time: 50)
        """
    try:
        oee = Oee()
        data = {"run_time": run_time,
                "total_time": total_time,
                }
        result = oee.calculate_availability(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_performance(actual_production: float, production_capacity: float):
    """Performance

        Takes into account performance/speed loss, which includes all the factors
        (e.g. slow cycles, small stops)
        that prevent the machine or cell to operate at maximum/optimal speed.
        It measures the proportion of produced units from the total number of possible
        produced units in a given run.

        Calculated as:
            Performance = Actual production/Production capacity

        Args:
            ::performance_input -> dictionary with performance parameters::
            actual_production, actual production
            production_capacity, production capacity

        Returns:
            performance value: float

        Example:
            get_performance(actual_production: 30, production_capacity: 50)
        """
    try:
        oee = Oee()
        data = {"actual_production": actual_production,
                "production_capacity": production_capacity,
                }
        result = oee.calculate_availability(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_quality(actual_products: float, production_output: float):
    """Quality

        Takes into account quality loss, which includes all the factors
        (e.g. reworks, scraps, defects).
        that lead to defective units that do not meet the customer’s quality
        standards and specifications.
        Quality measures the proportion of non-defective units compared
        to the total units produced.
        Calculated as:
            Quality = Actual good products/Product output
        Args:
            ::quality_input -> dictionary with performance parameters::
            actual_products, Actual good products
            production_output, Production output

        Returns:
            quality value: float

        Example:
            get_quality(actual_products: 30, production_output: 50)
        """
    try:
        oee = Oee()
        data = {"actual_products": actual_products,
                "production_output": production_output,
                }
        result = oee.calculate_quality(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None
