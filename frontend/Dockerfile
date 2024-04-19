# Use an official Node runtime as a parent image
FROM node:21.7.1
# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages
RUN npm install

# Bundle app source
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 5055

# Run npm start to start the app
CMD ["npm", "run", "dev"]
