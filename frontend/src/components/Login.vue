<template>
    <div class="login">
        <h1>
            Login
        </h1>
        <h2>Username(Correct Login Name: myid)</h2>
            <div>
                <p>{{ loginaccountname }}</p>
                <input id="loginaccount" v-model="loginaccountname"/>
            </div>
        <h2>Password(Correct Password: mypasswd1234)</h2>
            <div>
                <p>{{ loginpassword }}</p>
                <input type="password" id="loginpassword" v-model="loginpassword"/>
            </div>
        <div id="loginsubmit">
            <button v-on:click="checklogin">ログイン</button>
        </div>
        <div id="loginResult"></div>
    </div>
</template>

<script>
import Axios from 'axios'
import { KJUR } from 'jsrsasign'
import router from '../router/index.js'

export default {
  name: 'login',
  data: function () {
    return {
      loginaccountname: '',
      loginpassword: ''
    }
  },
  methods: {
    checklogin: function (event) {
      // checkloginイベント(htmlファイル内で定義している)の内容を記述

      var axios = Axios.create({
        // axiosインスタンスの作成
        baseURL: 'http://localhost:5000',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        responseType: 'json'
      })
      // nextページの取得
      try {
        var nextPage = this.$route.query.next
      } catch (e) {
        nextPage = 'PageA'
      }
      console.log(nextPage)

      // axiosのthenメソッドの中ではthisがvueコンポーネントを指さなくなるので別の変数に割り当てておく
      var self = this
      // バックエンドのAPIサーバにリクエストを送信
      axios.get('/auth', {
        // クエリパラメータをセット
        params: {
          username: document.getElementById('loginaccount').value,
          password: document.getElementById('loginpassword').value
        }
      }).then(function (response) {
        // 応答が戻ってきたら結果を処理。
        // "success" だったら次のページにジャンプし、失敗だったらその旨表示
        if (response.data.result === 'success') {
          // JWTトークンの生成
          var token = self.generateToken(document.getElementById('loginaccount').value)
          // cookieとしてトークンを付与
          document.cookie = 'token=' + token
          // 次のページにジャンプ
          // router.push({name: nextPage, params: { auth: 'authenticated' }})
          router.push({name: nextPage})
        } else {
          document.getElementById('loginResult').innerHTML = 'Login Failed !'
        }
      })
    },
    generateToken: function (uname) {
      /* JWTトークンの生成 */
      // JWT用のシークレットトークンをセット(【注意】実際にはコードの中に書いてはいけない！)
      var secretToken = 'oreore'
      // JWTのヘッダー部を定義
      var oHeader = {alg: 'HS256', typ: 'JWT'}
      // JWTペイロードを作成
      var offset = Math.floor(Math.random() * Math.floor(25))
      var DO = new Date()
      DO.setSeconds(DO.getSeconds() + offset)
      var dY = DO.getFullYear()
      var dm = DO.getMonth() + 1
      var dd = DO.getDate()
      var dH = ('0' + DO.getHours()).slice(-2)
      var dM = ('0' + DO.getMinutes()).slice(-2)
      var dS = ('0' + DO.getSeconds()).slice(-2)
      var dStr = dY + '/' + dm + '/' + dd + ' ' + dH + ':' + dM + ':' + dS + ' +0900'
      var oPayload = {username: uname, until: dStr}
      console.log(oHeader, oPayload)
      // JWTを生成
      var sJWT = KJUR.jws.JWS.sign('HS256', JSON.stringify(oHeader), JSON.stringify(oPayload), secretToken)
      console.log(sJWT)
      return sJWT
    }
  }
}
</script>
