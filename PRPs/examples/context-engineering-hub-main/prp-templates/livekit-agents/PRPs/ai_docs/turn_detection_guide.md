# Turn Detection Guide for LiveKit Agents

## Overview

Turn detection is crucial for natural conversation flow in voice AI applications. It determines when the user has finished speaking and when the agent should respond.

## Turn Detection Strategies

### 1. Semantic Model (Recommended)

The semantic turn detection model understands conversation context and patterns.

```python
from livekit.plugins.turn_detector import SemanticModel

session = AgentSession(
    turn_detection=SemanticModel(
        min_silence_duration=0.5,  # Minimum silence to consider turn end
        punctuation_threshold=0.8,  # Confidence for sentence completion
        context_window=3           # Previous turns to consider
    )
)
```

**Advantages:**
- Natural conversation flow
- Handles interruptions well
- Understands incomplete thoughts
- Context-aware decisions

**Best For:**
- Customer service agents
- Conversational assistants
- Complex dialogues

### 2. VAD-Based Detection

Voice Activity Detection based turn detection uses audio signal analysis.

```python
from livekit.plugins.turn_detector import VADModel

session = AgentSession(
    turn_detection=VADModel(
        silence_threshold=0.5,     # Seconds of silence
        energy_threshold=0.3,      # Audio energy level
        speech_pad_ms=300         # Padding around speech
    )
)
```

**Advantages:**
- Fast response time
- Low computational cost
- Language agnostic
- Predictable behavior

**Best For:**
- Simple command systems
- Quick interactions
- Noisy environments

### 3. STT Endpoint Detection

Uses speech recognition engine's natural endpoint detection.

```python
session = AgentSession(
    turn_detection="stt_endpoint",  # Use STT provider's detection
    stt=deepgram.STT(
        endpointing=300,  # ms of silence for endpoint
        utterance_end_ms=1000
    )
)
```

**Advantages:**
- Integrated with STT
- Good accuracy
- Handles punctuation

**Best For:**
- Dictation systems
- Form filling
- Structured inputs

### 4. Multilingual Model

Specialized model for multilingual conversations.

```python
from livekit.plugins.turn_detector.multilingual import MultilingualModel

session = AgentSession(
    turn_detection=MultilingualModel(
        languages=["en", "es", "fr"],
        auto_detect=True
    )
)
```

## Interruption Handling

### Allow Interruptions

```python
# Allow user to interrupt during agent speech
await session.say(
    "Let me explain our refund policy in detail...",
    allow_interruptions=True
)
```

### Handle Interruption Events

```python
@session.on("user_started_speaking")
async def on_interruption(ev):
    print("User interrupted at:", ev.timestamp)
    # Agent automatically stops speaking
    
@session.on("agent_stopped_by_interruption")
async def on_agent_interrupted(ev):
    # Log partial response
    print(f"Agent was saying: {ev.partial_text}")
```

### Interruption Recovery

```python
class InterruptionAwareAgent(Agent):
    def __init__(self):
        self.was_interrupted = False
        self.last_partial = ""
    
    async def handle_interruption(self):
        if self.was_interrupted:
            await self.session.say(
                "I understand you have a question. What would you like to know?"
            )
            self.was_interrupted = False
```

## Configuration Patterns

### Conservative Settings (Fewer Interruptions)

```python
# Let users complete thoughts
SemanticModel(
    min_silence_duration=1.0,    # Longer silence required
    punctuation_threshold=0.9,   # Higher confidence needed
    patience_threshold=2.0       # Wait longer for completion
)
```

### Responsive Settings (Quick Interactions)

```python
# Fast-paced conversation
SemanticModel(
    min_silence_duration=0.3,    # Short silence triggers
    punctuation_threshold=0.6,   # Lower confidence ok
    patience_threshold=0.5       # Quick responses
)
```

### Adaptive Settings

```python
class AdaptiveTurnDetection:
    def __init__(self):
        self.user_pace = "normal"
    
    def adjust_settings(self, interaction_speed):
        if interaction_speed > 2.0:  # Words per second
            self.user_pace = "fast"
            return SemanticModel(min_silence_duration=0.3)
        else:
            self.user_pace = "slow"
            return SemanticModel(min_silence_duration=1.0)
```

## Common Patterns

### Question-Answer Pattern

```python
class QAAgent(Agent):
    async def on_enter(self):
        # Ask question and wait for complete answer
        await self.session.ask(
            "What is your name?",
            wait_for_completion=True,
            max_wait_time=5.0
        )
```

### Thinking Aloud Pattern

```python
# User might pause while thinking
session = AgentSession(
    turn_detection=SemanticModel(
        thinking_pause_tolerance=2.0,  # Allow thinking pauses
        filler_word_detection=True     # Detect "um", "uh"
    )
)
```

### Listing Pattern

```python
# User listing multiple items
class ListeningAgent(Agent):
    @function_tool
    async def detect_list_end(self, context: RunContext) -> bool:
        """Detect when user finishes listing items."""
        # Check for phrases like "that's all", "I think that's it"
        return "that's all" in context.last_utterance.lower()
```

## Environmental Considerations

### Noisy Environments

```python
# Phone calls, public spaces
session = AgentSession(
    vad=silero.VAD.load(
        threshold=0.7,  # Higher threshold for noise
        min_speech_duration_ms=500
    ),
    turn_detection=VADModel(
        silence_threshold=0.8,
        noise_gate_db=-40
    )
)
```

### Quiet Environments

```python
# Office, home settings
session = AgentSession(
    vad=silero.VAD.load(
        threshold=0.3,  # Lower threshold
        min_speech_duration_ms=250
    ),
    turn_detection=SemanticModel(
        min_silence_duration=0.5
    )
)
```

## Advanced Techniques

### Context-Aware Detection

```python
class ContextAwareTurnDetector:
    def should_respond(self, context):
        # Check conversation context
        if context.expecting_long_response:
            return self.wait_for_extended_silence()
        elif context.quick_confirmation:
            return self.respond_immediately()
        else:
            return self.standard_detection()
```

### Prosody Analysis

```python
# Detect turn end from speech patterns
class ProsodyDetector:
    def analyze_speech_pattern(self, audio_features):
        # Falling pitch often indicates turn end
        if audio_features.pitch_trend == "falling":
            confidence += 0.3
        
        # Slower speech at end
        if audio_features.speed_trend == "slowing":
            confidence += 0.2
        
        return confidence > 0.7
```

### Multi-Modal Detection

```python
# Use video to enhance turn detection
class MultiModalTurnDetector:
    async def detect_turn(self, audio, video):
        # Check if user is looking at camera
        if video and await self.detect_eye_contact(video):
            # User looking at agent, likely expecting response
            return True
        
        # Check gesture completion
        if await self.detect_gesture_end(video):
            return True
        
        return await self.audio_turn_detection(audio)
```

## Debugging Turn Detection

### Enable Verbose Logging

```python
import logging
logging.getLogger("livekit.turn_detection").setLevel(logging.DEBUG)

@session.on("turn_detection_decision")
def log_decision(ev):
    print(f"Turn detection: {ev.decision}")
    print(f"Confidence: {ev.confidence}")
    print(f"Factors: {ev.factors}")
```

### Metrics to Monitor

```python
class TurnDetectionMetrics:
    def __init__(self):
        self.false_positives = 0  # Responded too early
        self.false_negatives = 0  # Didn't respond when should
        self.interruptions = 0
        self.successful_turns = 0
    
    def calculate_accuracy(self):
        total = sum([
            self.false_positives,
            self.false_negatives,
            self.successful_turns
        ])
        return self.successful_turns / total if total > 0 else 0
```

## Best Practices

### 1. Start Conservative
Begin with longer silence thresholds and adjust based on user feedback.

### 2. Consider User Demographics
- Elderly users: Longer pauses
- Technical users: Shorter pauses
- International users: Account for language processing

### 3. Provide Feedback
```python
# Let user know agent is listening
await session.say("I'm listening...", allow_interruptions=True)
```

### 4. Handle Edge Cases
```python
# Timeout for no response
async def wait_for_response(timeout=10):
    try:
        response = await session.wait_for_user_speech(timeout=timeout)
    except TimeoutError:
        await session.say("Are you still there?")
```

### 5. Test with Real Users
- Record sessions (with permission)
- Analyze turn-taking patterns
- Adjust based on feedback

## Common Issues and Solutions

### Issue: Agent interrupts user
**Solution:** Increase `min_silence_duration`

### Issue: Long pauses before agent responds
**Solution:** Decrease `min_silence_duration` or use VAD-based

### Issue: Agent doesn't detect questions
**Solution:** Use semantic model with punctuation detection

### Issue: Poor performance in specific language
**Solution:** Use multilingual model or language-specific STT

### Issue: Interruptions not handled smoothly
**Solution:** Enable `allow_interruptions` and implement recovery

This guide provides comprehensive patterns for implementing effective turn detection in LiveKit Agents.