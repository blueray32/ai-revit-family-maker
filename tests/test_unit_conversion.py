"""Tests for unit conversion utilities."""

import pytest
from revit_family_maker.tools import to_feet, parse_dimension


class TestUnitConversion:
    """Test suite for unit conversion functions."""

    def test_to_feet_from_mm(self):
        """Test conversion from millimeters to feet."""
        # 2400mm = 7.874016 feet
        result = to_feet(2400, "mm")
        assert abs(result - 7.874016) < 0.001

    def test_to_feet_from_cm(self):
        """Test conversion from centimeters to feet."""
        # 100cm = 3.28084 feet
        result = to_feet(100, "cm")
        assert abs(result - 3.28084) < 0.001

    def test_to_feet_from_m(self):
        """Test conversion from meters to feet."""
        # 2m = 6.56168 feet
        result = to_feet(2, "m")
        assert abs(result - 6.56168) < 0.001

    def test_to_feet_from_in(self):
        """Test conversion from inches to feet."""
        # 24in = 2.0 feet
        result = to_feet(24, "in")
        assert abs(result - 2.0) < 0.001

    def test_to_feet_from_ft(self):
        """Test conversion from feet to feet (identity)."""
        result = to_feet(5.0, "ft")
        assert result == 5.0

    def test_to_feet_invalid_unit(self):
        """Test that invalid units raise ValueError."""
        with pytest.raises(ValueError, match="Unknown unit"):
            to_feet(100, "invalid")

    def test_to_feet_case_insensitive(self):
        """Test that unit names are case-insensitive."""
        assert to_feet(100, "MM") == to_feet(100, "mm")
        assert to_feet(100, "FT") == to_feet(100, "ft")

    def test_parse_dimension_mm(self):
        """Test parsing dimension with mm unit."""
        value, unit = parse_dimension("2400mm")
        assert value == 2400.0
        assert unit == "mm"

    def test_parse_dimension_with_space(self):
        """Test parsing dimension with space between value and unit."""
        value, unit = parse_dimension("8 ft")
        assert value == 8.0
        assert unit == "ft"

    def test_parse_dimension_decimal(self):
        """Test parsing dimension with decimal value."""
        value, unit = parse_dimension("3.5m")
        assert value == 3.5
        assert unit == "m"

    def test_parse_dimension_invalid(self):
        """Test that invalid dimensions raise ValueError."""
        with pytest.raises(ValueError, match="Cannot parse dimension"):
            parse_dimension("invalid")

    def test_revit_standard_dimensions(self):
        """Test common Revit dimensions convert correctly."""
        # Door height: 2100mm = 6.89 feet
        door_height = to_feet(2100, "mm")
        assert abs(door_height - 6.89) < 0.01

        # Door width: 900mm = 2.95 feet
        door_width = to_feet(900, "mm")
        assert abs(door_width - 2.95) < 0.01

        # Window height: 1200mm = 3.94 feet
        window_height = to_feet(1200, "mm")
        assert abs(window_height - 3.94) < 0.01
