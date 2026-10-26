Production Debugging
Estimated time: 10 minutes
Scenario
An enterprise AI assistant streams responses to users.

After a deployment, some users report that responses stop midway through a sentence.

Your monitoring system shows that the model provider is responding successfully, but the frontend sometimes receives incomplete text.

Interview question: How would you investigate whether the problem originates in the model stream, backend application, network connection, or frontend rendering?

Consider how you would use request correlation IDs, distributed traces, stream completion markers, cancellation logs, and latency measurements.

Explain how you would distinguish an intentional user cancellation from a network failure or an application-enforced response limit.

Also describe how you would reproduce the problem using a deterministic mock stream before debugging the real model integration.

Spend approximately two minutes presenting your investigation strategy as though you were explaining it to another engineer during a production incident.

This is a simulated interview scenario, not a confirmed question from OpenAI.