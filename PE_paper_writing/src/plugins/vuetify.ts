import { createVuetify } from 'vuetify'
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // 添加这行

const vuetify = createVuetify({
  components: {
    VFileUpload,
  },
  icons: {
    defaultSet: 'mdi', // 设置默认图标集
  },
})

export default vuetify
