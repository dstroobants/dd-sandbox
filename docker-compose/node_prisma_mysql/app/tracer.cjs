// Official Prisma + Datadog tracing setup
// Based on https://www.prisma.io/docs/guides/data-dog

const Tracer = require("dd-trace");
const {
  PrismaInstrumentation,
  registerInstrumentations,
} = require("@prisma/instrumentation");

const tracer = Tracer.init({
  apmTracingEnabled: true,
  service: process.env.DD_SERVICE || "node-prisma-app",
  env: process.env.DD_ENV || "dev",
  version: process.env.DD_VERSION || "1.0.0",
  logInjection: true,
  debug: true,
});

// Register Prisma instrumentation
registerInstrumentations({
  instrumentations: [
    new PrismaInstrumentation({
      middleware: true, // Enable middleware-based tracing
    }),
  ],
});

console.log('Official Prisma + Datadog tracing initialized');

module.exports = tracer;
