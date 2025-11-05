# Real Test Setup Guide

This guide shows you how to run a REAL test with your actual OpenAI API key.

## What You Need

**Required for real test**:
- ✅ Your real OpenAI API key

**NOT required** (these are stubbed):
- ❌ APS credentials (mocked - won't actually call APS)
- ❌ Image-to-3D API key (mocked - won't actually call the service)
- ❌ Template catalog (uses mock templates)

## Setup

Create a `.env` file with your real OpenAI key:

```bash
cd "AI Revit Family Maker Assistant"

# Create .env file
cat > .env << 'EOF'
# REAL OpenAI API key (this will be used)
LLM_API_KEY=sk-proj-your-actual-openai-key-here
LLM_MODEL=gpt-4o-mini  # Or gpt-4, gpt-3.5-turbo

# Dummy values for stubbed services (won't be called)
APS_CLIENT_ID=dummy_id
APS_CLIENT_SECRET=dummy_secret
APS_DA_NICKNAME=dummy
APS_DA_ACTIVITY=DummyActivity
APS_TEMPLATE_URL=https://dummy.com/templates/
OUTPUT_BUCKET_OR_PATH=/tmp/revit_test
IMAGE_TO_3D_PROVIDER=promeai
IMAGE_TO_3D_API_KEY=dummy_key
EOF

# Make output directory
mkdir -p /tmp/revit_test
```

## Run Real Test

### Test 1: Simple Door Creation

```bash
python main.py "Create a door 2100mm high by 900mm wide"
```

**What happens**:
- ✅ Real LLM (GPT-4) processes your request
- ✅ Agent uses real reasoning to understand "door 2100mm x 900mm"
- ✅ Converts 2100mm → 6.89 feet, 900mm → 2.95 feet
- ✅ Selects door template and category
- ✅ Calls tool: `generate_family_from_prompt`
- ⚠️ APS workitem execution is STUBBED (prints mock output)
- ⚠️ No actual .rfa file created (APS is mocked)

**Expected output**:
```
🏗️  Revit Family Maker Agent
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
  Template: https://dummy.com/templates/DoorTemplate_2025.rft
  Activity: DummyActivity.prod
  Output: /tmp/revit_test/Generic_Doors_2025_v0.1.0.rfa

✅ Family generation complete!
```

### Test 2: Window with Hybrid Mode

```bash
python main.py "Create a window 1200mm x 1500mm"
```

### Test 3: Interactive Mode

```bash
python main.py
# Then type: "Create a table 2400mm x 900mm x 750mm"
```

### Test 4: Python API

Create `test_real_api.py`:

```python
import asyncio
from revit_family_maker import create_agent, create_dependencies

async def test_real():
    print("🧪 Real Test with OpenAI")
    print("=" * 60)

    agent = create_agent()
    deps = create_dependencies()

    prompts = [
        "Create a door 2100mm by 900mm",
        "Create a window 4ft by 3ft with grilles",
        "Create a table 2.4m x 0.9m x 0.75m",
    ]

    for prompt in prompts:
        print(f"\n📝 Testing: {prompt}")
        print("-" * 60)

        result = await agent.run(prompt, deps=deps)

        print("✅ Result:")
        print(result.data)
        print()

if __name__ == "__main__":
    asyncio.run(test_real())
```

Run it:
```bash
python test_real_api.py
```

## What Gets Tested

### ✅ Real (Using Your OpenAI Key)
1. **LLM reasoning**: GPT-4 understands your intent
2. **Category detection**: Agent identifies Doors, Windows, Furniture
3. **Dimension parsing**: Extracts "2100mm", "4ft", "2.4m"
4. **Unit conversion**: Converts to Revit's internal feet
5. **Tool selection**: Agent decides which tool to call
6. **Parameter generation**: Creates proper DIM_*, MTRL_* parameters
7. **Naming**: Generates `{Company}_{Category}_{Subtype}_v{semver}`

### ⚠️ Stubbed (Mock Output)
1. **APS workitem execution**: Prints "[STUB]" message
2. **Image-to-3D service**: Returns mock mesh URL
3. **Template catalog**: Uses 3 hardcoded mock templates
4. **File storage**: Logs output but doesn't persist

### ❌ Not Tested (Need Full Production Setup)
1. Actual .rfa file creation
2. Real Revit API operations
3. Flex testing in Revit
4. BIM360/ACC storage

## Verify It's Using Your Real Key

You can verify it's using your real OpenAI key by:

1. **Check the output**: You'll see intelligent responses that understand context
2. **Check your OpenAI dashboard**: You'll see API usage
3. **Try a tricky prompt**: "Create a door for a residential bathroom"
   - Real GPT-4 will infer reasonable dimensions (~2100mm x 800mm)
   - Mock would fail

## Cost Estimate

- **GPT-4o-mini**: ~$0.01 per test (very cheap)
- **GPT-4**: ~$0.10-0.20 per test (reasonable)
- **GPT-3.5-turbo**: ~$0.001 per test (almost free)

Recommendation: Start with `gpt-4o-mini` for testing.

## Troubleshooting

### "Invalid API key"
- Check your key starts with `sk-proj-` or `sk-`
- Make sure there are no spaces or newlines
- Try the key directly with OpenAI: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $LLM_API_KEY"`

### "Rate limit exceeded"
- You're hitting OpenAI's rate limits
- Wait a minute and try again
- Or use a different model (gpt-3.5-turbo has higher limits)

### "Model not found"
- Change `LLM_MODEL=gpt-4o-mini` or `gpt-3.5-turbo`
- Some accounts don't have GPT-4 access

## What This Proves

Running a real test with your OpenAI key proves:

✅ The agent architecture works
✅ Tool routing and selection works
✅ LLM integration is correct
✅ Unit conversion is accurate
✅ Parameter generation follows standards
✅ Error handling works
✅ The whole Pydantic AI pipeline functions

The only thing NOT proven is the actual Revit API integration (APS), which requires:
- Deploying the C# AppBundle
- Real APS credentials
- Template catalog setup

But that's expected - the agent logic is separate from the external service integrations.

## Ready to Test!

1. Add your OpenAI key to `.env`
2. Run: `python main.py "Create a door 2100mm x 900mm"`
3. Watch the magic happen! ✨
