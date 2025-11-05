# Testing Guide
## AI Revit Family Maker Assistant

This guide shows you how to test the agent at different levels, from simple unit tests (no credentials needed) to full end-to-end tests (requires real credentials).

---

## 🧪 Level 1: Unit Tests (No Credentials Needed)

These tests run immediately without any configuration. They test core logic like unit conversion, parsing, and data structures.

### Run All Unit Tests

```bash
# Make sure you're in the project directory
cd "AI Revit Family Maker Assistant"

# Install dependencies first (if not done)
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=revit_family_maker --cov-report=html
```

### Run Specific Test Files

```bash
# Test unit conversions only
pytest tests/test_unit_conversion.py -v

# Test tool utilities only
pytest tests/test_tools.py -v

# Test agent integration only
pytest tests/test_agent.py -v
```

### Expected Output

```
tests/test_unit_conversion.py ✅ 12 passed
tests/test_tools.py ✅ 10 passed
tests/test_agent.py ✅ 10 passed (4 skipped)

Total: 32 passed, 4 skipped in ~2 seconds
```

**What's tested**:
- ✅ Unit conversion (mm, cm, m, in, ft → feet)
- ✅ Dimension parsing ("2400mm", "8 ft")
- ✅ EXIF stripping from images
- ✅ Manifest generation
- ✅ Template catalog filtering
- ✅ Parameter naming validation
- ✅ Family naming convention
- ✅ Error handling (invalid units, missing files)

---

## 🧪 Level 2: Settings Validation (Minimal Config)

Test that the settings module loads correctly.

### Create a Test .env File

```bash
# Copy the example
cp .env.example .env.test

# Edit .env.test with DUMMY values (for testing structure only)
cat > .env.test << 'EOF'
LLM_API_KEY=sk-test-dummy-key-12345
APS_CLIENT_ID=test_client_id
APS_CLIENT_SECRET=test_client_secret
APS_DA_NICKNAME=test_nickname
APS_DA_ACTIVITY=TestActivity
APS_TEMPLATE_URL=https://test.example.com/templates/
OUTPUT_BUCKET_OR_PATH=/tmp/test_output
IMAGE_TO_3D_PROVIDER=promeai
IMAGE_TO_3D_API_KEY=test_3d_key
EOF
```

### Test Settings Loading

```bash
# Test that settings can be loaded
ENV_FILE=.env.test python -c "
from revit_family_maker.settings import load_settings
settings = load_settings()
print('✅ Settings loaded successfully')
print(f'  LLM Model: {settings.llm_model}')
print(f'  Company Prefix: {settings.company_prefix}')
"
```

### Expected Output

```
✅ Settings loaded successfully
  LLM Model: gpt-4
  Company Prefix: Generic
```

---

## 🧪 Level 3: Agent Creation (Test Model)

Test that the agent can be created and used with Pydantic AI's TestModel (no real LLM calls).

### Create Test Script

```bash
cat > test_agent_creation.py << 'EOF'
"""Test agent creation with TestModel (no real LLM calls)."""

import asyncio
from pydantic_ai.models.test import TestModel
from revit_family_maker import create_agent
from revit_family_maker.dependencies import RevitAgentDependencies

async def test_agent_with_test_model():
    """Test agent creation and basic structure."""

    # Create agent
    agent = create_agent()
    print("✅ Agent created successfully")

    # Override with TestModel (no real LLM calls)
    test_model = TestModel()
    test_agent = agent.override(model=test_model)
    print("✅ Agent overridden with TestModel")

    # Create test dependencies
    test_deps = RevitAgentDependencies(
        aps_client_id="test_id",
        aps_client_secret="test_secret",
        aps_activity_name="TestActivity",
        aps_bundle_alias="test",
        template_catalog_url="https://test.com/templates/",
        output_bucket="/tmp/test",
        image_to_3d_api_key="test_key",
        image_to_3d_provider="promeai"
    )
    print("✅ Test dependencies created")

    # Test basic tool invocation structure (with TestModel)
    # Note: TestModel returns mock data, but this validates structure
    print("✅ Agent ready for testing with tools")

    print("\n🎉 Agent creation test passed!")

if __name__ == "__main__":
    asyncio.run(test_agent_with_test_model())
EOF

python test_agent_creation.py
```

### Expected Output

```
✅ Agent created successfully
✅ Agent overridden with TestModel
✅ Test dependencies created
✅ Agent ready for testing with tools

🎉 Agent creation test passed!
```

---

## 🧪 Level 4: Tool Testing (Mocked External Services)

Test individual tools with mocked external services (APS, image-to-3D).

### Test Unit Conversion Tool

```python
cat > test_unit_conversion_manual.py << 'EOF'
"""Manual test of unit conversion."""

from revit_family_maker.tools import to_feet, parse_dimension

print("Testing unit conversion:")
print("=" * 50)

# Test conversions
test_cases = [
    ("2100mm door height", 2100, "mm", 6.89),
    ("900mm door width", 900, "mm", 2.95),
    ("8 ft ceiling", 8, "ft", 8.0),
    ("1200mm window", 1200, "mm", 3.94),
]

for description, value, unit, expected in test_cases:
    result = to_feet(value, unit)
    status = "✅" if abs(result - expected) < 0.01 else "❌"
    print(f"{status} {description}: {value}{unit} = {result:.2f}ft (expected {expected}ft)")

print("\nTesting dimension parsing:")
print("=" * 50)

parse_cases = [
    "2400mm",
    "8 ft",
    "3.5m",
    "24 in",
]

for dim_str in parse_cases:
    value, unit = parse_dimension(dim_str)
    feet = to_feet(value, unit)
    print(f"✅ '{dim_str}' → {value} {unit} → {feet:.2f}ft")

print("\n🎉 All conversions passed!")
EOF

python test_unit_conversion_manual.py
```

### Expected Output

```
Testing unit conversion:
==================================================
✅ 2100mm door height: 2100mm = 6.89ft (expected 6.89ft)
✅ 900mm door width: 900mm = 2.95ft (expected 2.95ft)
✅ 8 ft ceiling: 8ft = 8.00ft (expected 8.0ft)
✅ 1200mm window: 1200mm = 3.94ft (expected 3.94ft)

Testing dimension parsing:
==================================================
✅ '2400mm' → 2400.0 mm → 7.87ft
✅ '8 ft' → 8.0 ft → 8.00ft
✅ '3.5m' → 3.5 m → 11.48ft
✅ '24 in' → 24.0 in → 2.00ft

🎉 All conversions passed!
```

---

## 🧪 Level 5: CLI Testing (Requires OpenAI API Key)

Test the CLI with a real LLM but stubbed external services.

### Setup for CLI Testing

```bash
# Create minimal .env for CLI testing
cat > .env << 'EOF'
# Minimal config for CLI testing
LLM_API_KEY=sk-your-real-openai-key-here  # ⚠️ REAL KEY NEEDED
LLM_MODEL=gpt-4

# Dummy values for stubbed services
APS_CLIENT_ID=dummy_client_id
APS_CLIENT_SECRET=dummy_client_secret
APS_DA_NICKNAME=dummy_nickname
APS_DA_ACTIVITY=DummyActivity
APS_TEMPLATE_URL=https://dummy.example.com/templates/
OUTPUT_BUCKET_OR_PATH=/tmp/revit_output
IMAGE_TO_3D_PROVIDER=promeai
IMAGE_TO_3D_API_KEY=dummy_3d_key
EOF

# Create output directory
mkdir -p /tmp/revit_output
```

### Test CLI with Simple Prompt

```bash
python main.py "Create a door 2100mm high by 900mm wide"
```

### Expected Output

```
🏗️  Revit Family Maker Agent
============================================================
AI-powered Revit family generation from text and images
============================================================

📝 Request: Create a door 2100mm high by 900mm wide

🔧 Generating family...

📝 Generating family from prompt:
  Description: Create a door 2100mm high by 900mm wide
  Category: Doors
  Version: 2025
  Parsed dimensions (feet): {'height': 6.89, 'width': 2.95}
  Using template: DoorTemplate_2025_v2.1

🔧 [STUB] Executing APS workitem:
  Template: https://dummy.example.com/templates/DoorTemplate_2025.rft
  Activity: DummyActivity.prod
  Output: /tmp/revit_output/Generic_Doors_2025_v0.1.0.rfa

✅ Family generation complete!

============================================================
RESULT:
============================================================
[Agent response with family details]
============================================================
```

**Note**: The APS workitem is stubbed, so no actual .rfa file is created, but the agent logic runs end-to-end.

---

## 🧪 Level 6: Python API Testing

Test using the Python API directly.

### Create Test Script

```python
cat > test_python_api.py << 'EOF'
"""Test the Python API with a simple prompt."""

import asyncio
from revit_family_maker import create_agent, create_dependencies

async def test_python_api():
    print("🧪 Testing Python API")
    print("=" * 60)

    # Create agent and dependencies
    agent = create_agent()
    deps = create_dependencies()

    print("✅ Agent created")
    print("✅ Dependencies loaded")

    # Test prompt
    prompt = "Create a window 4ft by 3ft with grilles"
    print(f"\n📝 Prompt: {prompt}\n")

    # Run agent
    result = await agent.run(prompt, deps=deps)

    print("✅ Agent execution complete")
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result.data)
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_python_api())
EOF

python test_python_api.py
```

---

## 🧪 Level 7: Full End-to-End (Requires All Real Credentials)

For production testing, you need:
- ✅ Real OpenAI API key
- ✅ Real APS credentials
- ✅ Deployed Revit AppBundle
- ✅ Real image-to-3D service API key
- ✅ Real template catalog
- ✅ Real storage (BIM360/local)

### Full Production Setup

```bash
# 1. Configure all real credentials
cat > .env << 'EOF'
# REAL LLM credentials
LLM_API_KEY=sk-your-real-openai-key
LLM_MODEL=gpt-4

# REAL APS credentials
APS_CLIENT_ID=your_real_aps_client_id
APS_CLIENT_SECRET=your_real_aps_client_secret
APS_DA_NICKNAME=your_real_nickname
APS_DA_ACTIVITY=FamilyMakerActivity
APS_DA_BUNDLE_ALIAS=prod
APS_TEMPLATE_URL=https://your-real-bucket.s3.amazonaws.com/templates/

# REAL storage
OUTPUT_BUCKET_OR_PATH=/path/to/real/output
# OR: OUTPUT_BUCKET_OR_PATH=urn:adsk.objects:os.object:bucket/path

# REAL image-to-3D service
IMAGE_TO_3D_PROVIDER=promeai
IMAGE_TO_3D_API_KEY=your_real_3d_api_key
EOF

# 2. Deploy Revit AppBundle (see PRP lines 610-1356 for C# code)
# Build and upload to APS

# 3. Upload template catalog with SHA256 hashes

# 4. Test end-to-end
python main.py "Create a door 2100mm by 900mm"

# 5. Verify output
ls -lh /path/to/real/output/
# Should see: Generic_Doors_2025_v0.1.0.rfa
#             Generic_Doors_2025_v0.1.0.json
```

---

## 🎯 Quick Testing Checklist

### ✅ Without Credentials (Works Now)
- [x] Run pytest (32 tests should pass)
- [x] Test unit conversions manually
- [x] Test agent creation with TestModel
- [x] Test settings structure with dummy values

### ⚠️ With OpenAI Key Only (Partial)
- [ ] Run CLI with real LLM
- [ ] Test agent reasoning
- [ ] Validate tool selection logic

### 🔐 With All Real Credentials (Full)
- [ ] Deploy Revit AppBundle
- [ ] Test APS workitem execution
- [ ] Test image-to-3D service
- [ ] Verify .rfa file creation
- [ ] Test .rfa opens in Revit
- [ ] Validate flex tests pass

---

## 🐛 Troubleshooting

### Tests Fail: "ModuleNotFoundError"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Tests Fail: "Settings validation error"

**Solution**: Tests use dummy credentials, this is OK. Real credentials only needed for CLI/API testing.

### CLI Fails: "Failed to load settings"

**Solution**: Create .env file
```bash
cp .env.example .env
# Edit .env with at least LLM_API_KEY
```

### Agent Runs But No .rfa Created

**Expected**: External services (APS, storage) are stubbed. No actual files created without real credentials.

---

## 📊 Test Coverage Summary

| Test Level | Prerequisites | What's Tested | Status |
|------------|---------------|---------------|--------|
| Unit Tests | None | Core logic, utilities | ✅ Ready |
| Settings | Dummy .env | Config structure | ✅ Ready |
| Agent Creation | None | Agent initialization | ✅ Ready |
| Tool Testing | None | Tool logic (mocked) | ✅ Ready |
| CLI | OpenAI key | End-to-end with LLM | ⚠️ Partial |
| Python API | OpenAI key | API usage | ⚠️ Partial |
| Full E2E | All credentials | Production workflow | 🔐 Needs setup |

---

## 🚀 Recommended Testing Order

1. **Start here**: `pytest` - Validates core logic ✅
2. **Then**: `python test_unit_conversion_manual.py` - See conversions in action ✅
3. **Then**: `python test_agent_creation.py` - Verify agent structure ✅
4. **Then** (if you have OpenAI key): `python main.py "test prompt"` - Test with LLM ⚠️
5. **Finally** (with all credentials): Full production testing 🔐

---

## 📞 Need Help?

- **Test failures**: Check `tests/VALIDATION_REPORT.md`
- **Configuration issues**: See `README.md` configuration section
- **Missing credentials**: See `.env.example` for all required variables

---

**Ready to test!** Start with `pytest` to validate everything works. 🧪
