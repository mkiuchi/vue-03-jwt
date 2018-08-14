<template>
  <div class="pagea">
    This is page A.
    <div>
      Valid until {{ until.toString() }}
    </div>
  </div>
</template>

<script>
import {KJUR, b64utoutf8} from 'jsrsasign'
import router from '../router/index.js'

export default {
  name: 'PageA',
  beforeMount: function () {
    var sJWT = ''
    var ck = document.cookie.split(';')
    ck.forEach(function (value) {
      // cookie名と値に分ける
      var content = value.split('=')
      if (content[0] === 'token') {
        sJWT = content[1]
      }
    })
    // console.log(sJWT)
    var isValid = KJUR.jws.JWS.verify(sJWT, 'oreore', {alg: ['HS256']})
    // console.log(isValid)
    if (!isValid) {
      console.log('invalid authentication. route to login...')
      document.cookie = 'token=; max-age=0'
      router.push({ name: 'Login', query: { next: this.$route.name } })
    } else {
      var payload = KJUR.jws.JWS.readSafeJSONString(b64utoutf8(sJWT.split('.')[1]))
      var until = new Date(payload.until)
      var now = new Date()
      // console.log(until)
      if (now > until) {
        console.log('JWT is expired. route to login...')
        document.cookie = 'token=; max-age=0'
        router.push({ name: 'Login', query: { next: this.$route.name } })
      }
    }
  },
  computed: {
    until: function () {
      var sJWT = ''
      var ck = document.cookie.split(';')
      ck.forEach(function (value) {
        // cookie名と値に分ける
        var content = value.split('=')
        if (content[0] === 'token') {
          sJWT = content[1]
        }
      })
      // console.log(sJWT)
      if (sJWT.length > 0) {
        var payload = KJUR.jws.JWS.readSafeJSONString(b64utoutf8(sJWT.split('.')[1]))
        return new Date(payload.until)
      }
    }
  }
}
</script>
