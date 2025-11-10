## Kaggle 5 days of AI course

Repository for [5-day agents course](https://www.kaggle.com/learn-guide/5-day-agents).

Using on [Google ADK](https://google.github.io/adk-docs/)

## Setup

This project is using `uv` as package manager, so please install it.

```bash
> uv sync
```

## Commands

```bash
# Starts a FastAPI server with Web UI for agents.
> uv run adk web
```

```bash
# Runs an interactive CLI for a certain agent.
> uv run adk run agent_name
```

```bash
# Bootstrap a new agent
> uv run adk create agent_name
```
