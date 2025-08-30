# 小説投稿サイト - Laravel 12 + Vue.js + Inertia.js
# PHP 8.4 開発環境専用Dockerfile
# ホットリロード・デバッグ機能対応

FROM php:8.4-fpm

# 作業ディレクトリ設定
WORKDIR /var/www/html

# 開発用環境変数
ENV APP_ENV=local
ENV APP_DEBUG=true

# システムパッケージのインストール（開発ツール含む）
RUN apt-get update && apt-get install -y \
    # 基本ツール
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    # Node.js (Vue.js + Vite用)
    nodejs \
    npm \
    # 画像処理用（Intervention Image）
    libjpeg-dev \
    libfreetype6-dev \
    libwebp-dev \
    # MySQL用
    default-mysql-client \
    # Redis用
    redis-tools \
    # 開発ツール
    vim \
    nano \
    htop \
    procps \
    # その他
    supervisor \
    nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# PHP拡張のインストール
RUN docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp \
    && docker-php-ext-install \
    pdo_mysql \
    mbstring \
    exif \
    pcntl \
    bcmath \
    gd \
    opcache

# Redis拡張のインストール
RUN pecl install redis && docker-php-ext-enable redis

# Xdebugのインストール（開発環境専用）
RUN pecl install xdebug \
    && docker-php-ext-enable xdebug

# Composerのインストール
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Node.js最新LTS版のインストール
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs

# PHP設定（開発環境用）
COPY php.ini /usr/local/etc/php/conf.d/custom.ini

# Xdebug設定追加（開発用）
RUN echo "xdebug.mode=debug,coverage" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
    && echo "xdebug.client_host=host.docker.internal" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
    && echo "xdebug.client_port=9003" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
    && echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini

# Nginx設定
COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/sites-available/default

# Supervisor設定
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 開発用：package.jsonとcomposer.jsonを先にコピー（キャッシュ効率化）
COPY composer.json composer.lock* ./
COPY package.json package-lock.json* ./

# Composerパッケージのインストール（開発依存関係含む）
RUN composer install --dev --no-scripts --no-autoloader

# Node.jsパッケージのインストール
RUN npm install

# アプリケーションファイルをコピー（開発時はボリュームマウント前提）
COPY . .

# Composer autoload生成
RUN composer dump-autoloader --optimize

# 権限設定（開発環境用）
RUN chown -R www-data:www-data /var/www/html \
    && usermod -u 1000 www-data \
    && groupmod -g 1000 www-data \
    && chmod -R 775 /var/www/html/storage \
    && chmod -R 775 /var/www/html/bootstrap/cache

# ポート公開
EXPOSE 80 5173

# Supervisorでサービス起動
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]