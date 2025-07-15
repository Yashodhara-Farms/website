# Dockerfile
FROM node:18-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --production

# Copy code
COPY . .

# Expose port & start
ENV PORT 8080
CMD ["node", "index.js"]
