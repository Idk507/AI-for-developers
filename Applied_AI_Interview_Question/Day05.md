Interview scenario
An enterprise AI chatbot receives approximately 5,000 requests per minute.

After deploying a new version, users begin reporting slow responses and intermittent HTTP 429 errors.

Your monitoring dashboard shows increased API latency, but the root cause is unclear.

Your question: How would you determine whether the problem is caused by excessive incoming traffic, an overly restrictive rate limiter, slow LLM inference, or an external tool dependency?

Prepare a short explanation covering the signals you would inspect and how you would isolate the responsible component.

Consider request throughput, rejection rate, latency percentiles such as p95 and p99, model API response times, tool-call failures, and distributed traces.

Also think about how you would distinguish your application's own rate-limit responses from HTTP 429 responses returned by an upstream model provider.

A production design should use structured logs and correlation IDs while avoiding unnecessary logging of user prompts or sensitive information.