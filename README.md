# MQCO - Model Quality & Cost Optimization

A project to systematically optimize LLM model selection based on quality requirements and cost constraints.

## Goal

Reduce LLM API costs while maintaining (or improving) output quality by:
1. Understanding the cost/quality landscape
2. Measuring our actual needs
3. Routing tasks to appropriate models
4. Continuously monitoring and adjusting

## Project Structure

```
mqco/
├── README.md           # This file
├── RESEARCH.md         # Market research on pricing, benchmarks, evaluation
├── check_billing.py    # Utility to validate Anthropic API key
└── (future)
    ├── benchmarks/     # Our custom benchmark tests
    ├── data/           # Usage data, test datasets
    └── router/         # Model routing implementation
```

## Quick Stats (Feb 2026)

| Tier | Example Models | Input $/M | Output $/M |
|------|----------------|-----------|------------|
| Budget | DeepSeek V3, Gemini Flash | $0.10-0.27 | $0.40-1.10 |
| Mid | GPT-5, Claude Sonnet | $1.25-3.00 | $10-15 |
| Premium | Claude Opus, o3 | $5-15 | $25-75 |

**Potential savings: 10-100x** by routing appropriately.

## Next Steps

1. [ ] Document current token usage
2. [ ] Set up DeepEval framework
3. [ ] Create benchmark test suite
4. [ ] Design routing strategy

## See Also

- [RESEARCH.md](./RESEARCH.md) - Full research findings
