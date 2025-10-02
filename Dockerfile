FROM node:20-slim

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


RUN npm install -g anon-kode

WORKDIR /workspace

COPY package*.json ./

#RUN if [ -f package.json ]; then npm install; fi

CMD ["/bin/bash"]

