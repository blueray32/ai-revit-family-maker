# CLAUDE.md

This file provides comprehensive guidance to Claude Code when working with Node.js 23 applications.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

### Design Principles

- **Modular Architecture**: Build with small, focused modules that do one thing well
- **Error-First Callbacks**: Always handle errors as the first parameter in callbacks
- **Async by Default**: Use async/await for all I/O operations
- **Fail Fast**: Validate inputs early and throw meaningful errors immediately
- **Security First**: Never trust user input, always validate and sanitize

## 🤖 AI Assistant Guidelines

### Context Awareness

- When implementing features, always check existing patterns first
- Prefer composition over inheritance in all designs
- Use existing utilities before creating new ones
- Check for similar functionality in other domains/features

### Common Pitfalls to Avoid

- Creating duplicate functionality
- Overwriting existing tests
- Modifying core frameworks without explicit instruction
- Adding dependencies without checking existing alternatives

### Workflow Patterns

- Prefferably create tests BEFORE implementation (TDD)
- Use "think hard" for architecture decisions
- Break complex tasks into smaller, testable units
- Validate understanding before implementation

### Search Command Requirements

**CRITICAL**: Always use `rg` (ripgrep) instead of traditional `grep` and `find` commands:

```bash
# ❌ Don't use grep
grep -r "pattern" .

# ✅ Use rg instead
rg "pattern"

# ❌ Don't use find with name
find . -name "*.js"

# ✅ Use rg with file filtering
rg --files | rg "\.js$"
# or
rg --files -g "*.js"
```

**Enforcement Rules:**

```
(
    r"^grep\b(?!.*\|)",
    "Use 'rg' (ripgrep) instead of 'grep' for better performance and features",
),
(
    r"^find\s+\S+\s+-name\b",
    "Use 'rg --files | rg pattern' or 'rg --files -g pattern' instead of 'find -name' for better performance",
),
```

## 🚀 Node.js 23 Key Features

### Native TypeScript Support

Node.js 23.6+ now runs TypeScript files natively without additional configuration:

```bash
# Direct execution without transpilation
node index.ts

# No need for ts-node or tsx
```

### Performance Features

- **Virtual Threads**: Leverage Java 21-style virtual threads for better concurrency
- **HTTP/2 by Default**: Improved multiplexing and server push capabilities
- **Native Fetch API**: Built-in fetch() without external dependencies
- **WebAssembly Support**: Enhanced WASM integration for performance-critical code

### Security Enhancements

- **Permission Model**: Granular permissions for file system, network, and child processes
- **Secure by Default**: Stricter defaults for crypto and TLS
- **Built-in CSP**: Content Security Policy support at the platform level

## 🏗️ Project Structure (Domain-Driven Design)

```
project-root/
├── src/
│   ├── domains/           # Business domains
│   │   └── [domain]/
│   │       ├── __tests__/ # Domain-specific tests
│   │       ├── entities/  # Domain entities
│   │       ├── services/  # Business logic
│   │       ├── repos/     # Data access
│   │       └── index.ts   # Domain public API
│   ├── infrastructure/    # Technical concerns
│   │   ├── database/      # DB connections
│   │   ├── cache/         # Redis, etc.
│   │   ├── messaging/     # Queues, events
│   │   └── monitoring/    # Logs, metrics
│   ├── interfaces/        # External interfaces
│   │   ├── http/          # REST/GraphQL
│   │   ├── grpc/          # gRPC services
│   │   └── cli/           # CLI commands
│   └── shared/            # Cross-cutting concerns
│       ├── errors/        # Custom errors
│       ├── types/         # Shared types
│       └── utils/         # Helpers
├── tests/                 # Integration tests
├── scripts/               # Build/deploy scripts
├── .env.example           # Environment template
├── package.json
├── tsconfig.json          # If using TypeScript
└── CLAUDE.md
```

## 📦 Package Management Best Practices

### Dependencies

```json
{
  "engines": {
    "node": ">=23.0.0",
    "npm": ">=10.0.0"
  },
  "scripts": {
    "start": "node --env-file=.env src/index.js",
    "dev": "node --watch --env-file=.env src/index.js",
    "test": "node --test",
    "test:coverage": "node --test --experimental-test-coverage",
    "lint": "eslint src --max-warnings 0",
    "security": "npm audit --audit-level=moderate"
  }
}
```

### Essential Dependencies

```bash
# Production dependencies
npm install fastify          # High-performance web framework
npm install @fastify/helmet  # Security headers
npm install pino            # Fast JSON logger
npm install ajv             # JSON schema validation
npm install postgres        # PostgreSQL client
npm install ioredis         # Redis client

# Development dependencies
npm install -D @types/node   # TypeScript definitions
npm install -D eslint        # Linting
npm install -D prettier      # Code formatting
npm install -D husky         # Git hooks
npm install -D lint-staged   # Pre-commit linting
```

## 🎯 TypeScript Configuration (When Used)

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2023"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "allowJs": false
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

## 🛡️ Input Validation with AJV

### Schema-Based Validation (MANDATORY)

```javascript
import Ajv from "ajv";
import addFormats from "ajv-formats";

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

// Define schemas for all external inputs
const userSchema = {
  type: "object",
  properties: {
    id: { type: "string", format: "uuid" },
    email: { type: "string", format: "email" },
    username: {
      type: "string",
      minLength: 3,
      maxLength: 20,
      pattern: "^[a-zA-Z0-9_]+$",
    },
    age: { type: "integer", minimum: 18, maximum: 100 },
  },
  required: ["email", "username"],
  additionalProperties: false,
};

// Compile and use validators
const validateUser = ajv.compile(userSchema);

export function validateUserInput(data) {
  if (!validateUser(data)) {
    throw new ValidationError("Invalid user data", validateUser.errors);
  }
  return data;
}
```

## 🧪 Testing Strategy (Native Node.js Test Runner)

### Test Organization

```javascript
// src/domains/user/__tests__/user.service.test.js
import { describe, it, before, after, mock } from "node:test";
import assert from "node:assert/strict";

describe("UserService", () => {
  let userService;
  let mockRepo;

  before(async () => {
    mockRepo = {
      findById: mock.fn(() => Promise.resolve({ id: "123", name: "Test" })),
    };
    userService = new UserService(mockRepo);
  });

  it("should return user by id", async () => {
    const user = await userService.getById("123");

    assert.equal(user.id, "123");
    assert.equal(mockRepo.findById.mock.calls.length, 1);
  });
});
```

### Coverage Requirements

- Minimum 80% statement coverage
- Minimum 80% branch coverage
- Critical paths: 90%+ coverage
- All public APIs must have tests

## 🚀 Performance Best Practices

### Event Loop Protection

```javascript
// Prevent blocking with large JSON parsing
import { Worker } from "node:worker_threads";

export async function parseHugeJSON(jsonString) {
  return new Promise((resolve, reject) => {
    const worker = new Worker("./json-parser-worker.js");
    worker.postMessage(jsonString);
    worker.on("message", resolve);
    worker.on("error", reject);
  });
}

// Use setImmediate for CPU-intensive loops
async function processLargeArray(items) {
  const results = [];

  for (let i = 0; i < items.length; i++) {
    if (i % 1000 === 0) {
      await new Promise((resolve) => setImmediate(resolve));
    }
    results.push(await processItem(items[i]));
  }

  return results;
}
```

### Memory Management

```javascript
// Monitor memory usage
const used = process.memoryUsage();
console.log({
  rss: `${Math.round(used.rss / 1024 / 1024 * 100) / 100} MB`,
  heapTotal: `${Math.round(used.heapTotal / 1024 / 1024 * 100) / 100} MB`,
  heapUsed: `${Math.round(used.heapUsed / 1024 / 1024 * 100) / 100} MB`,
  external: `${Math.round(used.external / 1024 / 1024 * 100) / 100} MB`
});

// Set max heap size in package.json
"scripts": {
  "start": "node --max-old-space-size=4096 src/index.js"
}
```

## 🔐 Security Requirements

### Environment Variables

```javascript
// Use native --env-file support
// node --env-file=.env src/index.js

// Validate all environment variables at startup
const requiredEnvVars = [
  "NODE_ENV",
  "PORT",
  "DATABASE_URL",
  "JWT_SECRET",
  "REDIS_URL",
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

// Type-safe environment access
export const config = {
  nodeEnv: process.env.NODE_ENV,
  port: parseInt(process.env.PORT, 10),
  database: {
    url: process.env.DATABASE_URL,
    maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || "10", 10),
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || "1h",
  },
};
```

### Security Headers (Fastify + Helmet)

```javascript
import fastify from "fastify";
import helmet from "@fastify/helmet";

const app = fastify({ logger: true });

app.register(helmet, {
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
});
```

## 📊 Logging & Monitoring

### Structured Logging with Pino

```javascript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport:
    process.env.NODE_ENV === "development"
      ? { target: "pino-pretty" }
      : undefined,
  serializers: {
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
    err: pino.stdSerializers.err,
  },
  redact: ["password", "token", "authorization"],
});

// Use child loggers for context
export function createLogger(context) {
  return logger.child(context);
}

// Example usage
const userLogger = createLogger({ module: "UserService" });
userLogger.info({ userId: "123" }, "User created successfully");
```

## 🔄 Error Handling

### Custom Error Classes

```javascript
export class AppError extends Error {
  constructor(message, statusCode = 500, code = "INTERNAL_ERROR") {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message, errors = []) {
    super(message, 400, "VALIDATION_ERROR");
    this.errors = errors;
  }
}

export class NotFoundError extends AppError {
  constructor(resource) {
    super(`${resource} not found`, 404, "NOT_FOUND");
  }
}
```

### Global Error Handler

```javascript
// Fastify error handler
app.setErrorHandler((error, request, reply) => {
  const logger = request.log;

  if (error.isOperational) {
    logger.warn({ err: error }, "Operational error");
    reply.status(error.statusCode).send({
      error: {
        code: error.code,
        message: error.message,
        ...(error.errors && { details: error.errors }),
      },
    });
  } else {
    logger.error({ err: error }, "Unexpected error");
    reply.status(500).send({
      error: {
        code: "INTERNAL_ERROR",
        message: "An unexpected error occurred",
      },
    });
  }
});

// Uncaught exception handler
process.on("uncaughtException", (error) => {
  logger.fatal({ err: error }, "Uncaught exception");
  process.exit(1);
});

process.on("unhandledRejection", (reason, promise) => {
  logger.fatal({ err: reason, promise }, "Unhandled rejection");
  process.exit(1);
});
```

## 🐳 Docker Configuration

### Dockerfile

```dockerfile
FROM node:23-alpine AS base

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

WORKDIR /app

# Copy package files
COPY package*.json ./

# Production image
FROM base AS production

# Install production dependencies only
RUN npm ci --only=production && npm cache clean --force

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "--env-file=.env", "src/index.js"]
```

## ⚠️ Critical Guidelines

1. **NEVER block the event loop** - Use worker threads for CPU-intensive tasks
2. **ALWAYS validate inputs** - Use AJV schemas for all external data
3. **NEVER store secrets in code** - Use environment variables
4. **ALWAYS handle errors** - No silent failures
5. **MINIMUM 80% test coverage** - Use native Node.js test runner
6. **ALWAYS use structured logging** - Pino with proper serializers
7. **NEVER use synchronous I/O** - Always use async/await
8. **ALWAYS set memory limits** - Configure --max-old-space-size
9. **NEVER trust user input** - Sanitize and validate everything
10. **ALWAYS use security headers** - Helmet with proper CSP
11. **MONITOR performance** - Track event loop lag and memory usage
12. **USE native features** - Prefer built-in modules over external dependencies

## 📋 Pre-commit Checklist

- [ ] All tests passing with 80%+ coverage
- [ ] No ESLint warnings or errors
- [ ] Security audit passed (npm audit)
- [ ] Environment variables documented
- [ ] Error handling implemented
- [ ] Input validation schemas defined
- [ ] Logging added for critical paths
- [ ] Performance impact assessed
- [ ] Memory leaks checked
- [ ] Documentation updated

## 🔧 Useful Commands

```bash
# Development
npm run dev                          # Run with auto-reload
npm test -- --watch                  # Run tests in watch mode
npm run test:coverage                # Generate coverage report

# Debugging
node --inspect src/index.js          # Enable Chrome DevTools
node --trace-warnings src/index.js   # Trace promise rejections
node --prof src/index.js             # CPU profiling

# Production
node --env-file=.env src/index.js    # Run with environment file
pm2 start ecosystem.config.js        # Run with PM2

# Monitoring
node --trace-event-categories=node.perf src/index.js  # Performance tracing
```

---

_Keep this guide updated as patterns evolve. Performance and security over convenience, always._
_Last updated: June 2025_
