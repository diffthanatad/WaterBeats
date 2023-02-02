<template>
    <div class="navbar-component">
        <nav class="navbar navbar-expand-lg">
            <div class="container">
                <router-link :to="{ name: 'Home' }" class="nav-item nav-link" exact>
                    UCL WaterBeats
                </router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                    aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" disabled="true">
                                <router-link :to="{ name: 'Home' }">Home</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Graph' }">Graph</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Configuration' }">Configuration</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Admin' }">Admin</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link">
                                <router-link :to="{ name: 'Setting' }">Setting</router-link>
                            </a>
                        </li>
                        <li class="nav-item">
                            <button class="btn btn-outline-success" type="button">Sign Out</button>
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
    }
}
</script>

<style scoped>
.navbar {
    background-color: #98E6F6;
}
</style>