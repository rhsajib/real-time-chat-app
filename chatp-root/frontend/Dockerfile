# Use an official Node runtime as a parent image
FROM node:18.4.0-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm i

# Copy the entire project to the container
COPY . .

EXPOSE 5173

# Start the development server with npm run dev
CMD [ "npm", "run", "dev"]
