# CLAUDE.md

This file provides comprehensive guidance to Claude Code when working with Astro 5+ applications and the Islands Architecture.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

### Design Principles

- **Islands Architecture**: Ship minimal JavaScript, hydrate only what needs interactivity
- **Performance by Default**: Static-first with selective hydration for optimal performance
- **Framework Agnostic**: Mix React, Vue, Svelte, and other frameworks in the same project
- **Content-Driven**: Optimized for content-heavy websites with type-safe content management
- **Zero JavaScript by Default**: Only ship JavaScript when explicitly needed

## 🤖 AI Assistant Guidelines

### Context Awareness

- When implementing features, always check existing patterns first
- Prefer static generation over client-side rendering when possible
- Use framework-specific components only when interactivity is required
- Check for similar functionality across different framework integrations
- Understand when to use `.astro` vs framework components

### Common Pitfalls to Avoid

- Over-hydrating components that could be static
- Mixing multiple frameworks unnecessarily in single components
- Ignoring Astro's partial hydration benefits
- Creating duplicate functionality across different framework islands
- Overwriting existing integrations without checking alternatives

### Workflow Patterns

- Preferably create tests BEFORE implementation (TDD)
- Use "think hard" for hydration strategy decisions
- Break complex interactive components into smaller, focused islands
- Validate framework choice and hydration requirements before implementation

### Search Command Requirements

**CRITICAL**: Always use `rg` (ripgrep) instead of traditional `grep` and `find` commands:

```bash
# ❌ Don't use grep
grep -r "pattern" .

# ✅ Use rg instead
rg "pattern"

# ❌ Don't use find with name
find . -name "*.ts"

# ✅ Use rg with file filtering
rg --files | rg "\.ts$"
# or
rg --files -g "*.ts"
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

## 🧱 Code Structure & Modularity

### File and Component Limits

- **Never create a file longer than 500 lines of code.** If approaching this limit, refactor by splitting into modules or helper components.
- **Astro components should be under 200 lines** for better maintainability.
- **Functions should be short and focused sub 50 lines** and have a single responsibility.
- **Organize code by feature and framework**, keeping related components together.

## 🚀 Astro 5+ Key Features

### Content Layer (New in Astro 5)

- **Flexible Content Management**: Load content from any source (files, APIs, CMSs)
- **Type-Safe Content**: Automatic TypeScript types for all content collections
- **Performance Boost**: Up to 5x faster builds for Markdown, 2x for MDX
- **Unified API**: Single interface for all content sources

```typescript
// content/config.ts
import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string(),
    author: z.string(),
    image: z
      .object({
        url: z.string(),
        alt: z.string(),
      })
      .optional(),
    tags: z.array(z.string()),
  }),
});

export const collections = { blog };
```

### Server Islands (New in Astro 5)

- **Mixed Static/Dynamic Content**: Combine cached static content with personalized dynamic content
- **Independent Loading**: Each island loads separately for optimal performance
- **Custom Caching**: Set custom cache headers and fallback content per island

```astro
---
// components/PersonalizedContent.astro
export const prerender = false; // Server island
---

<div>
  <h2>Welcome back, {Astro.locals.user?.name}!</h2>
  <p>Your personalized content here...</p>
</div>
```

### Environment Configuration (astro:env)

- **Type-Safe Environment Variables**: Validation and TypeScript support
- **Runtime Validation**: Automatic validation at build time
- **Client/Server Separation**: Clear distinction between public and private variables

```typescript
// env.d.ts
import { defineEnv, envField } from "astro:env/config";

export default defineEnv({
  server: {
    DATABASE_URL: envField.string({ context: "server", access: "secret" }),
    API_SECRET: envField.string({ context: "server", access: "secret" }),
  },
  client: {
    PUBLIC_API_URL: envField.string({ context: "client", access: "public" }),
    PUBLIC_SITE_NAME: envField.string({ context: "client", access: "public" }),
  },
});
```

## 🏗️ Project Structure (Islands Architecture)

```
src/
├── components/            # Astro components (.astro)
│   ├── ui/               # Static UI components
│   ├── islands/          # Interactive components (framework-specific)
│   └── layouts/          # Layout components
├── content/              # Content collections
│   ├── config.ts         # Content configuration
│   ├── blog/            # Blog posts (markdown/mdx)
│   └── docs/            # Documentation
├── pages/                # File-based routing (REQUIRED)
│   ├── api/             # API routes
│   ├── blog/            # Blog pages
│   └── [...slug].astro  # Dynamic routes
├── lib/                  # Utility functions and configurations
│   ├── utils.ts         # Helper functions
│   ├── constants.ts     # Application constants
│   └── schemas.ts       # Zod validation schemas
├── styles/              # Global styles
│   └── global.css       # CSS custom properties and globals
├── assets/              # Processed assets (images, etc.)
└── env.d.ts            # Environment and type definitions
```

## 🎯 TypeScript Configuration (STRICT REQUIREMENTS)

### MUST Follow Astro TypeScript Templates

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/layouts/*": ["src/layouts/*"],
      "@/content/*": ["src/content/*"]
    },
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### MANDATORY Type Requirements

- **NEVER use `any` type** - use `unknown` if type is truly unknown
- **MUST use explicit type imports** with `import type { }` syntax
- **MUST define props interfaces** for all Astro components
- **MUST use Astro's built-in types** like `HTMLAttributes`, `ComponentProps`
- **MUST validate content with Zod schemas** in content collections

### Component Props Typing (MANDATORY)

```typescript
// Astro component props
export interface Props {
  title: string;
  description?: string;
  image?: {
    src: string;
    alt: string;
  };
  class?: string;
}

const { title, description, image, class: className } = Astro.props;
```

## 📦 Package Management & Dependencies

### MUST Use pnpm (MANDATORY)

**CRITICAL**: Always use pnpm for Astro projects for better performance and dependency management.

```bash
# Install pnpm globally
npm install -g pnpm
# or
curl -fsSL https://get.pnpm.io/install.sh | sh

# Project setup
pnpm create astro@latest
pnpm install
pnpm dev
```

### Essential Astro 5 Dependencies

```json
{
  "dependencies": {
    "astro": "^5.0.0",
    "@astrojs/check": "^0.9.0",
    "@astrojs/ts-plugin": "^1.10.0",
    "typescript": "^5.6.0"
  },
  "devDependencies": {
    "@astrojs/tailwind": "^5.1.0",
    "tailwindcss": "^3.4.0",
    "prettier": "^3.3.0",
    "prettier-plugin-astro": "^0.14.0"
  }
}
```

### Framework Integrations (Add as needed)

```bash
# React integration
pnpm astro add react
# or
npx astro add react

# Vue integration
pnpm astro add vue

# Svelte integration
pnpm astro add svelte

# Preact integration
pnpm astro add preact

# SolidJS integration
pnpm astro add solid

# Multiple frameworks (framework-agnostic approach)
pnpm astro add react vue svelte
```

### Essential Integrations

```bash
# Styling and UI
pnpm astro add tailwind
pnpm astro add mdx

# Performance and SEO
pnpm astro add sitemap
pnpm astro add compress

# Content and CMS
pnpm astro add @astrojs/content
pnpm astro add @astrojs/rss

# Manual package installation when needed
pnpm add package-name
pnpm add -D dev-package-name
```

## 🛡️ Data Validation with Zod (MANDATORY FOR CONTENT)

### Content Collections (REQUIRED Pattern)

```typescript
// src/content/config.ts
import { defineCollection, z } from "astro:content";

const blogSchema = z.object({
  title: z.string(),
  description: z.string(),
  pubDate: z.coerce.date(),
  updatedDate: z.coerce.date().optional(),
  heroImage: z.string().optional(),
  tags: z.array(z.string()).default([]),
  draft: z.boolean().default(false),
  author: z.object({
    name: z.string(),
    email: z.string().email().optional(),
    image: z.string().optional(),
  }),
});

const docsSchema = z.object({
  title: z.string(),
  description: z.string(),
  sidebar: z
    .object({
      order: z.number(),
      label: z.string().optional(),
    })
    .optional(),
});

export const collections = {
  blog: defineCollection({
    type: "content",
    schema: blogSchema,
  }),
  docs: defineCollection({
    type: "content",
    schema: docsSchema,
  }),
};

export type BlogPost = z.infer<typeof blogSchema>;
export type DocsPage = z.infer<typeof docsSchema>;
```

### API Route Validation

```typescript
// src/pages/api/newsletter.ts
import type { APIRoute } from "astro";
import { z } from "zod";

const subscribeSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
});

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.json();
    const validatedData = subscribeSchema.parse(data);

    // Process subscription
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return new Response(
        JSON.stringify({
          error: "Validation failed",
          details: error.errors,
        }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    return new Response(JSON.stringify({ error: "Internal server error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
};
```

## 🧪 Testing Strategy (VITEST RECOMMENDED)

### MUST Meet These Testing Standards

- **MINIMUM 80% code coverage** - NO EXCEPTIONS
- **MUST use Vitest** for unit and component tests (Jest-compatible, Vite-native)
- **MUST use Astro Container API** for component testing
- **MUST test islands separately** from static components
- **MUST mock external dependencies** appropriately

### Vitest Configuration (MANDATORY)

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import { getViteConfig } from "astro/config";

export default defineConfig(
  getViteConfig({
    test: {
      environment: "happy-dom", // or 'jsdom'
      coverage: {
        reporter: ["text", "json", "html"],
        threshold: {
          global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80,
          },
        },
      },
    },
  }),
);
```

### Component Testing with Container API

```typescript
// src/components/__tests__/Card.test.ts
import { experimental_AstroContainer as AstroContainer } from "astro/container";
import { expect, test } from "vitest";
import Card from "../Card.astro";

test("Card component renders correctly", async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    props: {
      title: "Test Title",
      description: "Test description",
    },
  });

  expect(result).toContain("Test Title");
  expect(result).toContain("Test description");
});

test("Card component handles missing props gracefully", async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    props: { title: "Test Title" },
  });

  expect(result).toContain("Test Title");
  expect(result).not.toContain("undefined");
});
```

### Integration Testing for API Routes

```typescript
// src/pages/api/__tests__/newsletter.test.ts
import { expect, test } from "vitest";

test("POST /api/newsletter validates email", async () => {
  const response = await fetch("/api/newsletter", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: "invalid-email", name: "Test" }),
  });

  expect(response.status).toBe(400);
  const data = await response.json();
  expect(data.error).toBe("Validation failed");
});
```

## 🎨 Component Guidelines (ASTRO-SPECIFIC)

### Astro Component Structure (MANDATORY)

```astro
---
// src/components/BlogCard.astro
export interface Props {
  title: string;
  description: string;
  pubDate: Date;
  image?: {
    src: string;
    alt: string;
  };
  tags?: string[];
  href: string;
}

const {
  title,
  description,
  pubDate,
  image,
  tags = [],
  href
} = Astro.props;

// Server-side logic here
const formattedDate = pubDate.toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
});
---

<article class="blog-card">
  {image && (
    <img
      src={image.src}
      alt={image.alt}
      loading="lazy"
      decoding="async"
    />
  )}

  <div class="content">
    <h3>
      <a href={href}>{title}</a>
    </h3>
    <p>{description}</p>

    <div class="meta">
      <time datetime={pubDate.toISOString()}>
        {formattedDate}
      </time>

      {tags.length > 0 && (
        <ul class="tags">
          {tags.map((tag) => (
            <li class="tag">{tag}</li>
          ))}
        </ul>
      )}
    </div>
  </div>
</article>

<style>
  .blog-card {
    /* Component-scoped styles */
    border: 1px solid var(--color-border);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s ease;
  }

  .blog-card:hover {
    transform: translateY(-2px);
  }

  .content {
    padding: 1rem;
  }

  .tags {
    display: flex;
    gap: 0.5rem;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .tag {
    background: var(--color-accent);
    color: var(--color-accent-text);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
  }
</style>
```

### Framework Component Integration

```astro
---
// src/components/InteractiveCounter.astro
export interface Props {
  initialCount?: number;
  maxCount?: number;
}

const { initialCount = 0, maxCount = 100 } = Astro.props;
---

<!-- Static wrapper with framework island -->
<div class="counter-wrapper">
  <h3>Interactive Counter</h3>

  <!-- React island with hydration directive -->
  <Counter
    client:load
    initialCount={initialCount}
    maxCount={maxCount}
  />
</div>

<style>
  .counter-wrapper {
    border: 2px solid var(--color-primary);
    padding: 1rem;
    border-radius: 8px;
  }
</style>
```

### Hydration Directives (CRITICAL UNDERSTANDING)

```astro
<!-- Load immediately -->
<Component client:load />

<!-- Load when component becomes visible -->
<Component client:visible />

<!-- Load when browser is idle -->
<Component client:idle />

<!-- Load on media query match -->
<Component client:media="(max-width: 768px)" />

<!-- Render only on client (no SSR) -->
<Component client:only="react" />
```

## 🔄 Content Management Patterns

### Content Collection Usage

```astro
---
// src/pages/blog/[...slug].astro
import { type CollectionEntry, getCollection } from 'astro:content';
import BlogLayout from '../../layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: post,
  }));
}

type Props = CollectionEntry<'blog'>;

const post = Astro.props;
const { Content } = await post.render();
---

<BlogLayout
  title={post.data.title}
  description={post.data.description}
  pubDate={post.data.pubDate}
  heroImage={post.data.heroImage}
>
  <Content />
</BlogLayout>
```

### Dynamic Content Loading

```typescript
// src/lib/content.ts
import { getCollection, type CollectionEntry } from "astro:content";

export async function getBlogPosts(): Promise<CollectionEntry<"blog">[]> {
  const posts = await getCollection("blog");

  return posts
    .filter((post) => !post.data.draft)
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export async function getPostsByTag(
  tag: string,
): Promise<CollectionEntry<"blog">[]> {
  const posts = await getBlogPosts();
  return posts.filter((post) => post.data.tags.includes(tag));
}

export async function getFeaturedPosts(): Promise<CollectionEntry<"blog">[]> {
  const posts = await getBlogPosts();
  return posts.filter((post) => post.data.featured).slice(0, 3);
}
```

## 🚀 Performance Optimization (ASTRO-SPECIFIC)

### Image Optimization (MANDATORY)

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<!-- Optimized images with Astro -->
<Image
  src={heroImage}
  alt="Hero image description"
  width={800}
  height={400}
  format="webp"
  quality={80}
  loading="eager"
/>

<!-- Responsive images -->
<Image
  src={heroImage}
  alt="Responsive hero"
  widths={[400, 800, 1200]}
  sizes="(max-width: 400px) 400px, (max-width: 800px) 800px, 1200px"
  format="webp"
/>
```

### Bundle Optimization

```typescript
// astro.config.mjs
import { defineConfig } from "astro/config";

export default defineConfig({
  build: {
    inlineStylesheets: "auto",
    splitting: true,
  },
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            "react-vendor": ["react", "react-dom"],
            "vue-vendor": ["vue"],
            utils: ["./src/lib/utils.ts"],
          },
        },
      },
    },
  },
  experimental: {
    contentIntellisense: true,
  },
});
```

### Server Islands for Performance

```astro
---
// src/components/DynamicContent.astro
export const prerender = false; // Mark as server island

// This runs on the server for each request
const userPreferences = await getUserPreferences(Astro.locals.userId);
const recommendations = await getRecommendations(userPreferences);
---

<section class="dynamic-content">
  <h2>Recommended for you</h2>
  <div class="recommendations">
    {recommendations.map((item) => (
      <div class="recommendation-card">
        <h3>{item.title}</h3>
        <p>{item.description}</p>
      </div>
    ))}
  </div>
</section>

<style>
  .dynamic-content {
    /* Styles for dynamic content */
  }
</style>
```

## 🔐 Security Requirements (MANDATORY)

### Environment Variables (MUST VALIDATE)

```typescript
// src/env.d.ts
import { envField, defineEnv } from "astro:env/config";

export default defineEnv({
  server: {
    DATABASE_URL: envField.string({
      context: "server",
      access: "secret",
      min: 1,
    }),
    API_SECRET_KEY: envField.string({
      context: "server",
      access: "secret",
      min: 32,
    }),
  },
  client: {
    PUBLIC_SITE_URL: envField.string({
      context: "client",
      access: "public",
    }),
    PUBLIC_ANALYTICS_ID: envField.string({
      context: "client",
      access: "public",
    }),
  },
});
```

### Content Security Policy

```astro
---
// src/layouts/BaseLayout.astro
export interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="description" content={description} />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" />
  <title>{title}</title>
</head>
<body>
  <slot />
</body>
</html>
```

## 💅 Code Style & Quality

### Astro Configuration (MANDATORY)

```typescript
// astro.config.mjs
import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import react from "@astrojs/react";
import vue from "@astrojs/vue";

export default defineConfig({
  integrations: [tailwind(), react(), vue()],
  markdown: {
    shikiConfig: {
      theme: "github-dark",
      wrap: true,
    },
  },
  build: {
    format: "directory",
  },
  experimental: {
    contentIntellisense: true,
  },
});
```

### Prettier Configuration

```json
{
  "plugins": ["prettier-plugin-astro"],
  "overrides": [
    {
      "files": "*.astro",
      "options": {
        "parser": "astro"
      }
    }
  ],
  "astroAllowShorthand": false
}
```

## 📋 Development Commands

### pnpm Scripts (MANDATORY)

```json
{
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro check && astro build",
    "preview": "astro preview",
    "check": "astro check",
    "sync": "astro sync",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext .js,.ts,.astro --max-warnings 0",
    "format": "prettier --write \"src/**/*.{astro,js,ts,md,json}\"",
    "format:check": "prettier --check \"src/**/*.{astro,js,ts,md,json}\"",
    "validate": "pnpm run check && pnpm run lint && pnpm run test:coverage"
  }
}
```

### pnpm Command Reference

```bash
# Development
pnpm dev              # Start development server
pnpm build            # Build for production
pnpm preview          # Preview production build

# Code Quality
pnpm run check        # TypeScript and Astro validation
pnpm run lint         # ESLint with zero warnings
pnpm run format       # Format code with Prettier
pnpm run validate     # Run all quality checks

# Testing
pnpm test             # Run tests
pnpm run test:coverage # Run tests with coverage

# Package Management
pnpm install          # Install dependencies
pnpm add package      # Add runtime dependency
pnpm add -D package   # Add dev dependency
pnpm update           # Update dependencies
pnpm audit            # Security audit
pnpm list             # List installed packages
pnpm outdated         # Check for outdated packages
```

## ⚠️ CRITICAL GUIDELINES (MUST FOLLOW ALL)

1. **MUST use pnpm** - Never use npm or yarn for package management
2. **ENFORCE TypeScript strict mode** - Use `astro/tsconfigs/strict` template
3. **VALIDATE all content with Zod** - Content collections MUST have schemas
4. **MINIMUM 80% test coverage** - Use Vitest with Container API
5. **MUST understand hydration strategy** - Use appropriate client directives
6. **MAXIMUM 500 lines per file** - Split large components
7. **MUST use semantic imports** - `import type` for type-only imports
8. **MUST optimize images** - Use Astro's Image component
9. **MUST validate environment variables** - Use astro:env for type safety
10. **NEVER over-hydrate** - Default to static, hydrate only when needed
11. **MUST use framework components sparingly** - Prefer Astro components for static content
12. **MUST pass astro check** - Zero TypeScript errors required

## 📋 Pre-commit Checklist (MUST COMPLETE ALL)

- [ ] `astro check` passes with ZERO errors
- [ ] Content collections have proper Zod schemas
- [ ] Components use appropriate hydration directives
- [ ] Images are optimized with Astro's Image component
- [ ] Tests written with 80%+ coverage using Vitest
- [ ] Environment variables are properly typed with astro:env
- [ ] No unnecessary framework components (static content uses .astro)
- [ ] TypeScript strict mode compliance
- [ ] Prettier formatting applied to all .astro files
- [ ] All API routes have proper Zod validation
- [ ] Content types are properly exported and used
- [ ] No client-side JavaScript for static content
- [ ] Performance budget maintained (check bundle size)
- [ ] SEO metadata properly configured

### FORBIDDEN Practices

- **NEVER use npm or yarn** - MUST use pnpm for all package management
- **NEVER use client:load** without justification - prefer client:visible or client:idle
- **NEVER skip content validation** - all content MUST have Zod schemas
- **NEVER ignore hydration impact** - understand JavaScript bundle size
- **NEVER use framework components for static content** - use .astro files
- **NEVER bypass TypeScript checking** - astro check must pass
- **NEVER store secrets in client-side code** - use astro:env server context
- **NEVER ignore image optimization** - always use Astro's Image component
- **NEVER mix concerns** - separate static content from interactive islands
- **NEVER use any type** - leverage Astro's built-in type safety
- **NEVER ignore build warnings** - address all build and TypeScript issues
- **NEVER use npx for regular commands** - use pnpm equivalents when available

---

_This guide is optimized for Astro 5+ with Islands Architecture and modern web performance._
_Focus on minimal JavaScript, optimal hydration, and type-safe content management._
_Last updated: January 2025_
