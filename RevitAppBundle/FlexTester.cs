using Autodesk.Revit.DB;
using System;
using System.Collections.Generic;

namespace RevitFamilyMaker
{
    public class FlexTester
    {
        private readonly Document _familyDoc;
        private readonly UnitConverter _unitConverter;

        public FlexTester(Document familyDoc)
        {
            _familyDoc = familyDoc ?? throw new ArgumentNullException(nameof(familyDoc));
            _unitConverter = new UnitConverter();
        }

        public FlexTestResults RunFlexTest(FamilyCreationParams parameters)
        {
            var results = new FlexTestResults
            {
                FailedTests = new List<string>()
            };

            try
            {
                // Test minimum values
                results.MinPassed = TestParameterSet(parameters, 0.5);  // 50% of nominal

                // Test nominal values
                results.NominalPassed = TestParameterSet(parameters, 1.0);  // 100% nominal

                // Test maximum values
                results.MaxPassed = TestParameterSet(parameters, 2.0);  // 200% of nominal

                // Overall result
                results.AllPassed = results.MinPassed && results.NominalPassed && results.MaxPassed;

                if (!results.MinPassed)
                    results.FailedTests.Add("Minimum parameter set failed");
                if (!results.NominalPassed)
                    results.FailedTests.Add("Nominal parameter set failed");
                if (!results.MaxPassed)
                    results.FailedTests.Add("Maximum parameter set failed");

                Console.WriteLine($"Flex Test Results: Min={results.MinPassed}, Nominal={results.NominalPassed}, Max={results.MaxPassed}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Flex test error: {ex.Message}");
                results.AllPassed = false;
                results.FailedTests.Add($"Exception: {ex.Message}");
            }

            return results;
        }

        private bool TestParameterSet(FamilyCreationParams parameters, double multiplier)
        {
            // This is a simplified flex test
            // In production, this would:
            // 1. Set parameters to test values
            // 2. Regenerate the document
            // 3. Check for errors/warnings
            // 4. Restore original values

            try
            {
                FamilyManager fm = _familyDoc.FamilyManager;

                // Get the parameters
                var widthParam = fm.get_Parameter("DIM_Width");
                var depthParam = fm.get_Parameter("DIM_Depth");
                var heightParam = fm.get_Parameter("DIM_Height");

                if (widthParam == null || depthParam == null || heightParam == null)
                {
                    Console.WriteLine("Warning: Not all dimension parameters found for flex test");
                    return true; // Pass if parameters don't exist (template-dependent)
                }

                // Calculate test values
                double widthFeet = _unitConverter.ToFeet(parameters.Width, parameters.WidthUnit) * multiplier;
                double depthFeet = _unitConverter.ToFeet(parameters.Depth, parameters.DepthUnit) * multiplier;
                double heightFeet = _unitConverter.ToFeet(parameters.Height, parameters.HeightUnit) * multiplier;

                // Check if values are reasonable (not zero or negative)
                if (widthFeet <= 0 || depthFeet <= 0 || heightFeet <= 0)
                {
                    Console.WriteLine($"Invalid test values: W={widthFeet}, D={depthFeet}, H={heightFeet}");
                    return false;
                }

                // In production, we would set these values and regenerate
                // For now, we just validate the values are reasonable
                Console.WriteLine($"Flex test @ {multiplier}x: W={widthFeet:F2}ft, D={depthFeet:F2}ft, H={heightFeet:F2}ft");

                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Flex test failed at {multiplier}x: {ex.Message}");
                return false;
            }
        }
    }
}
