package main

import (
	"context"
	"html/template"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"
	"go.opentelemetry.io/contrib/instrumentation/runtime"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	sdkmetric "go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	oteltrace "go.opentelemetry.io/otel/trace"
)

var tracer = otel.Tracer("gin-server")

func main() {
	ctx := context.Background()
	
	tp, err := initTracer()
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := tp.Shutdown(ctx); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
	}()
	
	// Initialize metrics provider
	mp, err := initMetrics()
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := mp.Shutdown(ctx); err != nil {
			log.Printf("Error shutting down metrics provider: %v", err)
		}
	}()
	
	// Start collecting runtime metrics
	err = runtime.Start(runtime.WithMinimumReadMemStatsInterval(time.Second))
	if err != nil {
		log.Fatal(err)
	}
	
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
	
	// Create OTLP gRPC exporter for traces
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

func initMetrics() (*sdkmetric.MeterProvider, error) {
	ctx := context.Background()
	
	// Get service name from environment
	serviceName := os.Getenv("OTEL_SERVICE_NAME")
	if serviceName == "" {
		serviceName = "go-web-app"
	}
	
	// Create resource with service information
	res, err := resource.New(ctx,
		resource.WithAttributes(
			attribute.String("service.name", serviceName),
			attribute.String("service.version", os.Getenv("DD_VERSION")),
			attribute.String("deployment.environment", os.Getenv("DD_ENV")),
		),
	)
	if err != nil {
		return nil, err
	}
	
	// Create OTLP gRPC exporter for metrics
	exporter, err := otlpmetricgrpc.New(ctx,
		otlpmetricgrpc.WithInsecure(),
	)
	if err != nil {
		return nil, err
	}
	
	// Create meter provider with periodic export
	mp := sdkmetric.NewMeterProvider(
		sdkmetric.WithResource(res),
		sdkmetric.WithReader(sdkmetric.NewPeriodicReader(exporter,
			sdkmetric.WithInterval(10*time.Second),
		)),
	)
	otel.SetMeterProvider(mp)
	return mp, nil
}

func getUser(c *gin.Context, id string) string {
	_, span := tracer.Start(c.Request.Context(), "getUser", oteltrace.WithAttributes(attribute.String("id", id)))
	defer span.End()
	
	if id == "123" {
		return "otelgin tester"
	}
	if id == "456" {
		return "another user"
	}
	return "unknown"
}
