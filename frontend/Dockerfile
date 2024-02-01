# Stage 1: Prepare dependencies
FROM node:18-alpine AS deps
ARG TARGETPLATFORM
ARG TARGETARCH
ARG TARGETVARIANT
RUN printf "I'm building for TARGETPLATFORM=${TARGETPLATFORM}"
RUN apk add --no-cache libc6-compat python3 py3-pip make g++
WORKDIR /app

COPY package.json package-lock.json ./

RUN if [ "$TARGETPLATFORM" = "linux/arm/v8" ]; then \
      npm install --arch=arm64 --platform=linux --libc=musl sharp; \
    else \
      npm install --omit=dev; \
    fi

# Stage 2: Build the application
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Stage 3: Run the application
FROM node:18-alpine AS runner
WORKDIR /app

# Create a non-root user and set permissions
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs \
    && chown -R nextjs:nodejs /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["npm", "start"]