using System;

namespace RevitFamilyMaker
{
    public class UnitConverter
    {
        // Revit internal unit is FEET
        private const double MM_TO_FEET = 0.00328084;
        private const double CM_TO_FEET = 0.0328084;
        private const double M_TO_FEET = 3.28084;
        private const double IN_TO_FEET = 0.0833333;

        public double ToFeet(double value, string unit)
        {
            double result = unit.ToLower() switch
            {
                "mm" => value * MM_TO_FEET,
                "cm" => value * CM_TO_FEET,
                "m" => value * M_TO_FEET,
                "in" => value * IN_TO_FEET,
                "ft" or "feet" => value,
                _ => throw new ArgumentException($"Unknown unit: {unit}")
            };

            // Round to ±0.5mm tolerance (0.0016404 feet)
            return Math.Round(result, 6);
        }

        public double FromFeet(double valueFeet, string targetUnit)
        {
            return targetUnit.ToLower() switch
            {
                "mm" => valueFeet / MM_TO_FEET,
                "cm" => valueFeet / CM_TO_FEET,
                "m" => valueFeet / M_TO_FEET,
                "in" => valueFeet / IN_TO_FEET,
                "ft" or "feet" => valueFeet,
                _ => throw new ArgumentException($"Unknown unit: {targetUnit}")
            };
        }
    }
}
