# AI Provider Matrix for LiveKit Agents

## Provider Comparison Overview

This guide helps you choose the right AI providers for your LiveKit Agents based on your specific requirements.

## Speech-to-Text (STT) Providers

| Provider | Model | Latency | Accuracy | Languages | Cost | Best For |
|----------|-------|---------|----------|-----------|------|----------|
| **Deepgram** | nova-2 | 200-300ms | 95%+ | 30+ | $0.0043/min | General use, best balance |
| **Deepgram** | nova-2-phonecall | 200-300ms | 96%+ | 30+ | $0.0048/min | Telephony |
| **AssemblyAI** | best | 300-500ms | 94%+ | 40+ | $0.00065/min | Accuracy focus |
| **Azure Speech** | latest | 250-400ms | 93%+ | 100+ | $0.006/min | Multi-language |
| **OpenAI Whisper** | whisper-1 | 500-1000ms | 95%+ | 50+ | $0.006/min | High accuracy |
| **Google STT** | latest_long | 300-400ms | 94%+ | 120+ | $0.006/min | Language variety |

### STT Configuration Examples

```python
# Deepgram - Recommended for most use cases
from livekit.plugins import deepgram

stt = deepgram.STT(
    model="nova-2",
    language="en",
    punctuate=True,
    endpointing=300,  # ms of silence for endpoint
    interim_results=True
)

# AssemblyAI - High accuracy
from livekit.plugins import assemblyai

stt = assemblyai.STT(
    sample_rate=16000,
    word_boost=["product_name", "company_name"],
    language_detection=True
)

# Azure - Multi-language support
from livekit.plugins import azure

stt = azure.STT(
    language="en-US",
    speech_recognition_language="en-US",
    enable_dictation=True
)
```

## Large Language Models (LLM)

| Provider | Model | First Token | Total Response | Context | Cost | Best For |
|----------|-------|-------------|----------------|---------|------|----------|
| **OpenAI** | gpt-4o-mini | 300-500ms | 2-3s | 128K | $0.15/1M | Cost-effective |
| **OpenAI** | gpt-4o | 400-600ms | 3-4s | 128K | $2.50/1M | Advanced reasoning |
| **Anthropic** | claude-3-haiku | 250-400ms | 2-3s | 200K | $0.25/1M | Fast, cheap |
| **Anthropic** | claude-3-sonnet | 400-600ms | 3-4s | 200K | $3/1M | Balanced |
| **Google** | gemini-1.5-flash | 300-500ms | 2-3s | 1M | $0.075/1M | Large context |
| **Groq** | llama-3-70b | 150-250ms | 1-2s | 8K | $0.70/1M | Ultra-fast |
| **Together** | mixtral-8x7b | 200-350ms | 1.5-2.5s | 32K | $0.60/1M | Open source |

### LLM Configuration Examples

```python
# OpenAI - Most popular choice
from livekit.plugins import openai

llm = openai.LLM(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=150,
    presence_penalty=0.1,
    frequency_penalty=0.1
)

# Anthropic - High quality responses
from livekit.plugins import anthropic

llm = anthropic.LLM(
    model="claude-3-haiku-20240307",
    temperature=0.5,
    max_tokens=200
)

# Groq - Fastest inference
from livekit.plugins import groq

llm = groq.LLM(
    model="llama3-70b-8192",
    temperature=0.7,
    max_tokens=150
)
```

## Text-to-Speech (TTS) Providers

| Provider | Voice Quality | Latency | Languages | Cost | Best For |
|----------|--------------|---------|-----------|------|----------|
| **OpenAI** | Good | 300-500ms | 50+ | $15/1M chars | Simple, reliable |
| **Cartesia** | Excellent | 200-300ms | 10+ | $8/1M chars | Fastest, natural |
| **ElevenLabs** | Best | 400-600ms | 29 | $30/1M chars | Premium quality |
| **PlayHT** | Excellent | 350-500ms | 40+ | $20/1M chars | Voice cloning |
| **Azure** | Good | 300-450ms | 100+ | $16/1M chars | Multi-language |
| **Google** | Good | 350-500ms | 50+ | $16/1M chars | Consistent |

### TTS Configuration Examples

```python
# OpenAI - Simple and reliable
from livekit.plugins import openai

tts = openai.TTS(
    voice="echo",  # or: alloy, fable, onyx, nova, shimmer
    speed=1.0,
    model="tts-1"  # or tts-1-hd for higher quality
)

# Cartesia - Fastest response
from livekit.plugins import cartesia

tts = cartesia.TTS(
    voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",
    model="sonic-english",
    speed=1.0,
    emotion="neutral"  # or: happy, sad, angry, surprise
)

# ElevenLabs - Premium quality
from livekit.plugins import elevenlabs

tts = elevenlabs.TTS(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    model="eleven_monolingual_v1",
    stability=0.5,
    similarity_boost=0.5
)
```

## Realtime Models (Speech-to-Speech)

| Provider | Model | Latency | Features | Cost | Best For |
|----------|-------|---------|----------|------|----------|
| **OpenAI** | Realtime API | 300-500ms | Audio in/out, tools | $0.06/min audio | Low latency voice |
| **Google** | Gemini Live | 400-600ms | Audio + video | $0.04/min | Multimodal |

### Realtime Model Configuration

```python
# OpenAI Realtime API
from livekit.plugins import openai

session = AgentSession(
    llm=openai.realtime.RealtimeModel(
        voice="echo",
        instructions="You are a helpful assistant",
        temperature=0.8,
        modalities=["text", "audio"]
    )
)

# Google Gemini Live
from livekit.plugins import google

session = AgentSession(
    llm=google.beta.realtime.RealtimeModel(
        voice="Puck",
        model="gemini-2.0-flash-exp",
        temperature=0.7
    )
)
```

## Voice Activity Detection (VAD)

| Provider | CPU Usage | Accuracy | Languages | Best For |
|----------|-----------|----------|-----------|----------|
| **Silero** | Low | 95%+ | Universal | Default choice |
| **WebRTC** | Very Low | 90% | Universal | Lightweight |
| **Custom** | Variable | Variable | Custom | Special needs |

```python
# Silero - Recommended
from livekit.plugins import silero

vad = silero.VAD.load(
    threshold=0.5,
    min_speech_duration_ms=250,
    min_silence_duration_ms=100
)
```

## Provider Selection Guide

### For Cost Optimization
```python
# Lowest cost configuration
session = AgentSession(
    stt=deepgram.STT(model="nova-2"),
    llm=openai.LLM(model="gpt-4o-mini"),
    tts=openai.TTS(voice="echo"),
    vad=silero.VAD.load()
)
# Approximate cost: $0.02-0.03 per minute
```

### For Lowest Latency
```python
# Fastest response configuration
session = AgentSession(
    llm=openai.realtime.RealtimeModel(voice="echo")
)
# Or traditional pipeline:
session = AgentSession(
    stt=deepgram.STT(model="nova-2"),
    llm=groq.LLM(model="llama3-8b-8192"),
    tts=cartesia.TTS(),
    vad=silero.VAD.load()
)
# First response: <500ms
```

### For Best Quality
```python
# Premium quality configuration
session = AgentSession(
    stt=deepgram.STT(model="nova-2"),
    llm=anthropic.LLM(model="claude-3-sonnet-20240229"),
    tts=elevenlabs.TTS(voice_id="premium_voice"),
    vad=silero.VAD.load()
)
# Higher cost but exceptional quality
```

### For Multi-Language Support
```python
# Multi-language configuration
session = AgentSession(
    stt=azure.STT(language_detection=True),
    llm=openai.LLM(model="gpt-4o"),
    tts=azure.TTS(auto_detect_language=True),
    vad=silero.VAD.load()
)
```

## Cost Estimation

### Per-Minute Costs (Approximate)

| Configuration | STT | LLM | TTS | Total |
|--------------|-----|-----|-----|-------|
| **Budget** | $0.004 | $0.01 | $0.01 | ~$0.024/min |
| **Balanced** | $0.004 | $0.02 | $0.02 | ~$0.044/min |
| **Premium** | $0.006 | $0.05 | $0.04 | ~$0.096/min |
| **Realtime** | Included | $0.06 | Included | ~$0.06/min |

### Monthly Cost Estimates

For 1000 hours of usage per month:

- **Budget Setup**: ~$1,440
- **Balanced Setup**: ~$2,640
- **Premium Setup**: ~$5,760
- **Realtime API**: ~$3,600

## Performance Benchmarks

### Latency Measurements

| Metric | Traditional Pipeline | Realtime Model |
|--------|---------------------|----------------|
| **First Word** | 1.5-2.5s | 300-500ms |
| **Full Response** | 3-5s | 1-2s |
| **Interruption** | 500ms | 100ms |
| **Turn Switch** | 1-2s | 300-500ms |

### Quality Metrics

| Provider Combo | WER (Word Error Rate) | User Satisfaction | Natural Flow |
|----------------|----------------------|-------------------|--------------|
| **Deepgram + OpenAI + OpenAI** | 5% | 4.2/5 | Good |
| **Deepgram + OpenAI + Cartesia** | 5% | 4.5/5 | Very Good |
| **Deepgram + Claude + ElevenLabs** | 4% | 4.7/5 | Excellent |
| **OpenAI Realtime** | 3% | 4.8/5 | Excellent |

## Provider-Specific Considerations

### OpenAI
- **Pros**: Well-documented, reliable, good all-around
- **Cons**: Rate limits, cost for premium models
- **Tips**: Use gpt-4o-mini for cost savings, cache responses

### Deepgram
- **Pros**: Fast, accurate, good for real-time
- **Cons**: Limited language support vs others
- **Tips**: Use nova-2-phonecall for phone audio

### Anthropic
- **Pros**: High quality, large context, safe outputs
- **Cons**: Higher latency, cost
- **Tips**: Use Claude Haiku for speed, Sonnet for quality

### ElevenLabs
- **Pros**: Best voice quality, voice cloning
- **Cons**: Higher cost, latency
- **Tips**: Pre-generate common responses

### Cartesia
- **Pros**: Fastest TTS, good quality
- **Cons**: Limited voices, newer service
- **Tips**: Great for latency-sensitive applications

## Migration Strategies

### Switching Providers

```python
# Easy provider switching with LiveKit Agents
def get_providers(config):
    """Select providers based on configuration."""
    
    if config.mode == "budget":
        return {
            "stt": deepgram.STT(model="nova-2"),
            "llm": openai.LLM(model="gpt-4o-mini"),
            "tts": openai.TTS(voice="echo")
        }
    elif config.mode == "premium":
        return {
            "stt": deepgram.STT(model="nova-2"),
            "llm": anthropic.LLM(model="claude-3-sonnet"),
            "tts": elevenlabs.TTS()
        }
    elif config.mode == "realtime":
        return {
            "llm": openai.realtime.RealtimeModel(voice="echo")
        }

# Use in session
providers = get_providers(config)
session = AgentSession(**providers)
```

### A/B Testing Providers

```python
import random

class ProviderABTest:
    def __init__(self):
        self.variants = {
            "A": {"tts": openai.TTS()},
            "B": {"tts": cartesia.TTS()},
            "C": {"tts": elevenlabs.TTS()}
        }
    
    def get_variant(self, user_id):
        # Consistent variant per user
        variant_key = hash(user_id) % len(self.variants)
        variant_name = list(self.variants.keys())[variant_key]
        return self.variants[variant_name]
```

This comprehensive provider matrix helps you make informed decisions about which AI providers to use for your LiveKit Agents based on your specific requirements and constraints.