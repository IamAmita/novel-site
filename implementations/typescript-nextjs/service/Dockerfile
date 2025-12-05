# ===========================================
# Base Stage: Node.js 20
# ===========================================
FROM node:20-alpine AS base

# 必要なパッケージをインストール
RUN apk add --no-cache libc6-compat

WORKDIR /app

# ===========================================
# Dependencies Stage: 依存関係インストール
# ===========================================
FROM base AS deps

# package.json と lock ファイルをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm ci

# ===========================================
# Backend Development Stage
# ===========================================
FROM base AS backend

WORKDIR /app

# 依存関係をコピー
COPY --from=deps /app/node_modules ./node_modules

# Prisma CLI用の設定
ENV PRISMA_CLI_BINARY_TARGETS=linux-musl-openssl-3.0.x

# 開発用ポート
EXPOSE 4000

# 開発サーバー起動（docker-compose.ymlでオーバーライド）
CMD ["npm", "run", "dev"]

# ===========================================
# Frontend Development Stage
# ===========================================
FROM base AS frontend

WORKDIR /app

# 依存関係をコピー
COPY --from=deps /app/node_modules ./node_modules

# Next.js テレメトリを無効化
ENV NEXT_TELEMETRY_DISABLED=1

# 開発用ポート
EXPOSE 3000

# 開発サーバー起動（docker-compose.ymlでオーバーライド）
CMD ["npm", "run", "dev"]

# ===========================================
# Backend Production Build Stage
# ===========================================
FROM base AS backend-builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# TypeScriptをビルド
RUN npm run build

# ===========================================
# Frontend Production Build Stage
# ===========================================
FROM base AS frontend-builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.jsをビルド
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# ===========================================
# Backend Production Stage
# ===========================================
FROM base AS backend-production

WORKDIR /app

ENV NODE_ENV=production

# 本番用の依存関係のみインストール
COPY package*.json ./
RUN npm ci --only=production

# ビルド成果物をコピー
COPY --from=backend-builder /app/dist ./dist
COPY --from=backend-builder /app/prisma ./prisma

# Prismaクライアント生成
RUN npx prisma generate

EXPOSE 4000

CMD ["node", "dist/index.js"]

# ===========================================
# Frontend Production Stage
# ===========================================
FROM base AS frontend-production

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# 本番用ユーザー作成
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Next.js standalone出力をコピー
COPY --from=frontend-builder /app/public ./public
COPY --from=frontend-builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=frontend-builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]

