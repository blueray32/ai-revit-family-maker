using Autodesk.Revit.DB;
using System;
using System.Collections.Generic;

namespace RevitFamilyMaker
{
    public class FamilyCreator
    {
        private readonly Document _familyDoc;
        private readonly UnitConverter _unitConverter;
        private List<ParameterInfo> _parameters = new List<ParameterInfo>();

        public FamilyCreator(Document familyDoc)
        {
            _familyDoc = familyDoc ?? throw new ArgumentNullException(nameof(familyDoc));
            _unitConverter = new UnitConverter();
        }

        public bool CreateFamily(FamilyCreationParams parameters)
        {
            using (Transaction trans = new Transaction(_familyDoc, "Create Family"))
            {
                trans.Start();

                try
                {
                    // Step 1: Add family parameters
                    AddFamilyParameters(parameters);

                    // Step 2: Create simple geometry (parametric box for demonstration)
                    if (parameters.GeometrySource == "parametric" || parameters.GeometrySource == "hybrid")
                    {
                        CreateSimpleGeometry(parameters);
                    }

                    trans.Commit();
                    return true;
                }
                catch (Exception ex)
                {
                    trans.RollBack();
                    Console.WriteLine($"Family creation error: {ex.Message}");
                    return false;
                }
            }
        }

        private void AddFamilyParameters(FamilyCreationParams parameters)
        {
            FamilyManager fm = _familyDoc.FamilyManager;

            // Convert dimensions to feet
            double widthFeet = _unitConverter.ToFeet(parameters.Width, parameters.WidthUnit);
            double depthFeet = _unitConverter.ToFeet(parameters.Depth, parameters.DepthUnit);
            double heightFeet = _unitConverter.ToFeet(parameters.Height, parameters.HeightUnit);

            // Add dimensional parameters with DIM_ prefix
            AddParameter(fm, "DIM_Width", SpecTypeId.Length, widthFeet, false);
            AddParameter(fm, "DIM_Depth", SpecTypeId.Length, depthFeet, false);
            AddParameter(fm, "DIM_Height", SpecTypeId.Length, heightFeet, false);

            // Add material parameter if specified
            if (!string.IsNullOrEmpty(parameters.Material))
            {
                // Material parameters need special handling in Revit
                // For now, we'll add as text
                AddParameter(fm, "MTRL_Surface", SpecTypeId.String.Text, parameters.Material, true);
            }

            // Add identity parameters
            AddParameter(fm, "ID_Manufacturer", SpecTypeId.String.Text,
                parameters.Manufacturer ?? "Generic", false);
            AddParameter(fm, "ID_ModelNumber", SpecTypeId.String.Text,
                parameters.ModelNumber ?? "N/A", false);

            // Add scale parameter for mesh imports
            if (parameters.GeometrySource == "mesh" || parameters.GeometrySource == "hybrid")
            {
                AddParameter(fm, "DIM_Scale", SpecTypeId.Number, parameters.MeshScale, false);
            }
        }

        private void AddParameter(FamilyManager fm, string name, ForgeTypeId typeId, object value, bool isInstance)
        {
            try
            {
                // Check if parameter already exists
                FamilyParameter existingParam = fm.get_Parameter(name);
                if (existingParam == null)
                {
#if REVIT2024 || REVIT2025
                    existingParam = fm.AddParameter(name, GroupTypeId.IdentityData, typeId, isInstance);
#else
                    existingParam = fm.AddParameter(name, BuiltInParameterGroup.PG_IDENTITY_DATA, typeId, isInstance);
#endif
                }

                if (existingParam != null && value != null)
                {
                    // Set the value
                    if (value is double doubleValue)
                    {
                        fm.Set(existingParam, doubleValue);
                        _parameters.Add(new ParameterInfo
                        {
                            Name = name,
                            Type = typeId.TypeId,
                            Value = doubleValue.ToString("F6"),
                            Unit = "feet",
                            IsInstance = isInstance
                        });
                    }
                    else if (value is string stringValue)
                    {
                        fm.Set(existingParam, stringValue);
                        _parameters.Add(new ParameterInfo
                        {
                            Name = name,
                            Type = typeId.TypeId,
                            Value = stringValue,
                            Unit = "",
                            IsInstance = isInstance
                        });
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to add parameter {name}: {ex.Message}");
            }
        }

        private void CreateSimpleGeometry(FamilyCreationParams parameters)
        {
            // This is a simplified version
            // In production, you would create proper parametric geometry
            // using FamilyItemFactory, reference planes, dimensions, etc.

            // For now, we're just ensuring the family has parameters
            // The actual geometry creation would depend on the template
            Console.WriteLine("Geometry creation delegated to template");
        }

        public List<ParameterInfo> GetParameterList()
        {
            return _parameters;
        }
    }
}
