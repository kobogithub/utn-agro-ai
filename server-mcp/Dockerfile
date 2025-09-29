# Multi-stage build for optimized image size
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# Final stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create directory for database
RUN mkdir -p /app/data

# Make mcp_server.py executable
RUN chmod +x mcp_server.py

# MCP server uses STDIO, no port exposure needed

# Run the MCP server
ENTRYPOINT ["python", "mcp_server.py"]