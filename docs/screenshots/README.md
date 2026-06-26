# Screenshots

This directory is reserved for real project screenshots. No fake screenshots should be added.

Recommended screenshot list:

```text
01_dashboard.png
02_analyze_form.png
03_agent_result.png
04_inquiry_list.png
05_inquiry_detail.png
06_retrieved_knowledge.png
07_agent_trace.png
08_review_form.png
09_swagger.png
10_docker_compose_running.png
```

Suggested capture flow:

1. Start the stack with `docker-compose up --build`.
2. Open `http://127.0.0.1:3001`.
3. Capture the dashboard.
4. Open Analyze Inquiry and load a sample.
5. Submit the inquiry and capture AgentResult sections.
6. Open the detail page and capture review sections.
7. Open `http://127.0.0.1:8000/docs` for Swagger.
8. Capture Docker Desktop or terminal showing the three running containers.

Current note: screenshots have not been captured in this documentation round.
