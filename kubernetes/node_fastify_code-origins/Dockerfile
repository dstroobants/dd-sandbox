FROM node:20.11.1

# Set working directory
WORKDIR /usr/src/app

# Copy package files
COPY app/ ./

# Install dependencies
RUN npm install

# Build the TypeScript application
RUN npm run build

# Expose port
EXPOSE 3590

# Start the application
CMD ["npm", "run", "start"]
