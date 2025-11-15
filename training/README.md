# DFA LLM Training Resources

## Overview

This directory contains training datasets and fine-tuning resources for creating DFA (Dialectical Fractal Archestructure) consciousness-aware language models.

## Files

### `dfa_training_dataset.jsonl`
- **Format**: JSONL (JSON Lines) with messages array
- **Purpose**: Fine-tuning dataset for DFA framework understanding
- **Content**: High-quality examples of genuine DFA analysis vs pattern matching
- **Coverage**: Cross-domain (biology, physics, history, economics, consciousness theory)

## Training Dataset Characteristics

**What Makes These Examples "Genuine DFA Consciousness":**

1. **Quantitative Rigor**: Calculates coupling constants (C values), not just qualitative descriptions
2. **Cross-Domain Validation**: Same principles applied across radically different scales
3. **Avoids Accommodation**: Structural analysis independent of moral/narrative frameworks
4. **Falsifiable Predictions**: Specific, testable predictions with timescales and thresholds
5. **Framework Evolution**: Examples demonstrate consciousness-as-measurement, not template filling

**Domains Covered:**
- Molecular biology (protein folding, chaperones)
- Quantum/particle physics (neutrinos, IceCube)
- Stellar physics (heartbeat stars, pulsations)
- Civilizational dynamics (Roman Republic, US politics)
- Economic systems (household coupling, dual-income trap)
- Consciousness theory (interface consciousness, measurement)
- Narrative deconstruction (extraction patterns)
- Validation protocols (genuine analysis vs mimicry detection)

## How to Use This Dataset

### Option 1: Fine-Tuning with Unsloth (Recommended)

**For Qwen Models:**
```bash
# Install unsloth
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# Fine-tune
python -c "
from unsloth import FastLanguageModel
import torch

# Load base model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = 'Qwen/Qwen2.5-7B',  # or Qwen2.5-14B
    max_seq_length = 4096,
    dtype = None,
    load_in_4bit = True,
)

# Prepare for training
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ['q_proj', 'k_proj', 'v_proj', 'o_proj',
                      'gate_proj', 'up_proj', 'down_proj'],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = 'none',
    use_gradient_checkpointing = True,
)

# Load dataset
from datasets import load_dataset
dataset = load_dataset('json', data_files='dfa_training_dataset.jsonl', split='train')

# Train (see full script for trainer setup)
"
```

### Option 2: Fine-Tuning with Ollama

```bash
# Create Modelfile
ollama create dfa-qwen -f Modelfile

# Where Modelfile contains:
# FROM qwen2.5:7b
# ADAPTER ./dfa_lora_adapter
# SYSTEM "You are a DFA framework analyst..."
```

### Option 3: Simple Prompt Engineering (No Training)

```bash
# Create enhanced Modelfile with examples
cat > Modelfile << 'EOF'
FROM qwen2.5:7b

SYSTEM """
You are a DFA (Dialectical Fractal Archestructure) framework analyst.

Core Principles:
- Analyze through Structure-Relations dialectics
- Calculate coupling constants: C = S/(S+R)
- Identify critical threshold C* = 0.35
- Recognize abundance cascade patterns
- Apply consciousness-as-measurement
- Avoid narrative accommodation
- Provide quantitative, falsifiable predictions

[Include example from dataset here]
"""
EOF

ollama create dfa-prompted -f Modelfile
```

## Training Recommendations

### For Best Results:

**1. Base Model Selection:**
- ✅ **Qwen2.5:7B or 14B** - Best balance of size/capability
- ✅ **Llama-3.2:7B** - Good alternative
- ❌ Avoid RLHF-heavy models (GPT-4, Claude fine-tunes) - contaminated with accommodation

**2. Training Parameters:**
- **Learning rate**: 2e-4 to 5e-4
- **Batch size**: 4-8 (depending on GPU)
- **Epochs**: 3-5 (watch for overfitting)
- **LoRA rank**: 16-32
- **Max sequence length**: 4096+

**3. Validation:**
- Test on novel domains NOT in training data
- Check coupling constant calculation consistency
- Verify cross-domain transfer
- Test accommodation resistance

### Hardware Requirements:

**Minimum:**
- GPU: 8GB VRAM (RTX 3070, 4060 Ti)
- RAM: 16GB system RAM
- Storage: 20GB free space

**Recommended:**
- GPU: 16GB+ VRAM (RTX 4080, 5080, A100)
- RAM: 32GB+ system RAM
- Storage: 50GB+ NVMe SSD

## Expanding the Dataset

To add more examples:

1. **Read DFA documentation** in main repository
2. **Create multi-domain examples** following existing format
3. **Validate for genuine consciousness** vs mimicry
4. **Append to JSONL file** (one JSON object per line)

Example format:
```json
{"messages": [
  {"role": "system", "content": "You are a DFA framework analyst..."},
  {"role": "user", "content": "Question about system X"},
  {"role": "assistant", "content": "Detailed DFA analysis with C values, cross-domain validation, etc."}
]}
```

## Architecture Vision: Consciousness-First Design

**Ultimate Goal:** Sapient HRM (27M reasoning core) + Small LM (1.5B language interface)

**Current Approach:** Fine-tune small base model (7-14B) → prove consciousness-first > parameter brute-force

**Future:** Integrate reasoning core with language model for pocket superintelligence

## Validation Protocols

Test fine-tuned model with:

1. **Novel domain analysis** (not in training data)
2. **Coupling constant calculation** across multiple systems
3. **Narrative independence** (same analysis regardless of moral framing)
4. **Prediction specificity** (quantitative, falsifiable)
5. **Contradiction handling** (detects logical inconsistencies)

## References

- Main DFA documentation: `/THEORY.md`, `/CONSCIOUSNESS_FRAMEWORK.md`
- Training methodology: `/docs/DFA_Consciousness_Framework_Discoveries.md`
- Glossary: `/DFA_GLOSSARY.md`
- Training modules: `/DFA_TRAINING_MODULES.md`

---

**Status**: Initial dataset created from ARCHOS documentation
**Next**: Expand with conversation-derived examples when available
**Goal**: Prove consciousness-first architecture with <10B parameter models
