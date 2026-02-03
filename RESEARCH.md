# MQCO Research: Model Quality & Cost Optimization

*Research compiled: 2026-02-03*

---

## Executive Summary

The LLM landscape in 2025-2026 is intensely competitive with pricing varying by **orders of magnitude** between providers. This research covers:
1. Current pricing across major providers
2. Quality benchmarks and leaderboards
3. Evaluation frameworks and metrics
4. Recommendations for our optimization strategy

---

## 1. Current LLM Pricing (as of Feb 2026)

### Price per Million Tokens (Input / Output)

| Model | Provider | Input $/M | Output $/M | Context | Notes |
|-------|----------|-----------|------------|---------|-------|
| **Budget Tier** |
| DeepSeek V3 | DeepSeek | $0.27 | $1.10 | 128K | Cache hits: $0.028 |
| Gemini 2.0 Flash | Google | $0.10 | $0.40 | 1M | Fast, cheap |
| GPT-4o mini | OpenAI | $0.15 | $0.60 | 128K | Good for simple tasks |
| Llama 4 Scout | Meta/Hosted | $0.11 | $0.34 | 10M | 2600 t/s - blazing fast |
| Nova Micro | Amazon | $0.04 | $0.14 | 128K | Cheapest option |
| **Mid Tier** |
| GPT-5 | OpenAI | $1.25 | $10.00 | 400K | Flagship |
| Gemini 2.5 Pro | Google | $1.25 | $10.00 | 1M | Large context |
| Claude 4 Sonnet | Anthropic | $3.00 | $15.00 | 200K | Good coding |
| Gemini 3 Pro | Google | $2.00 | $12.00 | 10M | Huge context |
| **Premium Tier** |
| Claude Opus 4.5 | Anthropic | $5.00 | $25.00 | 200K | Top SWE-Bench |
| Claude Opus 4.1 | Anthropic | $15.00 | $75.00 | 200K | Deep reasoning |
| OpenAI o3 | OpenAI | $10.00 | $40.00 | 200K | Reasoning model |
| GPT-4.5 | OpenAI | $75.00 | $150.00 | 128K | Most expensive |

### Key Pricing Insights

1. **DeepSeek is the cost leader** - ~90% cheaper than comparable models
2. **Flash/Mini models** are 10-50x cheaper than flagship versions
3. **Caching** can reduce input costs by 90% (Anthropic, DeepSeek, OpenAI)
4. **Batch processing** often offers 50% discounts

---

## 2. Quality Benchmarks

### Top Performers by Task (2025-2026 Data)

#### GPQA Diamond (Science: Biology, Physics, Chemistry)
| Model | Score |
|-------|-------|
| GPT 5.2 | 92.4% |
| Gemini 3 Pro | 91.9% |
| GPT 5.1 | 88.1% |
| Grok 4 | 87.5% |

#### AIME 2024 (Competitive Math)
| Model | Score |
|-------|-------|
| GPT 5.2 | 100% |
| Gemini 3 Pro | 100% |
| Kimi K2 Thinking | 99.1% |

#### SWE-Bench (GitHub Issue Resolution - Agentic Coding)
| Model | Score |
|-------|-------|
| **Claude Sonnet 4.5** | **82%** |
| Claude Opus 4.5 | 80.9% |
| GPT 5.2 | 80% |
| GPT 5.1 | 76.3% |
| Gemini 3 Pro | 76.2% |

#### MMLU (Broad Knowledge)
| Model | Score |
|-------|-------|
| Gemini 3 Pro | 91.8% |
| Claude Opus 4.5 | 90.8% |
| Claude Opus 4.1 | 89.5% |

#### Humanity's Last Exam (Hardest Multi-Domain)
| Model | Score |
|-------|-------|
| Gemini 3 Pro | 45.8% |
| Kimi K2 Thinking | 44.9% |
| GPT-5 | 35.2% |

### Speed Benchmarks

| Model | Tokens/sec | Time to First Token |
|-------|------------|---------------------|
| Llama 4 Scout | 2,600 | 0.33s |
| Llama 3.3 70b | 2,500 | 0.52s |
| Gemini 2.0 Flash | 257 | 0.34s |
| GPT oss 20b | 564 | 4.0s |
| Claude 3.7 Sonnet | 78 | 0.91s |

---

## 3. Evaluation Frameworks

### LLM-as-a-Judge (Recommended Approach)

Using an LLM to evaluate other LLM outputs. More accurate than traditional metrics (BLEU/ROUGE) because it captures semantic nuance.

**Key Metrics:**
- **Answer Relevancy** - Does output address the input?
- **Correctness** - Factually accurate vs ground truth?
- **Hallucination** - Contains made-up information?
- **Faithfulness** - Sticks to provided context? (RAG)
- **Task Completion** - Did the agent complete its goal?
- **Tool Correctness** - Did it call the right tools?

### DeepEval Framework

Open-source Python framework for LLM evaluation. Key features:
- G-Eval metric (research-backed, human-aligned scoring)
- DAG (Deep Acyclic Graph) for complex evaluations
- RAG-specific metrics (contextual precision/recall)
- Agentic metrics (task completion, tool use)
- Red teaming for 40+ safety vulnerabilities
- Standard benchmarks (MMLU, HumanEval, TruthfulQA, etc.)

```python
# Example: Basic DeepEval test
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

def test_correctness():
    metric = GEval(
        name="Correctness",
        criteria="Is the actual output correct based on expected output?",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        threshold=0.5
    )
    test_case = LLMTestCase(
        input="What's your return policy?",
        actual_output="30-day full refund.",
        expected_output="We offer a 30-day full refund."
    )
    assert_test(test_case, [metric])
```

### Other Evaluation Resources

- **LMSYS Chatbot Arena** - Crowdsourced ELO rankings from blind comparisons
- **HuggingFace Open LLM Leaderboard** - Aggregated benchmark scores
- **Vellum LLM Leaderboard** - Cost + quality comparisons
- **pricepertoken.com** - Daily updated pricing

---

## 4. Cost Optimization Strategies

### Immediate Wins

1. **Use tiered models** - Route simple queries to cheap models (GPT-4o mini, Gemini Flash), complex to premium
2. **Enable caching** - Anthropic prompt caching, OpenAI cached inputs reduce costs 90%
3. **Batch non-urgent requests** - 50% discount on most providers
4. **Optimize prompts** - Shorter prompts = fewer input tokens

### Model Selection Matrix

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Simple Q&A, classification | GPT-4o mini, Gemini 2.0 Flash | Cheapest, fast enough |
| Coding tasks | Claude Sonnet 4.5 | Top SWE-Bench scores |
| Long documents | Gemini 2.5/3 Pro | 1M+ context window |
| Complex reasoning | OpenAI o3, Claude Opus | Reasoning capabilities |
| High-volume, cost-sensitive | DeepSeek V3 | 90% cheaper |
| Real-time/latency-critical | Llama 4 Scout | 2600 t/s |

### Cost Calculation Example

**Scenario:** 1M tokens/day (500K in, 500K out)

| Model | Daily Cost | Monthly Cost |
|-------|------------|--------------|
| DeepSeek V3 | $0.69 | ~$21 |
| Gemini 2.0 Flash | $0.25 | ~$8 |
| GPT-5 | $5.63 | ~$169 |
| Claude Opus 4.1 | $45.00 | ~$1,350 |

**That's a 160x cost difference** between cheapest and most expensive.

---

## 5. MQCO Project Roadmap

### Phase 1: Data Collection (Current)
- [x] Research pricing landscape
- [x] Identify key benchmarks
- [x] Survey evaluation frameworks
- [ ] Document our current usage patterns

### Phase 2: Baseline Measurement
- [ ] Track current token usage (by model, by task type)
- [ ] Measure current costs
- [ ] Identify high-volume, low-complexity tasks

### Phase 3: Build Evaluation Pipeline
- [ ] Set up DeepEval or similar framework
- [ ] Create test dataset from real use cases
- [ ] Benchmark candidate models on our tasks

### Phase 4: Implement Routing
- [ ] Design model routing logic
- [ ] Implement A/B testing infrastructure
- [ ] Deploy tiered model approach

### Phase 5: Monitor & Iterate
- [ ] Dashboard for cost/quality metrics
- [ ] Automated alerts for quality degradation
- [ ] Regular re-evaluation as new models release

---

## Key Takeaways

1. **There's no "best" model** - It depends on task, budget, and latency needs
2. **Cost optimization is huge** - 10-100x savings possible with smart routing
3. **Quality must be measured** - Use LLM-as-a-judge, not vibes
4. **The landscape changes fast** - Re-evaluate quarterly
5. **DeepSeek is the disruptor** - Chinese models are undercutting everyone

---

## Resources

- [Vellum LLM Leaderboard](https://www.vellum.ai/llm-leaderboard)
- [pricepertoken.com](https://pricepertoken.com/)
- [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- [LMSYS Chatbot Arena](https://lmsys.org/blog/2023-05-03-arena/)
- [IntuitionLabs Pricing Comparison](https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025)
