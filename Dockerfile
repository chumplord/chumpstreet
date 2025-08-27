# Use a lightweight Python base image
FROM python:3.11-slim

# Install uv (fast dependency manager)
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy only dependency files first for caching
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of your code
COPY . .

# Expose the Hugging Face default port
EXPOSE 7860

# Run the MCP server on Hugging Face's expected port
CMD ["uv", "run", "-m", "chumpstreet.mcp_server"]
