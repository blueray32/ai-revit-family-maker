# CLAUDE.md

This file provides guidance to Claude Code when working with React 19 applications.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

### Component-First Architecture

Build with reusable, composable components. Each component should have a single, clear responsibility and be self-contained with its own styles, tests, and logic co-located.

### Performance by Default

With React 19's compiler, manual optimizations are largely unnecessary. Focus on clean, readable code and let the compiler handle performance optimizations.

### Design Principles (MUST FOLLOW)

- **Vertical Slice Architecture**: MUST organize by features, not layers
- **Composition Over Inheritance**: MUST use React's composition model
- **Fail Fast**: MUST validate inputs early with Zod, throw errors immediately

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
find . -name "*.tsx"

# ✅ Use rg with file filtering
rg --files | rg "\.tsx$"
# or
rg --files -g "*.tsx"
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

## 🚀 React 19 Key Features

### Automatic Optimizations

- **React Compiler**: Eliminates need for `useMemo`, `useCallback`, and `React.memo`
- Let the compiler handle performance - write clean, readable code

### Core Features

- **Server Components**: Use for data fetching and static content
- **Actions**: Handle async operations with built-in pending states
- **use() API**: Simplified data fetching and context consumption
- **Document Metadata**: Native support for SEO tags
- **Enhanced Suspense**: Better loading states and error boundaries

### React 19 TypeScript Integration (MANDATORY)

- **MUST use `ReactElement` instead of `JSX.Element`** for return types
- **MUST import `ReactElement` from 'react'** explicitly
- **NEVER use `JSX.Element` namespace** - use React types directly

```typescript
// ✅ CORRECT: Modern React 19 typing
import { ReactElement } from 'react';

function MyComponent(): ReactElement {
  return <div>Content</div>;
}

const renderHelper = (): ReactElement | null => {
  return condition ? <span>Helper</span> : null;
};

// ❌ FORBIDDEN: Legacy JSX namespace
function MyComponent(): JSX.Element {  // Cannot find namespace 'JSX'
  return <div>Content</div>;
}
```

### Actions Example (WITH MANDATORY DOCUMENTATION)

````typescript
/**
 * @fileoverview Contact form using React 19 Actions API
 * @module features/contact/components/ContactForm
 */

import { useActionState, ReactElement } from 'react';

/**
 * Contact form component using React 19 Actions.
 *
 * Leverages the Actions API for automatic pending state management
 * and error handling. Form data is validated with Zod before submission.
 *
 * @component
 * @example
 * ```tsx
 * <ContactForm onSuccess={() => router.push('/thank-you')} />
 * ```
 */
function ContactForm(): ReactElement {
  /**
   * Form action handler with built-in state management.
   *
   * @param previousState - Previous form state (unused in this implementation)
   * @param formData - Raw form data from submission
   * @returns Promise resolving to success or error state
   */
  const [state, submitAction, isPending] = useActionState(
    async (previousState: any, formData: FormData) => {
      // Extract and validate form data
      const result = contactSchema.safeParse({
        email: formData.get('email'),
        message: formData.get('message'),
      });

      if (!result.success) {
        return { error: result.error.flatten() };
      }

      // Process validated data
      await sendEmail(result.data);
      return { success: true };
    },
    null
  );

  return (
    <form action={submitAction}>
      <button disabled={isPending}>
        {isPending ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
}
````

## 🏗️ Project Structure (Vertical Slice Architecture)

```
src/
├── features/              # Feature-based modules
│   └── [feature]/
│       ├── __tests__/     # Co-located tests (MUST be documented)
│       ├── components/    # Feature components (MUST have JSDoc)
│       ├── hooks/         # Feature-specific hooks (MUST have JSDoc)
│       ├── api/           # API integration (MUST document endpoints)
│       ├── schemas/       # Zod validation schemas (MUST document validation rules)
│       ├── types/         # TypeScript types (MUST document complex types)
│       └── index.ts       # Public API (MUST have @module documentation)
├── shared/
│   ├── components/        # Shared UI components (MUST have prop documentation)
│   ├── hooks/            # Shared custom hooks (MUST have usage examples)
│   ├── utils/            # Helper functions (MUST have JSDoc with examples)
│   └── types/            # Shared TypeScript types
└── test/                 # Test utilities and setup
```

## 🎯 TypeScript Configuration (STRICT REQUIREMENTS) Assume strict requirements even if project settings are looser

### MUST follow These Compiler Options

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "allowJs": false
  }
}
```

### MANDATORY Type Requirements

- **NEVER use `any` type** - use `unknown` if type is truly unknown
- **MUST have explicit return types** for all functions and components
- **MUST use proper generic constraints** for reusable components
- **MUST use type inference from Zod schemas** using `z.infer<typeof schema>`
- **NEVER use `@ts-ignore`** or `@ts-expect-error` - fix the type issue properly

### Type Safety Hierarchy (STRICT ORDER)

1. **Specific Types**: Always prefer specific types when possible
2. **Generic Constraints**: Use generic constraints for reusable code
3. **Unknown**: Use `unknown` for truly unknown data that will be validated
4. **Never `any`**: The only exception is library declaration merging (must be commented)

### TypeScript Project Structure (MANDATORY)

- **App Code**: `tsconfig.app.json` - covers src/ directory
- **Node Config**: `tsconfig.node.json` - MUST include vite.config.ts, vitest.config.ts
- **ESLint Integration**: MUST reference both in parserOptions.project

### Branded Type Safety (MANDATORY)

- **MUST use Schema.parse() to convert plain types to branded types**
- **NEVER assume external data matches branded types**
- **Always validate at system boundaries**

```typescript
// ✅ CORRECT: Convert plain types to branded types
const cvId = CVIdSchema.parse(numericId);

// ❌ FORBIDDEN: Assuming type without validation
const cvId: CVId = numericId; // Type assertion without validation
```

### ExactOptionalPropertyTypes Compliance (MANDATORY)

- **MUST handle `undefined` vs `null` properly** in API interfaces
- **MUST use conditional spreads** instead of passing `undefined` to optional props
- **MUST convert `undefined` to `null`** for API body types

```typescript
// ✅ CORRECT: Handle exactOptionalPropertyTypes properly
const apiCall = async (data?: string) => {
  return fetch('/api', {
    method: 'POST',
    body: data ? JSON.stringify({ data }) : null,  // null, not undefined
  });
};

// Conditional prop spreading for optional properties
<Input
  label="Email"
  error={errors.email?.message}
  {...(showHelper ? { helperText: "Enter valid email" } : {})}  // Conditional spread
/>

// ❌ FORBIDDEN: Passing undefined to optional properties
<Input
  label="Email"
  error={errors.email?.message}
  helperText={showHelper ? "Enter valid email" : undefined}  // undefined not allowed
/>
```

## ⚡ React 19 Power Features

### Instant UI Patterns

- Use Suspense boundaries for ALL async operations
- Leverage Server Components for data fetching
- Use the new Actions API for form handling
- Let React Compiler handle optimization

### Component Templates

````typescript
// Quick component with all states
export function FeatureComponent(): ReactElement {
  const { data, isLoading, error } = useQuery({
    queryKey: ['feature'],
    queryFn: fetchFeature
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorBoundary error={error} />;
  if (!data) return <EmptyState />;

  return <FeatureContent data={data} />;
}

## 🛡️ Data Validation with Zod (MANDATORY FOR ALL EXTERNAL DATA)

### MUST Follow These Validation Rules
- **MUST validate ALL external data**: API responses, form inputs, URL params, environment variables
- **MUST use branded types**: For all IDs and domain-specific values
- **MUST fail fast**: Validate at system boundaries, throw errors immediately
- **MUST use type inference**: Always derive TypeScript types from Zod schemas
- **NEVER trust external data** without validation
- **MUST validate before using** any data from outside the application

### Schema Example (MANDATORY PATTERNS)
```typescript
import { z } from 'zod';

// MUST use branded types for ALL IDs
const UserIdSchema = z.string().uuid().brand<'UserId'>();
type UserId = z.infer<typeof UserIdSchema>;

// MUST include validation for ALL fields
export const userSchema = z.object({
  id: UserIdSchema,
  email: z.string().email(),
  username: z.string()
    .min(3)
    .max(20)
    .regex(/^[a-zA-Z0-9_]+$/),
  age: z.number().min(18).max(100),
  role: z.enum(['admin', 'user', 'guest']),
  metadata: z.object({
    lastLogin: z.string().datetime(),
    preferences: z.record(z.unknown()).optional(),
  }),
});

export type User = z.infer<typeof userSchema>;

// MUST validate ALL API responses
export const apiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema,
    error: z.string().optional(),
    timestamp: z.string().datetime(),
  });
````

### Form Validation with React Hook Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function UserForm(): JSX.Element {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<User>({
    resolver: zodResolver(userSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: User): Promise<void> => {
    // Handle validated data
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## 🧪 Testing Strategy (MANDATORY REQUIREMENTS)

### MUST Meet These Testing Standards

- **MINIMUM 80% code coverage** - NO EXCEPTIONS
- **MUST co-locate tests** with components in `__tests__` folders
- **MUST use React Testing Library** for all component tests
- **MUST test user behavior** not implementation details
- **MUST mock external dependencies** appropriately
- **NEVER skip tests** for new features or bug fixes

### SonarQube Quality Gates (MUST PASS ALL)

- **Cognitive Complexity**: MAXIMUM 15 per function
- **Cyclomatic Complexity**: MAXIMUM 10 per function
- **Duplicated Lines**: MAXIMUM 3%
- **Technical Debt Ratio**: MAXIMUM 5%
- **ZERO tolerance** for critical/blocker issues
- **ALL new code** must have 80%+ coverage

### Test Example (WITH MANDATORY DOCUMENTATION)

```typescript
/**
 * @fileoverview Tests for UserProfile component
 * @module features/user/__tests__/UserProfile.test
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@testing-library/react';

/**
 * Test suite for UserProfile component.
 *
 * Tests user interactions, state management, and error handling.
 * Mocks external dependencies to ensure isolated unit tests.
 */
describe('UserProfile', () => {
  /**
   * Tests that user name updates correctly on form submission.
   *
   * Verifies:
   * - Form renders with correct input fields
   * - User can type in the name field
   * - Submit button triggers update with correct data
   */
  it('should update user name on form submission', async () => {
    // Arrange: Set up user event and mock handler
    const user = userEvent.setup();
    const onUpdate = vi.fn();

    // Act: Render component and interact with form
    render(<UserProfile onUpdate={onUpdate} />);

    const input = screen.getByLabelText(/name/i);
    await user.type(input, 'John Doe');
    await user.click(screen.getByRole('button', { name: /save/i }));

    // Assert: Verify handler called with correct data
    expect(onUpdate).toHaveBeenCalledWith(
      expect.objectContaining({ name: 'John Doe' })
    );
  });
});
```

## 🧪 Testing Exceptions (LIMITED SCOPE)

### MANDATORY Test File Rules

- **MUST use `unknown` instead of `any`** in Vitest interface declarations
- **MUST disable React refresh warnings** in test utilities with explicit comments
- **MUST include test config files** in appropriate TypeScript projects
- **MUST use `globalThis` instead of `global`** for cross-platform compatibility

### Acceptable Test File Patterns

```typescript
// ✅ ACCEPTABLE: Library interface declaration merging
declare module "vitest" {
  interface Assertion {
    toCustomMatcher(): void; // void return, not generic T
  }
  interface AsymmetricMatchersContaining {
    toCustomMatcher(): unknown; // unknown, not any
  }
}

// ✅ ACCEPTABLE: Test utility with React refresh disable
// eslint-disable-next-line react-refresh/only-export-components
export * from "@testing-library/react";

// ✅ ACCEPTABLE: Cross-platform global object access
globalThis.fetch = vi.fn(); // Not global.fetch

// ✅ ACCEPTABLE: Vite environment variables in tests
Object.defineProperty(import.meta, "env", {
  value: { MODE: "test", DEV: false },
  writable: true,
});
```

### Test Configuration Requirements

```json
// tsconfig.node.json MUST include ALL Node.js config files
{
  "include": ["vite.config.ts", "vitest.config.ts", "eslint.config.js"]
}

// eslint.config.js MUST reference ALL TypeScript projects
{
  "parserOptions": {
    "project": ["./tsconfig.app.json", "./tsconfig.node.json"]
  }
}

// vite-env.d.ts MUST include vitest globals
/// <reference types="vite/client" />
/// <reference types="vitest/globals" />
```

## 💅 Code Style & Quality

### Linting Stack (MANDATORY)

- **ESLint 9.x** with TypeScript plugin
- **Prettier 3.x** for formatting
- **eslint-plugin-sonarjs** for code quality
- **Pre-commit validation** must pass before any commit

### ESLint TypeScript Integration (MANDATORY)

- **Project References**: MUST include ALL .ts/.tsx files in parserOptions.project
- **Config Files**: Node.js config files (vite.config.ts, vitest.config.ts) belong in tsconfig.node.json
- **Zero Warnings**: `--max-warnings 0` is MANDATORY - no exceptions
- **Complete Coverage**: Every TypeScript file MUST be parseable by ESLint

### MUST Follow These Rules

```javascript
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "error",
    "no-console": ["error", { "allow": ["warn", "error"] }],
    "react/function-component-definition": ["error", {
      "namedComponents": "arrow-function"
    }],
    "sonarjs/cognitive-complexity": ["error", 15],
    "sonarjs/no-duplicate-string": ["error", 3]
  }
}
```

## 🎨 Component Guidelines (STRICT REQUIREMENTS)

### MANDATORY JSDoc Documentation

**MUST document ALL exported functions, classes, and complex logic following Google JSDoc standards**

````typescript
/**
 * Calculates the discount price for a product.
 *
 * This method applies a percentage discount to the original price,
 * ensuring the final price doesn't go below the minimum threshold.
 *
 * @param originalPrice - The original price of the product in cents (must be positive)
 * @param discountPercent - The discount percentage (0-100)
 * @param minPrice - The minimum allowed price after discount in cents
 * @returns The calculated discount price in cents
 * @throws {ValidationError} If any parameter is invalid
 *
 * @example
 * ```typescript
 * const discountedPrice = calculateDiscount(10000, 25, 1000);
 * console.log(discountedPrice); // 7500
 * ```
 */
export function calculateDiscount(
  originalPrice: number,
  discountPercent: number,
  minPrice: number,
): number {
  // Validate inputs
  if (originalPrice <= 0) {
    throw new ValidationError("Original price must be positive");
  }

  // Calculate discount
  const discountAmount = originalPrice * (discountPercent / 100);
  const discountedPrice = originalPrice - discountAmount;

  // Ensure price doesn't go below minimum
  return Math.max(discountedPrice, minPrice);
}
````

### MANDATORY Component Documentation

````typescript
/**
 * Button component with multiple variants and sizes.
 *
 * Provides a reusable button with consistent styling and behavior
 * across the application. Supports keyboard navigation and screen readers.
 *
 * @component
 * @example
 * ```tsx
 * <Button
 *   variant="primary"
 *   size="medium"
 *   onClick={handleSubmit}
 * >
 *   Submit Form
 * </Button>
 * ```
 */
interface ButtonProps {
  /** Visual style variant of the button */
  variant: "primary" | "secondary";

  /** Size of the button @default 'medium' */
  size?: "small" | "medium" | "large";

  /** Click handler for the button */
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;

  /** Content to be rendered inside the button */
  children: React.ReactNode;

  /** Whether the button is disabled @default false */
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = (
  {
    /* props */
  },
) => {
  // Implementation
};
````

### MANDATORY Code Comment Standards

```typescript
// MUST use these comment patterns:

// 1. File headers (REQUIRED for all files)
/**
 * @fileoverview User authentication service handling login, logout, and session management.
 * @module features/auth/services/authService
 */

// 2. Complex logic (REQUIRED when cognitive complexity > 5)
/**
 * Validates user permissions against required roles.
 *
 * Uses a hierarchical role system where admin > editor > viewer.
 * Checks are performed using bitwise operations for performance.
 */
function checkPermissions(userRole: Role, requiredRole: Role): boolean {
  // Admin can access everything
  if (userRole === Role.Admin) return true;

  // Check hierarchical permissions
  return (userRole & requiredRole) === requiredRole;
}

// 3. TODOs (MUST include issue number)
// TODO(#123): Implement rate limiting for login attempts

// 4. Inline explanations (REQUIRED for non-obvious code)
// Use exponential backoff with jitter to prevent thundering herd
const delay = Math.min(
  1000 * Math.pow(2, retryCount) + Math.random() * 1000,
  30000,
);
```

### MANDATORY JSDoc Rules

- **MUST document ALL exported functions** with full JSDoc
- **MUST include @param** for every parameter with description
- **MUST include @returns** with description (unless void)
- **MUST include @throws** for any thrown errors
- **MUST include @example** for complex functions
- **MUST use @deprecated** with migration path when deprecating
- **MUST document component props** with descriptions
- **MUST add file-level @fileoverview** for each module
- **NEVER use single-line comments** for documentation (// is only for inline explanations)

### MANDATORY TypeScript Requirements

```typescript
// ✅ REQUIRED: Explicit types, clear props
interface ButtonProps {
  variant: "primary" | "secondary";
  size?: "small" | "medium" | "large";
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  children: React.ReactNode;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  variant,
  size = "medium",
  onClick,
  children,
  disabled = false,
}) => {
  // Implementation
};

// ❌ FORBIDDEN: Implicit types, loose typing
const Button = ({ variant, onClick, children }: any) => {
  // Implementation
};
```

### Component Integration (STRICT REQUIREMENTS)

- **MUST verify actual prop names** before using components
- **MUST use exact callback parameter types** from component interfaces
- **NEVER assume prop names match semantic expectations**
- **MUST import proper types** for callback parameters

```typescript
// ✅ CORRECT: Verify component interface and use exact prop names
import { EducationList } from './EducationList';
import { EducationSummary } from './schemas';

<EducationList
  cvId={cvId}
  onSelectEducation={(education: EducationSummary) => handleEdit(education.id)}
  onCreateEducation={() => handleCreate()}
  showCreateButton={showActions}  // Not showAddButton
  showActions={showActions}
/>

// ❌ FORBIDDEN: Assuming prop names without verification
<EducationList
  cvId={cvId}
  onEditEducation={(education) => handleEdit(education.id)}  // Wrong prop name
  onAddEducation={() => handleCreate()}  // Wrong prop name
  showAddButton={showActions}  // Wrong prop name
/>
```

### MUST Follow Component Best Practices

- **MAXIMUM 200 lines** per component file
- **MUST follow single responsibility** principle
- **MUST validate props** with Zod when accepting external data
- **MUST implement error boundaries** for all feature modules
- **MUST handle ALL states**: loading, error, empty, and success
- **NEVER return null** without explicit empty state handling
- **MUST include ARIA labels** for accessibility

## 🔄 State Management (STRICT HIERARCHY)

### MUST Follow This State Hierarchy

1. **Local State**: `useState` ONLY for component-specific state
2. **Context**: For cross-component state within a single feature
3. **Server State**: MUST use TanStack Query for ALL API data
4. **Global State**: Zustand ONLY when truly needed app-wide
5. **URL State**: MUST use search params for shareable state

### MANDATORY Server State Pattern

````typescript
/**
 * @fileoverview User data fetching hook with caching
 * @module features/user/hooks/useUser
 */

import { useQuery, useMutation } from "@tanstack/react-query";

/**
 * Custom hook for fetching and managing user data.
 *
 * Implements caching, automatic refetching, and optimistic updates.
 * All API responses are validated with Zod schemas before use.
 *
 * @param id - The unique identifier of the user to fetch
 * @returns Query result object with user data, loading, and error states
 *
 * @example
 * ```tsx
 * const { data: user, isLoading, error } = useUser('123');
 *
 * if (isLoading) return <Spinner />;
 * if (error) return <ErrorMessage error={error} />;
 * return <UserProfile user={user} />;
 * ```
 */
function useUser(id: UserId) {
  return useQuery({
    queryKey: ["user", id],
    queryFn: async () => {
      const response = await fetch(`/api/users/${id}`);

      // Handle HTTP errors
      if (!response.ok) {
        throw new ApiError("Failed to fetch user", response.status);
      }

      const data = await response.json();

      // MUST validate with Zod - this is non-negotiable
      return userSchema.parse(data);
    },
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
    retry: 3, // Retry failed requests 3 times
  });
}
````

## 🔐 Security Requirements (MANDATORY)

### Input Validation (MUST IMPLEMENT ALL)

- **MUST sanitize ALL user inputs** with Zod before processing
- **MUST validate file uploads**: type, size, and content
- **MUST prevent XSS** with proper escaping
- **MUST implement CSP headers** in production
- **NEVER use dangerouslySetInnerHTML** without sanitization

### API Security

- **MUST validate ALL API responses** with Zod schemas
- **MUST handle errors gracefully** without exposing internals
- **NEVER log sensitive data** (passwords, tokens, PII)

## 🚀 Performance Guidelines

### React 19 Optimizations

- **Trust the compiler** - avoid manual memoization
- **Use Suspense** for data fetching boundaries
- **Implement code splitting** at route level
- **Lazy load** heavy components

### Bundle Optimization (WITH DOCUMENTATION)

```typescript
/**
 * @fileoverview Vite configuration for optimized production builds
 * @module vite.config
 */

// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        /**
         * Manual chunk strategy for optimal loading performance.
         * Separates vendor libraries from application code to maximize
         * browser caching effectiveness.
         */
        manualChunks: {
          // React core libraries - rarely change
          "react-vendor": ["react", "react-dom"],
          // Data fetching libraries - moderate change frequency
          "query-vendor": ["@tanstack/react-query"],
          // Form handling libraries - moderate change frequency
          "form-vendor": ["react-hook-form", "zod"],
        },
      },
    },
  },
});
```

## ⚠️ CRITICAL GUIDELINES (MUST FOLLOW ALL)

1. **ENFORCE strict TypeScript** - ZERO compromises on type safety
2. **VALIDATE everything with Zod** - As much as possible
3. **MINIMUM 80% test coverage** - NO EXCEPTIONS
4. **MUST pass ALL SonarQube quality gates** - No merging without passing
5. **MUST co-locate related files** - Tests MUST be in `__tests__` folders
6. **MAXIMUM 200 lines per component** - Split if larger
7. **MAXIMUM cognitive complexity of 15** - Refactor if higher
8. **MUST handle ALL states** - Loading, error, empty, and success
9. **MUST use semantic commits** - feat:, fix:, docs:, refactor:, test:
10. **MUST write complete JSDoc** - ALL exports must be documented
11. **MUST pass ALL automated checks** - Before ANY merge

## 📦 npm Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext ts,tsx --max-warnings 0",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "type-check": "tsc --noEmit",
    "validate": "npm run type-check && npm run lint && npm run test:coverage"
  }
}
```

## 📋 Pre-commit Checklist (MUST COMPLETE ALL)

- [ ] TypeScript compiles with ZERO errors
- [ ] Zod schemas validate ALL external data
- [ ] Tests written and passing (MINIMUM 80% coverage)
- [ ] ESLint passes with ZERO warnings
- [ ] SonarQube quality gate PASSED
- [ ] ALL states handled (loading, error, empty, success)
- [ ] Accessibility requirements met (ARIA labels, keyboard nav)
- [ ] ZERO console.log statements
- [ ] ALL functions have complete JSDoc documentation
- [ ] Component props are fully documented
- [ ] Complex logic has explanatory comments
- [ ] File-level @fileoverview is present
- [ ] TODOs include issue numbers
- [ ] Component files under 200 lines
- [ ] Cognitive complexity under 15 for all functions

### FORBIDDEN Practices

- **NEVER use `any` type** (except library declaration merging with comments)
- **NEVER skip tests**
- **NEVER ignore TypeScript errors**
- **NEVER trust external data without validation**
- **NEVER exceed complexity limits**
- **NEVER skip documentation**
- **NEVER use undocumented code**
- **NEVER use `JSX.Element`** - use `ReactElement` instead
- **NEVER pass `undefined` to optional props** - use conditional spreads
- **NEVER assume component prop names** - verify interfaces first
- **NEVER use `global`** - use `globalThis` for cross-platform compatibility
- **NEVER omit config files from TypeScript projects** - include ALL .ts files

---

## 📝 Recent Updates

### June 2025 - TypeScript Strict Compliance Update

Added comprehensive guidance based on real-world troubleshooting of 54+ TypeScript/ESLint errors:

- **Testing Framework Integration**: Vitest globals, React refresh exceptions, cross-platform compatibility
- **React 19 TypeScript Patterns**: JSX.Element → ReactElement migration, modern import patterns
- **ExactOptionalPropertyTypes**: Undefined vs null handling, conditional spreads, API body types
- **Branded Type Safety**: Schema.parse() patterns, system boundary validation
- **Component Integration**: Prop name verification, callback type accuracy, interface consistency
- **Project Configuration**: Complete TypeScript project references, ESLint coverage requirements

These additions ensure zero TypeScript errors and complete IDE/CLI alignment in strict mode.

---

_This guide is a living document. Update it as new patterns emerge and tools evolve._
_Focus on quality over speed, maintainability over cleverness._
_Last updated: December 2024_
