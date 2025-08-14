// Official Prisma client with Datadog tracing extensions
// Based on https://www.prisma.io/docs/guides/data-dog

import { PrismaClient } from '@prisma/client'
import tracer from 'dd-trace'

const prisma = new PrismaClient({
  log: [{ emit: "event", level: "query" }],
})
  .$on("query", (e) => {
    const span = tracer.startSpan(`prisma_raw_query`, {
      childOf: tracer.scope().active() || undefined,
      tags: {
        "prisma.rawquery": e.query,
      },
    });
    span.finish();
  })
  .$extends({
    query: {
      async $allOperations({ operation, model, args, query }) {
        const span = tracer.startSpan(
          `prisma_query_${model?.toLowerCase()}_${operation}`,
          {
            tags: {
              "prisma.operation": operation,
              "prisma.model": model,
              "prisma.args": JSON.stringify(args),
              "prisma.rawQuery": query,
            },
            childOf: tracer.scope().active() || undefined,
          }
        );

        try {
          const result = await query(args);
          console.log('Raw DB result:')
          console.log('result', result)
          span.finish();
          return result;
        } catch (error) {
          span.setTag("error", error);
          span.finish();
          throw error;
        }
      },
    },
  });

export { prisma };
