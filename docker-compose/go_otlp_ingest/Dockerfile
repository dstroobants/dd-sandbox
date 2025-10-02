FROM golang:1.25

WORKDIR /usr/src/app

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
COPY app/go.mod ./
COPY app/go.sum ./
RUN go mod download && go mod verify

COPY app .
RUN go mod tidy
RUN go build -v -o /usr/local/bin/app ./...

CMD ["app"]
