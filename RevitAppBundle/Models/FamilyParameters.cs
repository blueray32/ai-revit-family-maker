using System.Collections.Generic;

namespace RevitFamilyMaker
{
    public class FamilyCreationParams
    {
        // Metadata
        public string CompanyPrefix { get; set; } = "Generic";
        public string Category { get; set; }
        public string Subtype { get; set; }
        public string Version { get; set; } = "0.1.0";
        public string TemplateId { get; set; }
        public string TemplateHash { get; set; }

        // Dimensions (in original units, will be converted to feet)
        public double Width { get; set; }
        public string WidthUnit { get; set; } = "mm";
        public double Depth { get; set; }
        public string DepthUnit { get; set; } = "mm";
        public double Height { get; set; }
        public string HeightUnit { get; set; } = "mm";

        // Materials
        public string Material { get; set; }

        // Control parameters
        public Dictionary<string, bool> ControlParameters { get; set; }

        // Identity
        public string Manufacturer { get; set; }
        public string ModelNumber { get; set; }

        // Geometry options
        public string GeometrySource { get; set; } = "parametric"; // parametric|mesh|hybrid
        public string MeshFilePath { get; set; }
        public double MeshScale { get; set; } = 1.0;

        // Optional features
        public bool AddPerimeter { get; set; } = false;
    }

    public class FlexTestResults
    {
        public bool AllPassed { get; set; }
        public bool MinPassed { get; set; }
        public bool NominalPassed { get; set; }
        public bool MaxPassed { get; set; }
        public List<string> FailedTests { get; set; } = new List<string>();
    }

    public class ParameterInfo
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public string Value { get; set; }
        public string Unit { get; set; }
        public bool IsInstance { get; set; }
    }

    public class FamilyManifest
    {
        public string FamilyName { get; set; }
        public string RevitVersion { get; set; }
        public string Category { get; set; }
        public string TemplateId { get; set; }
        public string TemplateHash { get; set; }
        public List<ParameterInfo> Parameters { get; set; }
        public string GeometrySource { get; set; }
        public bool FlexTestPassed { get; set; }
        public FlexTestResults FlexTestResults { get; set; }
        public System.DateTime CreationTimestamp { get; set; }
        public long FileSizeBytes { get; set; }
        public string ApsJobId { get; set; }
        public string MeshLicenseUrl { get; set; }
    }
}
