<template>
    <div class="navbar-component">
        <nav class="navbar navbar-expand-lg">
            <div class="container">
                <router-link :to="{ name: 'Home' }" class="waterbeats-home" style="text-decoration: none;">
                    <img src=".././assets/img/waterbeats_icon.png" class="icon">
                    WaterBeats
                </router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" disabled="true">
                                <router-link :to="{ name: 'Home' }" style="text-decoration: none;">HOME</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Graph' }" style="text-decoration: none;">VISUALISATION</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'ActuatorConfigurationView' }" style="text-decoration: none;">ACTUATOR CONFIG</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Admin' }" style="text-decoration: none;">ADMIN</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Setting' }" style="text-decoration: none;">SETTINGS</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <button class="btn btn-outline-success" type="button" @click.prevent="logOut">SIGN OUT</button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>

export default {
    name: "NavigationBar",
    components: {
    },
    computed: {
    },
    methods: {
        async logOut() {
            localStorage.removeItem('username');
            localStorage.removeItem('jwt');
            localStorage.removeItem('role');

            this.$router.push({ name: 'LogIn' })
        }
    }
}
</script>

<style scoped>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Kumbh Sans', sans-serif;
    color: #fff;
    ;
}

*:hover {
    color: #3fd9b3;
}

.navbar {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
    position: sticky;
    top: 0;
    z-index: 999;
}

.navbar::before {
    content: "";
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    position: absolute;
    background-image: url(".././assets/img/farm_background.jpg");
    background-position: center;
    background-size: cover;
    filter: brightness(80%);
}

.container {
    display: flex;
    justify-content: space-between;
    z-index: 1;
    width: 100%;
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 50px;
}

.navbar-toggler {
    display: flex;
    background-color: #fff;
}

.navbar-nav {
    display: flex;
    align-items: center;
    list-style: none;
    text-align: center;
}

.nav-item {
    /* height: 80px; */
    font-size: 14.5px;
}

.nav-link {
    display: flex;
    align-items: center;
    justify-content: center;
    /* padding: 0 1rem; */
    height: 100%;
}

.waterbeats-home {
    font-size: 17px;
}

.navbar-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 1rem;
    width: 100%;
}

.btn {
    display: flex;
    justify-content: center;
    align-items: center;
    text-decoration: none;
    border-radius: 30px;
    border-color: #fff;
    border-width: 2.5px;
    color: #fff;
    font-size: 14.5px;
    /* width: 100%; */
    padding: 7px 17px;
}

.btn:hover {
    background-color: #3fd9b3;
    border-color: #3fd9b3;
    color: #fff;
    font-weight: 700;
}

.icon {
    width: 35px
}
</style>