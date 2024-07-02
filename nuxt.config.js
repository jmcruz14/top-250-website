// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiUrl: 'http://127.0.0.1:8000'
    },
  },
  preset: 'node-server',
  devtools: { enabled: true },
  ssr: true,
  spaLoadingTemplate: false,
  // plugins: [
  //   '~/plugins/analytics.client.js',
  // ],
  srcDir: 'src/',
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-primevue'
  ],
  css: [
    '@/assets/css/main.css',
    'primeicons/primeicons.css',
    'primevue/resources/themes/lara-light-green/theme.css'
  ],
  app: {
    head: {
      htmlAttrs: {
        lang: 'en'
      },
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Raleway:ital,wght@0,100..900;1,100..900&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap',
          media: 'none',
          onload: "if(media!='all')media='all'",
        }
      ]
    }
  },

  primevue: {
    usePrimeVue: true,
    components: {
      prefix: '',
      include: '*'
    },
    options: {
      ripple: true,
      unstyled: false,
      // cssLayerOrder: 'reset,primevue'
    }
    // pt: {

    // }
  }
})