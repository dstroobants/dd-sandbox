package main

import (
	"context"
	"html/template"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	//stdout "go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	oteltrace "go.opentelemetry.io/otel/trace"

	"go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"
)

var tracer = otel.Tracer("gin-server")

func main() {
	tp, err := initTracer()
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := tp.Shutdown(context.Background()); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
	}()
	r := gin.New()
	r.Use(otelgin.Middleware("my-server"))
	tmplName := "user"
	tmplStr := "user {{ .name }} (id {{ .id }})\n"
	tmpl := template.Must(template.New(tmplName).Parse(tmplStr))
	r.SetHTMLTemplate(tmpl)
	r.GET("/users/:id", func(c *gin.Context) {
		id := c.Param("id")
		name := getUser(c, id)
		otelgin.HTML(c, http.StatusOK, tmplName, gin.H{
			"name": name,
			"id":   id,
		})
	})
	
	// Start goroutines to make periodic requests
	go makePeriodicRequest("http://localhost:8080/users/123", 5*time.Second)
	go makePeriodicRequest("http://localhost:8080/users/456", 20*time.Second)
	
	_ = r.Run(":8080")
}

func makePeriodicRequest(url string, interval time.Duration) {
	// Wait a bit for the server to start
	time.Sleep(2 * time.Second)
	
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	
	for range ticker.C {
		resp, err := http.Get(url)
		if err != nil {
			log.Printf("Error making request to %s: %v", url, err)
			continue
		}
		log.Printf("Request to %s: Status %d", url, resp.StatusCode)
		resp.Body.Close()
	}
}

func initTracer() (*sdktrace.TracerProvider, error) {
	ctx := context.Background()
	
	// Create OTLP gRPC exporter
	exporter, err := otlptracegrpc.New(ctx,
		otlptracegrpc.WithInsecure(),
	)
	if err != nil {
		return nil, err
	}
	
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
		sdktrace.WithBatcher(exporter),
	)
	otel.SetTracerProvider(tp)
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(propagation.TraceContext{}, propagation.Baggage{}))
	return tp, nil
}

func getUser(c *gin.Context, id string) string {
	// Pass the built-in `context.Context` object from http.Request to OpenTelemetry APIs
	// where required. It is available from gin.Context.Request.Context()
	_, span := tracer.Start(c.Request.Context(), "getUser", oteltrace.WithAttributes(attribute.String("id", id)))
	defer span.End()
	if id == "123" {
		return "otelgin tester"
	}
	return "unknown"
}
