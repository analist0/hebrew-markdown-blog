/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['res.cloudinary.com', 'images.unsplash.com'],
    formats: ['image/avif', 'image/webp'],
  },
  i18n: {
    locales: ['he', 'en'],
    defaultLocale: 'he',
  },
  experimental: {
    optimizeCss: true,
  },
}

module.exports = nextConfig
