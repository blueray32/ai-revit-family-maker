using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using DesignAutomationFramework;
using Newtonsoft.Json;
using System;
using System.IO;

namespace RevitFamilyMaker
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class FamilyMakerCommand : IExternalDBApplication
    {
        public ExternalDBApplicationResult OnStartup(ControlledApplication app)
        {
            DesignAutomationBridge.DesignAutomationReadyEvent += HandleDesignAutomationReady;
            return ExternalDBApplicationResult.Succeeded;
        }

        public ExternalDBApplicationResult OnShutdown(ControlledApplication app)
        {
            return ExternalDBApplicationResult.Succeeded;
        }

        private void HandleDesignAutomationReady(object sender, DesignAutomationReadyEventArgs e)
        {
            e.Succeeded = ProcessFamily(e.DesignAutomationData);
        }

        private bool ProcessFamily(DesignAutomationData data)
        {
            if (data == null) return false;

            Application app = data.RevitApp;
            if (app == null) return false;

            try
            {
                // Read input parameters from JSON
                string paramsPath = Path.Combine(Directory.GetCurrentDirectory(), "parameters.json");
                if (!File.Exists(paramsPath))
                {
                    LogError("Parameters file not found");
                    return false;
                }

                string paramsJson = File.ReadAllText(paramsPath);
                var parameters = JsonConvert.DeserializeObject<FamilyCreationParams>(paramsJson);

                if (parameters == null)
                {
                    LogError("Failed to deserialize parameters");
                    return false;
                }

                // Open family template
                string templatePath = Path.Combine(Directory.GetCurrentDirectory(), "template.rft");
                if (!File.Exists(templatePath))
                {
                    LogError($"Template file not found: {templatePath}");
                    return false;
                }

                Document familyDoc = app.OpenDocumentFile(templatePath);

                if (familyDoc == null || !familyDoc.IsFamilyDocument)
                {
                    LogError("Failed to open family template or not a family document");
                    return false;
                }

                LogSuccess($"Opened template: {templatePath}");

                // Create family using parameters
                var creator = new FamilyCreator(familyDoc);
                bool success = creator.CreateFamily(parameters);

                if (!success)
                {
                    LogError("Family creation failed");
                    return false;
                }

                LogSuccess("Family created successfully");

                // Run flex test
                var flexTester = new FlexTester(familyDoc);
                var flexResults = flexTester.RunFlexTest(parameters);

                if (!flexResults.AllPassed)
                {
                    LogError($"Flex test failed: {string.Join(", ", flexResults.FailedTests)}");
                    return false;
                }

                LogSuccess("Flex test passed");

                // Generate family name with versioning
                string familyName = GenerateFamilyName(parameters);
                string outputPath = Path.Combine(Directory.GetCurrentDirectory(), $"{familyName}.rfa");

                // Save family
                SaveAsOptions saveOptions = new SaveAsOptions
                {
                    OverwriteExistingFile = true
                };
                familyDoc.SaveAs(outputPath, saveOptions);

                LogSuccess($"Family saved: {outputPath}");

                // Generate JSON manifest
                var manifest = new FamilyManifest
                {
                    FamilyName = familyName,
                    RevitVersion = app.VersionNumber,
                    Category = parameters.Category,
                    TemplateId = parameters.TemplateId,
                    TemplateHash = parameters.TemplateHash,
                    Parameters = creator.GetParameterList(),
                    GeometrySource = parameters.GeometrySource,
                    FlexTestPassed = flexResults.AllPassed,
                    FlexTestResults = flexResults,
                    CreationTimestamp = DateTime.UtcNow,
                    FileSizeBytes = new FileInfo(outputPath).Length
                };

                string manifestPath = Path.Combine(Directory.GetCurrentDirectory(), $"{familyName}.json");
                File.WriteAllText(manifestPath, JsonConvert.SerializeObject(manifest, Formatting.Indented));

                LogSuccess($"Manifest saved: {manifestPath}");
                LogSuccess($"Family creation complete: {familyName}");

                return true;
            }
            catch (Exception ex)
            {
                LogError($"Exception: {ex.Message}\n{ex.StackTrace}");
                return false;
            }
        }

        private string GenerateFamilyName(FamilyCreationParams parameters)
        {
            // Format: {Company}_{Category}_{Subtype}_v{semver}
            string company = parameters.CompanyPrefix ?? "Generic";
            string category = parameters.Category.Replace(" ", "");
            string subtype = parameters.Subtype ?? "Default";
            string version = parameters.Version ?? "0.1.0";

            return $"{company}_{category}_{subtype}_v{version}";
        }

        private void LogError(string message)
        {
            Console.WriteLine($"ERROR: {message}");
            File.AppendAllText("error.log", $"{DateTime.Now}: {message}\n");
        }

        private void LogSuccess(string message)
        {
            Console.WriteLine($"SUCCESS: {message}");
        }
    }
}
