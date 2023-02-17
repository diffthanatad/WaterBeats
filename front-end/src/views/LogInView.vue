<template>
  <div class="sign-in-page vh-100">
    <div class="d-flex justify-content-center h-100 mx-auto">
      <div class="card d-flex">
        <div class="card-title align-items-center justify-content-center">
          <h1 class="web-title">WaterBeats</h1>
        </div>
        <div class="card-body align-items-center justify-content-center">
            <form @submit.prevent="logIn">
                <div class="form-group">
                  <div class="input-group">
                    <span class="input-group-append input-group-text"><i class="bi bi-person-badge"></i></span>
                    <input type="text" class="form-control input_user" v-model="inputUsername" placeholder="username"/>
                  </div>
                </div>
                <div class="form-group">
                  <div class="input-group">
                    <span class="input-group-append input-group-text"><i class="bi bi-key"></i></span>
                    <input type="password" class="form-control input_pass" v-model="inputPassword" placeholder="password">
                  </div>
                </div>
              <div class="d-flex align-items-center justify-content-center">
                <button type="submit" class="btn btn-primary">Sign in</button>
              </div>
            </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { logIn } from "@/services/userService.js";

export default {
  name: 'LogInPage',
  created() {
  },
  components: {
  },
  data() {
    return {
      /* search input fields. */ 
      inputUsername: "",
      inputPassword: "",
    };
  },
  computed: {
  },
  mounted() {
  },
  methods: {
    async logIn() {
      this.$router.push({ name: 'Home' })
      // try {
        // const obj = {
        //   username: this.inputUsername,
        //   password: this.inputPassword,
        // }

        // const response = await logIn(obj);
      //   if (response.status === 200) {
      //     await this.$store.dispatch("user/signin", response.data);
      //     this.$router.push({name: "Home"}); 
      //   } else {
      //     await this.$store.dispatch("user/signout");
      //   }
      // } catch (error) {
      //   console.log("LogInView, logIn():", error, "\n");
      // }
    },
  },
  watch: {
  }
}
</script>

<style scoped>
  .sign-in-page {
    background-color: #74E6F6;
  }

  .card-title {
    margin-top: 0px;
    text-align: center;
  }

  .card {
    margin-top: auto;
    margin-bottom: auto;
    position: relative;
    display: flex;
    justify-content: center;
    flex-direction: column;
    width: 22rem;
    height: 380px;
  }

  .brand_logo {
    height: 100px;
    width: 100px;
  }

  .web-title {
    margin-top: 50px;
  }

  .btn {
    margin-top: 10px;
  }

  #bottom {
    /* position: absolute; */
    bottom: 0;
    width: 100%;
    padding-bottom: 15px;
  }
  .input-group {
    margin-bottom: 10px;
  }
</style>
