import JSEncrypt from "jsencrypt";

// 公钥
const publicKey = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALELHbkIsziS29/oOUAw3mdTctJTNtCs\n' +
    'M2GHGLuldyl/cn7UnwvUYFyERAyAfRT2CkRzBJ64TCDgBiohU8/sFNMCAwEAAQ=='


// 私钥
const privateKey = 'MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAsQsduQizOJLb3 + g5\n' +
    'QDDeZ1Ny0lM20KwzYYcYu6V3KX9yftSfC9RgXIREDIB9FPYKRHMEnrhMIOAGKiFT\n' +
    'z + wU0wIDAQABAkBspsHK + MfkhFxkAYSBHHyhNNlWsrMFRWkTBXHsVxPWZtcuv70n\n' +
    'AX2QIwwyXk8ZsF2KZmnQaIA / dNNQ + Rmfr36hAiEA3rVcIPeF3HK3IdoSDc7VGGzP\n' +
    'OgGnGRYXmA1TQzNexpcCIQDLgj2UKT5RsiRU9IWyGztnCt2Vj / 3R9qmoJlmLJTbH\n' +
    'JQIgEWU7F / wdgZWYRlWhOWDhdjHxkcdVRPlbyG2qBkK58WsCIQCLcCmRItE4WL7c\n' +
    'Fs6kQlRpPeClYYugGUoVlHE2DcGCoQIgaMH4Njf / O2VhkQq1ILwXMiB4kbDHLRSn\n' +
    'Ir0ImWVCGq4 ='



// 加密
export const encrypt = (txt: any) => {
    const encryptor = new JSEncrypt()
    encryptor.setPublicKey(publicKey)
    return encryptor.encrypt(txt)
}

// 解密
export const decrypt = (txt: any) => {
    const encryptor = new JSEncrypt()
    encryptor.setPrivateKey(privateKey)
    return encryptor.decrypt(txt)
}