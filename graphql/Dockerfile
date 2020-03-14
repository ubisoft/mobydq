FROM node:alpine
LABEL description="Instant high-performance GraphQL API for your PostgreSQL database https://github.com/graphile/postgraphile"

# Set Node.js app folder
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app
WORKDIR /home/node/app

# Copy dependencies
COPY ./init/package*.json .

# Install dependencies
RUN npm install

# Copy application files
COPY --chown=node:node ./init .

# Install MobyDQ plugin
RUN cd ./mobydq-plugin && npm pack
RUN npm install ./mobydq-plugin/mobydq-plugin-0.0.1.tgz
RUN rm -rf ./mobydq-plugin

EXPOSE 8080
CMD [ "node", "server.js" ]